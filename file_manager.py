# file_manager.py
# Dosya arama, çöp kutusuna silme, yazdırma, bir klasördeki en son
# dosyayı açma.

import os
from send2trash import send2trash


def dosya_ara(dosya_adi: str, taban_dizin: str = None) -> str:
    taban_dizin = taban_dizin or os.path.expanduser("~")
    dosya_adi_kucuk = dosya_adi.strip().lower()
    bulunanlar = []

    for kok, dizinler, dosyalar in os.walk(taban_dizin):
        dizinler[:] = [
            d for d in dizinler
            if not d.startswith((".", "$")) and d.lower() not in ("appdata", "node_modules", "venv")
        ]
        for dosya in dosyalar:
            if dosya_adi_kucuk in dosya.lower():
                bulunanlar.append(os.path.join(kok, dosya))
                if len(bulunanlar) >= 5:
                    break
        if len(bulunanlar) >= 5:
            break

    if not bulunanlar:
        return f"'{dosya_adi}' bulunamadı."

    try:
        os.startfile(os.path.dirname(bulunanlar[0]))
    except Exception:
        pass

    liste = "\n".join(bulunanlar)
    return f"{len(bulunanlar)} sonuç bulundu, klasörünü açtım:\n{liste}"


def dosya_sil(yol: str) -> str:
    yol = yol.strip().strip('"')
    if not os.path.exists(yol):
        return f"Böyle bir dosya/klasör bulunamadı: {yol}"
    try:
        send2trash(yol)
        return f"Çöp kutusuna taşındı: {yol}"
    except Exception as e:
        return f"Silinemedi: {e}"


def son_dosyayi_ac(klasor_adi: str) -> str:
    bilinen = {
        "indirilenler": os.path.join(os.path.expanduser("~"), "Downloads"),
        "masaüstü": os.path.join(os.path.expanduser("~"), "Desktop"),
        "belgelerim": os.path.join(os.path.expanduser("~"), "Documents"),
    }
    klasor = bilinen.get(klasor_adi.strip().lower())
    if not klasor or not os.path.isdir(klasor):
        return f"'{klasor_adi}' klasörünü tanımıyorum (indirilenler / masaüstü / belgelerim kullanabilirsin)."

    dosyalar = [
        os.path.join(klasor, d) for d in os.listdir(klasor)
        if os.path.isfile(os.path.join(klasor, d))
    ]
    if not dosyalar:
        return f"{klasor_adi} klasöründe dosya yok."

    en_yeni = max(dosyalar, key=os.path.getmtime)
    os.startfile(en_yeni)
    return f"Açılıyor: {os.path.basename(en_yeni)}"


def belgeyi_yazdir(yol: str) -> str:
    yol = yol.strip().strip('"')
    if not os.path.exists(yol):
        return f"Böyle bir dosya bulunamadı: {yol}"
    try:
        os.startfile(yol, "print")
        return f"Yazdırılıyor: {yol}"
    except Exception as e:
        return f"Yazdırılamadı: {e}"
