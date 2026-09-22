# hud_durum.py
# Farklı thread'lerin (mikrofon dinleyici, komut işleyici, TTS) arayüzdeki
# HUD'un rengini/durumunu güvenli şekilde değiştirebilmesi için ortak kanal.
# Durumlar: "dinliyor" (yeşil, varsayılan), "dusunuyor" (sarı),
# "konusuyor" (mavi), "hata" (kırmızı).

_dinleyiciler = []


def dinleyici_ekle(fn):
    _dinleyiciler.append(fn)


def durum_ayarla(durum: str):
    for fn in list(_dinleyiciler):
        try:
            fn(durum)
        except Exception:
            pass
