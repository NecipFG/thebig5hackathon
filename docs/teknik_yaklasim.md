# Teknik Yaklaşım: Çok Kriterli A* ile Otonom Rota Planlama

## 1. Problem Tanımı

Bir ızgara haritası üzerinde, başlangıç noktasından hedef noktasına giden **güvenli ve optimal** rotayı bulmak istiyoruz. "Optimal" burada yalnızca mesafeyi değil; eğim maliyetini, enerji maliyetini ve araç kinematik kısıtlarını aynı anda minimize etmek anlamına gelir.

### Girdi
- **DEM (Yükseklik Haritası):** R×C boyutunda piksel ızgarası, her piksel metre cinsinden yükseklik değeri tutar.
- **Aydınlanma Haritası:** Aynı boyutta; piksel başına enerji elde edilebilirliği.
- **Başlangıç ve Hedef:** `(satır, sütun)` çifti.

### Çıktı
- Waypoint dizisi olarak rota: `[(r₀,c₀), (r₁,c₁), ..., (rₙ,cₙ)]`
- Metrikler: toplam mesafe, adım sayısı, maksimum eğim, ortalama eğim.

---

## 2. Arazi Ön İşleme

### 2.1 Koordinat Dönüşümü
Coğrafi koordinatlar (enlem/boylam °) piksel indekslerine `Affine` dönüşüm matrisiyle çevrilir:

```
row = (lat − origin_lat) / pixel_size_lat
col = (lon − origin_lon) / pixel_size_lon
```

Tüm arama süreci `(row, col)` ızgarası üzerinde yürütülür; coğrafi dönüşüm yalnızca giriş/çıkış aşamasında devreye girer.

### 2.2 Eğim Hesabı
Her pikselde yüzey eğimi `numpy.gradient()` ile merkez fark yöntemiyle hesaplanır:

```python
dz_dy, dz_dx = np.gradient(elevation_m, pixel_size_m)
slope_deg = np.degrees(np.arctan(np.sqrt(dz_dx**2 + dz_dy**2)))
```

### 2.3 Engel Maskesi
Eğim haritasından ikili engel maskesi üretilir:

```
slope ≤ 20°  →  geçilebilir (0)
slope > 20°  →  engel       (1)
```

Bu maske A\* algoritmasına doğrudan beslenir; ancak eğim maliyeti yalnızca bu ikili kararla sınırlı değildir (bkz. Bölüm 3.3a).

---

## 3. Algoritma: Kinematik Farkındalıklı A*

### 3.1 Durum Uzayı

Standart A\*'da durum yalnızca `(satır, sütun)`'dur. Bu implementasyonda duruma **gelen yön** eklenir:

```
durum = (satır, sütun, yön_indeksi)
```

Bu genişletme iki şeyi sağlar:
1. Dönüş maliyeti hesaplanabilir (önceki yön ile sonraki yön arasındaki açı).
2. Belirli dönüş açıları (≥90°) tamamen engellenebilir — araç kinematik kısıtı olarak.

### 3.2 Hareket Seti
22 hareket yönü tanımlanmıştır:
- **16 standart yön** — 8 ana + 8 ara yön
- **6 atlama hareketi** — knight-move benzeri (~26.5° ve ~63.4° açılar)

Atlama hareketleri, 8-yönlü ızgarada görülen "merdiven basamağı" yapaylığını azaltır ve yol kalitesini artırır.

### 3.3 Kenar Maliyet Fonksiyonu

```
maliyet(u → v) = mesafe_m × eğim_çarpanı(v) × dönüş_çarpanı(u,v) × enerji_çarpanı(v)
```

#### a) Eğim Çarpanı — Sürekli Ceza
```python
def slope_multiplier(slope_deg):
    if slope_deg > 20:
        return float('inf')           # sert engel
    return 1.0 + (slope_deg / 10.0) ** 2
```
Eşik altında parabol şeklinde artan maliyet: 10°'de 2.0×, 20°'de 5.0×. Sert ikili engelden farklı olarak algoritma, hafif eğimli yolları tercih etmeye yönlendirilir.

#### b) Dönüş Çarpanı — Kinematik Modelleme
```python
def turn_multiplier(prev_dir, next_dir):
    angle = abs(angle_between(prev_dir, next_dir))
    if angle >= 90:
        return float('inf')           # tank dönüşü yasak
    return 1.0 + 0.5 * (angle / 45.0) ** 2
```
45°'de 1.5×, 89°'de ~2.97×. Araç düz gitmeyi tercih eder; keskin dönüşler pahalıdır; geri dönüş imkânsızdır.

#### c) Enerji Çarpanı — Kaynak Yönetimi
```python
def energy_multiplier(illumination, val_min, val_max):
    norm = (illumination - val_min) / (val_max - val_min)
    return 3.0 - 2.0 * norm    # düşük enerji=3.0×, yüksek enerji=1.0×
```
Düşük aydınlanmalı (enerji fakiri) bölgeler 3 kat daha pahalıdır. Algoritma bu bölgelerden kaçınmayı otomatik olarak öğrenir.

### 3.4 Sezgisel Fonksiyon

Admissible (kabul edilebilir) sezgisel olarak düz-çizgi Öklid mesafesi kullanılır:

```python
h(n) = sqrt((n.row − goal.row)² + (n.col − goal.col)²) × pixel_size_m
```

Maliyet çarpanları uygulanmaz — bu A\*'ın optimallik garantisini korur.

### 3.5 Veri Yapısı

- **Açık set:** `heapq` min-heap; `(f, g, durum)` tuple'larını saklar.
- **Kapalı set:** `dict` — `{durum: (g_maliyeti, önceki_durum)}` yapısıyla hem ziyaret kontrolü hem de yol geri izlemesi sağlanır.

---

## 4. Bağımsız Doğrulama

A\* çıktısı ayrı bir modül tarafından sertifikalandırılır. Bu modül A\*'dan bağımsız olarak eğim haritasını yeniden hesaplar ve rotayı piksel piksel denetler:

| Metrik | Hesaplama |
|--------|-----------|
| Tehlikeli hücre sayısı | `sum(slope[r,c] > 20 for r,c in path)` |
| Yol uzunluğu (m) | Ardışık piksel çiftleri arası Öklid toplamı |
| Maksimum eğim (°) | `max(slope[r,c] for r,c in path)` |
| Ortalama eğim (°) | `mean(slope[r,c] for r,c in path)` |
| Karar | `tehlikeli_hücre == 0` → **PASS** |

Sonuçlar `mission{N}_result.json` ve `mission{N}_report.png` olarak dışa aktarılır.

---

## 5. Görselleştirme

Algoritma çıktısı Three.js tabanlı 3D görüntüleyicide sunulur:

- GeoTIFF, istemci tarafında **GeoTIFF.js** ile çözümlenir.
- Yükseklik verisi max 512×512 çözünürlüğe indirilir; her piksel Three.js `PlaneGeometry` tepe noktasına dönüşür.
- Araç modeli, A\*'ın ürettiği waypoint dizisi boyunca bilineer interpolasyonla yüzeye yapışarak animasyona girer.
- Kamera modları: serbest orbit, 3. şahıs takip, 1. şahıs.

---

## 6. Sistem Entegrasyon Akışı

```
DEM (GeoTIFF)
    │
    ▼
[Ön İşleme]  →  eğim haritası + engel maskesi + koordinat dönüşümü
    │
    ▼
[A* Arama]   →  mission{N}_path.json  (waypoint dizisi + metrikler)
    │
    ▼
[Doğrulama]  →  mission{N}_result.json + mission{N}_report.png
    │
    ▼
[3D Demo]    →  http://localhost:8080
```

---

## 7. Kompleksite

| Bileşen | Kompleksite |
|---------|-------------|
| Eğim hesabı | O(R × C) |
| A* durum uzayı | O(R × C × D), D = 22 yön |
| Yol doğrulama | O(\|yol\|) |
| Mesh üretimi | O(W × H), maks. 512² |

Tipik ızgara boyutu ~1000×1000 piksel; A\* saniyeler içinde tamamlanır.

---

*Bu belge TUA Astro Hackathon 2026 teknik sunumu için hazırlanmıştır. Takım: The Big 5.*
