import numpy as np
import rasterio
import os


def load_dem(tif_path: str) -> tuple[np.ndarray, float]:
    """
    Load a LOLA GeoTIFF DEM file.

    Returns:
        dem: 2D float32 numpy array of elevation values (meters)
        pixel_size_m: ground resolution in meters per pixel
    """
    if not os.path.exists(tif_path):
        raise FileNotFoundError(f"DEM file not found: {tif_path}")

    with rasterio.open(tif_path) as src:
        dem = src.read(1).astype(np.float32)
        # pixel size from transform (absolute value, meters)
        pixel_size_m = abs(src.transform.a)

    return dem, pixel_size_m
