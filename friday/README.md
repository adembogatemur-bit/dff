# Friday - Masaüstü Sesli Asistan (Tam Sürüm — 100'e Yakın Özellik)

Bilgisayarında **gerçek bir uygulama** olarak açılan (tarayıcı değil), tam
ekran çalışan, teknik/HUD tarzı bir arayüzü olan bir asistan. Kurulumdan
sonra masaüstünde bir **Friday** ikonu olur — ona çift tıklarsın, hepsi bu.

**Performans notu**: Arayüz bilerek hafif tutuldu — HUD'daki halkalar ağır
grafik efektleri değil, basit çizgi/daire güncellemeleriyle çiziliyor
(saniyede 10 kare). Bu sayede eski/zayıf bilgisayarlarda da bilgisayarı
yormadan sorunsuz çalışır.

## Arayüz nasıl çalışır?

- Açılışta **tam ekran** başlar (oyun gibi, görev çubuğunu da kapatır).
  **F1** ile normal pencereye dönersin, tekrar F1 ile tam ekrana geçersin
  — F1 uygulamayı asla kapatmaz.
- Ortadaki halkalar Friday'in o anki durumuna göre gerçekten renk
  değiştirir: 🟢 yeşil = dinliyor, 🟡 sarı = düşünüyor, 🔵 mavi = konuşuyor,
  🔴 kırmızı = bir hata oldu (program çökmez, hatayı söyler ve devam eder).
- **Sağ altta bir sohbet kutusu** var: sesle söylediğin her şey ve
  Friday'in cevapları buraya yazı olarak düşer. Mikrofonun yoksa ya da
  konuşmak istemiyorsan doğrudan oradan yazabilirsin.
- **"Friday" ya da "uyan bakalım" diyerek çağırma** — hiçbir butona
  basmadan sürekli dinliyor, tam doğru söylemesen bile ("fraydi" gibi)
  tanıyor.

---

## 1) Kurulum — SEN HİÇBİR ŞEY ÇALIŞTIRMADAN (önerilen yöntem)

Bilgisayarında hiçbir şey kurmak/çalıştırmak istemiyorsan, `Friday.exe`'yi
senin yerine **GitHub'ın bulut bilgisayarı** derlesin:

1. https://github.com adresinde ücretsiz bir hesap aç (yoksa).
2. Sağ üstten **"+"** → **"New repository"** → bir isim ver (örn. `friday`) →
   **Create repository**.
3. Açılan sayfada **"uploading an existing file"** yazısına tıkla, bu
   `friday` klasöründeki **tüm dosyaları** (klasörleri de dahil) sürükleyip
   bırak, en altta **"Commit changes"** butonuna bas.
4. Üstteki **"Actions"** sekmesine tıkla. Birkaç saniye içinde bir derleme
   otomatik başlayacak (turuncu nokta → yeşil tik olunca biter, ~2-3 dakika).
5. Bitince o çalışmaya tıkla, en altta **"Friday-Windows-Hazir"** adlı bir
   dosya göreceksin, ona tıklayıp indir.
6. İndirdiğin zip'i aç — içinde doğrudan **Friday.exe** var, çift tıkla,
   hiçbir kurulum ekranı çıkmadan direkt açılır.

Bu yöntemde bilgisayarına Python kurmana, `kur.bat` çalıştırmana gerek
kalmıyor — tüm "derleme" işini GitHub'ın kendi Windows bilgisayarı yapıyor,
sen sadece dosyaları yükleyip sonucu indiriyorsun.

## 1b) Alternatif — Kendi bilgisayarında (kur.bat ile)

### a) Python'u kur (sadece kurulum için, sonra görmeyeceksin)
https://www.python.org/downloads/ adresinden Python 3.9+ indir, kurulumda
**"Add Python to PATH"** kutusunu işaretle.

### b) `friday` klasörünü bilgisayarına indir

### c) `config.py`'yi doldur (hiçbirini doldurmasan da çalışır, sadece o özellikler kapalı kalır)

- **Gerçek sohbet için**: https://console.anthropic.com'dan `ANTHROPIC_API_KEY`
- **Kaliteli erkek sesi için**: https://elevenlabs.io'dan `ELEVENLABS_API_KEY`
- **Hava durumu için**: https://openweathermap.org/api'den `OPENWEATHER_API_KEY`
- **E-posta için**: Gmail "Uygulama Şifresi" → `EMAIL_ADDRESS` / `EMAIL_APP_PASSWORD`
- **Telegram mesajı için**: BotFather'dan bot oluştur → `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID`
- **Kişiler**: `CONTACTS` (WhatsApp) / `EMAIL_CONTACTS` (e-posta)
- **Rutinini** `KULLANICI_RUTINI`'ye, kişiliğini `FRIDAY_KISILIGI`'ye yaz —
  Friday'in seninle isabetli sohbet edebilmesi buna bağlı.
- **Telefon bağlantısı için**: `FRIDAY_PIN`

### d) `kur.bat` dosyasına çift tıkla

Her şeyi otomatik yapar: kütüphaneleri kurar, `Friday` klasörünü (içinde
`Friday.exe` ve `_internal` klasörü) `dist` altında oluşturur, masaüstüne
kısayol koyar. Bittiğinde masaüstündeki **Friday** ikonuna çift tıklaman
yeterli.

**Bunu başka bir bilgisayara taşımak/paylaşmak istersen**: `dist\Friday`
klasörünün **tamamını** (Friday.exe + _internal klasörü birlikte) kopyala.
O klasörü nereye götürürsen götür, `Friday.exe`'ye çift tıklayınca hiçbir
kurulum ekranı görmeden direkt açılır — kaynak kodu ya da `kur.bat`'a bir
daha ihtiyaç yok, sadece o `Friday` klasörünü taşımak yeterli.

---

## 2) Tüm özellikler

**Uygulama / Dosya** — uygulama aç (bulamazsa site açar) · klasör aç ·
site aç · dosya ara/sil · son dosyayı aç · yazdır · programı kapat ·
klasör boyutu · zip oluştur/aç · uzantıya göre dosya listele · olası
kopyaları bul

**İnternet / Bilgi** — google/youtube/spotify ara · kanalın son videosu ·
hava durumu · haberler · döviz/birim çevirme · Wikipedia özeti · çeviri ·
kripto fiyatı · son depremler · namaz vakitleri

**İletişim** — isimle/numarayla WhatsApp mesajı · e-posta · Telegram
mesajı · Zoom/Teams/Meet açma · takvime etkinlik ekleme (.ics ile)

**Bilgisayar** — sistem bilgisi · pil durumu · ekran parlaklığı · Wi-Fi
aç/kapat · ekran kilitleme · ses kontrolü · kapatma/yeniden başlatma ·
ekran görüntüsü/kaydı · Görev Yöneticisi · disk temizliği · aktif pencere
adı · son açılan uygulamalar · başlangıca ekleme · oyun modu · pencere
yerleştirme · ekran koruyucu · Windows Update ayarları · medya
oynat/durdur/sonraki/önceki parça

**Verimlilik** — not alma · pano · dikte modu · hatırlatıcı · hesap
makinesi · saat/tarih · sabah brifingi · pomodoro · kalıcı hafıza ·
ajanda/görev listesi · zamanlanmış otomatik görevler

**Eğlence** — yazı-tura · zar · rastgele sayı · kelime sayma · şaka ·
günün alıntısı · ruh haline göre müzik önerisi

**Güvenlik/Sistem** — şifre üretme · yedekleme · fabrika ayarlarına dönme
· sürüm bilgisi · sistem tepsisine küçültme · Windows bildirimleri

**Sohbet** — tanımadığı her şeyi gerçek yapay zeka sohbetine çevirir,
seni ismiyle tanır, kişiliği ayarlanabilir, kalıcı hafızası ve ajandası var

Tüm komutların tam listesi için uygulama içinde **"yardım"** yaz/söyle.

### Örnek komutlar

```
uygulama aç chrome
site aç trendyol.com
dosya ara fatura
zip oluştur C:\Users\Adem\Desktop\proje
hava durumu
wikipedi'de ara yapay zeka
kripto fiyatı bitcoin
son depremler
namaz vakitleri
mesaj gönder ahmet bugün eve geç geleceğim
telegram mesaj gönder toplantı 3'te
zoom aç
takvime ekle: yarın saat 15:00 doktor randevusu
sistem bilgisi
görev yöneticisini aç
başlangıca ekle
oyun modunu aç
videoyu durdur
pomodoro başlat
yazı tura
şaka yap
ruh halim enerjik
şifre üret
yedekle
uyan bakalım baba eve geldi
sohbeti sıfırla
```

---

## 3) Bilinçli olarak eklemediğim özellikler (dürüst olmak adına)

Şunlar Windows'ta güvenilir/basit bir yöntemle yapılamadığı için "yarım
çalışan" bir şey eklemek yerine dışarıda bıraktım:

- **Bluetooth açma/kapama** — Windows'ta buna güvenilir bir komut satırı
  yöntemi yok, ancak riskli/kararsız yollarla yapılabiliyor.
- **Uçak modu** — aynı şekilde basit bir CLI yöntemi yok.
- **Canlı spor skorları** — ücretsiz/güvenilir bir kaynak bulamadım.
- **Tam ikinci dilde (İngilizce) arayüz** — bu, tüm komut sistemini
  ikiye katlamak demek; ayrı, odaklı bir iş olarak yapılmalı.

İstersen bunlardan birini yine de (sınırlamalarını bilerek) denemek
istersen söyle.

---

## 4) WhatsApp mesajı göndermeden önce

Bilgisayarındaki tarayıcıda bir kere **web.whatsapp.com**'a girip telefonunla
QR kodu okutarak giriş yapmış olman gerekiyor.

---

## 5) Ayarlar (config.py) — hepsi tek dosyada

| Ayar | Ne işe yarar |
|---|---|
| `APP_PATHS` / `SITE_ALTERNATIFLERI` | Program yolları / bulunamazsa açılacak site |
| `CONTACTS` / `EMAIL_CONTACTS` | İsimle mesaj/mail için kişiler |
| `CHANNELS` | "son video" için YouTube kanalları |
| `ELEVENLABS_API_KEY` / `FRIDAY_KONUSMA_HIZI` | Ses kalitesi ve hızı |
| `OPENWEATHER_API_KEY` / `DEFAULT_CITY` | Hava durumu |
| `EMAIL_ADDRESS` / `EMAIL_APP_PASSWORD` | E-posta |
| `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` | Telegram mesajı |
| `ANTHROPIC_API_KEY` / `KULLANICI_ADI` / `FRIDAY_KISILIGI` / `KULLANICI_RUTINI` | Gerçek sohbet |
| `APP_ACILIS_SIFRESI` | Uygulama açılış şifresi |
| `SCHEDULED_TASKS` | Otomatik günlük görevler |
| `WAKE_WORDS` / `FRIDAY_PIN` | Uyandırma kelimesi / uzaktan erişim şifresi |

Değişiklik yaptıktan sonra `kur.bat`'ı tekrar çalıştır ki yeni `Friday.exe`
bu değişikliklerle yeniden oluşsun.

## 6) Sınırlamalar

- İnternet gerektiren özellikler (hava durumu, haberler, kripto, deprem,
  namaz vakitleri, sohbet, çeviri, Wikipedia) internet olmadan çalışmaz.
- Bazı Windows özellikleri (oyun modu, başlangıca ekleme, disk temizliği)
  bilgisayarına ve Windows sürümüne göre küçük farklılıklar gösterebilir.
- Telefon bağlantısı sadece aynı Wi-Fi ağı içinde çalışır.
- `kur.bat` Windows Güvenlik Duvarı'ndan izin isteyebilir — "İzin ver" de.
