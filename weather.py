# weather.py
# Hava durumu bilgisi (OpenWeatherMap ücretsiz API ile).

import requests
from config import OPENWEATHER_API_KEY, DEFAULT_CITY


def hava_durumu_soyle(sehir: str = None) -> str:
    if not OPENWEATHER_API_KEY:
        return ("Hava durumu için config.py içine ücretsiz bir OpenWeatherMap "
                "API anahtarı eklemen gerekiyor (openweathermap.org/api adresinden alabilirsin).")

    sehir = (sehir or DEFAULT_CITY or "").strip()
    if not sehir:
        return "Hangi şehrin hava durumunu istiyorsun? config.py'de DEFAULT_CITY ayarlayabilirsin."

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        parametreler = {"q": sehir, "appid": OPENWEATHER_API_KEY, "units": "metric", "lang": "tr"}
        r = requests.get(url, params=parametreler, timeout=10)
        veri = r.json()

        if r.status_code != 200:
            return f"Hava durumu alınamadı: {veri.get('message', 'bilinmeyen hata')}"

        sicaklik = veri["main"]["temp"]
        hissedilen = veri["main"]["feels_like"]
        aciklama = veri["weather"][0]["description"]
        return f"{sehir}: {aciklama}, {sicaklik:.0f} derece (hissedilen {hissedilen:.0f} derece)."
    except Exception as e:
        return f"Hava durumu alınamadı: {e}"
