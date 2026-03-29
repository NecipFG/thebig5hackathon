# DM1 Ay Istasyonu — Rota Planlayici

Ay guney kutbu bolgesinde otonom rover rota planlama araci. 3D arazi goruntuleyici, A* pathfinding, LIDAR simulasyonu ve Gemini AI asistan iceriyor.

## Calistirma

```bash
npm install
node server.js
```

Tarayicida `http://localhost:8080` adresine gidin.

## Kullanim

1. Sag paneldeki dropdown'dan **ldem_87s_10mpp_circle.tif** secin
2. 3D haritada iki nokta tiklayarak **baslangic** (yesil) ve **hedef** (kirmizi) secin
3. A* otomatik rota hesaplar, Wall-E animasyonu baslar
4. **Isik Haritasi** icin: Renk Modu > Isik Haritasi > **ldsm_87s_10mpp_circle_512.tif** secin
5. **LIDAR**: Engel Yerlestir butonuyla engel koyun, rover otomatik kacinir
6. **Gemini AI**: Sol panelden rota analizi, otonom senaryo veya misyon raporu isteyin

## Gereksinimler

- Node.js (herhangi bir surum)
- Modern tarayici (Chrome/Edge/Firefox)

