import numpy as np
import pytest
from person3.path_validator import validate_path, PathValidationResult

def make_safety_map(shape=(10, 10), hazard_cols=None):
    """All safe, optionally mark some columns as hazard."""
    m = np.zeros(shape, dtype=np.uint8)
    if hazard_cols:
        for c in hazard_cols:
            m[:, c] = 1
    return m

def make_slope_map(shape=(10, 10), value=5.0):
    return np.full(shape, value, dtype=np.float32)

def test_fully_safe_path_passes():
    safety = make_safety_map()
    slope = make_slope_map()
    path = [[1, 1], [2, 2], [3, 3]]
    result = validate_path(path, safety, slope, pixel_size_m=20.0)
    assert result.passed is True
    assert result.hazard_count == 0
    assert result.hazard_pct == 0.0

def test_path_through_hazard_fails():
    safety = make_safety_map(hazard_cols=[5])
    slope = make_slope_map()
    # path goes through column 5
    path = [[3, 3], [3, 5], [3, 7]]
    result = validate_path(path, safety, slope, pixel_size_m=20.0)
    assert result.passed is False
    assert result.hazard_count == 1

def test_path_length_calculation():
    safety = make_safety_map()
    slope = make_slope_map()
    # straight horizontal path: 4 steps of 1 pixel = 3 moves * 20m = 60m
    path = [[5, 0], [5, 1], [5, 2], [5, 3]]
    result = validate_path(path, safety, slope, pixel_size_m=20.0)
    assert abs(result.path_length_m - 60.0) < 1.0

def test_diagonal_path_length():
    safety = make_safety_map()
    slope = make_slope_map()
    # diagonal: 1 step of sqrt(2) pixels
    path = [[0, 0], [1, 1]]
    result = validate_path(path, safety, slope, pixel_size_m=20.0)
    expected_m = 20.0 * (2 ** 0.5)
    assert abs(result.path_length_m - expected_m) < 0.5

def test_max_slope_reported():
    safety = make_safety_map()
    slope = np.zeros((10, 10), dtype=np.float32)
    slope[3, 3] = 18.0
    slope[4, 4] = 7.0
    path = [[2, 2], [3, 3], [4, 4], [5, 5]]
    result = validate_path(path, safety, slope, pixel_size_m=20.0)
    assert abs(result.max_slope_deg - 18.0) < 0.01
    assert abs(result.mean_slope_deg - (0 + 18.0 + 7.0 + 0) / 4) < 0.01

def test_out_of_bounds_waypoint_raises():
    safety = make_safety_map(shape=(5, 5))
    slope = make_slope_map(shape=(5, 5))
    path = [[0, 0], [10, 10]]  # (10,10) is outside 5x5
    with pytest.raises(ValueError, match="out of bounds"):
        validate_path(path, safety, slope, pixel_size_m=20.0)
