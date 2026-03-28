"""Hazard mapper: converts slope arrays into binary safety maps and PNG visualizations."""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # non-interactive backend, safe for scripts
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def build_safety_map(slope_deg: np.ndarray, max_slope_deg: float = 20.0) -> np.ndarray:
    """
    Build binary safety map from slope array.

    Args:
        slope_deg: 2D float array of slope values in degrees.
        max_slope_deg: Threshold in degrees; slopes strictly above this are marked hazard (1).
                       Slopes at or below this value are marked safe (0).

    Returns:
        safety_map: uint8 array, 0 = safe, 1 = hazard
    """
    safety_map = (slope_deg > max_slope_deg).astype(np.uint8)
    return safety_map


def save_safety_map_png(
    safety_map: np.ndarray,
    slope_deg: np.ndarray,
    out_path: str,
    mission_name: str = "Mission",
) -> None:
    """
    Save a two-panel PNG: slope heatmap (left) + safety zones (right).
    Green = safe, Red = hazard.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(f"Terrain Safety Map — {mission_name}", fontsize=14, fontweight='bold')

    # Left: slope heatmap
    im = axes[0].imshow(slope_deg, cmap='RdYlGn_r', vmin=0, vmax=40)
    axes[0].set_title("Slope (degrees)")
    plt.colorbar(im, ax=axes[0], label="degrees")

    # Right: binary safety (0=safe=green, 1=hazard=red)
    cmap = mcolors.ListedColormap(['#2ecc71', '#e74c3c'])
    axes[1].imshow(safety_map, cmap=cmap, vmin=0, vmax=1)
    axes[1].set_title("Safety Map  (green=safe, red=hazard)")

    safe_pct = 100.0 * np.sum(safety_map == 0) / safety_map.size
    axes[1].set_xlabel(f"Safe coverage: {safe_pct:.1f}%")

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
