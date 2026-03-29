import os
import rasterio
from rasterio.enums import Resampling
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Ayarlar
TIFF_PATH = "ldsm_87s_5mpp.tif"
OUTPUT_PATH = "lunar_map_render.png"
DOWNSAMPLE_RATIO = 10
SLOPE_THRESHOLD = 20.0

def convert_tiff_to_map(tiff_file: str, output_file: str, downsample: int = 1):
    """
    Belirtilen GeoTIFF dosyasını okur, eğim değerlerini renklendirir
    ve bir görsel harita (PNG) olarak kaydeder.
    """
    if not os.path.exists(tiff_file):
        print(f"Hata: '{tiff_file}' bulunamadı!")
        return

    print(f"Harita yükleniyor: {tiff_file} (Küçültme oranı: 1/{downsample})")
    
    with rasterio.open(tiff_file) as src:
        # Downsample ile veriyi oku
        out_shape = (1, int(src.height / downsample), int(src.width / downsample))
        slope_data = src.read(
            1,
            out_shape=out_shape,
            resampling=Resampling.bilinear
        )

    # 1. Eğimi Normale Çevir (0 - 20 derece arasını 0-1 aralığına sıkıştır)
    # 20 decerenin üstündeki yerler renklendirme için 1 olarak kabul edilecek.
    norm_arr = np.clip(slope_data / SLOPE_THRESHOLD, 0, 1)

    # 2. Matplotlib Colormap Uygula (viridis kütüphanesini kullanıyoruz)
    # Bu bize RGBA (Red, Green, Blue, Alpha) matrisi verecek
    colormap = plt.get_cmap("viridis")
    rgba_map = colormap(norm_arr)

    # 3. Engelleri (20 derece üstü) Simsiyah Yap
    obstacle_mask = slope_data > SLOPE_THRESHOLD
    rgba_map[obstacle_mask] = [0.05, 0.05, 0.05, 1.0]

    # 4. Veriyi Görsel Formatına Çevir (0-255 arası tam sayılar)
    img_array = (rgba_map[:, :, :3] * 255).astype(np.uint8)

    # 5. Resmi Oluştur ve Kaydet
    img = Image.fromarray(img_array)
    img.save(output_file)
    print(f"Harita başarıyla oluşturuldu ve '{output_file}' olarak kaydedildi!")
    print(f"Boyut: {img.width}x{img.height} piksel")

if __name__ == "__main__":
    convert_tiff_to_map(TIFF_PATH, OUTPUT_PATH, downsample=DOWNSAMPLE_RATIO)
