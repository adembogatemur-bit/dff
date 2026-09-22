@echo off
title Friday Kurulumu
echo ================================================
echo   Friday kuruluyor, bu birkac dakika surebilir...
echo ================================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo Python bulunamadi.
    echo.
    echo Once https://www.python.org/downloads/ adresinden Python'u kur.
    echo Kurulum ekraninda "Add Python to PATH" kutucugunu MUTLAKA isaretle.
    echo Kurduktan sonra bu dosyaya (kur.bat) tekrar cift tikla.
    echo.
    pause
    exit /b
)

echo [1/4] Windows Defender bu klasoru "guvenilir" olarak isaretlemeye
echo       calisiliyor (aksi halde olusturulacak dosyalari Defender
echo       otomatik silebilir). Yonetici izni yoksa bu adim sessizce
echo       atlanir, sorun degil, asagida ne yapman gerektigini zaten
echo       anlatiyorum.
powershell -NoProfile -Command "Add-MpPreference -ExclusionPath '%cd%' -ErrorAction SilentlyContinue" >nul 2>nul

echo.
echo [2/4] Gerekli kutuphaneler kuruluyor...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo [3/4] Friday derleniyor (klasor modunda - daha hizli acilir,
echo       Defender'i daha az tetikler)...
pyinstaller --noconsole --name Friday --icon=icon.ico --add-data "templates;templates" --add-data "static;static" --add-data "icon.ico;." main.py

if not exist "dist\Friday\Friday.exe" (
    echo.
    echo ================================================
    echo   SORUN: Friday.exe olusturulamadi ya da hemen
    echo   sonra silindi. Bunun en sik sebebi Windows
    echo   Defender'in onu supheli gorup otomatik silmesi.
    echo.
    echo   COZUM:
    echo   1^) Baslat menusunden "Windows Guvenligi" ac
    echo   2^) "Virus ve tehdit korumasi" - "Koruma gecmisi"
    echo   3^) Karantinaya alinmis "Friday" varsa "Geri Yukle"
    echo   4^) Ayni ekrandan "Istisnalar ekle" ile bu klasoru
    echo      ^(%cd%^) istisnaya ekle
    echo   5^) Bu dosyaya ^(kur.bat^) tekrar cift tikla
    echo ================================================
    pause
    exit /b
)

echo.
echo [4/4] Masaustune kisayol olusturuluyor...
powershell -NoProfile -Command ^
  "$W = New-Object -ComObject WScript.Shell; $S = $W.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\Friday.lnk'); $S.TargetPath = (Get-Location).Path + '\dist\Friday\Friday.exe'; $S.WorkingDirectory = (Get-Location).Path + '\dist\Friday'; $S.IconLocation = (Get-Location).Path + '\icon.ico'; $S.Save()"

echo.
echo ================================================
echo   Bitti! Masaustunde kendi ikonuyla "Friday" kisayolu olustu.
echo   Bundan sonra sadece o ikona cift tikla.
echo.
echo   BASKA BIR SEYE TASIMAK/PAYLASMAK ISTERSEN:
echo   "dist\Friday" klasorunun TAMAMINI kopyala (icinde Friday.exe
echo   ve _internal klasoru birlikte olmali). O klasoru nereye
echo   goturursen goturur, Friday.exe'ye cift tiklayinca hicbir
echo   kurulum ekrani gormeden direkt acilir - tipki incelettigin
echo   ornekteki gibi.
echo ================================================
pause
