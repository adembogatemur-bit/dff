# tts.py
# Metni sese çevirir. ElevenLabs anahtarı tanımlıysa kaliteli, kalın erkek
# sesiyle bir ses dosyası üretir. Anahtar yoksa None döner.

import os
import requests
from config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID
from utils import veri_klasoru


def _cikti_yolu() -> str:
    return os.path.join(veri_klasoru(), "tts_output.mp3")


def sese_cevir(metin: str):
    if not ELEVENLABS_API_KEY or not metin:
        return None

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": metin,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        yol = _cikti_yolu()
        with open(yol, "wb") as f:
            f.write(r.content)
        return "/audio/tts_output.mp3?t=" + str(int(os.path.getmtime(yol)))
    except Exception as e:
        print("ElevenLabs hatası, bilgisayarın kendi sesine dönülüyor:", e)
        return None
