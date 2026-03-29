import pytest
from rasterio.transform import from_bounds
from person1.coord_utils import latlon_to_rowcol, rowcol_to_latlon


# Synthetic south pole DEM: lat -90 to -80, lon 0 to 360, 360x100 pixels
# pixel_width = 1.0 deg, pixel_height = 0.1 deg
TRANSFORM = from_bounds(west=0.0, south=-90.0, east=360.0, north=-80.0,
                        width=360, height=100)


def test_top_left_corner():
    row, col = latlon_to_rowcol(lat=-80.0, lon=0.0, transform=TRANSFORM)
    assert row == 0
    assert col == 0


def test_bottom_right_corner():
    row, col = latlon_to_rowcol(lat=-90.0, lon=360.0, transform=TRANSFORM)
    assert row == 100
    assert col == 360


def test_center_pixel():
    row, col = latlon_to_rowcol(lat=-85.0, lon=180.0, transform=TRANSFORM)
    assert row == 50
    assert col == 180


def test_roundtrip_lat():
    for lat in (-81.5, -85.0, -89.0):
        row, col = latlon_to_rowcol(lat=lat, lon=90.0, transform=TRANSFORM)
        lat_back, _ = rowcol_to_latlon(row=row, col=col, transform=TRANSFORM)
        assert abs(lat_back - lat) < 0.2, f"Roundtrip failed for lat={lat}"


def test_roundtrip_lon():
    for lon in (0.5, 90.0, 270.5):
        row, col = latlon_to_rowcol(lat=-85.0, lon=lon, transform=TRANSFORM)
        _, lon_back = rowcol_to_latlon(row=row, col=col, transform=TRANSFORM)
        assert abs(lon_back - lon) < 1.0, f"Roundtrip failed for lon={lon}"
