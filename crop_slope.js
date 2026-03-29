// crop_slope.js — ldsm (slope) haritasini ayni parametrelerle dairesel kes
const { fromFile, writeArrayBuffer } = require('geotiff');
const fs = require('fs');

const INPUT  = 'Site01/ldsm_87s_5mpp.tif';
const OUTPUT = 'Site01/ldsm_87s_10mpp_circle.tif';

const PPM_IN  = 5, PPM_OUT = 10, RATIO = PPM_OUT / PPM_IN;
const RADIUS_M = 60700, DIAMETER_M = RADIUS_M * 2;

async function main() {
    console.log('Kaynak:', INPUT);
    const tiff = await fromFile(INPUT);
    const image = await tiff.getImage();
    const srcW = image.getWidth(), srcH = image.getHeight();
    console.log(`Boyut: ${srcW}x${srcH}`);

    const cx = srcW/2, cy = srcH/2;
    const radiusSrcPx = RADIUS_M / PPM_IN;
    const outDiam = Math.ceil(DIAMETER_M / PPM_OUT);
    const outR = outDiam / 2;
    console.log(`Cikti: ${outDiam}x${outDiam}`);

    const winX0 = Math.max(0, Math.floor(cx - radiusSrcPx));
    const winY0 = Math.max(0, Math.floor(cy - radiusSrcPx));
    const winX1 = Math.min(srcW, Math.ceil(cx + radiusSrcPx));
    const winY1 = Math.min(srcH, Math.ceil(cy + radiusSrcPx));

    const outData = new Float32Array(outDiam * outDiam);
    const BATCH = 256, totalBatches = Math.ceil(outDiam / BATCH);

    for (let b = 0; b < totalBatches; b++) {
        const oyStart = b * BATCH, oyEnd = Math.min(oyStart + BATCH, outDiam);
        const srcYmin = Math.max(winY0, Math.floor(cy + (oyStart - outR) * RATIO));
        const srcYmax = Math.min(winY1, Math.ceil(cy + (oyEnd - outR) * RATIO) + 1);
        if (srcYmin >= srcYmax) continue;
        process.stdout.write(`\rBatch ${b+1}/${totalBatches}...`);
        const rasters = await image.readRasters({ window: [winX0, srcYmin, winX1, srcYmax] });
        const batchData = rasters[0], batchW = winX1 - winX0;
        for (let oy = oyStart; oy < oyEnd; oy++) {
            const dy = oy - outR, srcY = Math.round(cy + dy * RATIO);
            if (srcY < srcYmin || srcY >= srcYmax) continue;
            const localY = srcY - srcYmin;
            for (let ox = 0; ox < outDiam; ox++) {
                const dx = ox - outR;
                if (dx*dx + dy*dy > outR*outR) continue;
                const srcX = Math.round(cx + dx * RATIO), localX = srcX - winX0;
                if (localX < 0 || localX >= batchW) continue;
                outData[oy * outDiam + ox] = batchData[localY * batchW + localX];
            }
        }
    }

    console.log('\nYaziliyor:', OUTPUT);
    const ab = await writeArrayBuffer(outData, { width: outDiam, height: outDiam });
    fs.writeFileSync(OUTPUT, Buffer.from(ab));
    console.log(`Tamam! ${(fs.statSync(OUTPUT).size / 1024 / 1024).toFixed(1)} MB`);
}
main().catch(e => { console.error(e); process.exit(1); });
