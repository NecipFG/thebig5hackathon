import numpy as np
import rasterio


def load_dem(tif_path: str) -> tuple[np.ndarray, float]:
    """
    Load a LOLA GeoTIFF DEM file.

    Returns:
        dem: 2D float32 numpy array of elevation values (meters)
        pixel_size_m: ground resolution in meters per pixel (square pixels assumed)

    Raises:
        FileNotFoundError: if the file does not exist or cannot be opened
        ValueError: if the DEM has non-square pixels (not supported)
    """
    try:
        with rasterio.open(tif_path) as src:
            dem = src.read(1).astype(np.float32)
            x_res = abs(src.transform.a)
            y_res = abs(src.transform.e)
            if not np.isclose(x_res, y_res, rtol=1e-3):
                raise ValueError(
                    f"Non-square pixels not supported: x={x_res:.4f}m, y={y_res:.4f}m"
                )
            pixel_size_m = x_res
    except rasterio.errors.RasterioIOError as exc:
        raise FileNotFoundError(f"DEM file not found: {tif_path}") from exc

    return dem, pixel_size_m
