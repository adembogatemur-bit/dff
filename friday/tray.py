# tray.py
# Pencereyi kapatmadan sistem tepsisine (saat yanındaki küçük ikonlar)
# küçültme özelliği.

import threading


def sistem_tepsisine_ekle(pencere, geri_getir_callback):
    """pystray varsa sistem tepsisi ikonu kurar; yoksa sessizce hiçbir şey
    yapmaz (özellik devre dışı kalır, program yine çalışır)."""
    try:
        import pystray
        from PIL import Image, ImageDraw
    except ImportError:
        return None

    def simge_olustur():
        img = Image.new("RGB", (64, 64), "#03060a")
        cizim = ImageDraw.Draw(img)
        cizim.ellipse((14, 14, 50, 50), outline="#378ADD", width=4)
        return img

    def geri_getir(icon, item=None):
        icon.stop()
        geri_getir_callback()

    def cikis(icon, item=None):
        icon.stop()
        pencere.after(0, pencere.destroy)

    menu = pystray.Menu(
        pystray.MenuItem("Göster", geri_getir, default=True),
        pystray.MenuItem("Kapat", cikis),
    )
    icon = pystray.Icon("Friday", simge_olustur(), "Friday", menu)
    threading.Thread(target=icon.run, daemon=True).start()
    return icon
