"""
Coordinate conversion utilities for geographic lat/lon ↔ pixel (row, col).

Assumes the rasterio dataset uses a geographic CRS where x=longitude, y=latitude
in decimal degrees. This is standard for SLDEM2015 and LOLA equirectangular products.
"""
from rasterio.transform import Affine


def latlon_to_rowcol(lat: float, lon: float, transform: Affine) -> tuple[int, int]:
    """Convert geographic lat/lon (degrees) to pixel indices (row, col).

    Args:
        lat: Latitude in decimal degrees (negative = southern hemisphere)
        lon: Longitude in decimal degrees (0–360 or -180–180)
        transform: Affine transform from a rasterio dataset

    Returns:
        (row, col) integer pixel indices
    """
    col_f, row_f = ~transform * (lon, lat)
    return int(row_f), int(col_f)


def rowcol_to_latlon(row: int, col: int, transform: Affine) -> tuple[float, float]:
    """Convert pixel indices (row, col) to geographic lat/lon (degrees).

    Returns the center of the pixel.

    Returns:
        (lat, lon) in decimal degrees
    """
    lon, lat = transform * (col + 0.5, row + 0.5)
    return lat, lon
