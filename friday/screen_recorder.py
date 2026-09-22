# screen_recorder.py
# "ekran kaydı başlat" / "ekran kaydını durdur" ile video olarak ekran kaydı.

import os
import threading
import datetime
import numpy as np
import cv2
from PIL import ImageGrab
from utils import veri_klasoru

_KAYIT = {"aktif": False, "yol": None}


def ekran_kaydini_baslat() -> str:
    if _KAYIT["aktif"]:
        return "Zaten ekran kaydı yapıyorum."

    zaman_damgasi = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    masaustu = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.isdir(masaustu):
        masaustu = veri_klasoru()
    yol = os.path.join(masaustu, f"ekran_kaydi_{zaman_damgasi}.avi")

    _KAYIT["aktif"] = True
    _KAYIT["yol"] = yol
    threading.Thread(target=_kaydet, args=(yol,), daemon=True).start()
    return "Ekran kaydı başladı. Durdurmak için 'ekran kaydını durdur' de."


def _kaydet(yol: str):
    ilk_kare = ImageGrab.grab()
    genislik, yukseklik = ilk_kare.size
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    yazici = cv2.VideoWriter(yol, fourcc, 10.0, (genislik, yukseklik))

    try:
        while _KAYIT["aktif"]:
            kare = ImageGrab.grab()
            kare_np = cv2.cvtColor(np.array(kare), cv2.COLOR_RGB2BGR)
            yazici.write(kare_np)
    finally:
        yazici.release()


def ekran_kaydini_durdur() -> str:
    if not _KAYIT["aktif"]:
        return "Zaten ekran kaydı yapmıyordum."
    _KAYIT["aktif"] = False
    return f"Ekran kaydı durduruldu. Dosya: {_KAYIT.get('yol')}"
