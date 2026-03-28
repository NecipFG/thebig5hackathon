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
        assert abs(pixel_size - 20.0) < 1.0
    finally:
        os.unlink(path)

def test_load_dem_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_dem("nonexistent.tif")
