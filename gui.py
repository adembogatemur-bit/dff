# gui.py
# Friday'in gerçek masaüstü penceresi — tam ekran, teknik HUD görünümü
# (Canvas ile çizilen ince çizgiler/daireler, ağır grafik YOK — zayıf
# bilgisayarlarda da sorunsuz çalışır) + köşede sohbet kutusu.

import math
import os
import threading
import customtkinter as ctk
from PIL import ImageTk
import qrcode

from commands import komutu_isle
from desktop_tts import konus
from wake_listener import UyanmaDinleyici
from scheduler import Zamanlayici
from server import app as flask_app, yerel_ip_al
from config import FLASK_PORT, WAKE_WORDS
import bildirim
import hud_durum
from utils import kaynak_klasoru

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

_DURUM_RENKLERI = {
    "dinliyor": "#1D9E75",
    "dusunuyor": "#E3A008",
    "konusuyor": "#378ADD",
    "hata": "#D92D20",
}
_DURUM_ETIKETLERI = {
    "dinliyor": "// DİNLİYOR",
    "dusunuyor": "// DÜŞÜNÜYOR",
    "konusuyor": "// KONUŞUYOR",
    "hata": "// HATA",
}

# HUD'un yenilenme sıklığı — 100ms (saniyede 10 kare) yeterince akıcı
# görünür ama eski/zayıf bilgisayarları da yormaz.
HUD_TIK_MS = 100


class FridayApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Friday")
        self._logo_ayarla()
        self.geometry("480x680")
        self.minsize(420, 560)

        # Tam ekran (oyun gibi, görev çubuğunu da kapatır). F1 ile
        # açıp kapatabilirsin — uygulamayı KAPATMAZ, sadece pencere
        # moduna döner.
        self._tam_ekran = True
        self.attributes("-fullscreen", self._tam_ekran)
        self.bind("<F1>", self._tam_ekrani_degistir)

        self._durum = "dinliyor"
        self._ring_aci = 0.0
        self._pulse_faz = 0.0

        bildirim.dinleyici_ekle(self.mesaj_ekle)
        hud_durum.dinleyici_ekle(lambda durum: self.after(0, self._durumu_uygula, durum))

        self._arayuz_kur()
        self._hud_kur()
        self._hud_donguyu_baslat()
        self._sunucuyu_baslat()
        self._dinleyiciyi_baslat()
        self._zamanlayiciyi_baslat()

        self.mesaj_ekle(
            "friday",
            f'Merhaba! "{WAKE_WORDS[0]}" ya da "uyan bakalım" diyerek beni '
            f'çağırabilirsin, ya da aşağıya yazabilirsin.',
        )

    # ---------- Genel arayüz iskeleti ----------
    def _arayuz_kur(self):
        # Tüm ekranı kaplayan HUD tuvali (en altta)
        self.canvas = ctk.CTkCanvas(self, bg="#03060a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._canvas_boyutu_degisti)

        # Üst çubuk (canvas'ın üzerinde, sağ üstte telefon butonu)
        ust = ctk.CTkFrame(self, fg_color="#03060a", corner_radius=0)
        ust.place(relx=0, rely=0, relwidth=1, y=0, height=40)
        ctk.CTkLabel(
            ust, text="FRIDAY // SISTEM AKTIF", font=ctk.CTkFont(family="Consolas", size=11),
            text_color="#7fb7ec",
        ).pack(side="left", padx=16)
        ctk.CTkButton(
            ust, text="📱", width=32, height=28, fg_color="#0c1c2c", hover_color="#163a56",
            command=self.qr_goster,
        ).pack(side="right", padx=12, pady=4)

        # Köşedeki sohbet kutusu — sesle söylediklerin buraya metin olarak
        # düşer, mikrofonun yoksa buradan yazabilirsin.
        self.sohbet_paneli = ctk.CTkFrame(self, fg_color="#0a0e16", corner_radius=10,
                                           border_width=1, border_color="#163a56")
        self.sohbet_paneli.place(relx=1.0, rely=1.0, anchor="se", x=-16, y=-16,
                                  relwidth=0.32, relheight=0.42)
        self.sohbet_paneli.pack_propagate(False)

        ctk.CTkLabel(
            self.sohbet_paneli, text="SOHBET", font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#4a7599",
        ).pack(anchor="w", padx=10, pady=(8, 2))

        self.sohbet_kutusu = ctk.CTkTextbox(
            self.sohbet_paneli, fg_color="#03060a", text_color="#cfe8ff",
            font=ctk.CTkFont(family="Consolas", size=11), wrap="word", state="disabled",
        )
        self.sohbet_kutusu.pack(fill="both", expand=True, padx=8, pady=4)

        alt = ctk.CTkFrame(self.sohbet_paneli, fg_color="transparent")
        alt.pack(fill="x", padx=8, pady=(0, 8))
        self.giris = ctk.CTkEntry(alt, placeholder_text="Mikrofonun yoksa buraya yaz...", height=32)
        self.giris.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.giris.bind("<Return>", lambda e: self.metin_gonder())
        ctk.CTkButton(alt, text="➤", width=32, height=32, command=self.metin_gonder).pack(side="left")

    def _canvas_boyutu_degisti(self, event):
        self._cx = event.width / 2
        self._cy = event.height / 2 - 20  # üst çubuğa yer aç
        self._yaricap = max(60, min(event.width, event.height) * 0.16)
        self._hud_yeniden_konumlandir()

    # ---------- HUD (Canvas üzerinde çizilen halkalar) ----------
    def _hud_kur(self):
        self._cx, self._cy, self._yaricap = 240, 300, 90
        c = self.canvas

        # Statik dış çember
        self._disCember = c.create_oval(0, 0, 0, 0, outline="#163a56", width=1)

        # Statik pusula çentikleri (8 yön)
        self._centikler = [c.create_line(0, 0, 0, 0, fill="#163a56", width=1) for _ in range(8)]

        # Dönen halkadaki 16 küçük çentik (gerçek "dönme" hissi bunlarla verilir)
        self._donen_centikler = [
            c.create_line(0, 0, 0, 0, fill=_DURUM_RENKLERI["dinliyor"], width=1)
            for _ in range(16)
        ]

        # Ters yönde dönen ark
        self._ters_ark = c.create_arc(0, 0, 0, 0, start=0, extent=70, style="arc",
                                       outline=_DURUM_RENKLERI["dinliyor"], width=2)

        # Altıgen çekirdek çerçevesi
        self._hexagon = c.create_polygon(0, 0, outline=_DURUM_RENKLERI["dinliyor"],
                                          fill="", width=2)

        # Nabız gibi atan merkez nokta
        self._merkez_nokta = c.create_oval(0, 0, 0, 0, fill=_DURUM_RENKLERI["dinliyor"], outline="")

        # Durum etiketi (altta)
        self._durum_yazisi = c.create_text(
            0, 0, text=_DURUM_ETIKETLERI["dinliyor"], fill=_DURUM_RENKLERI["dinliyor"],
            font=("Consolas", 13, "bold"),
        )

        # Alt bilgi çizgisi
        self._alt_bilgi = c.create_text(
            0, 0, text="[F1] TAM EKRANDAN ÇIK (uygulamayı kapatmaz)",
            fill="#2c4f6b", font=("Consolas", 9),
        )

        self._hud_yeniden_konumlandir()

    def _hud_yeniden_konumlandir(self):
        cx, cy, r = self._cx, self._cy, self._yaricap
        c = self.canvas

        c.coords(self._disCember, cx - r, cy - r, cx + r, cy + r)

        for i, item in enumerate(self._centikler):
            aci = math.radians(i * 45)
            ic_r, dis_r = r - 8, r
            c.coords(
                item,
                cx + ic_r * math.cos(aci), cy + ic_r * math.sin(aci),
                cx + dis_r * math.cos(aci), cy + dis_r * math.sin(aci),
            )

        c.coords(self._ters_ark, cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.7)

        self._hexagon_koordinatlarini_guncelle(cx, cy, r * 0.4)

        c.coords(self._durum_yazisi, cx, cy + r + 26)
        c.coords(self._alt_bilgi, cx, cy + r + 50)

        self._donen_centikleri_ciz()
        self._merkez_noktayi_ciz()

    def _hexagon_koordinatlarini_guncelle(self, cx, cy, r):
        noktalar = []
        for i in range(6):
            aci = math.radians(60 * i - 90)
            noktalar.extend([cx + r * math.cos(aci), cy + r * math.sin(aci)])
        self.canvas.coords(self._hexagon, *noktalar)

    def _donen_centikleri_ciz(self):
        cx, cy, r = self._cx, self._cy, self._yaricap * 0.75
        for i, item in enumerate(self._donen_centikler):
            aci = math.radians(i * (360 / len(self._donen_centikler)) + self._ring_aci)
            ic_r, dis_r = r - 6, r
            self.canvas.coords(
                item,
                cx + ic_r * math.cos(aci), cy + ic_r * math.sin(aci),
                cx + dis_r * math.cos(aci), cy + dis_r * math.sin(aci),
            )

    def _merkez_noktayi_ciz(self):
        cx, cy = self._cx, self._cy
        nabiz = 5 + 2.5 * math.sin(self._pulse_faz)
        self.canvas.coords(self._merkez_nokta, cx - nabiz, cy - nabiz, cx + nabiz, cy + nabiz)

    def _hud_donguyu_baslat(self):
        self._ring_aci = (self._ring_aci + 4) % 360
        self._pulse_faz += 0.35
        self._donen_centikleri_ciz()
        self._merkez_noktayi_ciz()

        # Ters ark yavaşça geri döner
        mevcut_baslangic = self.canvas.itemcget(self._ters_ark, "start")
        try:
            yeni_baslangic = (float(mevcut_baslangic) - 3) % 360
        except ValueError:
            yeni_baslangic = 0
        self.canvas.itemconfig(self._ters_ark, start=yeni_baslangic)

        self.after(HUD_TIK_MS, self._hud_donguyu_baslat)

    def _durumu_uygula(self, durum: str):
        if durum not in _DURUM_RENKLERI:
            return
        self._durum = durum
        renk = _DURUM_RENKLERI[durum]
        c = self.canvas
        for item in self._donen_centikler:
            c.itemconfig(item, fill=renk)
        c.itemconfig(self._ters_ark, outline=renk)
        c.itemconfig(self._hexagon, outline=renk)
        c.itemconfig(self._merkez_nokta, fill=renk)
        c.itemconfig(self._durum_yazisi, text=_DURUM_ETIKETLERI[durum], fill=renk)

    # ---------- Sohbet paneli ----------
    def mesaj_ekle(self, kimden, metin):
        onek = "Sen: " if kimden == "user" else "Friday: "
        self.sohbet_kutusu.configure(state="normal")
        self.sohbet_kutusu.insert("end", f"{onek}{metin}\n\n")
        self.sohbet_kutusu.see("end")
        self.sohbet_kutusu.configure(state="disabled")

    def metin_gonder(self):
        metin = self.giris.get().strip()
        if not metin:
            return
        self.giris.delete(0, "end")
        self.mesaj_ekle("user", metin)
        cevap = komutu_isle(metin)
        self.mesaj_ekle("friday", cevap)
        konus(cevap)

    # ---------- Diğer eylemler ----------
    def _logo_ayarla(self):
        try:
            yol = os.path.join(kaynak_klasoru(), "icon.ico")
            if os.path.exists(yol):
                self.iconbitmap(yol)
        except Exception:
            pass  # ikon bulunamazsa program yine de çalışsın

    def _tam_ekrani_degistir(self, event=None):
        self._tam_ekran = not self._tam_ekran
        self.attributes("-fullscreen", self._tam_ekran)
        if not self._tam_ekran:
            self.geometry("480x680")

    def qr_goster(self):
        pencere = ctk.CTkToplevel(self)
        pencere.title("Telefondan Bağlan")
        pencere.geometry("300x400")
        pencere.attributes("-topmost", True)

        ip = yerel_ip_al()
        url = f"http://{ip}:{FLASK_PORT}"
        img = qrcode.make(url).resize((220, 220))
        foto = ImageTk.PhotoImage(img)

        etiket = ctk.CTkLabel(pencere, text="", image=foto)
        etiket.image = foto
        etiket.pack(pady=16)

        ctk.CTkLabel(pencere, text="Aynı Wi-Fi ağındayken\ntelefonunla tarat:", justify="center").pack()
        ctk.CTkLabel(pencere, text=url, wraplength=260, text_color="#9aa0ad").pack(pady=8)

    # ---------- Arka plan servisleri ----------
    def _sunucuyu_baslat(self):
        def calistir():
            flask_app.run(host="0.0.0.0", port=FLASK_PORT, debug=False, use_reloader=False)
        threading.Thread(target=calistir, daemon=True).start()

    def _dinleyiciyi_baslat(self):
        try:
            self.dinleyici = UyanmaDinleyici(self.mesaj_ekle)
            self.dinleyici.baslat()
        except Exception as e:
            hud_durum.durum_ayarla("hata")
            self.mesaj_ekle(
                "friday",
                f"Mikrofon dinleme başlatılamadı: {e}\n"
                "(Mikrofonun bağlı mı? Sorun değil, sağ alttaki kutudan "
                "yazarak komut vermeye devam edebilirsin.)",
            )

    def _zamanlayiciyi_baslat(self):
        self.zamanlayici = Zamanlayici()
        self.zamanlayici.baslat()


if __name__ == "__main__":
    app = FridayApp()
    app.mainloop()
