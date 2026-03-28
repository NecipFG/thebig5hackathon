import numpy as np
import pytest
import os, tempfile
from person3.hazard_mapper import build_safety_map, save_safety_map_png

def test_all_safe_when_slope_low():
    slope = np.full((5, 5), 10.0, dtype=np.float32)  # 10° everywhere
    safety = build_safety_map(slope, max_slope_deg=20.0)
    assert safety.shape == (5, 5)
    assert np.all(safety == 0)  # 0 = safe

def test_all_hazard_when_slope_high():
    slope = np.full((5, 5), 30.0, dtype=np.float32)  # 30° everywhere
    safety = build_safety_map(slope, max_slope_deg=20.0)
    assert np.all(safety == 1)  # 1 = hazard

def test_mixed_terrain():
    slope = np.array([[5.0, 25.0], [15.0, 22.0]], dtype=np.float32)
    safety = build_safety_map(slope, max_slope_deg=20.0)
    expected = np.array([[0, 1], [0, 1]])
    assert np.array_equal(safety, expected)

def test_boundary_exactly_20_is_safe():
    slope = np.array([[20.0]], dtype=np.float32)
    safety = build_safety_map(slope, max_slope_deg=20.0)
    assert safety[0, 0] == 0  # exactly 20° is still traversable

def test_save_safety_map_png_creates_file():
    slope = np.full((10, 10), 10.0, dtype=np.float32)
    safety = build_safety_map(slope, max_slope_deg=20.0)
    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = os.path.join(tmpdir, "test_safety.png")
        save_safety_map_png(safety, slope, out_path, mission_name="Test Mission")
        assert os.path.exists(out_path)
        assert os.path.getsize(out_path) > 1000  # non-trivial PNG
