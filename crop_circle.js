// crop_circle.js
// Merkez noktadan 60.7km yaricap ile dairesel kesim, 5mpp -> 10mpp
const { fromFile, writeArrayBuffer } = require('geotiff');
const fs = require('fs');

const INPUT  = 'Site01/ldem_87s_5mpp.tif';
const OUTPUT = 'Site01/ldem_87s_10mpp_circle.tif';

const PPM_IN  = 5;      // kaynak: 5 metre/piksel
const PPM_OUT = 10;     // hedef: 10 metre/piksel
const RATIO   = PPM_OUT / PPM_IN; // 2
const RADIUS_M = 60700;  // 60.7 km yaricap
const DIAMETER_M = RADIUS_M * 2; // 121.4 km cap

async function main() {
    console.log('Kaynak dosya aciliyor:', INPUT);
    const tiff = await fromFile(INPUT);
    const image = await tiff.getImage();
    const srcW = image.getWidth();
    const srcH = image.getHeight();
    console.log(`Kaynak boyut: ${srcW} x ${srcH} piksel`);
    console.log(`Kaynak alan: ${(srcW * PPM_IN / 1000).toFixed(1)} x ${(srcH * PPM_IN / 1000).toFixed(1)} km`);

    // Merkez (piksel)
    const cx = srcW / 2;
    const cy = srcH / 2;

    // Kaynak pikselde yaricap
    const radiusSrcPx = RADIUS_M / PPM_IN; // 6070 px

    // Cikti boyutu
    const outDiam = Math.ceil(DIAMETER_M / PPM_OUT); // ~4047 px
    const outR = outDiam / 2;

    console.log(`Cikti boyut: ${outDiam} x ${outDiam} piksel (${(outDiam * outDiam * 4 / 1024 / 1024).toFixed(1)} MB)`);

    // Kaynaktan okunacak pencere (merkez etrafinda kare)
    const winX0 = Math.max(0, Math.floor(cx - radiusSrcPx));
    const winY0 = Math.max(0, Math.floor(cy - radiusSrcPx));
    const winX1 = Math.min(srcW, Math.ceil(cx + radiusSrcPx));
    const winY1 = Math.min(srcH, Math.ceil(cy + radiusSrcPx));
    const winW = winX1 - winX0;
    const winH = winY1 - winY0;

    console.log(`Okuma penceresi: [${winX0}, ${winY0}] -> [${winX1}, ${winY1}] (${winW}x${winH})`);

    // Cikti dizisi
    const outData = new Float32Array(outDiam * outDiam);

    // Batch halinde oku (her batch ~256 cikti satiri)
    const BATCH = 256;
    const totalBatches = Math.ceil(outDiam / BATCH);

    for (let b = 0; b < totalBatches; b++) {
        const oyStart = b * BATCH;
        const oyEnd = Math.min(oyStart + BATCH, outDiam);

        // Bu batch icin kaynak Y araligi
        const srcYmin = Math.max(winY0, Math.floor(cy + (oyStart - outR) * RATIO));
        const srcYmax = Math.min(winY1, Math.ceil(cy + (oyEnd - outR) * RATIO) + 1);

        if (srcYmin >= srcYmax) continue;

        process.stdout.write(`\rBatch ${b + 1}/${totalBatches} okunuyor... (satir ${oyStart}-${oyEnd})`);

        const rasters = await image.readRasters({
            window: [winX0, srcYmin, winX1, srcYmax]
        });
        const batchData = rasters[0];
        const batchW = winX1 - winX0;

        for (let oy = oyStart; oy < oyEnd; oy++) {
            const dy = oy - outR;
            const srcY = Math.round(cy + dy * RATIO);
            if (srcY < srcYmin || srcY >= srcYmax) continue;
            const localY = srcY - srcYmin;

            for (let ox = 0; ox < outDiam; ox++) {
                const dx = ox - outR;

                // Daire kontrolu
                if (dx * dx + dy * dy > outR * outR) continue;

                const srcX = Math.round(cx + dx * RATIO);
                const localX = srcX - winX0;
                if (localX < 0 || localX >= batchW) continue;

                outData[oy * outDiam + ox] = batchData[localY * batchW + localX];
            }
        }
    }

    console.log('\nTIF yaziliyor:', OUTPUT);
    const metadata = {
        height: outDiam,
        width: outDiam
    };
    const arrayBuffer = await writeArrayBuffer(outData, metadata);

    fs.writeFileSync(OUTPUT, Buffer.from(arrayBuffer));

    const outSize = fs.statSync(OUTPUT).size;
    console.log(`Tamamlandi! Cikti: ${(outSize / 1024 / 1024).toFixed(1)} MB`);
}

main().catch(e => { console.error('Hata:', e); process.exit(1); });
