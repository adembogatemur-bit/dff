# dictation.py
# Dikte modu: "dikte başlat" dedikten sonra söylediğin her şey uyandırma
# kelimesi gerekmeden bir metin dosyasına yazılır, "dikte durdur" deyince biter.

import os
import datetime
from utils import veri_klasoru

_AKTIF = {"durum": False, "dosya_yolu": None}


def dikte_baslat() -> str:
    zaman_damgasi = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    masaustu = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.isdir(masaustu):
        masaustu = veri_klasoru()
    yol = os.path.join(masaustu, f"dikte_{zaman_damgasi}.txt")

    _AKTIF["durum"] = True
    _AKTIF["dosya_yolu"] = yol
    return f"Dikte başladı, konuştuklarını şuraya yazacağım: {yol}\nBitirmek için 'dikte durdur' de."


def dikte_aktif_mi() -> bool:
    return _AKTIF["durum"]


def dikte_yaz(metin: str):
    if not _AKTIF["durum"] or not _AKTIF["dosya_yolu"]:
        return
    with open(_AKTIF["dosya_yolu"], "a", encoding="utf-8") as f:
        f.write(metin + " ")


def dikte_durdur() -> str:
    yol = _AKTIF["dosya_yolu"]
    _AKTIF["durum"] = False
    _AKTIF["dosya_yolu"] = None
    return f"Dikte durduruldu. Dosya: {yol}" if yol else "Zaten dikte modunda değildim."
