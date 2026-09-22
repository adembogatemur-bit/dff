# agenda.py
# Basit görev/ajanda listesi. Friday'in "bugün ne yapacağız" gibi
# sorularda tahmin yürütmek yerine gerçek verilerle cevap verebilmesi için.

import os
import json
import datetime
from utils import veri_klasoru

_DOSYA_ADI = "ajanda.json"


def _dosya_yolu() -> str:
    return os.path.join(veri_klasoru(), _DOSYA_ADI)


def _yukle():
    yol = _dosya_yolu()
    if not os.path.exists(yol):
        return []
    try:
        with open(yol, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _kaydet(gorevler):
    with open(_dosya_yolu(), "w", encoding="utf-8") as f:
        json.dump(gorevler, f, ensure_ascii=False, indent=2)


def gorev_ekle(metin: str) -> str:
    metin = metin.strip()
    if not metin:
        return "Ajandaya ne eklememi istediğini söylemedin. Örn: ajandama ekle: yarın matematik ödevi"

    gorevler = _yukle()
    gorevler.append({
        "metin": metin,
        "eklenme_tarihi": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
        "tamamlandi": False,
    })
    _kaydet(gorevler)
    return f"Ajandana ekledim: {metin}"


def ajandayi_listele() -> str:
    gorevler = _yukle()
    bekleyenler = [g for g in gorevler if not g["tamamlandi"]]
    if not bekleyenler:
        return "Ajandanda bekleyen bir görev yok."
    satirlar = [f"- {g['metin']}" for g in bekleyenler]
    return "Ajandandakiler:\n" + "\n".join(satirlar)


def gorev_tamamla(anahtar_kelime: str) -> str:
    anahtar_kelime = anahtar_kelime.strip().lower()
    if not anahtar_kelime:
        return "Hangi görevi tamamladığını söylemedin. Örn: görevi tamamla: matematik ödevi"

    gorevler = _yukle()
    for g in gorevler:
        if not g["tamamlandi"] and anahtar_kelime in g["metin"].lower():
            g["tamamlandi"] = True
            _kaydet(gorevler)
            return f"Tamamlandı olarak işaretledim: {g['metin']}"

    return f"'{anahtar_kelime}' ile eşleşen bekleyen bir görev bulamadım."


def ajandayi_metne_cevir() -> str:
    """Chat.py'nin sistem promptuna eklemesi için düz metin özet."""
    gorevler = _yukle()
    bekleyenler = [g for g in gorevler if not g["tamamlandi"]]
    if not bekleyenler:
        return ""
    return "\n".join(f"- {g['metin']} (eklendi: {g['eklenme_tarihi']})" for g in bekleyenler)
