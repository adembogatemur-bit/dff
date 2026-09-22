# web_actions.py
import re
import webbrowser
import urllib.parse
import requests
import xml.etree.ElementTree as ET
from config import CHANNELS


def google_ara(sorgu: str) -> str:
    url = "https://www.google.com/search?q=" + urllib.parse.quote(sorgu)
    webbrowser.open(url)
    return f"Google'da aranıyor: {sorgu}"


def youtube_ara(sorgu: str) -> str:
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(sorgu)
    webbrowser.open(url)
    return f"YouTube'da aranıyor: {sorgu}"


def spotify_ara(sorgu: str) -> str:
    uri = "spotify:search:" + urllib.parse.quote(sorgu)
    try:
        webbrowser.open(uri)
    except Exception:
        webbrowser.open("https://open.spotify.com/search/" + urllib.parse.quote(sorgu))
    return f"Spotify'da aranıyor: {sorgu}"


def site_ac(adres: str) -> str:
    adres = adres.strip()
    if not adres.startswith("http://") and not adres.startswith("https://"):
        adres = "https://" + adres
    webbrowser.open(adres)
    return f"Açılıyor: {adres}"


def _kanal_id_bul(deger: str):
    deger = deger.strip()
    if re.match(r"^UC[\w-]{20,}$", deger):
        return deger
    handle = deger if deger.startswith("@") else "@" + deger
    try:
        r = requests.get(f"https://www.youtube.com/{handle}", timeout=10)
        eslesme = re.search(r'"channelId":"(UC[\w-]{20,})"', r.text)
        if eslesme:
            return eslesme.group(1)
    except Exception:
        pass
    return None


def kanalin_son_videosunu_ac(kanal_adi: str) -> str:
    kanal_adi_kucuk = kanal_adi.strip().lower()
    deger = CHANNELS.get(kanal_adi_kucuk, kanal_adi)
    kanal_id = _kanal_id_bul(deger)

    if not kanal_id:
        return (f"'{kanal_adi}' kanalını bulamadım. config.py içindeki CHANNELS "
                f'sözlüğüne şunu ekleyebilirsin: "{kanal_adi_kucuk}": "@kanalkullaniciadi"')

    try:
        r = requests.get(
            f"https://www.youtube.com/feeds/videos.xml?channel_id={kanal_id}", timeout=10
        )
        kok = ET.fromstring(r.content)
        ad_alani = {"yt": "http://www.youtube.com/xml/schemas/2015"}
        video_id_elemani = kok.find(".//yt:videoId", ad_alani)
        if video_id_elemani is None:
            return f"{kanal_adi} kanalının videosu bulunamadı."
        video_url = f"https://www.youtube.com/watch?v={video_id_elemani.text}"
        webbrowser.open(video_url)
        return f"{kanal_adi} kanalının son videosu açılıyor."
    except Exception as e:
        return f"Video açılamadı: {e}"
