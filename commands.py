# commands.py
# Gelen her komut (yazarak, sesle ya da telefondan) buradan geçer.

import re
from system_actions import (
    uygulama_ac, klasor_ac, ekrani_kilitle,
    bilgisayari_kapat, bilgisayari_yeniden_baslat,
    not_al, ses_ayarla, saat_soyle, tarih_soyle, ekran_goruntusu_al,
)
from web_actions import google_ara, youtube_ara, spotify_ara, site_ac, kanalin_son_videosunu_ac
from messaging import whatsapp_mesaj_gonder
from weather import hava_durumu_soyle
from reminders import hatirlatici_kur
from calculator import hesapla
from converter import birim_cevir, doviz_cevir
from file_manager import dosya_ara, dosya_sil, son_dosyayi_ac, belgeyi_yazdir
from system_info import sistem_bilgisi, pil_durumu, ekran_parlakligi_ayarla, wifi_ayarla, programi_kapat
from email_sender import eposta_gonder
from clipboard_actions import panoya_kopyala, panodakini_oku
from dictation import dikte_baslat, dikte_durdur
from news import haber_basliklarini_oku
from screen_recorder import ekran_kaydini_baslat, ekran_kaydini_durdur
from chat import sohbet_et, sohbeti_sifirla
from hafiza import beni_hatirla, hafizayi_listele, hafizayi_unut
from agenda import gorev_ekle, ajandayi_listele, gorev_tamamla
from media_control import medya_oynat_durdur, sonraki_parca, onceki_parca
from extras_bilgi import wikipedia_ozeti, cevir, kripto_fiyati, son_depremler, namaz_vakitleri
from extras_eglence import (
    yazi_tura, zar_at, rastgele_sayi, kelime_karakter_say,
    saka_anlat, gunun_alintisi, ruh_haline_gore_muzik,
)
from extras_dosya import klasor_boyutu, zip_olustur, zip_ac, uzantiya_gore_listele, olasi_kopyalari_bul
from extras_windows import (
    gorev_yoneticisini_ac, disk_temizligi_baslat, aktif_pencere_adi,
    son_acilan_uygulamalar, baslangica_ekle, baslangictan_kaldir,
    oyun_modu_ayarla, pencereyi_yerlestir, ekran_koruyucu_baslat,
    windows_update_ayarlarini_ac,
)
from extras_guvenlik import sifre_uret, yedekle, fabrika_ayarlarina_dondur, surum_bilgisi
from extras_takvim import takvime_etkinlik_ekle
from extras_mesaj import telegram_mesaj_gonder, toplanti_sitesi_ac
from pomodoro import pomodoro_baslat
import hud_durum

YARDIM = """Şunları yapabilirim (kısaltılmış liste — çok daha fazlası var):

UYGULAMA / DOSYA
• uygulama aç <isim> · klasör aç <yol> · site aç <adres>
• dosya ara/sil <isim> · son dosyayı aç <klasör> · yazdır <yol>
• programı kapat <isim> · klasör boyutu <yol>
• zip oluştur/aç <yol> · <uzantı> dosyalarını listele <klasör>
• olası kopyaları bul <klasör>

İNTERNET / BİLGİ
• google/youtube/spotify ara <sorgu> · son video <kanal>
• hava durumu · haberleri oku · döviz/birim çevir
• wikipedi'de ara <konu> · çevir <metin> · kripto fiyatı <coin>
• son depremler · namaz vakitleri

İLETİŞİM
• mesaj gönder / whatsapp mesaj / mail gönder / telegram mesaj gönder
• zoom aç / teams aç / meet aç
• takvime ekle: <açıklama>

BİLGİSAYAR
• sistem bilgisi · pil durumu · ekranı parlat/karart
• wifi aç/kapat · ekranı kilitle · sesi aç/kapat/kıs
• bilgisayarı kapat/yeniden başlat onayla
• ekran görüntüsü al · ekran kaydı başlat/durdur
• görev yöneticisini aç · disk temizliği başlat
• aktif pencere ne · son açtıklarım
• başlangıca ekle/kaldır · oyun modunu aç/kapat
• pencereyi sola/sağa yerleştir · ekran koruyucu başlat
• windows update ayarlarını aç
• videoyu durdur/oynat · sonraki/önceki parça

VERİMLİLİK
• not al · panoya kopyala / panoda ne var · dikte başlat/durdur
• <sayı> dakika/saat sonra hatırlat · hesapla
• saat kaç / bugünün tarihi / sabah brifingi
• pomodoro başlat

EĞLENCE
• yazı tura · zar at · rastgele sayı <a> <b> · şaka yap · günün alıntısı
• ruh halim <kelime> (müzik önerir) · kelime say: <metin>

GÜVENLİK / SİSTEM
• şifre üret · yedekle · fabrika ayarlarına dön onayla · sürüm bilgisi

SOHBET / HAFIZA
• Tanımadığım her şeyi gerçek sohbete çeviririm (ANTHROPIC_API_KEY gerekir)
• sohbeti sıfırla · beni hatırla: ... · hafızanda ne var · hakkımdaki her şeyi unut
• ajandama ekle: ... · ajandamda ne var · görevi tamamla: ...

Beni çağırmak için uyandırma kelimeni söyle (örn: "friday" ya da "uyan bakalım")."""


def _sabah_brifingi() -> str:
    parcalar = [saat_soyle(), tarih_soyle(), hava_durumu_soyle(), haber_basliklarini_oku(3)]
    return "\n\n".join(parcalar)


def komutu_isle(komut: str) -> str:
    """Her komut önce buradan geçer: HUD'u 'düşünüyor' yapar, işi
    _komutu_isle_ic'e devreder, beklenmeyen bir hata olursa program
    çökmez, HUD kısaca kırmızıya döner ve düzgün bir mesaj döner."""
    hud_durum.durum_ayarla("dusunuyor")
    try:
        return _komutu_isle_ic(komut)
    except Exception as e:
        hud_durum.durum_ayarla("hata")
        return f"Bir şeyler ters gitti ama çökmedim: {e}"


def _komutu_isle_ic(komut: str) -> str:
    komut = (komut or "").strip()
    kucuk = komut.lower()

    if kucuk in ("yardım", "help", "neler yapabilirsin", "ne yapabilirsin"):
        return YARDIM

    # --- Uygulama / dosya ---
    if kucuk.startswith("uygulama aç "):
        return uygulama_ac(komut[len("uygulama aç "):])

    if kucuk.startswith("klasör aç "):
        return klasor_ac(komut[len("klasör aç "):])

    if kucuk.startswith("site aç "):
        return site_ac(komut[len("site aç "):])

    if kucuk.startswith("dosya ara "):
        return dosya_ara(komut[len("dosya ara "):])

    if kucuk.startswith("dosya sil "):
        return dosya_sil(komut[len("dosya sil "):])

    if kucuk.startswith("son dosyayı aç "):
        return son_dosyayi_ac(komut[len("son dosyayı aç "):])

    if kucuk.startswith("yazdır "):
        return belgeyi_yazdir(komut[len("yazdır "):])

    if kucuk.startswith("programı kapat "):
        return programi_kapat(komut[len("programı kapat "):])

    if kucuk.startswith("klasör boyutu "):
        return klasor_boyutu(komut[len("klasör boyutu "):])

    if kucuk.startswith("zip oluştur "):
        return zip_olustur(komut[len("zip oluştur "):])
    if kucuk.startswith("zip aç "):
        return zip_ac(komut[len("zip aç "):])

    eslesme = re.match(r"^(\w+) dosyalarını listele (.+)$", kucuk)
    if eslesme:
        uzanti, klasor = eslesme.groups()
        return uzantiya_gore_listele(klasor, uzanti)

    if kucuk.startswith("olası kopyaları bul "):
        return olasi_kopyalari_bul(komut[len("olası kopyaları bul "):])

    # --- İnternet / bilgi ---
    if kucuk.startswith("google ara "):
        return google_ara(komut[len("google ara "):])

    if kucuk.startswith("youtube ara "):
        return youtube_ara(komut[len("youtube ara "):])

    if kucuk.startswith("spotify ara "):
        return spotify_ara(komut[len("spotify ara "):])

    if kucuk.startswith("son video "):
        return kanalin_son_videosunu_ac(komut[len("son video "):])

    eslesme = re.match(r"^(.*) kanalının son videosunu aç$", kucuk)
    if eslesme:
        return kanalin_son_videosunu_ac(eslesme.group(1))

    if kucuk in ("hava durumu", "hava nasıl"):
        return hava_durumu_soyle()
    if kucuk.startswith("hava durumu "):
        return hava_durumu_soyle(komut[len("hava durumu "):])

    if kucuk in ("haberleri oku", "haber başlıkları", "haberler"):
        return haber_basliklarini_oku()

    if kucuk.startswith("döviz çevir "):
        eslesme = re.match(r"^döviz çevir\s+([\d\.]+)\s+(\w+)\s+(\w+)", kucuk)
        if eslesme:
            miktar, kaynak, hedef = eslesme.groups()
            return doviz_cevir(float(miktar), kaynak, hedef)
        return "Kullanım: döviz çevir <miktar> <kaynak> <hedef> (örn: döviz çevir 100 usd try)"

    if kucuk.startswith("çevir ") and re.match(r"^çevir\s+[\d\.]+\s+\w+\s+\w+", kucuk):
        eslesme = re.match(r"^çevir\s+([\d\.]+)\s+(\w+)\s+(\w+)", kucuk)
        deger, kaynak, hedef = eslesme.groups()
        return birim_cevir(float(deger), kaynak, hedef)

    if kucuk.startswith("wikipedi'de ara ") or kucuk.startswith("wikipedia'da ara "):
        onek = "wikipedi'de ara " if kucuk.startswith("wikipedi'de ara ") else "wikipedia'da ara "
        return wikipedia_ozeti(komut[len(onek):])

    if kucuk.startswith("çevir "):
        return cevir(komut[len("çevir "):])

    if kucuk.startswith("kripto fiyatı "):
        return kripto_fiyati(komut[len("kripto fiyatı "):])

    if kucuk in ("son depremler", "deprem oldu mu"):
        return son_depremler()

    if kucuk in ("namaz vakitleri",):
        return namaz_vakitleri()
    if kucuk.startswith("namaz vakitleri "):
        return namaz_vakitleri(komut[len("namaz vakitleri "):])

    # --- İletişim ---
    if kucuk.startswith("whatsapp mesaj "):
        geri_kalan = komut[len("whatsapp mesaj "):]
        parcalar = geri_kalan.split(" ", 1)
        if len(parcalar) < 2:
            return "Kullanım: whatsapp mesaj <numara> <mesaj>"
        numara, mesaj = parcalar
        return whatsapp_mesaj_gonder(numara, mesaj)

    if kucuk.startswith("mesaj gönder ") or kucuk.startswith("mesaj at "):
        onek = "mesaj gönder " if kucuk.startswith("mesaj gönder ") else "mesaj at "
        geri_kalan = komut[len(onek):]
        parcalar = geri_kalan.split(" ", 1)
        if len(parcalar) < 2:
            return "Kullanım: mesaj gönder <kişi adı> <mesaj>"
        isim, mesaj = parcalar
        return whatsapp_mesaj_gonder(isim, mesaj)

    if kucuk.startswith("mail gönder ") or kucuk.startswith("eposta gönder "):
        onek = "mail gönder " if kucuk.startswith("mail gönder ") else "eposta gönder "
        geri_kalan = komut[len(onek):]
        parcalar = geri_kalan.split(" ", 1)
        if len(parcalar) < 2:
            return "Kullanım: mail gönder <kişi/e-posta> <mesaj>"
        hedef, govde = parcalar
        return eposta_gonder(hedef, "Friday'den mesaj", govde)

    if kucuk.startswith("telegram mesaj gönder "):
        return telegram_mesaj_gonder(komut[len("telegram mesaj gönder "):])

    if kucuk in ("zoom aç", "teams aç", "meet aç", "google meet aç"):
        isim = kucuk.replace(" aç", "")
        return toplanti_sitesi_ac(isim)

    if kucuk.startswith("takvime ekle:"):
        return takvime_etkinlik_ekle(komut[len("takvime ekle:"):])
    if kucuk.startswith("takvime ekle "):
        return takvime_etkinlik_ekle(komut[len("takvime ekle "):])

    # --- Bilgisayar ---
    if kucuk in ("sistem bilgisi", "bilgisayar nasıl"):
        return sistem_bilgisi()

    if kucuk in ("pil durumu", "şarj durumu", "pil yüzde kaç"):
        return pil_durumu()

    if kucuk in ("ekranı parlat", "ekran parlaklığını artır"):
        return ekran_parlakligi_ayarla("artir")
    if kucuk in ("ekranı karart", "ekran parlaklığını azalt"):
        return ekran_parlakligi_ayarla("azalt")

    if kucuk == "wifi aç":
        return wifi_ayarla("ac")
    if kucuk == "wifi kapat":
        return wifi_ayarla("kapat")

    if kucuk == "ekranı kilitle":
        return ekrani_kilitle()

    if kucuk == "sesi aç":
        return ses_ayarla("ac")
    if kucuk == "sesi kapat":
        return ses_ayarla("kapat")
    if kucuk == "sesi kıs":
        return ses_ayarla("kis")

    if kucuk == "bilgisayarı kapat onayla":
        return bilgisayari_kapat()
    if kucuk == "bilgisayarı yeniden başlat onayla":
        return bilgisayari_yeniden_baslat()
    if kucuk in ("bilgisayarı kapat", "bilgisayarı yeniden başlat"):
        return ("Emin misin? Yanlışlıkla olmasın diye, sonuna 'onayla' ekleyerek "
                "tekrar söylemen gerekiyor. Örn: bilgisayarı kapat onayla")

    if kucuk in ("ekran görüntüsü al", "ekran görüntüsü"):
        return ekran_goruntusu_al()

    if kucuk in ("ekran kaydı başlat", "ekran kaydını başlat"):
        return ekran_kaydini_baslat()
    if kucuk in ("ekran kaydını durdur", "ekran kaydı durdur"):
        return ekran_kaydini_durdur()

    if kucuk in ("görev yöneticisini aç", "görev yöneticisi aç"):
        return gorev_yoneticisini_ac()

    if kucuk in ("disk temizliği başlat", "disk temizliği"):
        return disk_temizligi_baslat()

    if kucuk in ("aktif pencere ne", "hangi pencere açık"):
        return aktif_pencere_adi()

    if kucuk in ("son açtıklarım", "son açılan uygulamalar"):
        return son_acilan_uygulamalar()

    if kucuk == "başlangıca ekle":
        return baslangica_ekle()
    if kucuk == "başlangıçtan kaldır":
        return baslangictan_kaldir()

    if kucuk == "oyun modunu aç":
        return oyun_modu_ayarla("ac")
    if kucuk == "oyun modunu kapat":
        return oyun_modu_ayarla("kapat")

    if kucuk == "pencereyi sola yerleştir":
        return pencereyi_yerlestir("sol")
    if kucuk == "pencereyi sağa yerleştir":
        return pencereyi_yerlestir("sag")

    if kucuk == "ekran koruyucu başlat":
        return ekran_koruyucu_baslat()

    if kucuk in ("windows update ayarlarını aç", "güncelleme ayarlarını aç"):
        return windows_update_ayarlarini_ac()

    if kucuk in ("videoyu durdur", "videoyu oynat", "müziği durdur", "müziği oynat", "oynat durdur"):
        return medya_oynat_durdur()
    if kucuk in ("sonraki parça", "sonraki şarkı"):
        return sonraki_parca()
    if kucuk in ("önceki parça", "önceki şarkı"):
        return onceki_parca()

    # --- Verimlilik ---
    if kucuk.startswith("not al "):
        return not_al(komut[len("not al "):])

    if kucuk.startswith("panoya kopyala "):
        return panoya_kopyala(komut[len("panoya kopyala "):])
    if kucuk in ("panoda ne var", "pano ne var"):
        return panodakini_oku()

    if kucuk == "dikte başlat":
        return dikte_baslat()
    if kucuk == "dikte durdur":
        return dikte_durdur()

    if re.match(r"^\d+\s*(dakika|saat)\s*sonra hatırlat", kucuk):
        return hatirlatici_kur(komut)

    if kucuk.startswith("hesapla "):
        return hesapla(komut[len("hesapla "):])

    if kucuk in ("saat kaç", "saat kaç?", "saat ne"):
        return saat_soyle()

    if kucuk in ("bugünün tarihi", "tarih nedir", "bugün günlerden ne"):
        return tarih_soyle()

    if kucuk in ("sabah brifingi", "günaydın", "gunaydin"):
        return _sabah_brifingi()

    if kucuk in ("pomodoro başlat", "pomodoro"):
        return pomodoro_baslat()

    # --- Eğlence ---
    if kucuk in ("yazı tura", "yazı tura at"):
        return yazi_tura()

    if kucuk in ("zar at",):
        return zar_at()
    eslesme = re.match(r"^(\d+) yüzlü zar at$", kucuk)
    if eslesme:
        return zar_at(int(eslesme.group(1)))

    eslesme = re.match(r"^rastgele sayı (\d+) (\d+)$", kucuk)
    if eslesme:
        alt, ust = eslesme.groups()
        return rastgele_sayi(int(alt), int(ust))

    if kucuk.startswith("kelime say:") or kucuk.startswith("kelime say "):
        metin = komut.split(":", 1)[1] if ":" in komut else komut[len("kelime say "):]
        return kelime_karakter_say(metin)

    if kucuk in ("şaka yap", "bir şaka anlat"):
        return saka_anlat()

    if kucuk in ("günün alıntısı", "bugünün sözü"):
        return gunun_alintisi()

    if kucuk.startswith("ruh halim "):
        return ruh_haline_gore_muzik(komut[len("ruh halim "):])

    # --- Güvenlik / sistem ---
    if kucuk == "şifre üret":
        return sifre_uret()
    eslesme = re.match(r"^(\d+) haneli şifre üret$", kucuk)
    if eslesme:
        return sifre_uret(int(eslesme.group(1)))

    if kucuk == "yedekle":
        return yedekle()

    if kucuk == "fabrika ayarlarına dön onayla":
        return fabrika_ayarlarina_dondur()
    if kucuk == "fabrika ayarlarına dön":
        return "Emin misin? Onaylamak için: fabrika ayarlarına dön onayla"

    if kucuk in ("sürüm bilgisi", "hangi sürümdesin"):
        return surum_bilgisi()

    # --- Sohbet / hafıza / ajanda ---
    if kucuk in ("sohbeti sıfırla",):
        return sohbeti_sifirla()

    if kucuk.startswith("beni hatırla:"):
        return beni_hatirla(komut[len("beni hatırla:"):])
    if kucuk.startswith("beni hatırla "):
        return beni_hatirla(komut[len("beni hatırla "):])

    if kucuk in ("hafızanda ne var", "benim hakkımda ne biliyorsun", "beni nasıl tanıyorsun"):
        return hafizayi_listele()
    if kucuk in ("hakkımdaki her şeyi unut", "beni unut"):
        return hafizayi_unut()

    if kucuk.startswith("ajandama ekle:"):
        return gorev_ekle(komut[len("ajandama ekle:"):])
    if kucuk.startswith("ajandama ekle "):
        return gorev_ekle(komut[len("ajandama ekle "):])

    if kucuk in ("ajandamda ne var", "ajandam ne var"):
        return ajandayi_listele()

    if kucuk.startswith("görevi tamamla:"):
        return gorev_tamamla(komut[len("görevi tamamla:"):])
    if kucuk.startswith("görevi tamamla "):
        return gorev_tamamla(komut[len("görevi tamamla "):])

    # --- Hiçbir kalıba uymadıysa: gerçek sohbete geç ---
    return sohbet_et(komut)
