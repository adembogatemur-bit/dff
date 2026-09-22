# bildirim.py
# Arka planda çalışan görevlerin (hatırlatıcı, zamanlanmış komut, ekran
# kaydı vb.) arayüze mesaj gönderebilmesi için ortak, basit bir kanal.

_dinleyiciler = []


def dinleyici_ekle(fn):
    """fn(kimden, metin) imzasında bir fonksiyon kaydeder (örn: GUI'nin
    mesaj_ekle metodu)."""
    _dinleyiciler.append(fn)


def bildir(kimden: str, metin: str):
    for fn in list(_dinleyiciler):
        try:
            fn(kimden, metin)
        except Exception:
            pass
