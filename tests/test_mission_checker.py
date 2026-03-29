import numpy as np
import pytest
import rasterio
from rasterio.transform import from_bounds
from rasterio.crs import CRS
import tempfile, os

from person1.mission_checker import check_mission


MOON_GEO_CRS = CRS.from_proj4("+proj=longlat +a=1737400 +b=1737400 +no_defs")


def _write_dem(path: str, data: np.ndarray,
               min_lat=-90, max_lat=-80, min_lon=0, max_lon=10):
    h, w = data.shape
    t = from_bounds(west=min_lon, south=min_lat, east=max_lon, north=max_lat,
                    width=w, height=h)
    with rasterio.open(path, "w", driver="GTiff", height=h, width=w,
                       count=1, dtype=data.dtype, crs=MOON_GEO_CRS,
                       transform=t) as dst:
        dst.write(data, 1)


def test_valid_mission_returns_ok(tmp_path):
    dem_path = str(tmp_path / "dem.tif")
    data = np.ones((100, 100), dtype=np.float32) * 500.0
    _write_dem(dem_path, data)

    result = check_mission(
        start_lat=-85.0, start_lon=5.0,
        goal_lat=-87.0, goal_lon=7.0,
        dem_path=dem_path,
    )
    assert result["valid"] is True
    assert result["start_in_bounds"] is True
    assert result["goal_in_bounds"] is True
    assert result["start_elevation_valid"] is True
    assert result["goal_elevation_valid"] is True


def test_start_outside_bounds_is_invalid(tmp_path):
    dem_path = str(tmp_path / "dem.tif")
    data = np.ones((100, 100), dtype=np.float32) * 500.0
    _write_dem(dem_path, data)

    result = check_mission(
        start_lat=-75.0,  # outside -90 to -80
        start_lon=5.0,
        goal_lat=-85.0,
        goal_lon=7.0,
        dem_path=dem_path,
    )
    assert result["valid"] is False
    assert result["start_in_bounds"] is False


def test_nan_elevation_at_goal_is_invalid(tmp_path):
    dem_path = str(tmp_path / "dem.tif")
    data = np.ones((100, 100), dtype=np.float32) * 500.0
    data[80, 80] = np.nan  # goal pixel is NaN
    _write_dem(dem_path, data)

    result = check_mission(
        start_lat=-85.0, start_lon=5.0,
        goal_lat=-88.0, goal_lon=8.0,  # maps near row=80,col=80
        dem_path=dem_path,
    )
    assert result["valid"] is False
    assert result["goal_elevation_valid"] is False
