# reminders.py
# "15 dakika sonra hatırlat: X" gibi tek seferlik hatırlatıcılar.

import re
import threading
from desktop_tts import konus
import bildirim
from toast import bildirim_goster


def hatirlatici_kur(komut_metni: str) -> str:
    eslesme = re.match(
        r"(\d+)\s*(dakika|saat)\s*sonra hatırlat:?\s*(.*)",
        komut_metni.strip(), re.IGNORECASE,
    )
    if not eslesme:
        return "Kullanım: <sayı> dakika/saat sonra hatırlat: <mesaj>"

    sayi, birim, mesaj = eslesme.groups()
    saniye = int(sayi) * (3600 if birim.lower() == "saat" else 60)
    mesaj = mesaj.strip() or "Hatırlatma zamanı geldi!"

    def calistir():
        konus(f"Hatırlatma: {mesaj}")
        bildirim.bildir("friday", f"⏰ Hatırlatma: {mesaj}")
        bildirim_goster("Friday - Hatırlatma", mesaj)

    threading.Timer(saniye, calistir).start()
    return f"Tamam, {sayi} {birim} sonra hatırlatacağım: {mesaj}"
