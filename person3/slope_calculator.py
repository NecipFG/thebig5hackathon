import numpy as np


def compute_slope_degrees(dem: np.ndarray, pixel_size_m: float) -> np.ndarray:
    """
    Compute slope in degrees at each pixel of a DEM.

    Uses central differences (np.gradient) with correct metric scale.

    Args:
        dem: 2D float32 elevation array (meters)
        pixel_size_m: horizontal distance per pixel (meters)

    Returns:
        slope: 2D float32 array of slope values in degrees
    """
    # gradient returns rise/pixel — divide by pixel_size_m to get rise/meter
    dz_dy, dz_dx = np.gradient(dem, pixel_size_m)
    slope_rad = np.arctan(np.sqrt(dz_dx**2 + dz_dy**2))
    return np.degrees(slope_rad).astype(np.float32)
