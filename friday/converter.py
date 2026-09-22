# converter.py
# Birim çevirme (km/mil, kg/pound, santigrat/fahrenayt) ve döviz kuru çevirme.

import requests

_BIRIM_CARPANLARI = {
    ("km", "mil"): 0.621371,
    ("mil", "km"): 1.60934,
    ("kg", "pound"): 2.20462,
    ("pound", "kg"): 0.453592,
    ("santigrat", "fahrenayt"): lambda c: c * 9 / 5 + 32,
    ("fahrenayt", "santigrat"): lambda f: (f - 32) * 5 / 9,
    ("metre", "feet"): 3.28084,
    ("feet", "metre"): 0.3048,
}


def birim_cevir(deger: float, kaynak: str, hedef: str) -> str:
    anahtar = (kaynak.lower(), hedef.lower())
    if anahtar not in _BIRIM_CARPANLARI:
        return (f"'{kaynak}' -> '{hedef}' dönüşümünü bilmiyorum. "
                f"Bilinenler: km/mil, kg/pound, santigrat/fahrenayt, metre/feet")

    islem = _BIRIM_CARPANLARI[anahtar]
    sonuc = islem(deger) if callable(islem) else deger * islem
    return f"{deger} {kaynak} = {sonuc:.2f} {hedef}"


def doviz_cevir(miktar: float, kaynak: str, hedef: str) -> str:
    try:
        r = requests.get(f"https://api.exchangerate-api.com/v4/latest/{kaynak.upper()}", timeout=10)
        veri = r.json()
        kur = veri.get("rates", {}).get(hedef.upper())
        if kur is None:
            return f"'{hedef}' para birimini bulamadım."
        sonuc = miktar * kur
        return f"{miktar} {kaynak.upper()} = {sonuc:.2f} {hedef.upper()}"
    except Exception as e:
        return f"Döviz kuru alınamadı: {e}"
