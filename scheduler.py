# scheduler.py
# "Her sabah 08:00'de sabah brifingi ver" gibi, config.py'deki
# SCHEDULED_TASKS listesine göre otomatik komut çalıştırma.

import threading
import time
import datetime
from config import SCHEDULED_TASKS
from commands import komutu_isle
from desktop_tts import konus
import bildirim


class Zamanlayici:
    def __init__(self):
        self._durduruldu = threading.Event()
        self._calisan = set()

    def baslat(self):
        threading.Thread(target=self._dongu, daemon=True).start()

    def durdur(self):
        self._durduruldu.set()

    def _dongu(self):
        while not self._durduruldu.is_set():
            simdi = datetime.datetime.now().strftime("%H:%M")
            for gorev in SCHEDULED_TASKS:
                anahtar = (gorev["saat"], simdi)
                if gorev["saat"] == simdi and anahtar not in self._calisan:
                    self._calisan.add(anahtar)
                    cevap = komutu_isle(gorev["komut"])
                    bildirim.bildir("friday", f"[Zamanlanmış] {cevap}")
                    konus(cevap)

            if len(self._calisan) > 300:
                self._calisan.clear()

            time.sleep(20)
