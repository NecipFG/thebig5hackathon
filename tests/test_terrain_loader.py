import numpy as np
import pytest
import tempfile, os
import rasterio
from rasterio.transform import from_bounds
from person3.terrain_loader import load_dem

def make_test_tif(path, data, pixel_size_m=20.0):
    """Write a tiny synthetic GeoTIFF for testing."""
    h, w = data.shape
    transform = from_bounds(0, 0, w * pixel_size_m, h * pixel_size_m, w, h)
    with rasterio.open(
        path, 'w', driver='GTiff', height=h, width=w,
        count=1, dtype=data.dtype, crs='EPSG:32636', transform=transform
    ) as dst:
        dst.write(data, 1)

def test_load_dem_returns_array_and_pixel_size():
    data = np.array([[100.0, 110.0], [120.0, 130.0]], dtype=np.float32)
    with tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as f:
        path = f.name
    try:
        make_test_tif(path, data, pixel_size_m=20.0)
        dem, pixel_size = load_dem(path)
        assert dem.shape == (2, 2)
        assert np.allclose(dem, data)
        assert abs(pixel_size - 20.0) < 0.01
    finally:
        os.unlink(path)

def test_load_dem_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_dem("nonexistent.tif")

def test_load_dem_non_square_pixels_raises():
    import rasterio
    from rasterio.transform import Affine
    data = np.ones((4, 4), dtype=np.float32)
    with tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as f:
        path = f.name
    try:
        # 20m x-res, 40m y-res → non-square
        transform = Affine(20.0, 0.0, 0.0, 0.0, -40.0, 0.0)
        with rasterio.open(
            path, 'w', driver='GTiff', height=4, width=4,
            count=1, dtype='float32', crs='EPSG:32636', transform=transform
        ) as dst:
            dst.write(data, 1)
        with pytest.raises(ValueError, match="Non-square pixels"):
            load_dem(path)
    finally:
        os.unlink(path)
