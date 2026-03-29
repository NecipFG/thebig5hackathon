# Ay Yüzeyi İçin Rota Optimizasyonu

**Ay'in guney kutbu bolgesinde otonom rover navigasyonu icin gelistirilmis, tarayici tabanli 3D rota planlama ve simulasyon platformu.**

A* pathfinding algoritmasi, gercek lunar toporafya verisi (GeoTIFF), LIDAR engel tespit simulasyonu ve Gemini AI destekli misyon planlama yeteneklerini tek bir arayuzde birlestiriyor.

---

## Ozellikler

### 3D Arazi Gorsellemesi
- Gercek Ay guney kutbu yukseklik verileri uzerinde dairesel 3D arazi modeli (~121 km cap)
- Uc farkli renk modu: **Yukseklik** (renkli toporafya), **Ay Modu** (siyah-beyaz), **Isik Haritasi** (slope overlay)
- Serbest orbit, 3. sahis ve 1. sahis kamera modlari
- Wall-E 3D rover modeli ile gercek zamanli rota animasyonu
- Uzay arka plani (prosedural yildiz alani)

### A* Pathfinding Algoritmasi
- **16-yonlu hareket**: 4 cardinal + 4 diagonal + 8 knight-move ile pururuzsuz rota olusturma
- **Egim cezasi**: `1 + (slope/10)^2` — dik yamaclarda eksponansiyel maliyet artisi
- **Kinematik donus kisitlamasi**: `1 + 0.5 x (aci/45)^2` — sert donuslere (>=90 derece) izin verilmez
- Ayarlanabilir parametreler: egim esigi, heuristic agirlik, arac hizi
- Gercek zamanli yuzey mesafe hesabi (yukseklik farklari dahil)

### LIDAR Simulasyonu
- **3 km menzilli** kirmizi lazer tarama cizgisi, yuzey takipli
- Haritaya tiklayarak engel yerlestirme (guvenlik zonlu)
- Engel tespit edildiginde **otomatik yeniden rotalama** (A* anlik yeniden hesaplama)
- Orijinal rota korunur, yeni rota turuncu renkte goruntulenir

### Bilimsel Waypoint Sistemi
- **8 akademik oneme sahip Ay guney kutbu noktasi**: Shackleton Ridge, De Gerlache, Amundsen-Ganswindt, Haworth-Shoemaker, Malapert Massif, Sverdrup Crater, Connecting Ridge, Leibniz Beta
- Rota yakinlik taramasi (ayarlanabilir yaricap)
- Opsiyonel waypoint ekleme — zorla yonlendirme yok, secim kullanicida
- Coklu waypoint seciminde greedy nearest-neighbor siralama ile multi-segment A*

### AI Asistan
- Rota analizi ve degerlendirme
- **Otonom kesfif senaryosu**: AI baslangic/bitis noktasi onerir, gidis + farkli guzergahtan donus rotasi cizdiriyor
- Akademik misyon raporu olusturma
- Dogal dilde soru-cevap
- Chat gecmisi ile baglamsal konusma

---

## Kurulum ve Calistirma

### Gereksinimler
- **Node.js** (v16+)
- Modern tarayici (Chrome / Edge / Firefox — WebGL destekli)

### Kurulum

```bash
git clone <repo-url>
cd "the big 5"
npm install
```

### Calistirma

```bash
node server.js
```

Tarayicida `http://localhost:8080` adresine gidin.

> **Not:** Build adimi veya bundler yoktur. Tum bagimliliklar CDN uzerinden tarayicida yuklenir.

---

## Kullanim Kilavuzu

### 1. Harita Yukleme
Sag paneldeki dropdown'dan bir TIF dosyasi secin:
- `ldem_87s_10mpp_circle_512.tif` — Yukseklik haritasi (1 MB, hizli yukleme)
- `ldem_87s_10mpp_circle.tif` — Yuksek cozunurluklu yukseklik (563 MB)

### 2. Rota Olusturma
- Haritada bir noktaya tiklayin → **baslangic** (yesil isaret)
- Ikinci noktaya tiklayin → **hedef** (kirmizi isaret)
- A* algoritmasi otomatik olarak en uygun rotayi hesaplar
- Wall-E rover modeli rota uzerinde animasyonlu olarak hareket eder

### 3. Isik Haritasi Overlay
- Sag panel → **Renk Modu** → **Isik Haritasi**
- Dropdown'dan `ldsm_87s_10mpp_circle_512.tif` secin
- 3D arazi slope verisine gore renklendirilir (inferno skalasi)

### 4. LIDAR Simulasyonu
- **Engel Yerlestir** butonuna basin (crosshair cursor aktif olur)
- Haritaya tiklayarak engel yerlestirin
- Rover ilerlerken kirmizi LIDAR lazeri onu tarar
- Engel tespit edildiginde rover otomatik olarak yeni rota hesaplar

### 5. Waypoint Sistemi
- Rota hesaplandiktan sonra yakin bilimsel noktalar listelenir
- Checkbox ile istediginiz waypoint'leri rotaya ekleyin
- Tarama yaricapini slider ile ayarlayin (5-60 km)

### 6. AI Asistan
- **Otonom Senaryo**: AI kesfif senaryosu olusturur ve otomatik uygular
- **Misyon Raporu**: Mevcut rotanin akademik ozeti
- **Rota Analizi**: Detayli risk ve performans degerlendirmesi
- Serbest metin ile soru sorun veya komut verin

### Kontroller
| Eylem | Kontrol |
|-------|---------|
| Nokta sec | Sol tik |
| Kamerayi dondur | Sag tik + surukle |
| Yakinlastir/Uzaklastir | Scroll |
| Kamerayi kaydir | Orta tik + surukle |

---

## Teknik Mimari

### Teknoloji Yigini
- **Three.js r128** — 3D render (legacy non-module build)
- **GeoTIFF.js v2.1.3** — Tarayicida GeoTIFF parse
- **Gemini 2.0 Flash API** — AI asistan
- **Node.js** — Statik dosya sunucu (saf, express bagimliligi yok)

### Proje Yapisi
```
the big 5/
├── app.html              # Ana uygulama (tek sayfa, inline JS)
├── server.js             # Node.js statik sunucu + API
├── crop_circle.js        # Elevation TIF dairesel kesim scripti
├── crop_slope.js         # Slope TIF dairesel kesim scripti
├── Site01/               # GeoTIFF veri dosyalari
│   ├── ldem_87s_*        # Lunar DEM (yukseklik)
│   └── ldsm_87s_*        # Lunar DSM (egim/slope)
├── Assets/
│   └── WALLE.glb         # Wall-E 3D rover modeli
└── person2/
    └── lunar_pathfinder.py  # Python A* referans implementasyonu
```

### Harita Parametreleri
| Parametre | Deger |
|-----------|-------|
| Kapsam | Ay Guney Kutbu (87°S - 90°S) |
| Cap | ~121.4 km (yaricap 60.7 km) |
| Orijinal cozunurluk | 5 m/piksel |
| Kullanilan cozunurluk | 10 m/piksel (crop sonrasi) |
| 3D grid boyutu | 505 x 505 piksel |
| Projeksiyon | Polar Stereographic |

### A* Maliyet Formulu
```
maliyet = mesafe x egim_cezasi x donus_cezasi

egim_cezasi  = 1 + (slope / 10)^2
donus_cezasi = 1 + 0.5 x (aci / 45)^2
sert_donus   = >= 90° → YASAK
```

---

## Veri Onisleme

Orijinal NASA LDEM/LDSM dosyalari (~4-5 GB) cok buyuk oldugu icin dairesel kesim ve downsampling uygulanir:

```bash
# Yukseklik haritasi kesimi (5mpp → 10mpp, yaricap 60.7km)
node --max-old-space-size=4096 crop_circle.js

# Egim haritasi kesimi (ayni parametreler)
node --max-old-space-size=4096 crop_slope.js
```

Cikti dosyalari `Site01/` klasorune kaydedilir.

---

## Bilimsel Waypoint'ler

| Nokta | Koordinat | Bilimsel Onemi |
|-------|-----------|----------------|
| Shackleton Ridge | 89.6°S, 212.5°E | Kalici gunesli sirt, enerji istasyonu adayi |
| De Gerlache Mnts | 88.7°S, 40.0°W | Yuksek toporafya, radar gozlem noktasi |
| Amundsen-Ganswindt | 88.7°S, 105.0°E | Derin krater, buzul analiz sahasi |
| Haworth-Shoemaker | 88.6°S, 20.0°E | Kalici golge krateri, su buzu potansiyeli |
| Malapert Massif | 88.5°S, 0.0°E | Dunya goruslu iletisim tepesi |
| Sverdrup Crater | 88.5°S, 155.0°W | Golge krateri, volatil madde arastirmasi |
| Connecting Ridge | 89.4°S, 201.0°E | Shackleton baglanti sirt gecidi |
| Leibniz Beta | 88.2°S, 330.0°E | Yuksek plato, jeolojik ornekleme sahasi |

---

## Lisans

Bu proje akademik arastirma amaciyla gelistirilmistir.

Lunar toporafya verileri: **NASA Lunar Reconnaissance Orbiter (LRO) — LOLA/LDEM**
