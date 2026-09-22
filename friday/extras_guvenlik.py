# extras_guvenlik.py
# Güvenli şifre üretme, hafıza/ajanda yedekleme, fabrika ayarlarına dönme.

import os
import secrets
import string
import shutil
import datetime
from utils import veri_klasoru

FRIDAY_SURUMU = "Friday v4.0 — 100 özellikli sürüm"


def sifre_uret(uzunluk: int = 16) -> str:
    if uzunluk < 6:
        uzunluk = 6
    karakterler = string.ascii_letters + string.digits + "!@#$%&*"
    sifre = "".join(secrets.choice(karakterler) for _ in range(uzunluk))
    return f"Üretilen şifre: {sifre}"


def yedekle() -> str:
    kaynak = veri_klasoru()
    zaman_damgasi = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    hedef = os.path.join(kaynak, "yedekler", f"yedek_{zaman_damgasi}")

    try:
        os.makedirs(hedef, exist_ok=True)
        for dosya_adi in ("hafiza.txt", "ajanda.json", "notlarim.txt"):
            kaynak_dosya = os.path.join(kaynak, dosya_adi)
            if os.path.exists(kaynak_dosya):
                shutil.copy2(kaynak_dosya, hedef)
        return f"Yedeklendi: {hedef}"
    except Exception as e:
        return f"Yedeklenemedi: {e}"


def fabrika_ayarlarina_dondur() -> str:
    kaynak = veri_klasoru()
    silinenler = []
    for dosya_adi in ("hafiza.txt", "ajanda.json", "notlarim.txt"):
        yol = os.path.join(kaynak, dosya_adi)
        if os.path.exists(yol):
            os.remove(yol)
            silinenler.append(dosya_adi)
    if not silinenler:
        return "Zaten silinecek bir şey yoktu."
    return f"Şunlar silindi, sıfırdan başlıyoruz: {', '.join(silinenler)}"


def surum_bilgisi() -> str:
    return FRIDAY_SURUMU
