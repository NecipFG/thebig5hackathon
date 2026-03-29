"""
Generate PNG preview images for each mission showing:
- DEM displayed as a hillshade-style grayscale
- Start position: green star marker
- Goal position: red star marker
- Mission name, difficulty, and objective in the title
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")  # no display needed
import matplotlib.pyplot as plt
import rasterio

from person1.coord_utils import latlon_to_rowcol


def plot_mission(
    mission: dict,
    dem_path: str,
    output_path: str,
) -> None:
    """Save a PNG preview of the mission DEM with start/goal markers.

    Args:
        mission: One dict from missions_data.MISSIONS
        dem_path: Path to the clipped GeoTIFF for this mission
        output_path: Where to save the PNG
    """
    with rasterio.open(dem_path) as src:
        dem = src.read(1).astype(np.float32)
        transform = src.transform

    # Compute start/goal pixel positions
    s_row, s_col = latlon_to_rowcol(mission["start_lat"], mission["start_lon"],
                                    transform)
    g_row, g_col = latlon_to_rowcol(mission["goal_lat"], mission["goal_lon"],
                                    transform)

    # Hillshade approximation: normalize + light from top-left
    gy, gx = np.gradient(dem)
    hillshade = -gx - gy
    hillshade = (hillshade - hillshade.min()) / (hillshade.max() - hillshade.min() + 1e-9)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.imshow(hillshade, cmap="gray", origin="upper", interpolation="nearest")

    ax.plot(s_col, s_row, "g*", markersize=15, label="Start", zorder=5)
    ax.plot(g_col, g_row, "r*", markersize=15, label="Goal", zorder=5)
    ax.legend(loc="upper right", fontsize=9)

    title = (
        f"Mission {mission['id']}: {mission['name']} [{mission['difficulty']}]\n"
        f"{mission['objective']}\n"
        f"Start ({mission['start_lat']:.2f}°, {mission['start_lon']:.2f}°) → "
        f"Goal ({mission['goal_lat']:.2f}°, {mission['goal_lon']:.2f}°)"
    )
    ax.set_title(title, fontsize=9, pad=8)
    ax.set_xlabel("Column (pixels)")
    ax.set_ylabel("Row (pixels)")
    ax.set_facecolor("#1a1a2e")
    fig.patch.set_facecolor("#0f0f23")
    ax.title.set_color("white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.tick_params(colors="white")

    plt.tight_layout()
    plt.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"[plotter] Saved preview: {output_path}")
