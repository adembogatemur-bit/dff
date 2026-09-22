# extras_dosya.py
# Dosya işlemleriyle ilgili ek özellikler: klasör boyutu, zip oluşturma/açma,
# uzantıya göre dosya listeleme, olası duplicate (aynı isimli) dosya bulma.

import os
import shutil
import zipfile
from collections import defaultdict


def klasor_boyutu(yol: str) -> str:
    yol = yol.strip().strip('"')
    if not os.path.isdir(yol):
        return f"Böyle bir klasör bulunamadı: {yol}"

    toplam_boyut = 0
    for kok, _, dosyalar in os.walk(yol):
        for dosya in dosyalar:
            try:
                toplam_boyut += os.path.getsize(os.path.join(kok, dosya))
            except Exception:
                pass

    mb = toplam_boyut / (1024 * 1024)
    if mb > 1024:
        return f"{yol}: {mb / 1024:.2f} GB"
    return f"{yol}: {mb:.1f} MB"


def zip_olustur(kaynak_yol: str) -> str:
    kaynak_yol = kaynak_yol.strip().strip('"')
    if not os.path.exists(kaynak_yol):
        return f"Böyle bir dosya/klasör bulunamadı: {kaynak_yol}"

    hedef_yol = kaynak_yol.rstrip("\\/") + ".zip"
    try:
        if os.path.isdir(kaynak_yol):
            shutil.make_archive(kaynak_yol, "zip", kaynak_yol)
        else:
            with zipfile.ZipFile(hedef_yol, "w", zipfile.ZIP_DEFLATED) as z:
                z.write(kaynak_yol, os.path.basename(kaynak_yol))
        return f"Zip oluşturuldu: {hedef_yol}"
    except Exception as e:
        return f"Zip oluşturulamadı: {e}"


def zip_ac(zip_yolu: str) -> str:
    zip_yolu = zip_yolu.strip().strip('"')
    if not os.path.exists(zip_yolu):
        return f"Böyle bir zip dosyası bulunamadı: {zip_yolu}"

    hedef_klasor = zip_yolu.rsplit(".", 1)[0]
    try:
        with zipfile.ZipFile(zip_yolu, "r") as z:
            z.extractall(hedef_klasor)
        os.startfile(hedef_klasor)
        return f"Zip açıldı: {hedef_klasor}"
    except Exception as e:
        return f"Zip açılamadı: {e}"


def uzantiya_gore_listele(klasor: str, uzanti: str) -> str:
    klasor = klasor.strip().strip('"')
    uzanti = uzanti.strip().lower().lstrip(".")
    if not os.path.isdir(klasor):
        return f"Böyle bir klasör bulunamadı: {klasor}"

    bulunanlar = [
        d for d in os.listdir(klasor)
        if d.lower().endswith("." + uzanti) and os.path.isfile(os.path.join(klasor, d))
    ]
    if not bulunanlar:
        return f"{klasor} içinde .{uzanti} uzantılı dosya bulunamadı."
    return f"{len(bulunanlar)} dosya bulundu:\n" + "\n".join(f"- {d}" for d in bulunanlar[:20])


def olasi_kopyalari_bul(klasor: str) -> str:
    """Aynı isme sahip (farklı klasörlerdeki) dosyaları bulur — gerçek
    içerik karşılaştırması yapmaz, sadece isim eşleşmesine bakar."""
    klasor = klasor.strip().strip('"')
    if not os.path.isdir(klasor):
        return f"Böyle bir klasör bulunamadı: {klasor}"

    isim_haritasi = defaultdict(list)
    for kok, _, dosyalar in os.walk(klasor):
        for dosya in dosyalar:
            isim_haritasi[dosya.lower()].append(os.path.join(kok, dosya))

    kopyalar = {isim: yollar for isim, yollar in isim_haritasi.items() if len(yollar) > 1}
    if not kopyalar:
        return "Aynı isimli dosya bulunamadı."

    satirlar = []
    for isim, yollar in list(kopyalar.items())[:10]:
        satirlar.append(f"{isim} ({len(yollar)} kopya)")
    return "Olası kopyalar (isim bazlı):\n" + "\n".join(f"- {s}" for s in satirlar)
