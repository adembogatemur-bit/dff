# extras_eglence.py
# Eğlence/pratik küçük özellikler: yazı-tura, zar, rastgele sayı, kelime
# sayma, şaka, günün alıntısı, ruh haline göre müzik önerisi.

import random
from web_actions import spotify_ara

_SAKALAR = [
    "Bilgisayarım bir şaka anlatmaya çalıştı ama RAM'i yetmedi.",
    "Neden programcılar karanlıkta çalışır? Çünkü ışık bug'ları çeker.",
    "İki tel karşılaşmış, biri diğerine 'Selam nötr' demiş.",
    "Bir SQL sorgusu bara girer, iki masaya yaklaşır ve sorar: Katılabilir miyim?",
]

_ALINTILAR = [
    "Başarı, her gün küçük çabaların toplamıdır.",
    "En karanlık gece bile biter, güneş yine doğar.",
    "Bugün yapabileceğini yarına bırakma.",
    "Küçük adımlar, büyük yolculukların başlangıcıdır.",
]

_RUH_HALI_MUZIK = {
    "mutlu": "upbeat pop hits",
    "üzgün": "sad acoustic songs",
    "sakin": "chill lofi beats",
    "enerjik": "workout motivation",
    "odaklanmış": "focus instrumental",
    "nostaljik": "2000ler türkçe pop",
}


def yazi_tura() -> str:
    return random.choice(["Yazı!", "Tura!"])


def zar_at(yuz_sayisi: int = 6) -> str:
    return f"{random.randint(1, yuz_sayisi)} geldi."


def rastgele_sayi(alt: int, ust: int) -> str:
    if alt > ust:
        alt, ust = ust, alt
    return f"{random.randint(alt, ust)}"


def kelime_karakter_say(metin: str) -> str:
    kelime_sayisi = len(metin.split())
    karakter_sayisi = len(metin)
    return f"{kelime_sayisi} kelime, {karakter_sayisi} karakter."


def saka_anlat() -> str:
    return random.choice(_SAKALAR)


def gunun_alintisi() -> str:
    return random.choice(_ALINTILAR)


def ruh_haline_gore_muzik(ruh_hali: str) -> str:
    ruh_hali_kucuk = ruh_hali.strip().lower()
    sorgu = _RUH_HALI_MUZIK.get(ruh_hali_kucuk)
    if not sorgu:
        secenekler = ", ".join(_RUH_HALI_MUZIK.keys())
        return f"'{ruh_hali}' ruh halini tanımıyorum. Şunları deneyebilirsin: {secenekler}"
    return spotify_ara(sorgu)
