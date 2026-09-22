# utils.py
# Programın .exe haline getirilince de düzgün çalışması için ortak yardımcılar.

import os
import sys


def veri_klasoru() -> str:
    """Çalışma zamanında oluşturulan dosyalar (ses kaydı, notlar) için her
    zaman yazılabilir bir klasör döner. .exe haline getirilince bile kalıcı
    olsun diye AppData altında saklanır."""
    if getattr(sys, "frozen", False):
        taban = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "Friday")
    else:
        taban = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(taban, exist_ok=True)
    return taban


def kaynak_klasoru() -> str:
    """templates/static gibi programla birlikte gelen dosyaların bulunduğu
    klasörü döner (.exe içine gömülüyken farklı bir yerdedir)."""
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))
