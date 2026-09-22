# calculator.py
# Sesle/yazıyla basit matematik işlemleri: "127 çarpı 34 kaç eder" gibi.

import re

_KELIME_OPERATOR = {
    "artı": "+",
    "eksi": "-",
    "çarpı": "*",
    "bölü": "/",
    "üzeri": "**",
}


def hesapla(ifade: str) -> str:
    ifade_islenmis = ifade.lower()
    ifade_islenmis = ifade_islenmis.replace("kaç eder", "").replace("kaçtır", "").replace("kaç", "")

    for kelime, sembol in _KELIME_OPERATOR.items():
        ifade_islenmis = ifade_islenmis.replace(kelime, f" {sembol} ")

    ifade_islenmis = ifade_islenmis.strip()

    # Güvenlik: sadece rakam, nokta, boşluk ve izin verilen operatörler kalsın
    if not ifade_islenmis or not re.fullmatch(r"[\d\.\s\+\-\*/\(\)]+", ifade_islenmis):
        return "Bunu bir hesap işlemi olarak anlayamadım."

    try:
        sonuc = eval(ifade_islenmis, {"__builtins__": {}})
        return f"Sonuç: {sonuc}"
    except Exception:
        return "Bu işlemi hesaplayamadım."
