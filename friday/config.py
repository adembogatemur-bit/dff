# config.py
# Kendi ayarlarını buradan yapıyorsun.

# --- Bilinen program yolları (istediğin kadar ekleyebilirsin) ---
APP_PATHS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "spotify": r"C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe",
    "whatsapp": r"C:\Users\%USERNAME%\AppData\Local\WhatsApp\WhatsApp.exe",
    # "isim": r"tam\dosya\yolu.exe",
}

# Bilgisayarda bulunamayan bir uygulama için web sitesi karşılığı.
SITE_ALTERNATIFLERI = {
    "instagram": "https://instagram.com",
    "whatsapp": "https://web.whatsapp.com",
    "netflix": "https://netflix.com",
    "discord": "https://discord.com/app",
    "twitter": "https://twitter.com",
    "x": "https://twitter.com",
    "gmail": "https://mail.google.com",
    "youtube": "https://youtube.com",
    "spotify": "https://open.spotify.com",
    "facebook": "https://facebook.com",
    "tiktok": "https://tiktok.com",
    "amazon": "https://amazon.com.tr",
    "trendyol": "https://trendyol.com",
}

DEFAULT_COUNTRY_CODE = "+90"

# --- Kişiler (isim söyleyerek mesaj gönderebilmek için) ---
CONTACTS = {
    # "ahmet": "+905551112233",
    # "anne": "+905559998877",
}

# --- YouTube kanalları (bir kanalın son videosunu açabilmek için) ---
CHANNELS = {
    # "ahmet abi": "@ahmetabikanali",
}

# --- Ses (TTS) ayarları ---
ELEVENLABS_API_KEY = ""
ELEVENLABS_VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # "Adam" adlı hazır kalın erkek sesi

# --- Uyandırma kelimesi ---
# "uyan bakalım" da eklendi (tek başına "uyan" değil — sıradan konuşmada
# yanlışlıkla tetiklenmesin diye iki kelimelik daha spesifik bir kalıp
# kullanıyoruz), böylece "uyan bakalım baba eve geldi" gibi cümleler de
# Friday'i çağırabilir.
WAKE_WORDS = ["friday", "hey friday", "uyan bakalım"]

# --- Güvenlik (telefon bağlantısı için) ---
FRIDAY_PIN = ""

FLASK_PORT = 5000

# --- Hava durumu ---
# https://openweathermap.org/api adresinden ücretsiz bir anahtar alabilirsin.
OPENWEATHER_API_KEY = ""
DEFAULT_CITY = "Istanbul"

# --- E-posta gönderme (Gmail üzerinden) ---
# EMAIL_APP_PASSWORD normal şifren DEĞİL; Google Hesabı > Güvenlik >
# Uygulama Şifreleri kısmından oluşturduğun 16 haneli özel şifre.
EMAIL_ADDRESS = ""
EMAIL_APP_PASSWORD = ""
EMAIL_CONTACTS = {
    # "ahmet": "ahmet@example.com",
}

# --- Zamanlanmış otomatik komutlar ---
# Her saat başında Friday'in kendiliğinden çalıştıracağı komutlar.
# Örnek: her sabah 08:00'de sana sabah brifingi versin istersen alttaki
# satırın başındaki # işaretini kaldır.
SCHEDULED_TASKS = [
    # {"saat": "08:00", "komut": "sabah brifingi"},
]

# --- Yapay zeka ile serbest sohbet ---
# Yukarıdaki komutların hiçbirine uymayan her şey (örn. "naber", "bugün
# canım sıkkın", "uyan bakalım baba eve geldi") buraya, gerçek bir yapay
# zekaya gider. Anahtar boşsa Friday sana bunu nereden alacağını söyler.
#
# https://console.anthropic.com adresinden bir API anahtarı alabilirsin
# (kredi kartı gerektirir ama kişisel kullanımda maliyeti çok düşüktür).
ANTHROPIC_API_KEY = ""
ANTHROPIC_MODEL = "claude-sonnet-5"  # daha ucuzu istersen: "claude-haiku-4-5-20251001"

# Friday'in seni nasıl çağıracağı.
KULLANICI_ADI = "Adem"

# Friday'in kişiliği/konuşma tarzı — istediğin gibi değiştirebilirsin.
FRIDAY_KISILIGI = (
    "Enerjik, esprili, samimi ve sıcakkanlı bir kişisel asistansın. Kısa, "
    "doğal, arkadaşça cümleler kur; resmi ve robotik konuşma; ara sıra "
    "hafif espri yap ama abartma; kullanıcıyı gerçekten önemsiyormuş gibi konuş."
)

# Friday'in seni tanıması için rutinin/hayatın hakkında bilgi. Ne kadar
# detaylı yazarsan Friday seninle o kadar isabetli sohbet eder. Örneği
# kendi hayatına göre değiştir.
KULLANICI_RUTINI = """
Pazartesi-Cuma okula gidiyor. Okuldan sonra genelde önce ödev yapıyor,
sonra boş vakti oluyor. Hafta sonları daha rahat, oyun oynamayı ve
müzik dinlemeyi seviyor. (Bunu kendi rutinine göre güncelle.)
"""

# --- Telegram mesajı (BotFather üzerinden ücretsiz alınır) ---
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""

# --- Sesin konuşma hızı (bilgisayarın kendi sesi için, kelime/dakika) ---
FRIDAY_KONUSMA_HIZI = 165

# --- Uygulama açılış şifresi (boş bırakırsan şifre sorulmaz) ---
APP_ACILIS_SIFRESI = ""
