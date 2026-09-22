# extras_bilgi.py
# Bilgi/sorgu özellikleri: Wikipedia özeti, çeviri, kripto para fiyatı,
# son depremler, namaz vakitleri. Hepsi ücretsiz, anahtarsız servisler kullanır.

import requests
from config import DEFAULT_CITY


def wikipedia_ozeti(konu: str) -> str:
    konu = konu.strip()
    if not konu:
        return "Neyi aramamı istediğini söylemedin."
    try:
        url = f"https://tr.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(konu)}"
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return f"'{konu}' için bir şey bulamadım."
        veri = r.json()
        ozet = veri.get("extract", "")
        return ozet if ozet else f"'{konu}' için bir özet bulamadım."
    except Exception as e:
        return f"Wikipedia'ya ulaşamadım: {e}"


def cevir(metin: str, kaynak_dil: str = "tr", hedef_dil: str = "en") -> str:
    metin = metin.strip()
    if not metin:
        return "Ne çevirmemi istediğini söylemedin."
    try:
        url = "https://api.mymemory.translated.net/get"
        parametreler = {"q": metin, "langpair": f"{kaynak_dil}|{hedef_dil}"}
        r = requests.get(url, params=parametreler, timeout=10)
        veri = r.json()
        ceviri = veri.get("responseData", {}).get("translatedText")
        return ceviri if ceviri else "Çeviremedim."
    except Exception as e:
        return f"Çeviri servisine ulaşamadım: {e}"


def kripto_fiyati(coin: str) -> str:
    coin_kucuk = coin.strip().lower()
    coin_isimleri = {
        "bitcoin": "bitcoin", "btc": "bitcoin",
        "ethereum": "ethereum", "eth": "ethereum",
        "dogecoin": "dogecoin", "doge": "dogecoin",
        "solana": "solana", "sol": "solana",
    }
    coin_id = coin_isimleri.get(coin_kucuk, coin_kucuk)
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        parametreler = {"ids": coin_id, "vs_currencies": "usd,try"}
        r = requests.get(url, params=parametreler, timeout=10)
        veri = r.json()
        if coin_id not in veri:
            return f"'{coin}' adlı bir kripto para bulamadım."
        fiyat = veri[coin_id]
        return f"{coin.capitalize()}: ${fiyat.get('usd')} / ₺{fiyat.get('try')}"
    except Exception as e:
        return f"Kripto fiyatı alınamadı: {e}"


def son_depremler(adet: int = 5) -> str:
    try:
        r = requests.get("https://api.orhanaydogdu.com.tr/deprem/kandilli/live", timeout=10)
        veri = r.json()
        sonuclar = veri.get("result", [])[:adet]
        if not sonuclar:
            return "Deprem verisi bulunamadı."
        satirlar = [
            f"- {d.get('title', '?')} — büyüklük {d.get('mag', '?')} ({d.get('date', '?')})"
            for d in sonuclar
        ]
        return "Son depremler:\n" + "\n".join(satirlar)
    except Exception as e:
        return f"Deprem verisi alınamadı: {e}"


def namaz_vakitleri(sehir: str = None) -> str:
    sehir = (sehir or DEFAULT_CITY or "Istanbul").strip()
    try:
        url = f"https://api.aladhan.com/v1/timingsByCity"
        parametreler = {"city": sehir, "country": "Turkey", "method": 13}
        r = requests.get(url, params=parametreler, timeout=10)
        veri = r.json()
        vakitler = veri.get("data", {}).get("timings", {})
        if not vakitler:
            return f"{sehir} için namaz vakti bulunamadı."
        return (f"{sehir} namaz vakitleri — İmsak: {vakitler.get('Fajr')}, "
                f"Güneş: {vakitler.get('Sunrise')}, Öğle: {vakitler.get('Dhuhr')}, "
                f"İkindi: {vakitler.get('Asr')}, Akşam: {vakitler.get('Maghrib')}, "
                f"Yatsı: {vakitler.get('Isha')}")
    except Exception as e:
        return f"Namaz vakitleri alınamadı: {e}"
