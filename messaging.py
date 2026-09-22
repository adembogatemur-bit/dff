# messaging.py
# WhatsApp Web üzerinden mesaj gönderme. İsim söyleyerek de (CONTACTS
# listesinden bularak) ya da doğrudan numara vererek gönderebilirsin.
#
# Not: Bilgisayarındaki tarayıcıda web.whatsapp.com'a daha önce QR ile
# giriş yapmış olman gerekir.

import re
import pywhatkit
from config import DEFAULT_COUNTRY_CODE, CONTACTS


def _ismi_normallestir(s: str) -> str:
    s = s.strip().lower().replace("’", "'")
    s = s.split("'")[0]
    s = re.sub(r"(e|a|ye|ya|nin|nın|nun|nün|ın|in|un|ün|i|ı|u|ü)$", "", s)
    return s


def kisi_numarasi_bul(isim_veya_numara: str):
    ham = isim_veya_numara.strip()
    sadece_sayi = ham.replace("+", "").replace(" ", "")
    if sadece_sayi.isdigit():
        return ham

    hedef = _ismi_normallestir(ham)
    for isim, numara in CONTACTS.items():
        if _ismi_normallestir(isim) == hedef:
            return numara
    return None


def whatsapp_mesaj_gonder(hedef: str, mesaj: str) -> str:
    numara = kisi_numarasi_bul(hedef)
    if not numara:
        return (f"'{hedef}' isimli bir kişi bulamadım. config.py içindeki CONTACTS "
                f'sözlüğüne şunu ekleyebilirsin: "{hedef.lower()}": "+90XXXXXXXXXX"')

    if not numara.startswith("+"):
        numara = DEFAULT_COUNTRY_CODE + numara.lstrip("0")

    try:
        pywhatkit.sendwhatmsg_instantly(
            phone_no=numara,
            message=mesaj,
            wait_time=20,
            tab_close=True,
        )
        return f"Mesaj gönderiliyor: {hedef} -> {mesaj}"
    except Exception as e:
        return f"Mesaj gönderilemedi: {e}"
