# system_actions.py
# Bilgisayar üzerinde doğrudan etki eden komutlar burada.

import os
import ctypes
import subprocess
import datetime
import webbrowser
from config import APP_PATHS, SITE_ALTERNATIFLERI
from utils import veri_klasoru
from extras_windows import uygulama_gecmisine_ekle


def uygulama_ac(isim: str) -> str:
    isim_kucuk = isim.strip().lower()
    uygulama_gecmisine_ekle(isim)

    # 1) config.py içindeki bilinen tam yollardan dene
    if isim_kucuk in APP_PATHS:
        yol = os.path.expandvars(APP_PATHS[isim_kucuk])
        try:
            os.startfile(yol)
            return f"{isim} açılıyor."
        except FileNotFoundError:
            pass  # yol yanlışsa aşağıdaki yöntemlere devam et

    # 2) Windows'un kendi tanıdığı isimlerle dene (notepad, calc, mspaint...)
    try:
        os.startfile(isim_kucuk)
        return f"{isim} açılıyor."
    except FileNotFoundError:
        pass
    except Exception:
        pass

    # 3) 'start' komutu ile dene (PATH'te olan her şeyi açabilir)
    try:
        sonuc = subprocess.run(f'start "" "{isim}"', shell=True, capture_output=True)
        if sonuc.returncode == 0:
            return f"{isim} açılıyor."
    except Exception:
        pass

    # 4) Hiçbiri olmadıysa, bilinen bir web sitesi karşılığı var mı bak
    if isim_kucuk in SITE_ALTERNATIFLERI:
        webbrowser.open(SITE_ALTERNATIFLERI[isim_kucuk])
        return f"'{isim}' bilgisayarında bulunamadı, web sitesini açtım."

    return f"'{isim}' açılamadı. config.py dosyasına tam yolunu ekleyebilirsin."


def klasor_ac(yol: str) -> str:
    yol = yol.strip().strip('"')
    if not os.path.exists(yol):
        return f"Böyle bir klasör bulunamadı: {yol}"
    try:
        os.startfile(yol)
        return f"Klasör açıldı: {yol}"
    except Exception as e:
        return f"Klasör açılamadı: {e}"


def ekrani_kilitle() -> str:
    ctypes.windll.user32.LockWorkStation()
    return "Ekran kilitlendi."


def bilgisayari_kapat() -> str:
    subprocess.Popen("shutdown /s /t 5", shell=True)
    return "Bilgisayar 5 saniye içinde kapanacak. İptal etmek istersen komut istemine 'shutdown /a' yaz."


def bilgisayari_yeniden_baslat() -> str:
    subprocess.Popen("shutdown /r /t 5", shell=True)
    return "Bilgisayar 5 saniye içinde yeniden başlayacak. İptal etmek istersen komut istemine 'shutdown /a' yaz."


def not_al(metin: str) -> str:
    yol = os.path.join(veri_klasoru(), "notlarim.txt")
    with open(yol, "a", encoding="utf-8") as f:
        zaman = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        f.write(f"[{zaman}] {metin}\n")
    return "Not kaydedildi."


def ses_ayarla(yon: str) -> str:
    import keyboard
    if yon == "ac":
        for _ in range(6):
            keyboard.send("volume up")
        return "Ses açıldı."
    if yon == "kapat":
        keyboard.send("volume mute")
        return "Ses kapatıldı (tekrar söylersen açılır)."
    if yon == "kis":
        for _ in range(6):
            keyboard.send("volume down")
        return "Ses kısıldı."
    return "Anlaşılamadı."


def saat_soyle() -> str:
    simdi = datetime.datetime.now()
    return f"Saat {simdi.strftime('%H:%M')}"


def tarih_soyle() -> str:
    simdi = datetime.datetime.now()
    gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    return f"Bugün {simdi.strftime('%d.%m.%Y')}, {gunler[simdi.weekday()]}"


def ekran_goruntusu_al() -> str:
    try:
        from PIL import ImageGrab
        goruntu = ImageGrab.grab()
        masaustu = os.path.join(os.path.expanduser("~"), "Desktop")
        if not os.path.isdir(masaustu):
            masaustu = veri_klasoru()
        zaman_damgasi = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        yol = os.path.join(masaustu, f"ekran_goruntusu_{zaman_damgasi}.png")
        goruntu.save(yol)
        return f"Ekran görüntüsü kaydedildi: {yol}"
    except Exception as e:
        return f"Ekran görüntüsü alınamadı: {e}"
