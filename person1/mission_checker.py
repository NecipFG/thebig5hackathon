"""
Validate that mission start/goal coordinates are within DEM bounds
and have valid (non-NaN, non-nodata) elevation values.
"""
import math
import numpy as np
import rasterio

from person1.coord_utils import latlon_to_rowcol


def check_mission(
    start_lat: float,
    start_lon: float,
    goal_lat: float,
    goal_lon: float,
    dem_path: str,
) -> dict:
    """Check that start and goal are valid positions within the DEM.

    Returns:
        dict with keys:
            valid (bool): True only if all checks pass
            start_in_bounds (bool)
            goal_in_bounds (bool)
            start_elevation_valid (bool)
            goal_elevation_valid (bool)
            start_row, start_col (int): pixel coordinates of start
            goal_row, goal_col (int): pixel coordinates of goal
            message (str): human-readable summary
    """
    with rasterio.open(dem_path) as src:
        h, w = src.height, src.width
        nodata = src.nodata
        transform = src.transform

        def _check_point(lat, lon):
            row, col = latlon_to_rowcol(lat, lon, transform)
            in_bounds = 0 <= row < h and 0 <= col < w
            if not in_bounds:
                return row, col, in_bounds, False
            elev = src.read(1)[row, col]
            elev_valid = not math.isnan(float(elev))
            if nodata is not None:
                elev_valid = elev_valid and float(elev) != float(nodata)
            return row, col, in_bounds, elev_valid

        s_row, s_col, s_bounds, s_elev = _check_point(start_lat, start_lon)
        g_row, g_col, g_bounds, g_elev = _check_point(goal_lat, goal_lon)

    valid = s_bounds and g_bounds and s_elev and g_elev
    issues = []
    if not s_bounds:
        issues.append("start outside DEM bounds")
    if not g_bounds:
        issues.append("goal outside DEM bounds")
    if s_bounds and not s_elev:
        issues.append("start has invalid elevation (NaN/nodata)")
    if g_bounds and not g_elev:
        issues.append("goal has invalid elevation (NaN/nodata)")

    return {
        "valid": valid,
        "start_in_bounds": s_bounds,
        "goal_in_bounds": g_bounds,
        "start_elevation_valid": s_elev,
        "goal_elevation_valid": g_elev,
        "start_row": s_row,
        "start_col": s_col,
        "goal_row": g_row,
        "goal_col": g_col,
        "message": "OK" if valid else "; ".join(issues),
    }
