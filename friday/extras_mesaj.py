# extras_mesaj.py
# Telegram mesajı gönderme (Bot API ile) ve Zoom/Teams gibi toplantı
# sitelerini açma.

import webbrowser
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def telegram_mesaj_gonder(mesaj: str) -> str:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return ("Telegram mesajı göndermek için config.py içine TELEGRAM_BOT_TOKEN "
                "ve TELEGRAM_CHAT_ID eklemen gerekiyor (BotFather üzerinden ücretsiz alınır).")
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        r = requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": mesaj}, timeout=10)
        if r.status_code == 200:
            return "Telegram mesajı gönderildi."
        return f"Telegram mesajı gönderilemedi: {r.text}"
    except Exception as e:
        return f"Telegram mesajı gönderilemedi: {e}"


def toplanti_sitesi_ac(isim: str) -> str:
    siteler = {
        "zoom": "https://zoom.us/join",
        "teams": "https://teams.microsoft.com",
        "meet": "https://meet.google.com",
        "google meet": "https://meet.google.com",
    }
    url = siteler.get(isim.strip().lower())
    if not url:
        return f"'{isim}' adlı bir toplantı sitesini tanımıyorum (zoom/teams/meet)."
    webbrowser.open(url)
    return f"{isim} açılıyor."
