# system_info.py
# Sistem bilgisi, pil durumu, ekran parlaklığı, Wi-Fi, program kapatma.

import subprocess
import psutil


def sistem_bilgisi() -> str:
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    try:
        disk = psutil.disk_usage("C:\\")
        disk_str = f", Disk kullanımı %{disk.percent:.0f}"
    except Exception:
        disk_str = ""

    return (f"İşlemci kullanımı %{cpu:.0f}, RAM kullanımı %{ram.percent:.0f} "
            f"({ram.used // (1024**3)} GB / {ram.total // (1024**3)} GB){disk_str}.")


def pil_durumu() -> str:
    pil = psutil.sensors_battery()
    if pil is None:
        return "Bu bilgisayarda pil bilgisi bulunamadı (masaüstü olabilir)."
    durum = "şarj oluyor" if pil.power_plugged else "şarjda değil"
    return f"Pil yüzde {pil.percent:.0f}, {durum}."


def ekran_parlakligi_ayarla(yon: str) -> str:
    try:
        import screen_brightness_control as sbc
        mevcut = sbc.get_brightness(display=0)[0]
        yeni = min(100, mevcut + 20) if yon == "artir" else max(0, mevcut - 20)
        sbc.set_brightness(yeni)
        return f"Ekran parlaklığı yüzde {yeni} yapıldı."
    except Exception as e:
        return f"Ekran parlaklığı ayarlanamadı: {e}\n(Bazı monitörler/ekran kartları desteklemeyebilir.)"


def wifi_ayarla(durum: str) -> str:
    komut = "enable" if durum == "ac" else "disable"
    try:
        subprocess.run(f'netsh interface set interface "Wi-Fi" {komut}', shell=True, check=True)
        return "Wi-Fi açıldı." if durum == "ac" else "Wi-Fi kapatıldı."
    except Exception as e:
        return f"Wi-Fi ayarlanamadı: {e}\n(Bu komut yönetici izni isteyebilir, ya da adaptör adın 'Wi-Fi' değil.)"


def programi_kapat(isim: str) -> str:
    isim = isim.strip().lower()
    isim_exe = isim if isim.endswith(".exe") else isim + ".exe"

    kapatilan = 0
    for p in psutil.process_iter(["name"]):
        try:
            if p.info["name"] and p.info["name"].lower() == isim_exe:
                p.terminate()
                kapatilan += 1
        except Exception:
            pass

    if kapatilan:
        return f"{isim} kapatıldı ({kapatilan} işlem)."
    return f"'{isim}' çalışır durumda bulunamadı."
