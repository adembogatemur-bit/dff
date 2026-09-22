# email_sender.py
# Gmail üzerinden e-posta gönderme.

import smtplib
from email.mime.text import MIMEText
from config import EMAIL_ADDRESS, EMAIL_APP_PASSWORD, EMAIL_CONTACTS


def eposta_gonder(hedef: str, konu: str, govde: str) -> str:
    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:
        return ("E-posta göndermek için config.py içine EMAIL_ADDRESS ve "
                "EMAIL_APP_PASSWORD (Gmail Uygulama Şifresi) eklemen gerekiyor.")

    alici = EMAIL_CONTACTS.get(hedef.strip().lower(), hedef.strip())
    if "@" not in alici:
        return f"'{hedef}' için bir e-posta adresi bulamadım. config.py'deki EMAIL_CONTACTS'a ekleyebilirsin."

    try:
        mesaj = MIMEText(govde)
        mesaj["Subject"] = konu
        mesaj["From"] = EMAIL_ADDRESS
        mesaj["To"] = alici

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as sunucu:
            sunucu.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
            sunucu.send_message(mesaj)
        return f"E-posta gönderildi: {alici}"
    except Exception as e:
        return f"E-posta gönderilemedi: {e}"
