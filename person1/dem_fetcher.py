"""
Download the LOLA south pole DEM and clip it to each mission's bounding box.

Real data source: NASA PGDA SLDEM2015 south pole product.
  See: https://pgda.gsfc.nasa.gov/products/54
  The GeoTIFF version is available from USGS Astropedia:
  https://astrogeology.usgs.gov/search/map/Moon/LRO/LOLA/

If the download fails (network unavailable at hackathon), run main.py with
  --synthetic flag to generate usable stand-in DEMs automatically.
"""
import os
import requests
import rasterio
from rasterio.windows import from_bounds as window_from_bounds

# Update this URL to point to the actual LOLA south pole GeoTIFF.
# Recommended: SLDEM2015 at 128 ppd (~240 m/px) for the south pole strip.
# Obtain URL from: https://pgda.gsfc.nasa.gov/products/54
LOLA_DEM_URL = os.environ.get(
    "LOLA_DEM_URL",
    "https://pgda.gsfc.nasa.gov/data/SLDEM2015/south_pole/ldem_s_128ppd.tif",
)
CACHE_PATH = os.environ.get("LOLA_DEM_CACHE", "data/dem/south_pole_full.tif")

# Padding around each mission's start/goal in degrees
MISSION_PADDING_DEG = 1.0


def download_dem(url: str = LOLA_DEM_URL, dest: str = CACHE_PATH) -> str:
    """Download the south pole DEM to a local cache file.

    Returns the dest path. Skips download if the file already exists.
    Raises requests.HTTPError on non-200 response.
    """
    if os.path.exists(dest):
        print(f"[dem_fetcher] Using cached DEM: {dest}")
        return dest

    print(f"[dem_fetcher] Downloading DEM from {url} ...")
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)

    with requests.get(url, stream=True, timeout=600) as resp:
        resp.raise_for_status()
        total = int(resp.headers.get("content-length", 0))
        downloaded = 0
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=65536):
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded / total * 100
                    print(f"\r  {pct:.1f}%", end="", flush=True)
    print(f"\n[dem_fetcher] Saved to {dest}")
    return dest


def mission_bounding_box(
    start_lat: float, start_lon: float,
    goal_lat: float, goal_lon: float,
    padding_deg: float = MISSION_PADDING_DEG,
) -> tuple[float, float, float, float]:
    """Return (min_lat, min_lon, max_lat, max_lon) bounding box for a mission.

    Clamps longitude to [0, 360] and latitude to [-90, -60].
    """
    min_lat = max(-90.0, min(start_lat, goal_lat) - padding_deg)
    max_lat = min(-60.0, max(start_lat, goal_lat) + padding_deg)
    min_lon = max(0.0, min(start_lon, goal_lon) - padding_deg)
    max_lon = min(360.0, max(start_lon, goal_lon) + padding_deg)
    return min_lat, min_lon, max_lat, max_lon


def clip_dem_to_mission(
    src_path: str,
    min_lat: float, max_lat: float,
    min_lon: float, max_lon: float,
    dest_path: str,
) -> None:
    """Clip a GeoTIFF to a lat/lon bounding box and save as a new GeoTIFF.

    The bounding box uses geographic coordinates (degrees).
    """
    with rasterio.open(src_path) as src:
        window = window_from_bounds(
            left=min_lon, bottom=min_lat, right=max_lon, top=max_lat,
            transform=src.transform,
        )
        data = src.read(1, window=window)
        transform = src.window_transform(window)
        profile = src.profile.copy()
        profile.update(
            height=data.shape[0],
            width=data.shape[1],
            transform=transform,
        )

    os.makedirs(os.path.dirname(dest_path) or ".", exist_ok=True)
    with rasterio.open(dest_path, "w", **profile) as dst:
        dst.write(data, 1)
    print(f"[dem_fetcher] Clipped DEM saved to {dest_path} "
          f"({data.shape[0]}x{data.shape[1]} px)")
