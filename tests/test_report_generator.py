import numpy as np
import os, tempfile
from person3.path_validator import validate_path
from person3.hazard_mapper import build_safety_map
from person3.report_generator import generate_safety_report

def make_full_scenario():
    slope = np.zeros((20, 20), dtype=np.float32)
    slope[10, 10] = 5.0
    safety = build_safety_map(slope, max_slope_deg=20.0)
    path = [[2, 2], [5, 5], [10, 10], [15, 15], [18, 18]]
    result = validate_path(path, safety, slope, pixel_size_m=20.0, mission_name="Test Mission")
    return slope, safety, path, result

def test_report_creates_png_file():
    slope, safety, path, result = make_full_scenario()
    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = os.path.join(tmpdir, "report.png")
        generate_safety_report(result, safety, slope, path, out_path)
        assert os.path.exists(out_path)
        assert os.path.getsize(out_path) > 5000
