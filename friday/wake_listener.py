# wake_listener.py
# Mikrofonu sürekli dinler; uyandırma kelimesini duyunca (tam doğru
# söylemesen bile, "fraydi" gibi yakın söyleyişleri de tanır) komutu
# algılayıp çalıştırır. Dikte modundayken uyandırma kelimesi aranmaz,
# söylediğin her şey doğrudan dosyaya yazılır.

import difflib
import threading
import numpy as np
import sounddevice as sd
import speech_recognition as sr

from config import WAKE_WORDS
from commands import komutu_isle
from desktop_tts import konus
from dictation import dikte_aktif_mi, dikte_yaz, dikte_durdur

ORNEKLEME_HIZI = 16000  # Hz
PARCA_SURESI = 4        # saniye
BENZERLIK_ESIGI = 0.6   # 0-1 arası; düşürürsen daha kolay ama yanlış da tetiklenebilir


def _benzerlik(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()


def _uyandirma_kelimesi_var_mi(metin: str):
    kelimeler = metin.lower().split()
    if not kelimeler:
        return None, None

    en_iyi = (None, None, 0.0)

    for wake in WAKE_WORDS:
        wake_kelimeler = wake.lower().split()
        n = len(wake_kelimeler)
        for i in range(len(kelimeler) - n + 1):
            aday = " ".join(kelimeler[i:i + n])
            skor = _benzerlik(aday, wake.lower())
            if skor > en_iyi[2]:
                kalan = " ".join(kelimeler[i + n:])
                en_iyi = (wake, kalan, skor)

    if en_iyi[2] >= BENZERLIK_ESIGI:
        return en_iyi[0], en_iyi[1]
    return None, None


class UyanmaDinleyici:
    """Arka planda sürekli mikrofonu dinler (sounddevice ile, PyAudio gerekmez)."""

    def __init__(self, mesaj_geldiginde):
        self.mesaj_geldiginde = mesaj_geldiginde
        self.recognizer = sr.Recognizer()
        self._durduruldu = threading.Event()
        self._thread = None

    def baslat(self):
        sd.check_input_settings(samplerate=ORNEKLEME_HIZI, channels=1)
        self._thread = threading.Thread(target=self._dongu, daemon=True)
        self._thread.start()

    def durdur(self):
        self._durduruldu.set()

    def _dongu(self):
        while not self._durduruldu.is_set():
            try:
                kayit = sd.rec(
                    int(PARCA_SURESI * ORNEKLEME_HIZI),
                    samplerate=ORNEKLEME_HIZI,
                    channels=1,
                    dtype="int16",
                )
                sd.wait()
            except Exception as e:
                print("Mikrofon kayıt hatası:", e)
                break
            self._parcayi_isle(kayit)

    def _parcayi_isle(self, kayit: np.ndarray):
        ham_veri = kayit.tobytes()
        ses = sr.AudioData(ham_veri, ORNEKLEME_HIZI, 2)

        try:
            metin = self.recognizer.recognize_google(ses, language="tr-TR")
        except (sr.UnknownValueError, sr.RequestError):
            return

        # Dikte modundaysak uyandırma kelimesi aramadan doğrudan yaz
        if dikte_aktif_mi():
            if "dikte durdur" in metin.lower():
                cevap = dikte_durdur()
                self.mesaj_geldiginde("user", metin)
                self.mesaj_geldiginde("friday", cevap)
                konus(cevap)
            else:
                dikte_yaz(metin)
                self.mesaj_geldiginde("user", metin)
            return

        uyandirma, kalan = _uyandirma_kelimesi_var_mi(metin)
        if not uyandirma:
            return

        self.mesaj_geldiginde("user", metin)
        cevap = komutu_isle(kalan) if kalan else "Efendim?"
        self.mesaj_geldiginde("friday", cevap)
        konus(cevap)
