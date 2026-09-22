# pomodoro.py
# Pomodoro çalışma tekniği: 25 dakika çalış, 5 dakika mola — sesli olarak
# haber verir.

import threading
from desktop_tts import konus
import bildirim

_CALISMA_SURESI = 25 * 60
_MOLA_SURESI = 5 * 60


def pomodoro_baslat() -> str:
    def mola_baslat():
        konus("25 dakika doldu! Şimdi 5 dakika mola zamanı.")
        bildirim.bildir("friday", "🍅 Pomodoro: mola zamanı (5 dakika)")
        threading.Timer(_MOLA_SURESI, mola_bitti).start()

    def mola_bitti():
        konus("Mola bitti, tekrar çalışma zamanı!")
        bildirim.bildir("friday", "🍅 Pomodoro: mola bitti, çalışmaya devam")

    threading.Timer(_CALISMA_SURESI, mola_baslat).start()
    return "Pomodoro başladı: 25 dakika çalışma süresi başlıyor."
