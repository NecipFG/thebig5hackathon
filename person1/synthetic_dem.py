"""
Generate synthetic lunar south pole DEMs for offline testing.

Uses superimposed sine waves + Gaussian craters to produce realistic-looking
elevation data. All missions' DEMs are created from the same base terrain
so the pipeline can be tested end-to-end without downloading real data.
"""
import os
import numpy as np
import rasterio
from rasterio.transform import from_bounds
from rasterio.crs import CRS


# Moon IAU sphere (no EPSG, use proj4)
MOON_GEO_CRS = CRS.from_proj4("+proj=longlat +a=1737400 +b=1737400 +no_defs")


def _add_crater(dem: np.ndarray, row: int, col: int, radius_px: int,
                depth: float) -> np.ndarray:
    """Stamp a bowl-shaped crater onto the DEM array."""
    rr, cc = np.ogrid[:dem.shape[0], :dem.shape[1]]
    dist = np.sqrt((rr - row) ** 2 + (cc - col) ** 2)
    mask = dist < radius_px
    dem[mask] -= depth * (1 - dist[mask] / radius_px)
    return dem


def make_synthetic_dem(
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    dest_path: str,
    resolution_deg: float = 0.05,
    seed: int = 42,
) -> None:
    """Create a synthetic DEM GeoTIFF covering the given lat/lon bounding box.

    Args:
        min_lat, max_lat: Latitude range (degrees, negative for south)
        min_lon, max_lon: Longitude range (degrees)
        dest_path: Output GeoTIFF path
        resolution_deg: Degrees per pixel (default 0.05 ≈ 1.5 km at equator)
        seed: Random seed for reproducibility
    """
    rng = np.random.default_rng(seed)

    height = max(1, int(round((max_lat - min_lat) / resolution_deg)))
    width = max(1, int(round((max_lon - min_lon) / resolution_deg)))

    # Base terrain: large-scale undulation
    x = np.linspace(0, 4 * np.pi, width)
    y = np.linspace(0, 4 * np.pi, height)
    xx, yy = np.meshgrid(x, y)
    dem = (
        200 * np.sin(xx * 0.3) * np.cos(yy * 0.2)
        + 100 * np.sin(xx * 0.7 + 1.0) * np.sin(yy * 0.5)
        + rng.normal(0, 5, (height, width))
    ).astype(np.float32)

    # Add 4–8 craters of random size
    n_craters = rng.integers(4, 9)
    for _ in range(n_craters):
        cr = rng.integers(10, height - 10)
        cc = rng.integers(10, width - 10)
        radius = rng.integers(5, min(20, height // 4, width // 4))
        depth = rng.uniform(50, 300)
        dem = _add_crater(dem, cr, cc, radius, depth)

    transform = from_bounds(
        west=min_lon, south=min_lat, east=max_lon, north=max_lat,
        width=width, height=height,
    )

    os.makedirs(os.path.dirname(dest_path) or ".", exist_ok=True)
    with rasterio.open(
        dest_path, "w",
        driver="GTiff",
        height=height, width=width,
        count=1, dtype=np.float32,
        crs=MOON_GEO_CRS,
        transform=transform,
    ) as dst:
        dst.write(dem, 1)
