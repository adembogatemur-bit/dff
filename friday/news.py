# news.py
# Güncel haber başlıklarını RSS'ten okuma.

import requests
import xml.etree.ElementTree as ET

_HABER_KAYNAGI = "https://www.ntv.com.tr/gundem.rss"


def haber_basliklarini_oku(adet: int = 5) -> str:
    try:
        r = requests.get(_HABER_KAYNAGI, timeout=10)
        kok = ET.fromstring(r.content)
        basliklar = [oge.text for oge in kok.findall(".//item/title")][:adet]
        if not basliklar:
            return "Haber başlığı bulunamadı."
        return "Son haberler:\n" + "\n".join(f"- {b}" for b in basliklar)
    except Exception as e:
        return f"Haberler alınamadı: {e}"
