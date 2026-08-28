# 🎵 Music Converter PRO

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Executable](https://img.shields.io/badge/executable-Standalone%20EXE-orange.svg)
![Language](https://img.shields.io/badge/language-Türkçe%20%7C%20English-brightgreen.svg)

**Music Converter PRO**, M4A, MP4 (video) ve WAV dosyalarını yüksek kaliteli MP3 formatına toplu dönüştüren, FFmpeg veya yt-dlp kurulumu gerektirmeyen, Türkçe ve İngilizce dil destekli portatif bir konsol uygulamasıdır.

---

## 🌟 Öne Çıkan Özellikler (Key Features)

- 🎚️ **Kalite (Bitrate) Seçim Menüsü**: 128, 192, 256 ve 320 kbps ses kalitesi seçenekleri.
- 🚀 **Otomatik FFmpeg & yt-dlp Kurulumu**: Kullanıcının sisteminde FFmpeg veya yt-dlp olmasa bile internetten otomatik indirip `ffmpeg_bin/` ve `yt-dlp_bin/` klasörlerine kurar. PATH ayarı gerektirmez!
- 🔄 **Akıllı Çeviri Kontrolü**: `Cevrilen_Muzikler/` klasöründe zaten bulunan dosyaları tespit edip atlar, gereksiz işlem yapmaz.
- ⏱️ **Kilitlenme Önleyici (Deadlock Fix & Timeout)**: 120 saniye içinde yanıt vermeyen bozuk dosyaları kilitlenmeden otomatik iptal eder ve sonraki dosyaya geçer.
- 🔍 **Başarısız Dosyalar İçin YouTube İndirici**: Dönüştürülemeyen bozuk veya desteklenmeyen dosyaları YouTube'da aratır, sonuçları listeler ve kullanıcının seçtiği kaliteli MP3 sürümünü otomatik indirir.
- 🌐 **Türkçe & İngilizce Dil Desteği (i18n)**: İstediğiniz an diller arasında geçiş yapabilirsiniz. Seçiminiz `ayarlar.json` dosyasında saklanır.
- 📦 **Tek EXE Portatif Dağıtım**: PyInstaller ile derlenmiş ~8.5MB tek dosya. Python veya kütüphane kurulumu gerektirmez.

---

## 🖥️ Ekran Görüntüleri (Console UI)

### 📌 Ana Menü / Main Menu
```
================================================================
          OTOMATİK SES DÖNÜŞTÜRÜCÜ PRO               
================================================================
 Bulunulan Klasör: C:\Muziklerim
================================================================

 FFmpeg: ✓ Hazır (Yerel kurulum (ffmpeg_bin/))

 Lütfen yapmak istediğiniz işlemi seçin:

 [1] M4A'dan MP3'e Çevir
 [2] MP4'ten (Videodan) MP3'e Çevir
 [3] WAV'dan MP3'e Çevir
 [L] Dil Seçimi / Language (TR / EN)
 [0] Çıkış
================================================================
```

### 📊 Dönüşüm Süreci & Sonuç Raporu
```
[███████████████] %100 | Süre: 00:14 | ✓ Bitti     : sarki_01.m4a
[███████████████] %100 | Süre: 00:15 | ○ Zaten var : sarki_02.m4a
----------------------------------------------------------------

================================================================
                      SONUÇ RAPORU
================================================================
  Toplam dosya     : 5
  ✓ Başarılı       : 4
  ✗ Başarısız      : 0
  ○ Zaten çevrilmiş: 1
  Kalite           : 320 kbps
  Toplam süre      : 0 dakika 15 saniye
  Çıktı klasörü    : Cevrilen_Muzikler/
================================================================
```

---

## 🚀 Kullanım (Usage)

### Yöntem 1: Hazır EXE Dosyası ile (Önerilen)

1. `Music_Converter.exe` dosyasını dönüştürmek istediğiniz müziklerin yer aldığı klasöre atın.
2. `Music_Converter.exe` dosyasına çift tıklayarak çalıştırın.
3. Çevrilen MP3'ler otomatik olarak `Cevrilen_Muzikler/` klasörüne kaydedilecektir.

---

### Yöntem 2: Python Kodları ile Çalıştırma

Gereksinimler: Python 3.10+ (Standart kütüphaneler dışında ek bağımlılık gerekmez).

```bash
# Repoyu klonlayın
git clone https://github.com/KULLANICI_ADI/Music_Converter.git
cd Music_Converter

# Scripti çalıştırın
python Music_Converter.py
```

---

## 🛠️ EXE Derleme (Build Executable)

Projeyi kendiniz tek bir EXE dosyasına dönüştürmek isterseniz `PyInstaller` kullanabilirsiniz:

```bash
pip install pyinstaller

python -m PyInstaller --onefile --console --name "Music_Converter" --noconfirm Music_Converter.py
```

Derlenen `Music_Converter.exe` dosyası `dist/` klasörü içerisinde oluşacaktır.

---

## 📁 Proje Yapısı (Project Structure)

```
Music_Converter/
│
├── Music_Converter.py        # Ana Python kaynak kodu
├── README.md                 # Proje dokümantasyonu
├── ayarlar.json              # Dil tercihi ayar dosyası (otomatik oluşur)
│
├── ffmpeg_bin/               # Otomatik indirilen FFmpeg bağımlılığı (otomatik oluşur)
├── yt-dlp_bin/               # Otomatik indirilen yt-dlp bağımlılığı (otomatik oluşur)
└── Cevrilen_Muzikler/        # Çıktı MP3 klasörü (otomatik oluşur)
```

---

## 📄 Lisans (License)

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır. Dilediğiniz gibi geliştirebilir, özelleştirebilir ve kullanabilirsiniz.
