"""Safety report generator: produces 1-page PNG reports with path overlay and metrics table."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from person3.path_validator import PathValidationResult


def generate_safety_report(
    result: PathValidationResult,
    safety_map: np.ndarray,
    slope_deg: np.ndarray,
    path: list[list[int]],
    out_path: str,
) -> None:
    """
    Generate a 1-page safety report as a PNG image.

    Args:
        result: PathValidationResult from validate_path()
        safety_map: 2D uint8 safety map (0=safe, 1=hazard)
        slope_deg: 2D float32 slope array
        path: list of [row, col] waypoints
        out_path: file path for the output PNG

    Layout:
        Title + PASS/FAIL banner at top
        Left panel: safety map with path overlay
        Right panel: metrics table
    """
    verdict_color = '#27ae60' if result.passed else '#e74c3c'
    verdict_text  = 'PASS ✓' if result.passed else 'FAIL ✗'

    fig = plt.figure(figsize=(14, 8))
    fig.patch.set_facecolor('#1a1a2e')

    # Title + verdict
    fig.text(0.5, 0.95, f"Safety Validation Report — {result.mission_name}",
             ha='center', va='top', fontsize=16, color='white', fontweight='bold')
    fig.text(0.5, 0.90, verdict_text,
             ha='center', va='top', fontsize=22, color=verdict_color, fontweight='bold')

    # Left: safety map with path overlay
    ax_map = fig.add_axes([0.05, 0.10, 0.50, 0.75])
    cmap = mcolors.ListedColormap(['#2ecc71', '#e74c3c'])
    ax_map.imshow(safety_map, cmap=cmap, vmin=0, vmax=1, alpha=0.7)
    ax_map.imshow(slope_deg, cmap='gray', alpha=0.3)

    legend_handles = [
        mpatches.Patch(color='#2ecc71', label='Safe (slope ≤ 20°)'),
        mpatches.Patch(color='#e74c3c', label='Hazard (slope > 20°)'),
    ]

    if path:
        rows_list = [wp[0] for wp in path]
        cols_list = [wp[1] for wp in path]
        path_line, = ax_map.plot(cols_list, rows_list, 'b-', linewidth=2, label='Rover path')
        start_dot, = ax_map.plot(cols_list[0], rows_list[0], 'go', markersize=10, label='Start')
        end_star, = ax_map.plot(cols_list[-1], rows_list[-1], 'r*', markersize=12, label='End')
        legend_handles = [path_line, start_dot, end_star] + legend_handles

    ax_map.legend(handles=legend_handles, loc='lower right', fontsize=9,
                  facecolor='#1a1a2e', labelcolor='white')
    ax_map.set_title('Terrain Safety Map + Path', color='white', fontsize=12)
    ax_map.tick_params(colors='white')
    for spine in ax_map.spines.values():
        spine.set_edgecolor('white')

    # Right: metrics table
    ax_tbl = fig.add_axes([0.60, 0.10, 0.38, 0.75])
    ax_tbl.axis('off')
    ax_tbl.set_facecolor('#1a1a2e')

    metrics = [
        ['Metric', 'Value'],
        ['Mission', result.mission_name],
        ['Verdict', verdict_text],
        ['Waypoints', str(result.waypoint_count)],
        ['Hazard cells', str(result.hazard_count)],
        ['Hazard %', f'{result.hazard_pct:.1f}%'],
        ['Path length', f'{result.path_length_m / 1000:.3f} km'],
        ['Max slope', f'{result.max_slope_deg:.1f}°'],
        ['Mean slope', f'{result.mean_slope_deg:.1f}°'],
    ]

    tbl = ax_tbl.table(
        cellText=metrics[1:],
        colLabels=metrics[0],
        loc='center',
        cellLoc='left',
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(11)
    tbl.scale(1.2, 2.0)

    # Style header row
    for (row, col), cell in tbl.get_celld().items():
        cell.set_facecolor('#2c3e50' if row == 0 else '#1a1a2e')
        cell.set_text_props(color='white')
        cell.set_edgecolor('#3d5a80')

    # Highlight verdict row
    for col in range(2):
        tbl[2, col].set_facecolor(verdict_color)
        tbl[2, col].set_text_props(color='white', fontweight='bold')

    ax_tbl.set_title('Safety Metrics', color='white', fontsize=12, pad=10)

    plt.savefig(out_path, dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    plt.close(fig)
