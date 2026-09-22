# extras_takvim.py
# Windows/Outlook/Google Takvim'in okuyabileceği bir .ics dosyası üreterek
# takvime etkinlik ekleme (API anahtarı gerekmez, varsayılan takvim
# uygulamasını açar, kullanıcı "Kaydet"e basar).

import os
import re
import datetime
from utils import veri_klasoru


def _ics_zaman(dt: datetime.datetime) -> str:
    return dt.strftime("%Y%m%dT%H%M%S")


def takvime_etkinlik_ekle(aciklama: str) -> str:
    """'yarın saat 15:00 doktor randevusu' gibi basit bir ifadeyi ayrıştırır."""
    aciklama = aciklama.strip()
    saat_eslesme = re.search(r"(\d{1,2})[:.](\d{2})", aciklama)
    simdi = datetime.datetime.now()

    if "yarın" in aciklama.lower():
        gun = simdi + datetime.timedelta(days=1)
    else:
        gun = simdi

    if saat_eslesme:
        saat, dakika = int(saat_eslesme.group(1)), int(saat_eslesme.group(2))
        baslangic = gun.replace(hour=saat, minute=dakika, second=0, microsecond=0)
    else:
        baslangic = gun.replace(hour=9, minute=0, second=0, microsecond=0)

    bitis = baslangic + datetime.timedelta(hours=1)
    baslik = aciklama or "Friday Etkinliği"

    icerik = (
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "BEGIN:VEVENT\r\n"
        f"DTSTART:{_ics_zaman(baslangic)}\r\n"
        f"DTEND:{_ics_zaman(bitis)}\r\n"
        f"SUMMARY:{baslik}\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )

    yol = os.path.join(veri_klasoru(), "etkinlik.ics")
    with open(yol, "w", encoding="utf-8") as f:
        f.write(icerik)

    try:
        os.startfile(yol)
    except Exception:
        pass

    return f"Takvim uygulaman açılıyor, '{baslik}' etkinliğini onaylaman yeterli."
