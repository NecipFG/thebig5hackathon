import numpy as np
import math
from dataclasses import dataclass


@dataclass
class PathValidationResult:
    mission_name: str
    passed: bool          # True if zero hazard cells
    hazard_count: int     # number of waypoints in hazard zones
    hazard_pct: float     # percentage of waypoints in hazard zones
    path_length_m: float  # total Euclidean path length in meters
    max_slope_deg: float  # highest slope value along the path
    mean_slope_deg: float # mean slope value along the path
    waypoint_count: int


def validate_path(
    path: list[list[int]],
    safety_map: np.ndarray,
    slope_deg: np.ndarray,
    pixel_size_m: float,
    mission_name: str = "Mission",
) -> PathValidationResult:
    """
    Validate a rover path against a safety map.

    Args:
        path: list of [row, col] waypoints (integers)
        safety_map: 2D uint8 array (0=safe, 1=hazard)
        slope_deg: 2D float32 slope array
        pixel_size_m: meters per pixel
        mission_name: label for the report

    Returns:
        PathValidationResult with all safety metrics

    Raises:
        ValueError: if any waypoint is outside the map bounds
    """
    rows, cols = safety_map.shape

    for wp in path:
        r, c = wp
        if not (0 <= r < rows and 0 <= c < cols):
            raise ValueError(
                f"Waypoint [{r},{c}] is out of bounds for map shape {safety_map.shape}"
            )

    hazard_count = 0
    slope_values = []

    for wp in path:
        r, c = wp
        if safety_map[r, c] == 1:
            hazard_count += 1
        slope_values.append(float(slope_deg[r, c]))

    # Euclidean path length
    path_length_m = 0.0
    for i in range(len(path) - 1):
        dr = path[i+1][0] - path[i][0]
        dc = path[i+1][1] - path[i][1]
        path_length_m += math.sqrt(dr**2 + dc**2) * pixel_size_m

    n = len(path)
    return PathValidationResult(
        mission_name=mission_name,
        passed=(hazard_count == 0),
        hazard_count=hazard_count,
        hazard_pct=100.0 * hazard_count / n if n > 0 else 0.0,
        path_length_m=path_length_m,
        max_slope_deg=max(slope_values) if slope_values else 0.0,
        mean_slope_deg=sum(slope_values) / n if n > 0 else 0.0,
        waypoint_count=n,
    )
