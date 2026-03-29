# DM1 Ay Istasyonu — Devir Teslim Dokumani
**Tarih:** 2026-03-29
**Proje:** Ay guney kutbu otonom rover rota planlama sistemi
**Calisan dizin:** `c:\Metehan\projeler\1071\the big 5`

---

## 1. PROJENIN AMACI

Ay'in guney kutbu bolgesinde (87°-90° guney enlemi) otonom bir rover icin **3D gorsel rota planlama araci**. Kullanici 3D harita uzerinde baslangic/bitis noktasi secer, A* pathfinding algoritmasi en uygun rotayi hesaplar, Wall-E 3D modeli rotayi canlandirir. Bilimsel waypoint'ler opsiyonel olarak rotaya eklenebilir. Gemini AI asistan rota analizi ve otonom senaryo uretimi yapar.

---

## 2. DOSYA YAPISI VE ROLLER

### Ana Uygulama (aktif)
| Dosya | Satir | Rol |
|-------|-------|-----|
| `app.html` | ~1800 | **ANA DOSYA.** Tek sayfa uygulama: 3D viewer + A* pathfinder + Gemini AI + UI. Tum JS inline. |
| `server.js` | 67 | Node.js statik dosya sunucu. Range request + `/api/tif-list` endpoint. |

### Veri Isleme Scriptleri
| Dosya | Rol |
|-------|-----|
| `crop_circle.js` | ldem (elevation) TIF'i dairesel keser. 5mpp → 10mpp, yaricap 60.7km |
| `crop_slope.js` | ldsm (slope) TIF'i ayni parametrelerle dairesel keser |

### Veri Dosyalari (`Site01/`)
| Dosya | Boyut | Aciklama |
|-------|-------|----------|
| `ldem_87s_5mpp.tif` | 3.3 GB | Orijinal elevation (yukseklik) haritasi, 40000x40000 px, 5m/px |
| `ldsm_87s_5mpp.tif` | 4.9 GB | Orijinal slope (egim) haritasi, ayni boyut |
| **`ldem_87s_10mpp_circle.tif`** | 563 MB | **AKTIF KULLANILAN.** Dairesel crop, 12140x12140 px, 10m/px, ~121km cap |
| **`ldsm_87s_10mpp_circle.tif`** | 563 MB | **ISIK HARITASI OVERLAY.** Slope verisi, ayni boyut/kesim |
| `ldem_87s_15mpp_circle.tif` | 63 MB | Eski dusuk cozunurluklu crop (artik kullanilmiyor) |
| Diger `Site01_*.tif` dosyalari | 40 MB | Kucuk bolge TIF'leri (Site01 spesifik) |

### Eski/Arsiv Dosyalar
| Dosya | Not |
|-------|-----|
| `3d_V1.1.html` — `3d_V1.4.html` | Onceki iterasyonlar. V1.4 son bağımsız surum. `app.html` bunlarin uzerine insa edildi. |
| `3d-viewer.html`, `index.html` | Eski bagimsiz viewer'lar (CesiumJS vb) |
| `person2/lunar_pathfinder.py` | Python Streamlit uygulamasi — A* algoritmasi buradan JS'ye port edildi |
| `person2/lunar_engine.py` | **EKSIK DOSYA** — `lunar_pathfinder.py` bunu import eder ama dosya repoda yok. Kullanicida mevcut. |

### Assets
| Dosya | Rol |
|-------|-----|
| `Assets/WALLE.glb` | 21 MB — Wall-E 3D modeli (GLTF Binary). Draco/Meshopt YOK. |
| `Assets/wallpaper.webp` | Eski arka plan (artik kullanilmiyor, yildiz sistemi var) |

---

## 3. CALISTIRMA

```bash
cd "c:\Metehan\projeler\1071\the big 5"
node server.js
# http://localhost:8080 → app.html otomatik sunulur
```

Build yok, bundler yok, npm install sadece `geotiff` paketi icin (crop scriptleri). Tarayici CDN'lerden yukler:
- Three.js r128 (legacy non-module)
- GeoTIFF.js v2.1.3
- GLTFLoader, OrbitControls (Three.js examples)

---

## 4. APP.HTML MIMARI DETAYI

### 4.1 Layout (3 sutun)
```
┌──────────────┬──────────────────────────┬─────────────────┐
│  SOL (280px) │   ORTA (flex)            │  SAG (310px)    │
│  Gemini AI   │   3D Viewer (Three.js)   │  Kontrol Paneli │
│  Chat        │   Canvas + Overlays      │  Parametreler   │
│  Butonlar    │                          │  Sonuclar       │
│  Text input  │                          │  Waypoints      │
└──────────────┴──────────────────────────┴─────────────────┘
```

### 4.2 Onemli Global Degiskenler
```javascript
// Terrain
gridElevData    // Float32Array — 3D mesh yukseklik verisi (heightScale ile olceklenmis)
rawElevGrid     // Float32Array — metre cinsinden ham yukseklik (A* icin)
slopeGrid       // Float32Array — derece cinsinden egim (A* icin, elevation verisinden turetilir)
gridW, gridH    // Grid boyutu (max 512x512, downsample sonrasi)
heightScale     // Y ekseni abartma katsayisi: (terrainSize * 0.3) / elevationRange
meterPerUnit    // 1 grid birim = kac metre. PIXEL_SIZE(10) * downsample_step
gridLiftOffset  // 50 — terrain min Y=50'de, taban Y=0'da

// Overlay
lightMapData    // Float32Array — isik/slope overlay verisi (ayni grid boyutu)
colorMode       // 'elevation' | 'bw' | 'light'

// Waypoints
LUNAR_WAYPOINTS       // 8 bilimsel nokta (lat/lon)
waypointGridPositions // grid koordinatlarina donusturulmus waypoint'ler
selectedWaypoints     // Set — secili waypoint id'leri

// Pathfinding
lastPathResult  // Son hesaplanan A* yolu [[row,col], ...]
```

### 4.3 Temel Fonksiyonlar

**GeoTIFF Yukleme:**
- `loadTIF(file, url)` — Blob veya URL'den TIF yukler. Buyuk dosyalar icin serit-serit okuma. Max 512x512 grid'e downsample.
- `fromUrl()` kullanir (HTTP range request ile hizli), `fromBlob()` fallback.

**Terrain Builder:**
- `buildSolidTerrain(data, w, h, step)` — Dairesel 3D mesh olusturur:
  - Ust yuzey: PlaneBufferGeometry, daire disindaki ucgenler index'ten cikarilir
  - Alt yuzey: CircleBufferGeometry (duz taban)
  - Yan duvar: 256 segmentli silindirik duvar
  - Kenar alpha fade (%8 band)
  - `slopeGrid` otomatik turetilir (central difference)

**Renk Modlari:**
- `elevationColor(t, gridIdx)` — t: normalize yukseklik, gridIdx: light map icin
- `setColorMode(mode)` — 'elevation' (renkli), 'bw' (ay gorunumu), 'light' (overlay TIF)
- `loadLightTIF(url)` — Ikinci TIF'i yukler, `lightMapData`'ya yazar, grid'e downsample eder
- `lightColor(gridIdx)` — Inferno-benzeri renk skalasi

**A* Pathfinding (JS Port):**
```
Maliyet = mesafe × egim_cezasi × donus_cezasi

egim_cezasi = 1 + (slope/10)²
donus_cezasi = 1 + 0.5 × (aci/45)²
>=90° donus = YASAK (Infinity)
```
- `astarSearch(startR, startC, goalR, goalC)` — 16-yonlu A* (4 cardinal + 4 diagonal + 8 knight)
- MinHeap sinifi ile optimize edilmis priority queue
- State: `(row, col, direction_row, direction_col)` — kinematik gecmis
- Parametreler UI slider'dan alinir: `slopeThreshold`, `heuristicWeight`, `vehicleSpeed`
- Daire disi pikseller otomatik engellenir

**Waypoint Sistemi:**
- `latLonToGrid(lat, lon)` — Polar stereographic projeksiyon ile lat/lon → grid
- `placeWaypointMarkers()` — 8 bilimsel noktayi 3D sahnede mor diamond marker olarak yerlestirir
- `checkNearbyWaypoints(path)` — Rota hesaplandiktan sonra yaricap icindeki waypoint'leri tespit eder
- `toggleWaypoint(id)` → `recomputeRouteWithWaypoints()` — Secili waypoint'ler uzerinden multi-segment A*
- Waypoint siralama: Greedy nearest-neighbor

**Wall-E Animasyon:**
- `preloadWallE()` — Sayfa yuklendiginde GLB'yi onbellegeler. Basarisiz olursa retry, sonra fallback kutu.
- `applyWalleScale()` — Slider degerine gore boyut ayarlar
- `spawnVehicle()` — CatmullRomCurve3 uzerinde animasyon
- 3 kamera modu: Serbest, 3. sahis (arkadan takip), 1. sahis (icerideki)

**Mesafe Hesabi:**
```javascript
// XZ: grid birim × meterPerUnit → metre
// Y: scene Y / heightScale → gercek metre farki
dx = deltaX * meterPerUnit
dz = deltaZ * meterPerUnit
dy = deltaY / heightScale  // abartilmis Y'yi gercek metreye cevir
mesafe = sqrt(dx² + dy² + dz²)
```

**Gemini AI Entegrasyonu:**
- `callGemini(message, systemExtra)` — Gemini 2.0 Flash API
- API Key: `app.html` icinde hardcoded (satir ~1489)
- Rate limit (429) icin 5sn bekle + retry mekanizmasi
- `geminiAutoScenario()` — AI otonom kesfif senaryosu oneriri. JSON formatinda koordinat dondurur, otomatik rota cizirir + farkli guzergahtan donus rotasi (turuncu)
- `geminiMissionReport()` — Akademik misyon raporu
- `geminiCompare()` — Detayli rota analizi
- `processGeminiCommands(response)` — AI yanitindaki JSON'u parse edip otomatik rota cizdirme
- `getRouteContext()` — Mevcut durum bilgisini Gemini'ye context olarak gonderir
- Chat gecmisi son 20 mesajda tutulur (10'a kirpilir)
- Otomatik analiz DEVRE DISI — kullanici butonla tetikler (rate limit korumasi)

**Donus Rotasi:**
- `drawReturnRoute(path)` — Turuncu renkte ikinci rota cizer
- `clearReturnRoute()` — Temizler
- Gemini otonom senaryosu gidis + farkli donus koordinati verir

### 4.4 Server.js Detay
- Saf Node.js (express/dependency yok)
- Port 8080, varsayilan sayfa `app.html`
- HTTP Range Request destegi (206 Partial Content) — buyuk TIF'ler icin kritik
- `/api/tif-list` — `Site01/` klasorundeki TIF dosyalarini JSON olarak dondurur

---

## 5. BILINEN SORUNLAR VE EKSIKLER

### Aktif Sorunlar
1. **Gemini rate limit** — Sik istek atildiginda 429 hatasi. 5sn retry var ama ard arda kullanildiginda yine tikanabilir.
2. **Waypoint koordinat dogrulugu** — `latLonToGrid` polar stereographic projeksiyonu basitlestirilmis. Bazi waypoint'ler harita disina dusebilir.
3. **person2/lunar_engine.py eksik** — Python Streamlit uygulamasi bagimsiz calismiyor. JS portu `app.html`'de zaten mevcut.

### Yapilmamis / Gelecek Ozellikler
1. **Gunes haritasi (solar exposure)** entegrasyonu — person2'de `South_Sun.tiff` referansi var ama dosya mevcut degil. A* maliyet formulune `sun_multiplier` eklenebilir (kod person2'de var, JS'ye port edilmedi).
2. **Waypoint detaylandirma** — Gemini'nin donus rotasi onerisiyle ilk adim atildi ama waypoint ziyaret sirasi optimizasyonu (TSP) yok.
3. **Export ozellikleri** — GeoTIFF export (person2'deki gibi gorsel rota + maske export)
4. **Dogal dil komutlari** — "Egim esigini 25 yap" gibi komutlarin UI'yi guncellemesi planlanmisti.
5. **Gercek rover boyut kalibrasyonu** — Slider var ama gercek rover olculerine gore kalibrasyon yapilmadi.

---

## 6. KRITIK TEKNIK DETAYLAR

### Harita Boyutlari
- Dairesel kesim: **yaricap 60.7 km, cap ~121.4 km**
- Orijinal kaynak: 40000x40000 px, 5m/px (200x200 km kare)
- Crop sonucu: 12140x12140 px, 10m/px
- 3D mesh: max 512x512 grid'e downsample edilir (step hesaplanir)
- `meterPerUnit = step * PIXEL_SIZE(10)` — 1 grid birim kac metreye karsilik gelir

### Koordinat Sistemi
```
Grid: (row, col) — sol ust kose (0,0)
World: (x, y, z) — merkez (0, 0, 0)
  x = col - gridW/2    (yatay)
  z = row - gridH/2    (derinlik)
  y = elevation         (yukseklik, heightScale ile abartilmis)
Metre: world × meterPerUnit (XZ), world / heightScale (Y)
```

### Elevation → Slope Turetimi
`buildSolidTerrain` icinde, `rawElevGrid`'den central difference ile hesaplanir:
```javascript
dEdx = (elev[ix+1] - elev[ix-1]) / (2 * meterPerUnit)
dEdz = (elev[iy+1] - elev[iy-1]) / (2 * meterPerUnit)
slope_degrees = atan(sqrt(dEdx² + dEdz²)) × 180/π
```

### Three.js Versiyonu
**r128 (legacy)** — CDN non-module build. `THREE.PlaneBufferGeometry`, `THREE.GLTFLoader` vb. legacy API kullanilir. Yeni Three.js'e gecis yapilacaksa import yapisini degistirmek gerekir.

---

## 7. PERSON2 A* ALGORITMASI (PYTHON REFERANS)

`person2/lunar_pathfinder.py` — Streamlit uygulamasi. JS portu icin referans kaynak.

**JS'ye port EDILEN ozellikler:**
- 16-yonlu A* arama (DIRECTIONS sabiti)
- Egim maliyet fonksiyonu: `1 + (slope/10)²`
- Donus cezasi: `1 + 0.5 × (angle/45)²`, >=90° yasak
- Heuristic: Euclidean distance × weight
- State: (row, col, in_dr, in_dc) — kinematik gecmis

**JS'ye port EDILMEYEN ozellikler:**
- `get_sun_multiplier()` — Gunes/sicaklik cezasi: `3.0 - 2.0 × norm`
- `export_route_mask_to_tif()` — GeoTIFF maske export
- `export_visual_map_to_tif()` — GeoTIFF gorsel export
- `load_aligned_maps()` — Geospatial eslestirme (rasterio)

**Eksik dependency:** `lunar_engine.py` — DIRECTIONS, astar_search, export fonksiyonlari burada. Dosya kullanicida mevcut ama repoda yok.

---

## 8. OTURUM KRONOLOJISI

1. Wall-E GLB modeli entegrasyonu (3d_V1.4.html)
2. Buyuk TIF yukleme hatasi cozumu (fromBlob + serit okuma)
3. Server.js range request destegi
4. Dairesel terrain render (kare → daire gecisi)
5. Dairesel grid helper, mavi kare artefact temizligi
6. Wall-E model yukleme retry mekanizmasi
7. Uzay arka plani (yildiz sistemi)
8. `crop_circle.js` — 3.3GB elevation TIF'i dairesel kesim (yaricap 60.7km, 10mpp)
9. `crop_slope.js` — 4.9GB slope TIF'i ayni parametrelerle kesim
10. **app.html olusturma** — 3 panelli birlesiK arayuz:
    - Sol: Gemini AI chat
    - Orta: 3D terrain viewer
    - Sag: kontrol paneli + A* parametreleri + sonuclar
11. A* pathfinding JS'ye port edildi (person2'den)
12. Waypoint sistemi (8 bilimsel nokta, proximity tarama, opsiyonel rota ekleme)
13. Gemini API entegrasyonu (rota analizi, otonom senaryo, misyon raporu)
14. Donus rotasi sistemi (farkli guzergah, turuncu renk)
15. Mesafe hesabi duzeltmesi (PIXEL_SIZE=10, heightScale kompanzasyonu)
16. Isik haritasi overlay (ikinci TIF ile renk giydirme, 3 renk modu)
17. API key guncelleme, rate limit korumasi

---

## 9. HIZLI BASLANGIÇ (YENI ASISTAN ICIN)

```bash
# 1. Sunucuyu baslat
cd "c:\Metehan\projeler\1071\the big 5"
node server.js

# 2. Tarayicida ac
http://localhost:8080

# 3. Haritayi yukle
# Sag panel → dropdown → ldem_87s_10mpp_circle.tif sec

# 4. Rota planla
# 3D haritada iki nokta tikla → A* otomatik calisir

# 5. Isik haritasi (opsiyonel)
# Sag panel → Renk Modu → Isik Haritasi → ldsm_87s_10mpp_circle.tif sec
```

### Kodda degisiklik yapilacaksa:
- **Ana dosya:** `app.html` — butun JS inline, ~1800 satir
- **Sunucu:** `server.js` — 67 satir, basit
- Degisiklikten sonra tarayicida `Ctrl+Shift+R` (hard refresh)
- JS syntax kontrolu: `node -e "new Function(require('fs').readFileSync('app.html','utf8').match(/<script>([\s\S]*)<\/script>/)[1])"`

### Gemini API Key
Dosyada hardcoded: `app.html` satir ~1489. Degistirmek icin `GEMINI_KEY` ara.
Model: `gemini-2.0-flash`

---

## 10. ONEMLI UYARILAR

1. **Three.js r128 LEGACY** — Modern Three.js API'leri (ES modules, BufferGeometry) KULLANMA. `PlaneBufferGeometry`, `THREE.GLTFLoader` gibi eski API'ler kullaniliyor.
2. **Buyuk dosyalar** — 3.3GB+ TIF'ler `fromUrl` + range request ile okunmali. `fromBlob` + `arrayBuffer()` tarayiciyi cokertiyor.
3. **PIXEL_SIZE = 10** — Crop sonucu dosyalar 10m/piksel. Orijinaller 5m/piksel. Karistirma.
4. **heightScale** — Y ekseni gorsel abartma icin olceklenmis. Mesafe hesabinda `/ heightScale` ile gercek metreye donusturulmeli.
5. **Dairesel harita** — Daire disindaki pikseller sifir. A* ve min/max hesaplarinda `v === 0` kontrol ediliyor.
6. **Gemini otomatik analiz KAPALI** — Rate limit sorunu nedeniyle devre disi birakildi. Kullanici butonla tetikler.
