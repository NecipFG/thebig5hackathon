# Detaylı Çözüm: Otonom Rota Planlama Algoritması

## Proje Özeti

Bu proje, zorlu ve kısıtlı bir arazide otonom hareket eden bir araç için **güvenli, verimli ve kinematik açıdan geçerli rota planlaması** yapan bir algoritma sistemi geliştirmektedir. Uygulama alanı Ay Güney Kutbu'dur; ancak sistemin özü, gerçek yükseklik verisi üzerinde çalışan çok kriterli bir rota optimizasyon algoritmasıdır.

---

## Çözülen Problem

Bir araç için sadece "en kısa yolu bulmak" yetmez. Gerçek dünya kısıtları altında çalışan otonom bir sistemin aynı anda birden fazla hedefi dengelemesi gerekir:

- **Güvenlik kısıtı:** Zemin eğimi belirli bir eşiği aşarsa araç geçemez — bu bir sabit engel değil, sürekli değişen bir maliyet alanıdır.
- **Enerji kısıtı:** Bazı bölgeler enerji açısından daha pahalıdır (gölgeli/soğuk alanlar); algoritmanın bunu rotaya yansıtması gerekir.
- **Kinematik kısıt:** Fiziksel bir araç anında yön değiştiremez; keskin dönüşler hem zaman hem mekanik stres kaybıdır.
- **Ölçek kısıtı:** Gerçek veri üzerinde, milyonlarca hücreden oluşan bir ızgarada, saniyeler içinde çözüm üretilmelidir.

Standart en-kısa-yol algoritmaları (Dijkstra, basit A\*) yalnızca mesafeyi minimize eder ve bu kısıtları modelleyemez. **Bu projenin algoritması tüm bu kısıtları tek bir maliyet fonksiyonuna entegre eder.**

---

## Algoritmanın Çözüm Yaklaşımı

Geliştirilen sistem dört katmandan oluşur:

```
Ham Yükseklik Verisi (DEM)
        │
        ▼
[ Arazi Ön İşleme ]    ← Eğim haritası, tehlike maskesi, koordinat dönüşümleri
        │
        ▼
[ Rota Planlama (A*) ] ← Çok kriterli maliyet: eğim + enerji + kinematik
        │
        ▼
[ Bağımsız Doğrulama ] ← Rota güvenlik sertifikasyonu, metrik raporu
        │
        ▼
[ 3D Görselleştirme ]  ← Algoritma çıktısının interaktif sunumu
```

Her katman bağımsız modül olarak geliştirilmiş, standart dosya formatlarıyla (GeoTIFF, JSON, CSV) birbirine bağlıdır.

---

## Üç Test Senaryosu

Algoritma, artan zorlukta üç senaryoda doğrulanmaktadır:

| Senaryo | Mesafe | Zorluk | Test Ettiği Özellik |
|---------|--------|--------|---------------------|
| **Shackleton Rim** | ~6 km | Kolay | Temel rota bulma, eğim kaçınma |
| **de Gerlache Havzası** | ~22 km | Orta | Enerji maliyeti dengeleme, uzun mesafe |
| **Haworth-Nobile Geçişi** | ~38 km | Zor | Tüm kısıtların eş zamanlı optimizasyonu |

---

## Algoritmanın Temel Özellikleri

| Özellik | Standart A\* | Bu Proje |
|---------|-------------|----------|
| Maliyet kriteri | Mesafe | Mesafe × Eğim × Dönüş × Enerji |
| Durum uzayı | (satır, sütun) | (satır, sütun, yön) — kinematik farkındalık |
| Hareket sayısı | 8 yön | 22 yön — ızgara yapaylığı azaltılmış |
| Güvenlik | Engel maskesi | Sürekli maliyet alanı + sert eşik |
| Doğrulama | Yok | Bağımsız sertifikasyon modülü |

---

## Sonuçlar

- Her senaryo için **garantili optimal** rota üretilir (kabul edilebilir sezgisel kullanımı ile).
- Rota **0 tehlikeli hücre** içerecek şekilde sertifikalandırılır.
- Güzergah metrikleri (uzunluk, adım sayısı, maks./ort. eğim) dışa aktarılır.
- Gerçek yükseklik verisi ve sentetik test verisi üzerinde çalışır.
- Etkileşimli 3D görüntüleyici üzerinden sonuçlar gösterilebilir.

---

## Kullanılan Teknolojiler

| Katman | Araç/Kütüphane |
|--------|---------------|
| Veri kaynağı | NASA LOLA SLDEM2015 (5 m/piksel DEM) |
| Programlama dili | Python 3, JavaScript |
| Coğrafi veri işleme | rasterio, numpy, affine |
| Algoritma | A* (özel çok kriterli maliyet fonksiyonu) |
| Görselleştirme | Three.js r128, GeoTIFF.js |
| Demo arayüzü | Streamlit + tarayıcı tabanlı 3D görüntüleyici |

---

*Bu belge TUA Astro Hackathon 2026 sunumu için hazırlanmıştır. Takım: The Big 5.*
