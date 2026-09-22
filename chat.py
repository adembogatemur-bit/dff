# chat.py
# Yapılandırılmış komutların hiçbirine uymayan her şey buraya gelir ve
# Claude API ile gerçek, serbest, kişilikli bir sohbete dönüşür.

import requests
from config import (
    ANTHROPIC_API_KEY, ANTHROPIC_MODEL,
    KULLANICI_ADI, FRIDAY_KISILIGI, KULLANICI_RUTINI,
)
from hafiza import hafizayi_oku
from agenda import ajandayi_metne_cevir

_GECMIS = []          # basit konuşma geçmişi (son birkaç mesaj)
_GECMIS_LIMIT = 12     # bu sayının üstü otomatik silinir


def _sistem_promptu() -> str:
    hafiza_metni = hafizayi_oku()
    ajanda_metni = ajandayi_metne_cevir()

    hafiza_blogu = f"\n\nHakkında hatırladığın özel bilgiler:\n{hafiza_metni}" if hafiza_metni else ""
    ajanda_blogu = f"\n\nAjandasındaki bekleyen görevler:\n{ajanda_metni}" if ajanda_metni else ""

    return (
        f"Sen '{KULLANICI_ADI}' adlı kullanıcının kişisel sesli asistanısın, "
        f"adın Friday. {FRIDAY_KISILIGI}\n\n"
        f"Kullanıcı hakkında bildiklerin:\n{KULLANICI_RUTINI.strip()}"
        f"{hafiza_blogu}{ajanda_blogu}\n\n"
        "Cevapların sesli olarak okunacak; kısa, doğal ve konuşma diline "
        "uygun ol, uzun paragraflar ya da maddeler yazma. Her zaman Türkçe "
        "cevap ver."
    )


def sohbet_et(mesaj: str) -> str:
    if not ANTHROPIC_API_KEY:
        return ("Benimle serbest sohbet edebilmen için config.py içine bir "
                "ANTHROPIC_API_KEY eklemen gerekiyor "
                "(console.anthropic.com üzerinden alabilirsin).")

    if not mesaj.strip():
        return "Efendim?"

    _GECMIS.append({"role": "user", "content": mesaj})
    if len(_GECMIS) > _GECMIS_LIMIT:
        del _GECMIS[: len(_GECMIS) - _GECMIS_LIMIT]

    try:
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            json={
                "model": ANTHROPIC_MODEL,
                "max_tokens": 300,
                "system": _sistem_promptu(),
                "messages": _GECMIS,
            },
            timeout=30,
        )
        r.raise_for_status()
        veri = r.json()
        cevap = "".join(parca.get("text", "") for parca in veri.get("content", []))
        cevap = cevap.strip() or "Ne diyeceğimi bilemedim."
        _GECMIS.append({"role": "assistant", "content": cevap})
        return cevap
    except requests.exceptions.HTTPError as e:
        if _GECMIS and _GECMIS[-1]["role"] == "user":
            _GECMIS.pop()
        return f"API'den cevap alamadım (anahtarını kontrol et): {e}"
    except Exception as e:
        if _GECMIS and _GECMIS[-1]["role"] == "user":
            _GECMIS.pop()
        return f"Şu an sana cevap veremedim: {e}"


def sohbeti_sifirla() -> str:
    _GECMIS.clear()
    return "Hafızamı temizledim, sıfırdan başlayabiliriz."
