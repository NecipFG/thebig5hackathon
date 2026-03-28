import numpy as np
import pytest
from person3.slope_calculator import compute_slope_degrees

def test_flat_terrain_gives_zero_slope():
    dem = np.full((10, 10), 100.0, dtype=np.float32)
    slope = compute_slope_degrees(dem, pixel_size_m=20.0)
    assert slope.shape == dem.shape
    assert np.allclose(slope, 0.0, atol=1e-4)

def test_inclined_plane_gives_correct_slope():
    # 1m rise per 1 pixel at 20m/pixel → arctan(1/20) ≈ 2.86°
    dem = np.zeros((10, 10), dtype=np.float32)
    for col in range(10):
        dem[:, col] = col * 1.0  # 1m per pixel in x direction
    slope = compute_slope_degrees(dem, pixel_size_m=20.0)
    expected_deg = np.degrees(np.arctan(1.0 / 20.0))
    # interior pixels — edges use one-sided gradient so may differ slightly
    assert np.allclose(slope[1:-1, 1:-1], expected_deg, atol=0.5)

def test_steep_terrain_exceeds_20_degrees():
    # 10m rise per pixel at 1m/pixel → arctan(10) ≈ 84°
    dem = np.zeros((5, 5), dtype=np.float32)
    for col in range(5):
        dem[:, col] = col * 10.0
    slope = compute_slope_degrees(dem, pixel_size_m=1.0)
    assert slope[2, 2] > 20.0

def test_output_dtype_is_float32():
    dem = np.ones((5, 5), dtype=np.float32)
    slope = compute_slope_degrees(dem, pixel_size_m=20.0)
    assert slope.dtype == np.float32
