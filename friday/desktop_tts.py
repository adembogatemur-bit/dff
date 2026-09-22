# desktop_tts.py
# Masaüstü uygulamasında Friday'in sesli cevap vermesini sağlar.

import os
import threading
from config import ELEVENLABS_API_KEY, FRIDAY_KONUSMA_HIZI
from tts import sese_cevir, _cikti_yolu
from utils import veri_klasoru
import hud_durum

_pyttsx_engine = None
_kilit = threading.Lock()


def _pyttsx_al():
    global _pyttsx_engine
    if _pyttsx_engine is None:
        import pyttsx3
        _pyttsx_engine = pyttsx3.init()
        sesler = _pyttsx_engine.getProperty("voices")
        erkek_id = None
        for s in sesler:
            if "david" in s.name.lower():
                erkek_id = s.id
                break
        if not erkek_id:
            for s in sesler:
                cinsiyet = getattr(s, "gender", "") or ""
                if "male" in cinsiyet.lower():
                    erkek_id = s.id
                    break
        if erkek_id:
            _pyttsx_engine.setProperty("voice", erkek_id)
        _pyttsx_engine.setProperty("rate", FRIDAY_KONUSMA_HIZI)
    return _pyttsx_engine


def konus(metin: str):
    threading.Thread(target=_konus_thread, args=(metin,), daemon=True).start()


def _konus_thread(metin: str):
    hud_durum.durum_ayarla("konusuyor")
    with _kilit:
        if ELEVENLABS_API_KEY:
            url = sese_cevir(metin)
            if url:
                _mp3_oynat()
                hud_durum.durum_ayarla("dinliyor")
                return
        try:
            engine = _pyttsx_al()
            engine.say(metin)
            engine.runAndWait()
        except Exception as e:
            print("Sesli okuma hatası:", e)
    hud_durum.durum_ayarla("dinliyor")


def _mp3_oynat():
    import pygame
    yol = _cikti_yolu()
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    pygame.mixer.music.load(yol)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)
