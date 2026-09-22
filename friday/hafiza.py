# hafiza.py
# Friday'in senin hakkında öğrendiği ve programı kapatıp açsan, hatta
# bilgisayarı yeniden başlatsan bile UNUTMAYACAĞI kalıcı bilgiler.
# ("sohbeti sıfırla" komutu bunu SİLMEZ, sadece o anki konuşma akışını
# temizler — kalıcı hafıza ayrı bir şeydir.)

import os
import datetime
from utils import veri_klasoru

_DOSYA_ADI = "hafiza.txt"


def _dosya_yolu() -> str:
    return os.path.join(veri_klasoru(), _DOSYA_ADI)


def beni_hatirla(bilgi: str) -> str:
    bilgi = bilgi.strip()
    if not bilgi:
        return "Ne hatırlamamı istediğini söylemedin. Örn: beni hatırla: cuma günleri yüzmeye gidiyorum"

    with open(_dosya_yolu(), "a", encoding="utf-8") as f:
        zaman = datetime.datetime.now().strftime("%d.%m.%Y")
        f.write(f"[{zaman}] {bilgi}\n")

    return f"Not ettim, unutmayacağım: {bilgi}"


def hafizayi_oku() -> str:
    """Chat.py'nin sistem promptuna eklemesi için düz metin döner."""
    yol = _dosya_yolu()
    if not os.path.exists(yol):
        return ""
    with open(yol, encoding="utf-8") as f:
        return f.read().strip()


def hafizayi_listele() -> str:
    icerik = hafizayi_oku()
    if not icerik:
        return "Hakkında henüz hatırladığım özel bir şey yok. 'Beni hatırla: ...' diyerek bir şey ekleyebilirsin."
    return "Hakkında hatırladıklarım:\n" + icerik


def hafizayi_unut() -> str:
    yol = _dosya_yolu()
    if os.path.exists(yol):
        os.remove(yol)
    return "Hakkındaki tüm hatıralarımı sildim."
