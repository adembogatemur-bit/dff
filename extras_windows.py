# extras_windows.py
# Windows'a özgü ek kontroller: Görev Yöneticisi, disk temizliği, aktif
# pencere adı, son açılan uygulamalar, başlangıca ekleme, oyun modu,
# pencere yerleştirme, ekran koruyucu, Windows Update ayarları.

import os
import subprocess
import ctypes
import sys
import winreg
from utils import veri_klasoru

_GECMIS_DOSYASI = "son_uygulamalar.txt"


def gorev_yoneticisini_ac() -> str:
    subprocess.Popen("taskmgr", shell=True)
    return "Görev Yöneticisi açılıyor."


def disk_temizligi_baslat() -> str:
    subprocess.Popen("cleanmgr", shell=True)
    return "Disk Temizliği başlatılıyor."


def aktif_pencere_adi() -> str:
    try:
        pencere = ctypes.windll.user32.GetForegroundWindow()
        uzunluk = ctypes.windll.user32.GetWindowTextLengthW(pencere)
        arabellek = ctypes.create_unicode_buffer(uzunluk + 1)
        ctypes.windll.user32.GetWindowTextW(pencere, arabellek, uzunluk + 1)
        return f"Şu an aktif pencere: {arabellek.value or 'bilinmiyor'}"
    except Exception as e:
        return f"Aktif pencere okunamadı: {e}"


def uygulama_gecmisine_ekle(isim: str):
    """uygulama_ac her çağrıldığında buraya kaydedilir (system_actions.py'den çağrılır)."""
    try:
        yol = os.path.join(veri_klasoru(), _GECMIS_DOSYASI)
        with open(yol, "a", encoding="utf-8") as f:
            f.write(isim + "\n")
        # Sadece son 50 kaydı tut
        with open(yol, encoding="utf-8") as f:
            satirlar = f.readlines()
        if len(satirlar) > 50:
            with open(yol, "w", encoding="utf-8") as f:
                f.writelines(satirlar[-50:])
    except Exception:
        pass


def son_acilan_uygulamalar(adet: int = 5) -> str:
    yol = os.path.join(veri_klasoru(), _GECMIS_DOSYASI)
    if not os.path.exists(yol):
        return "Henüz bir uygulama geçmişi yok."
    with open(yol, encoding="utf-8") as f:
        satirlar = [s.strip() for s in f.readlines() if s.strip()]
    if not satirlar:
        return "Henüz bir uygulama geçmişi yok."
    son_kayitlar = list(reversed(satirlar[-adet:]))
    return "Son açtıkların:\n" + "\n".join(f"- {s}" for s in son_kayitlar)


def baslangica_ekle() -> str:
    try:
        exe_yolu = sys.executable if getattr(sys, "frozen", False) else None
        if not exe_yolu:
            return "Bu özellik sadece Friday.exe olarak paketlendikten sonra çalışır (kur.bat ile oluştur)."

        anahtar = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE,
        )
        winreg.SetValueEx(anahtar, "Friday", 0, winreg.REG_SZ, exe_yolu)
        winreg.CloseKey(anahtar)
        return "Friday artık bilgisayar açılınca otomatik başlayacak."
    except Exception as e:
        return f"Başlangıca eklenemedi: {e}"


def baslangictan_kaldir() -> str:
    try:
        anahtar = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE,
        )
        winreg.DeleteValue(anahtar, "Friday")
        winreg.CloseKey(anahtar)
        return "Friday artık otomatik başlamayacak."
    except FileNotFoundError:
        return "Zaten başlangıca eklenmemiş."
    except Exception as e:
        return f"Kaldırılamadı: {e}"


def oyun_modu_ayarla(durum: str) -> str:
    try:
        deger = 1 if durum == "ac" else 0
        anahtar = winreg.CreateKeyEx(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\GameBar",
            0, winreg.KEY_SET_VALUE,
        )
        winreg.SetValueEx(anahtar, "AutoGameModeEnabled", 0, winreg.REG_DWORD, deger)
        winreg.CloseKey(anahtar)
        return "Oyun modu açıldı." if durum == "ac" else "Oyun modu kapatıldı."
    except Exception as e:
        return f"Oyun modu ayarlanamadı: {e}"


def pencereyi_yerlestir(yon: str) -> str:
    import keyboard
    if yon == "sol":
        keyboard.press_and_release("windows+left")
        return "Pencere sola yerleştirildi."
    if yon == "sag":
        keyboard.press_and_release("windows+right")
        return "Pencere sağa yerleştirildi."
    return "Yön anlaşılamadı (sol/sağ)."


def ekran_koruyucu_baslat() -> str:
    try:
        windir = os.environ.get("WINDIR", r"C:\Windows")
        subprocess.Popen(f'{windir}\\system32\\scrnsave.scr /s', shell=True)
        return "Ekran koruyucu başlatıldı."
    except Exception as e:
        return f"Ekran koruyucu başlatılamadı: {e}"


def windows_update_ayarlarini_ac() -> str:
    subprocess.Popen("start ms-settings:windowsupdate", shell=True)
    return "Windows Update ayarları açılıyor."
