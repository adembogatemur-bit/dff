# clipboard_actions.py
# Panoya kopyalama ve pano içeriğini okuma.

import pyperclip


def panoya_kopyala(metin: str) -> str:
    pyperclip.copy(metin)
    return "Panoya kopyalandı."


def panodakini_oku() -> str:
    icerik = pyperclip.paste()
    if not icerik:
        return "Panoda bir şey yok."
    return f"Panoda şu var: {icerik}"
