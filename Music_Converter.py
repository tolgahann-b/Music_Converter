import os
import subprocess
import time
import sys
import zipfile
import shutil
import urllib.request
import glob
import tempfile
import json
import re
import threading

# ===================================================================
#  MUSIC CONVERTER PRO (TR/EN)
#  - Kalite (kbps) seçimi
#  - FFmpeg ve yt-dlp otomatik kurulum
#  - Başarısız dosya raporu ve YouTube indirme
#  - Türkçe / İngilizce Dil Desteği
# ===================================================================

FFMPEG_DOWNLOAD_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
YTDLP_DOWNLOAD_URL = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"

AKTIF_DIL = 'tr'

METINLER = {
    'tr': {
        'baslik': "OTOMATİK SES DÖNÜŞTÜRÜCÜ PRO",
        'bulunulan_klasor': "Bulunulan Klasör",
        'ffmpeg_durum': "FFmpeg: ✓ Hazır",
        'menu_secim': "Lütfen yapmak istediğiniz işlemi seçin:",
        'menu_m4a': "M4A'dan MP3'e Çevir",
        'menu_mp4': "MP4'ten (Videodan) MP3'e Çevir",
        'menu_wav': "WAV'dan MP3'e Çevir",
        'menu_dil': "Dil Seçimi / Language (TR / EN)",
        'menu_cikis': "Çıkış",
        'seciminiz': "Seçiminiz",
        'gecersiz_secim': "[HATA] Geçersiz seçim! Lütfen listedeki numaralardan birini girin.",
        'cikis_mesaj': "Çıkış yapılıyor. Görüşmek üzere!",

        'kalite_baslik': "KALİTE SEÇİMİ (Bit Rate)",
        'kalite_1': "128 kbps  — Küçük boyut, düşük kalite",
        'kalite_2': "192 kbps  — Orta kalite (önerilen)",
        'kalite_3': "256 kbps  — Yüksek kalite",
        'kalite_4': "320 kbps  — Maksimum kalite (en büyük boyut)",
        'kalite_secilen': "Seçilen kalite",
        'kalite_varsayilan': "Varsayılan kalite seçildi: 192 kbps",

        'dosya_bulunamadi': "[UYARI] Bu klasörde '{uzanti}' uzantılı dosya bulunamadı!",
        'klasor_olusturuldu': "[BILGI] '{klasor}' klasörü oluşturuldu/kontrol edildi.",
        'toplam_dosya_donusturulecek': "[BILGI] Toplam {toplam} adet dosya dönüştürülecek...",
        'secilen_kalite_bilgi': "[BILGI] Seçilen kalite: {bitrate} kbps",

        'durum_bitti': "✓ Bitti     ",
        'durum_hata': "✗ HATA      ",
        'durum_timeout': "⏱ TIMEOUT   ",
        'durum_zaten_var': "○ Zaten var ",
        'durum_cevriliyor': "Çevriliyor",
        'sure_etiket': "Süre",

        'sonuc_raporu_baslik': "SONUÇ RAPORU",
        'toplam_dosya': "Toplam dosya     ",
        'basarili': "✓ Başarılı       ",
        'basarisiz': "✗ Başarısız      ",
        'zaten_cevrilmis': "○ Zaten çevrilmiş",
        'zaman_asimi': "⏱ Zaman aşımı    ",
        'kalite_etiket': "Kalite           ",
        'toplam_sure_etiket': "Toplam süre      ",
        'cikti_klasoru_etiket': "Çıktı klasörü    ",
        'dakika': "dakika",
        'saniye': "saniye",
        'basarisiz_liste_baslik': "BAŞARISIZ DOSYALAR VE HATA NEDENLERİ:",
        'neden_etiket': "Neden",
        'enter_devam': "Devam etmek icin Enter'a bas...",
        'enter_menu': "Menüye dönmek icin Enter'a bas...",

        'yt_baslik': "YOUTUBE'DAN İNDİRME",
        'yt_bilgi': "  {sayi} adet başarısız dosya YouTube'dan indirilebilir.\n  Her dosya için arama yapılacak ve size sonuçlar gösterilecek.",
        'yt_soru': "  YouTube'dan indirmek ister misiniz? (E/h): ",
        'yt_araniyor': "YouTube'da aranıyor",
        'yt_sonuc_yok': "Sonuç bulunamadı!",
        'yt_sonuclar': "Sonuçlar:",
        'yt_atla': "[0] Atla (indirme)",
        'yt_degistir': "[A] Arama terimini değiştir",
        'yt_yeni_arama': "Yeni arama terimi: ",
        'yt_indiriliyor': "⬇ İndiriliyor: {baslik}",
        'yt_basarili': "✓ Başarıyla indirildi!",
        'yt_basarisiz': "✗ İndirme başarısız!",
        'yt_rapor_baslik': "YOUTUBE İNDİRME RAPORU",
        'yt_kullanici_atladi': "Kullanıcı atladı",

        'ffmpeg_bulunamadi_baslik': "FFmpeg bulunamadı! Otomatik kurulum başlatılıyor...",
        'ytdlp_bulunamadi_baslik': "yt-dlp bulunamadı! Otomatik kurulum başlatılıyor...",
        'kaynak': "Kaynak",
        'boyut': "Boyut",
        'hedef': "Hedef",
        'indirilsin_mi': "İndirmek istiyor musunuz? (E/h): ",
        'ffmpeg_olmadan_uyari': "[UYARI] FFmpeg olmadan dönüştürme yapılamaz!",
        'ytdlp_olmadan_uyari': "[UYARI] yt-dlp olmadan YouTube'dan indirme yapılamaz!",

        'dil_menu_baslik': "DİL SEÇİMİ / LANGUAGE SELECTION",
        'dil_secilen_mesaj': "✓ Uygulama dili Türkçe olarak ayarlandı.",
    },
    'en': {
        'baslik': "AUTOMATIC AUDIO CONVERTER PRO",
        'bulunulan_klasor': "Current Directory",
        'ffmpeg_durum': "FFmpeg: ✓ Ready",
        'menu_secim': "Please select an operation:",
        'menu_m4a': "Convert M4A to MP3",
        'menu_mp4': "Convert MP4 (Video) to MP3",
        'menu_wav': "Convert WAV to MP3",
        'menu_dil': "Language / Dil Seçimi (EN / TR)",
        'menu_cikis': "Exit",
        'seciminiz': "Your choice",
        'gecersiz_secim': "[ERROR] Invalid selection! Please choose a valid number.",
        'cikis_mesaj': "Exiting. See you next time!",

        'kalite_baslik': "QUALITY SELECTION (Bit Rate)",
        'kalite_1': "128 kbps  — Small size, lower quality",
        'kalite_2': "192 kbps  — Medium quality (recommended)",
        'kalite_3': "256 kbps  — High quality",
        'kalite_4': "320 kbps  — Maximum quality (largest size)",
        'kalite_secilen': "Selected quality",
        'kalite_varsayilan': "Default quality selected: 192 kbps",

        'dosya_bulunamadi': "[WARNING] No '{uzanti}' files found in this directory!",
        'klasor_olusturuldu': "[INFO] '{klasor}' directory created/checked.",
        'toplam_dosya_donusturulecek': "[INFO] Total {toplam} file(s) will be converted...",
        'secilen_kalite_bilgi': "[INFO] Selected quality: {bitrate} kbps",

        'durum_bitti': "✓ Done     ",
        'durum_hata': "✗ ERROR    ",
        'durum_timeout': "⏱ TIMEOUT   ",
        'durum_zaten_var': "○ Already  ",
        'durum_cevriliyor': "Converting",
        'sure_etiket': "Time",

        'sonuc_raporu_baslik': "SUMMARY REPORT",
        'toplam_dosya': "Total files      ",
        'basarili': "✓ Successful     ",
        'basarisiz': "✗ Failed         ",
        'zaten_cevrilmis': "○ Already converted",
        'zaman_asimi': "⏱ Timeout        ",
        'kalite_etiket': "Quality          ",
        'toplam_sure_etiket': "Total duration   ",
        'cikti_klasoru_etiket': "Output folder    ",
        'dakika': "minutes",
        'saniye': "seconds",
        'basarisiz_liste_baslik': "FAILED FILES AND ERROR REASONS:",
        'neden_etiket': "Reason",
        'enter_devam': "Press Enter to continue...",
        'enter_menu': "Press Enter to return to menu...",

        'yt_baslik': "YOUTUBE DOWNLOAD",
        'yt_bilgi': "  {sayi} failed file(s) can be downloaded from YouTube.\n  Search will be performed for each file and options will be displayed.",
        'yt_soru': "  Would you like to download from YouTube? (Y/n): ",
        'yt_araniyor': "Searching on YouTube",
        'yt_sonuc_yok': "No results found!",
        'yt_sonuclar': "Results:",
        'yt_atla': "[0] Skip (do not download)",
        'yt_degistir': "[A] Change search query",
        'yt_yeni_arama': "New search query: ",
        'yt_indiriliyor': "⬇ Downloading: {baslik}",
        'yt_basarili': "✓ Successfully downloaded!",
        'yt_basarisiz': "✗ Download failed!",
        'yt_rapor_baslik': "YOUTUBE DOWNLOAD REPORT",
        'yt_kullanici_atladi': "User skipped",

        'ffmpeg_bulunamadi_baslik': "FFmpeg not found! Automatic setup starting...",
        'ytdlp_bulunamadi_baslik': "yt-dlp not found! Automatic setup starting...",
        'kaynak': "Source",
        'boyut': "Size",
        'hedef': "Target",
        'indirilsin_mi': "Do you want to download? (Y/n): ",
        'ffmpeg_olmadan_uyari': "[WARNING] Conversion cannot proceed without FFmpeg!",
        'ytdlp_olmadan_uyari': "[WARNING] YouTube download cannot proceed without yt-dlp!",

        'dil_menu_baslik': "LANGUAGE SELECTION / DİL SEÇİMİ",
        'dil_secilen_mesaj': "✓ Application language set to English.",
    }
}


def t(key, **kwargs):
    """Aktif dile göre metni döndürür ve parametreleri yerleştirir."""
    global AKTIF_DIL
    metin = METINLER.get(AKTIF_DIL, METINLER['tr']).get(key, METINLER['tr'].get(key, key))
    if kwargs:
        try:
            return metin.format(**kwargs)
        except Exception:
            return metin
    return metin


def dil_yukle():
    """ayarlar.json dosyasından dil seçimini yükler."""
    global AKTIF_DIL
    ayarlar_dosyasi = os.path.join(uygulama_klasoru(), "ayarlar.json")
    if os.path.isfile(ayarlar_dosyasi):
        try:
            with open(ayarlar_dosyasi, 'r', encoding='utf-8') as f:
                data = json.load(f)
                AKTIF_DIL = data.get('dil', 'tr')
        except Exception:
            AKTIF_DIL = 'tr'


def dil_kaydet(dil_kodu):
    """Dil seçimini ayarlar.json dosyasına kaydeder."""
    global AKTIF_DIL
    AKTIF_DIL = dil_kodu
    ayarlar_dosyasi = os.path.join(uygulama_klasoru(), "ayarlar.json")
    try:
        with open(ayarlar_dosyasi, 'w', encoding='utf-8') as f:
            json.dump({'dil': dil_kodu}, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _ag_hata_mesaji_anlamlandir(e):
    """Ağ hatalarını kullanıcı dostu Türkçe/İngilizce mesaja çevirir."""
    err_str = str(e)
    if "11001" in err_str or "getaddrinfo failed" in err_str or "Name or service not known" in err_str:
        if AKTIF_DIL == 'en':
            return "No internet connection or DNS lookup failed (getaddrinfo failed).\n        Please check your internet connection and try again."
        return "İnternet bağlantısı yok veya DNS sunucusuna ulaşılamıyor (getaddrinfo failed).\n        Lütfen internet bağlantınızı kontrol edip tekrar deneyin."
    elif "timed out" in err_str.lower():
        if AKTIF_DIL == 'en':
            return "Connection timed out. Server did not respond."
        return "Bağlantı zaman aşımına uğradı. Sunucu yanıt vermiyor."
    elif "Certificate" in err_str or "SSL" in err_str:
        if AKTIF_DIL == 'en':
            return "SSL/Security certificate verification error."
        return "SSL/Güvenlik sertifikası doğrulama hatası."
    return f"{e}"


def indir_dosya_useragent(url, hedef_path, ilerleme_cb=None):
    """Custom User-Agent ile internetten dosya indirir."""
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    )
    with urllib.request.urlopen(req, timeout=30) as response, open(hedef_path, 'wb') as out_file:
        toplam_boyut = int(response.headers.get('Content-Length', 0))
        indirilen = 0
        blok_boyutu = 8192
        blok_sayisi = 0
        while True:
            buffer = response.read(blok_boyutu)
            if not buffer:
                break
            out_file.write(buffer)
            indirilen += len(buffer)
            blok_sayisi += 1
            if ilerleme_cb:
                ilerleme_cb(blok_sayisi, blok_boyutu, toplam_boyut)


def uygulama_klasoru():
    """EXE olarak çalışıyorsa EXE'nin bulunduğu klasörü, değilse script klasörünü döndürür."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def ffmpeg_bul():
    """FFmpeg'i bulmaya çalışır."""
    yerel_klasor = os.path.join(uygulama_klasoru(), "ffmpeg_bin")
    if os.path.isdir(yerel_klasor):
        sonuclar = glob.glob(os.path.join(yerel_klasor, "**", "ffmpeg.exe"), recursive=True)
        if sonuclar:
            return sonuclar[0]

    try:
        sonuc = subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        if sonuc.returncode == 0:
            return "ffmpeg"
    except FileNotFoundError:
        pass

    return None


def ffmpeg_indir():
    """FFmpeg'i indirir ve ffmpeg_bin/ klasörüne çıkarır."""
    hedef_klasor = os.path.join(uygulama_klasoru(), "ffmpeg_bin")
    zip_yolu = os.path.join(uygulama_klasoru(), "ffmpeg_temp.zip")

    print("\n" + "=" * 64)
    print(f"  {t('ffmpeg_bulunamadi_baslik')}")
    print("=" * 64)
    print(f"\n  {t('kaynak')} : gyan.dev (resmi FFmpeg build)")
    print(f"  {t('boyut')}  : ~90 MB")
    print(f"  {t('hedef')}  : {hedef_klasor}")
    print()

    onay = input(f"  {t('indirilsin_mi')}").strip().lower()
    if onay in ['h', 'n']:
        print(f"\n{t('ffmpeg_olmadan_uyari')}")
        input(f"\n{t('enter_devam')}")
        return None

    print("\n  ...", end="", flush=True)

    def ilerleme_goster(blok_sayisi, blok_boyutu, toplam_boyut):
        indirilen = blok_sayisi * blok_boyutu
        if toplam_boyut > 0:
            yuzde = min(indirilen * 100 / toplam_boyut, 100)
            mb_indirilen = indirilen / (1024 * 1024)
            mb_toplam = toplam_boyut / (1024 * 1024)
            sys.stdout.write(f"\r  [{mb_indirilen:.1f} / {mb_toplam:.1f} MB]  [%{yuzde:.0f}]   ")
            sys.stdout.flush()
        else:
            sys.stdout.write(".")
            sys.stdout.flush()

    try:
        indir_dosya_useragent(FFMPEG_DOWNLOAD_URL, zip_yolu, ilerleme_goster)
        print("\n\n  ✓ OK! Unzipping...")

        os.makedirs(hedef_klasor, exist_ok=True)

        with zipfile.ZipFile(zip_yolu, 'r') as zf:
            zf.extractall(hedef_klasor)

        os.remove(zip_yolu)

        ffmpeg_yolu = ffmpeg_bul()
        if ffmpeg_yolu:
            print(f"  ✓ FFmpeg OK! Location: {ffmpeg_yolu}")
            input(f"\n  {t('enter_devam')}")
            return ffmpeg_yolu
        else:
            print("\n  [HATA / ERROR] FFmpeg exe not found!")
            input(f"\n  {t('enter_devam')}")
            return None

    except Exception as e:
        hata = _ag_hata_mesaji_anlamlandir(e)
        print(f"\n\n  [HATA / ERROR]")
        print(f"  Detay: {hata}")
        if os.path.exists(zip_yolu):
            os.remove(zip_yolu)
        input(f"\n  {t('enter_devam')}")
        return None


def ytdlp_bul():
    """yt-dlp.exe'yi bulmaya çalışır."""
    yerel_yol = os.path.join(uygulama_klasoru(), "yt-dlp_bin", "yt-dlp.exe")
    if os.path.isfile(yerel_yol):
        return yerel_yol

    try:
        sonuc = subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        if sonuc.returncode == 0:
            versiyon = sonuc.stdout.strip()
            if versiyon >= "2026.08.01":
                return "yt-dlp"
    except Exception:
        pass

    return None


def ytdlp_guncelle(ytdlp_yolu):
    """Yerel yt-dlp.exe dosyasını günceller."""
    if ytdlp_yolu and os.path.isfile(ytdlp_yolu):
        try:
            print("  yt-dlp update check...", end="", flush=True)
            subprocess.run(
                [ytdlp_yolu, "-U"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=15,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            print(" OK.")
        except Exception:
            print()


def ytdlp_indir():
    """yt-dlp.exe'yi GitHub releases'tan indirir."""
    hedef_klasor = os.path.join(uygulama_klasoru(), "yt-dlp_bin")
    hedef_dosya = os.path.join(hedef_klasor, "yt-dlp.exe")

    print(f"\n{'=' * 64}")
    print(f"  {t('ytdlp_bulunamadi_baslik')}")
    print(f"{'=' * 64}")
    print(f"\n  {t('kaynak')} : GitHub (yt-dlp releases)")
    print(f"  {t('boyut')}  : ~10 MB")
    print(f"  {t('hedef')}  : {hedef_klasor}")
    print()

    onay = input(f"  {t('indirilsin_mi')}").strip().lower()
    if onay in ['h', 'n']:
        print(f"\n{t('ytdlp_olmadan_uyari')}")
        input(f"\n{t('enter_devam')}")
        return None

    print("\n  ...", end="", flush=True)

    def ilerleme_goster(blok_sayisi, blok_boyutu, toplam_boyut):
        indirilen = blok_sayisi * blok_boyutu
        if toplam_boyut > 0:
            yuzde = min(indirilen * 100 / toplam_boyut, 100)
            mb_indirilen = indirilen / (1024 * 1024)
            mb_toplam = toplam_boyut / (1024 * 1024)
            sys.stdout.write(f"\r  [{mb_indirilen:.1f} / {mb_toplam:.1f} MB]  [%{yuzde:.0f}]   ")
            sys.stdout.flush()
        else:
            sys.stdout.write(".")
            sys.stdout.flush()

    try:
        os.makedirs(hedef_klasor, exist_ok=True)
        indir_dosya_useragent(YTDLP_DOWNLOAD_URL, hedef_dosya, ilerleme_goster)
        print(f"\n\n  ✓ yt-dlp OK!")
        print(f"    Location: {hedef_dosya}")
        input(f"\n  {t('enter_devam')}")
        return hedef_dosya
    except Exception as e:
        hata = _ag_hata_mesaji_anlamlandir(e)
        print(f"\n\n  [HATA / ERROR]")
        print(f"  Detay: {hata}")
        input(f"\n  {t('enter_devam')}")
        return None


def dosya_adindan_arama_terimi(dosya_adi):
    """Dosya adından YouTube arama terimi çıkarır."""
    isim = os.path.splitext(dosya_adi)[0]
    temizle_kaliplari = [
        r'\(\d+\)',
        r'\[\d+\]',
        r'\b\d{3,4}kbps\b',
        r'\bMP3\b',
        r'\bM4A\b',
        r'\bFLAC\b',
        r'\bWAV\b',
        r'\bHQ\b',
        r'\bHD\b',
        r'\bOfficial\b',
        r'\bVideo\b',
        r'\bAudio\b',
        r'\bLyrics\b',
        r'www\..+?\.(com|net|org)',
    ]
    for kalip in temizle_kaliplari:
        isim = re.sub(kalip, '', isim, flags=re.IGNORECASE)
    isim = isim.replace('_', ' ').replace('-', ' ')
    isim = re.sub(r'\s+', ' ', isim).strip()
    return isim


def youtube_ara(ytdlp_yolu, arama_terimi, sonuc_sayisi=5):
    """YouTube'da arama yapar ve sonuçları döndürür."""
    try:
        sonuc = subprocess.run(
            [
                ytdlp_yolu,
                f"ytsearch{sonuc_sayisi}:{arama_terimi}",
                "--dump-json",
                "--no-download",
                "--flat-playlist",
            ],
            capture_output=True,
            text=True,
            timeout=30,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )

        sonuclar = []
        for satir in sonuc.stdout.strip().split('\n'):
            if satir.strip():
                try:
                    veri = json.loads(satir)
                    sonuclar.append({
                        'baslik': veri.get('title', 'Bilinmeyen'),
                        'sure': veri.get('duration', 0),
                        'url': veri.get('url', veri.get('webpage_url', '')),
                        'id': veri.get('id', ''),
                        'kanal': veri.get('channel', veri.get('uploader', 'Bilinmeyen')),
                    })
                except json.JSONDecodeError:
                    continue

        return sonuclar

    except subprocess.TimeoutExpired:
        print(f"\n  [UYARI / WARNING] {t('yt_araniyor')} timeout.")
        return []
    except Exception as e:
        print(f"\n  [HATA / ERROR] {e}")
        return []


def sure_formatla(saniye):
    """Saniyeyi dk:sn formatına çevirir."""
    if not saniye or saniye <= 0:
        return "?:??"
    dk, sn = divmod(int(saniye), 60)
    if dk >= 60:
        saat, dk = divmod(dk, 60)
        return f"{saat}:{dk:02d}:{sn:02d}"
    return f"{dk}:{sn:02d}"


def youtube_indir(ytdlp_yolu, ffmpeg_yolu, video_id, cikti_klasoru, bitrate, dosya_adi):
    """YouTube'dan MP3 olarak indirir."""
    cikti_adi = os.path.splitext(dosya_adi)[0]
    cikti_sablonu = os.path.join(cikti_klasoru, f"{cikti_adi}.%(ext)s")

    cmd = [
        ytdlp_yolu,
        f"https://www.youtube.com/watch?v={video_id}",
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", f"{bitrate}k",
        "-o", cikti_sablonu,
        "--no-playlist",
        "--no-warnings",
    ]

    if ffmpeg_yolu != "ffmpeg":
        ffmpeg_klasoru = os.path.dirname(ffmpeg_yolu) if os.path.isfile(ffmpeg_yolu) else ffmpeg_yolu
        cmd.extend(["--ffmpeg-location", ffmpeg_klasoru])

    try:
        islem = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        if islem.returncode == 0:
            return True, "OK"
        else:
            hata_mesaji = islem.stderr if islem.stderr else islem.stdout
            anlamli_hata = _hata_mesaji_ayikla(hata_mesaji.encode('utf-8') if hata_mesaji else b"")
            return False, anlamli_hata
    except subprocess.TimeoutExpired:
        return False, "Timeout (5 min)"
    except Exception as e:
        return False, str(e)


def basarisiz_dosyalari_youtube_indir(basarisiz_liste, cikti_klasoru, bitrate, ffmpeg_yolu):
    """Başarısız dosyaları YouTube'dan indirmeyi teklif eder."""
    print(f"\n{'=' * 64}")
    print(f"  {t('yt_baslik')}")
    print(f"{'=' * 64}")
    print(f"\n{t('yt_bilgi', sayi=len(basarisiz_liste))}\n")

    onay = input(t('yt_soru')).strip().lower()
    if onay in ['h', 'n']:
        return

    ytdlp_yolu = ytdlp_bul()
    if ytdlp_yolu is None:
        ytdlp_yolu = ytdlp_indir()
        if ytdlp_yolu is None:
            print(f"\n  {t('ytdlp_olmadan_uyari')}")
            input(f"\n  {t('enter_devam')}")
            return
    else:
        ytdlp_guncelle(ytdlp_yolu)

    indirme_raporu = []

    for idx, (dosya_adi, hata) in enumerate(basarisiz_liste, 1):
        print(f"\n{'─' * 64}")
        print(f"  [{idx}/{len(basarisiz_liste)}] \"{dosya_adi}\"")
        print(f"  {t('neden_etiket')}: {hata}")
        print(f"{'─' * 64}")

        arama = dosya_adindan_arama_terimi(dosya_adi)
        print(f"\n  Search: \"{arama}\"")
        print(f"  {t('yt_araniyor')}", end="", flush=True)

        sonuclar = []
        arama_bitti = threading.Event()
        arama_sonuc = []

        def arama_yap():
            arama_sonuc.extend(youtube_ara(ytdlp_yolu, arama))
            arama_bitti.set()

        t_thread = threading.Thread(target=arama_yap)
        t_thread.start()

        while not arama_bitti.is_set():
            sys.stdout.write(".")
            sys.stdout.flush()
            arama_bitti.wait(timeout=0.5)

        t_thread.join()
        sonuclar = arama_sonuc
        print()

        if not sonuclar:
            print(f"\n  [UYARI] {t('yt_sonuc_yok')}")
            indirme_raporu.append((dosya_adi, "✗", t('yt_sonuc_yok')))
            continue

        print(f"\n  {t('yt_sonuclar')}")
        for i, s in enumerate(sonuclar, 1):
            sure_str = sure_formatla(s['sure'])
            baslik = s['baslik'] if len(s['baslik']) <= 50 else s['baslik'][:47] + "..."
            kanal = s['kanal'] if len(s['kanal']) <= 20 else s['kanal'][:17] + "..."
            print(f"   [{i}] {baslik:<50} {sure_str:>7}  ({kanal})")

        print(f"\n   {t('yt_atla')}")
        print(f"   {t('yt_degistir')}")

        while True:
            secim = input(f"\n  {t('seciminiz')}: ").strip().lower()

            if secim == '0':
                indirme_raporu.append((dosya_adi, "⊘", t('yt_kullanici_atladi')))
                break
            elif secim == 'a':
                yeni_arama = input(f"  {t('yt_yeni_arama')}").strip()
                if yeni_arama:
                    print(f"\n  {t('yt_araniyor')}", end="", flush=True)
                    sonuclar = youtube_ara(ytdlp_yolu, yeni_arama)
                    print()
                    if not sonuclar:
                        print(f"\n  [UYARI] {t('yt_sonuc_yok')}")
                        continue
                    print(f"\n  {t('yt_sonuclar')}")
                    for i, s in enumerate(sonuclar, 1):
                        sure_str = sure_formatla(s['sure'])
                        baslik = s['baslik'] if len(s['baslik']) <= 50 else s['baslik'][:47] + "..."
                        kanal = s['kanal'] if len(s['kanal']) <= 20 else s['kanal'][:17] + "..."
                        print(f"   [{i}] {baslik:<50} {sure_str:>7}  ({kanal})")
                    print(f"\n   {t('yt_atla')}")
                    print(f"   {t('yt_degistir')}")
                continue
            elif secim.isdigit() and 1 <= int(secim) <= len(sonuclar):
                secilen = sonuclar[int(secim) - 1]
                print(f"\n  {t('yt_indiriliyor', baslik=secilen['baslik'])}")
                print(f"    Kalite: {bitrate} kbps | Format: MP3")

                basarili, hata_detay = youtube_indir(
                    ytdlp_yolu, ffmpeg_yolu,
                    secilen['id'], cikti_klasoru, bitrate, dosya_adi
                )

                if basarili:
                    print(f"    {t('yt_basarili')}")
                    indirme_raporu.append((dosya_adi, "✓", secilen['baslik']))
                else:
                    print(f"    {t('yt_basarisiz')} ({hata_detay})")
                    indirme_raporu.append((dosya_adi, "✗", f"{hata_detay} ({secilen['baslik']})"))
                break
            else:
                print(f"  {t('gecersiz_secim')}")

    if indirme_raporu:
        print(f"\n{'=' * 64}")
        print(f"              {t('yt_rapor_baslik')}")
        print(f"{'=' * 64}")
        for dosya_adi, durum, detay in indirme_raporu:
            dosya_kisa = dosya_adi if len(dosya_adi) <= 25 else dosya_adi[:22] + "..."
            print(f"  {durum} {dosya_kisa:<25} → {detay}")
        print(f"{'=' * 64}")

    input(f"\n{t('enter_menu')}")


def temizle():
    os.system('cls' if os.name == 'nt' else 'clear')


def baslik_yazdir():
    temizle()
    print("================================================================")
    print(f"          {t('baslik')}               ")
    print("================================================================")
    print(f" {t('bulunulan_klasor')}: {os.getcwd()}")
    print("================================================================\n")


def kalite_sec():
    """Kullanıcıya kalite seçtirip bitrate değeri döndürür."""
    baslik_yazdir()
    print(f"              {t('kalite_baslik')}")
    print("================================================================\n")

    kalite_secenekleri = {
        '1': ('128', t('kalite_1')),
        '2': ('192', t('kalite_2')),
        '3': ('256', t('kalite_3')),
        '4': ('320', t('kalite_4')),
    }

    for anahtar, (_, aciklama) in kalite_secenekleri.items():
        varsayilan = " ◄" if anahtar == '2' else ""
        print(f"  [{anahtar}] {aciklama}{varsayilan}")

    print("\n================================================================")
    secim = input(f"\n  {t('seciminiz')} (default 2): ").strip()

    if secim in kalite_secenekleri:
        bitrate = kalite_secenekleri[secim][0]
        print(f"\n  ✓ {t('kalite_secilen')}: {bitrate} kbps")
        time.sleep(0.5)
        return bitrate
    else:
        print(f"\n  → {t('kalite_varsayilan')}")
        time.sleep(0.5)
        return '192'


def donustur(hedef_uzanti, ffmpeg_yolu, cikti_klasor_adi="Cevrilen_Muzikler"):
    bitrate = kalite_sec()

    baslik_yazdir()

    mevcut_klasor = os.getcwd()
    cikti_klasoru = os.path.join(mevcut_klasor, cikti_klasor_adi)

    dosyalar = [f for f in os.listdir(mevcut_klasor) if f.lower().endswith(hedef_uzanti)]

    if not dosyalar:
        print(f"\n{t('dosya_bulunamadi', uzanti=hedef_uzanti)}")
        input(f"\n{t('enter_devam')}")
        return

    os.makedirs(cikti_klasoru, exist_ok=True)
    print(f"\n{t('klasor_olusturuldu', klasor=cikti_klasor_adi)}")
    print(f"{t('toplam_dosya_donusturulecek', toplam=len(dosyalar))}")
    print(f"{t('secilen_kalite_bilgi', bitrate=bitrate)}\n")
    print("-" * 64)

    basarili = 0
    basarisiz = 0
    atlanan = 0
    zaten_var = 0
    basarisiz_liste = []
    baslangic_genel = time.time()
    toplam = len(dosyalar)
    TIMEOUT_SANIYE = 120

    for i, dosya in enumerate(dosyalar, 1):
        girdi = os.path.join(mevcut_klasor, dosya)
        cikti = os.path.join(cikti_klasoru, dosya.rsplit('.', 1)[0] + ".mp3")

        dosya_gosterimi = dosya if len(dosya) <= 22 else dosya[:19] + "..."

        if os.path.exists(cikti) and os.path.getsize(cikti) > 0:
            zaten_var += 1
            yuzde = i / toplam
            bar_uzunluk = 15
            dolu = int(bar_uzunluk * yuzde)
            bar = '█' * dolu + '-' * (bar_uzunluk - dolu)
            gecen_sure = int(time.time() - baslangic_genel)
            dk, sn = divmod(gecen_sure, 60)
            sys.stdout.write(f"\r[{bar}] %{int(yuzde * 100):02d} | {t('sure_etiket')}: {dk:02d}:{sn:02d} | {t('durum_zaten_var')} : {dosya_gosterimi:<22}          \n")
            sys.stdout.flush()
            continue

        dosya_baslangic = time.time()
        timeout_oldu = False

        stderr_dosya = tempfile.NamedTemporaryFile(mode='w+b', delete=False, suffix='.log')

        try:
            islem = subprocess.Popen(
                [ffmpeg_yolu, "-y", "-i", girdi, "-b:a", f"{bitrate}k", cikti],
                stdout=subprocess.DEVNULL,
                stderr=stderr_dosya
            )

            while islem.poll() is None:
                gecen_sure = int(time.time() - baslangic_genel)
                dk, sn = divmod(gecen_sure, 60)

                dosya_gecen = int(time.time() - dosya_baslangic)
                ddk, dsn = divmod(dosya_gecen, 60)

                if dosya_gecen > TIMEOUT_SANIYE:
                    islem.kill()
                    timeout_oldu = True
                    break

                animasyon = ["|", "/", "-", "\\"][int(time.time() * 8) % 4]

                yuzde = (i - 1) / toplam
                bar_uzunluk = 15
                dolu = int(bar_uzunluk * yuzde)
                bar = '█' * dolu + '-' * (bar_uzunluk - dolu)

                sys.stdout.write(f"\r[{bar}] %{int(yuzde * 100):02d} | {t('sure_etiket')}: {dk:02d}:{sn:02d} | {animasyon} {t('durum_cevriliyor')}: {dosya_gosterimi:<22} ({ddk:02d}:{dsn:02d})")
                sys.stdout.flush()
                time.sleep(0.1)

            stderr_dosya.close()
            with open(stderr_dosya.name, 'rb') as f:
                stderr_cikti = f.read()

        except Exception as e:
            stderr_dosya.close()
            stderr_cikti = str(e).encode('utf-8')
            timeout_oldu = True
        finally:
            try:
                os.unlink(stderr_dosya.name)
            except OSError:
                pass

        yuzde = i / toplam
        dolu = int(bar_uzunluk * yuzde)
        bar = '█' * dolu + '-' * (bar_uzunluk - dolu)
        gecen_sure = int(time.time() - baslangic_genel)
        dk, sn = divmod(gecen_sure, 60)

        if timeout_oldu:
            atlanan += 1
            basarisiz_liste.append((dosya, f"Timeout ({TIMEOUT_SANIYE}s)"))
            sys.stdout.write(f"\r[{bar}] %{int(yuzde * 100):02d} | {t('sure_etiket')}: {dk:02d}:{sn:02d} | {t('durum_timeout')} : {dosya_gosterimi:<22}          \n")
            if os.path.exists(cikti):
                try:
                    os.remove(cikti)
                except OSError:
                    pass
        elif islem.returncode == 0:
            basarili += 1
            sys.stdout.write(f"\r[{bar}] %{int(yuzde * 100):02d} | {t('sure_etiket')}: {dk:02d}:{sn:02d} | {t('durum_bitti')} : {dosya_gosterimi:<22}          \n")
        else:
            basarisiz += 1
            hata_mesaji = _hata_mesaji_ayikla(stderr_cikti)
            basarisiz_liste.append((dosya, hata_mesaji))
            sys.stdout.write(f"\r[{bar}] %{int(yuzde * 100):02d} | {t('sure_etiket')}: {dk:02d}:{sn:02d} | {t('durum_hata')} : {dosya_gosterimi:<22}          \n")

        sys.stdout.flush()

    print("-" * 64)

    genel_dk, genel_sn = divmod(int(time.time() - baslangic_genel), 60)

    print(f"\n{'=' * 64}")
    print(f"                      {t('sonuc_raporu_baslik')}")
    print(f"{'=' * 64}")
    print(f"  {t('toplam_dosya')} : {toplam}")
    print(f"  {t('basarili')} : {basarili}")
    print(f"  {t('basarisiz')} : {basarisiz}")
    if zaten_var > 0:
        print(f"  {t('zaten_cevrilmis')} : {zaten_var}")
    if atlanan > 0:
        print(f"  {t('zaman_asimi')} : {atlanan}")
    print(f"  {t('kalite_etiket')} : {bitrate} kbps")
    print(f"  {t('toplam_sure_etiket')} : {genel_dk} {t('dakika')} {genel_sn} {t('saniye')}")
    print(f"  {t('cikti_klasoru_etiket')} : {cikti_klasor_adi}/")

    if basarisiz_liste:
        print(f"\n{'─' * 64}")
        print(f"  {t('basarisiz_liste_baslik')}")
        print(f"{'─' * 64}")
        for idx, (dosya_adi, hata) in enumerate(basarisiz_liste, 1):
            print(f"\n  {idx}. {dosya_adi}")
            print(f"     {t('neden_etiket')}: {hata}")

    print(f"{'=' * 64}")

    if basarisiz_liste:
        basarisiz_dosyalari_youtube_indir(
            basarisiz_liste, cikti_klasoru, bitrate, ffmpeg_yolu
        )
    else:
        input(f"\n{t('enter_menu')}")


def _hata_mesaji_ayikla(stderr_bytes):
    """FFmpeg stderr çıktısından anlamlı hata mesajını çıkarır."""
    if not stderr_bytes:
        return "Bilinmeyen hata / Unknown error"

    try:
        stderr_text = stderr_bytes.decode('utf-8', errors='replace')
    except Exception:
        return "Hata mesajı çözümlenemedi / Decode error"

    satirlar = stderr_text.strip().split('\n')
    hata_kaliplari = [
        "Invalid data found",
        "No such file or directory",
        "Permission denied",
        "could not find codec",
        "Decoder not found",
        "Error while decoding",
        "Invalid argument",
        "Protocol not found",
        "does not contain any stream",
        "Output file is empty",
        "Conversion failed",
        "corrupt",
        "moov atom not found",
    ]

    for satir in reversed(satirlar):
        satir_temiz = satir.strip()
        if not satir_temiz:
            continue
        for kalip in hata_kaliplari:
            if kalip.lower() in satir_temiz.lower():
                return satir_temiz

    for satir in reversed(satirlar):
        satir_temiz = satir.strip()
        if satir_temiz and not satir_temiz.startswith("frame="):
            if len(satir_temiz) > 120:
                return satir_temiz[:117] + "..."
            return satir_temiz

    return "Bilinmeyen hata / Unknown error"


def dil_secimi_menu():
    """Dil değiştirme menüsü."""
    baslik_yazdir()
    print(f"          {t('dil_menu_baslik')}")
    print("================================================================")
    print("  [1] Türkçe (Turkish)")
    print("  [2] English (İngilizce)")
    print("================================================================")
    secim = input(f"\n  {t('seciminiz')}: ").strip()
    if secim == '1':
        dil_kaydet('tr')
        print(f"\n  {t('dil_secilen_mesaj')}")
        time.sleep(1)
    elif secim == '2':
        dil_kaydet('en')
        print(f"\n  {t('dil_secilen_mesaj')}")
        time.sleep(1)


def ana_menu():
    dil_yukle()

    ffmpeg_yolu = ffmpeg_bul()

    if ffmpeg_yolu is None:
        ffmpeg_yolu = ffmpeg_indir()
        if ffmpeg_yolu is None:
            print("\n[HATA / ERROR] FFmpeg missing. Exiting.")
            time.sleep(2)
            return

    while True:
        baslik_yazdir()

        if ffmpeg_yolu == "ffmpeg":
            ffmpeg_durum = t('ffmpeg_hazir_global')
        else:
            ffmpeg_durum = t('ffmpeg_hazir_yerel')
        print(f" {t('ffmpeg_durum')} ({ffmpeg_durum})\n")

        print(f" {t('menu_secim')}\n")
        print(f" [1] {t('menu_m4a')}")
        print(f" [2] {t('menu_mp4')}")
        print(f" [3] {t('menu_wav')}")
        print(f" [L] {t('menu_dil')}")
        print(f" [0] {t('menu_cikis')}")
        print("\n================================================================")

        secim = input(f" {t('seciminiz')}: ").strip().lower()

        if secim == '1':
            donustur('.m4a', ffmpeg_yolu)
        elif secim == '2':
            donustur('.mp4', ffmpeg_yolu)
        elif secim == '3':
            donustur('.wav', ffmpeg_yolu)
        elif secim in ['l', 'L', '4']:
            dil_secimi_menu()
        elif secim == '0':
            print(f"\n{t('cikis_mesaj')}")
            time.sleep(1)
            break
        else:
            print(f"\n{t('gecersiz_secim')}")
            time.sleep(2)


if __name__ == "__main__":
    ana_menu()
