"""
Person 3 — Terrain & Validation Pipeline

Usage:
    python -m person3.main --mission 1
    python -m person3.main --all

NOTE: Must be run from the repository root (thebig5hackathon/) so that
relative paths data/ and output/ resolve correctly.

Expects:
    data/dem/mission{N}.tif       — LOLA GeoTIFF from Person 1
    data/paths/mission{N}_path.json — path from Person 2: [[row,col],...]

Outputs (for Person 4 & 5):
    output/safety_maps/mission{N}_safety.png
    output/validation_results/mission{N}_result.json
    output/reports/mission{N}_report.png
"""
import argparse
import json
import os
import sys
import numpy as np

from person3.terrain_loader import load_dem
from person3.slope_calculator import compute_slope_degrees
from person3.hazard_mapper import build_safety_map, save_safety_map_png
from person3.path_validator import validate_path
from person3.report_generator import generate_safety_report


MISSIONS = {
    1: "Shackleton Crater Rim",
    2: "South Pole Aitken Basin Edge",
    3: "Haworth Crater Approach",
}


def process_mission(mission_id: int) -> dict:
    name = MISSIONS.get(mission_id, f"Mission {mission_id}")
    dem_path   = f"data/dem/mission{mission_id}.tif"
    path_file  = f"data/paths/mission{mission_id}_path.json"

    print(f"\n=== Processing {name} (Mission {mission_id}) ===")

    # 1. Load DEM
    print(f"  Loading DEM: {dem_path}")
    dem, pixel_size_m = load_dem(dem_path)
    print(f"  DEM shape: {dem.shape}, pixel size: {pixel_size_m:.1f} m/px")

    # 2. Compute slope
    print("  Computing slope...")
    slope = compute_slope_degrees(dem, pixel_size_m)

    # 3. Build safety map
    print("  Building safety map (threshold: 20°)...")
    safety = build_safety_map(slope, max_slope_deg=20.0)
    safe_pct = 100.0 * np.sum(safety == 0) / safety.size
    print(f"  Safe terrain: {safe_pct:.1f}%")

    # 4. Save safety map PNG
    os.makedirs("output/safety_maps", exist_ok=True)
    map_out = f"output/safety_maps/mission{mission_id}_safety.png"
    save_safety_map_png(safety, slope, map_out, mission_name=name)
    print(f"  Safety map saved: {map_out}")

    # 5. Load path from Person 2
    print(f"  Loading path: {path_file}")
    with open(path_file) as f:
        path = json.load(f)
    print(f"  Path waypoints: {len(path)}")

    # 6. Validate path
    print("  Validating path...")
    result = validate_path(path, safety, slope, pixel_size_m, mission_name=name)
    status = "PASS ✓" if result.passed else "FAIL ✗"
    print(f"  Verdict: {status}")
    print(f"  Hazard cells: {result.hazard_count} ({result.hazard_pct:.1f}%)")
    print(f"  Path length: {result.path_length_m/1000:.3f} km")
    print(f"  Max slope: {result.max_slope_deg:.1f}°  Mean: {result.mean_slope_deg:.1f}°")

    # 7. Save validation result JSON (for Person 5 to include in docs)
    os.makedirs("output/validation_results", exist_ok=True)
    result_out = f"output/validation_results/mission{mission_id}_result.json"
    result_dict = {
        "mission_id": mission_id,
        "mission_name": name,
        "passed": result.passed,
        "hazard_count": result.hazard_count,
        "hazard_pct": round(result.hazard_pct, 2),
        "path_length_km": round(result.path_length_m / 1000, 3),
        "max_slope_deg": round(result.max_slope_deg, 2),
        "mean_slope_deg": round(result.mean_slope_deg, 2),
        "waypoint_count": result.waypoint_count,
    }
    with open(result_out, 'w') as f:
        json.dump(result_dict, f, indent=2)
    print(f"  Validation result saved: {result_out}")

    # 8. Generate 1-page safety report
    os.makedirs("output/reports", exist_ok=True)
    report_out = f"output/reports/mission{mission_id}_report.png"
    generate_safety_report(result, safety, slope, path, report_out)
    print(f"  Safety report saved: {report_out}")

    return result_dict


def main():
    if not os.path.isdir('person3'):
        print("ERROR: Run this script from the repository root (thebig5hackathon/).", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Person 3: Terrain & Validation Pipeline")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--mission', type=int, choices=[1, 2, 3],
                       help="Process a single mission (1, 2, or 3)")
    group.add_argument('--all', action='store_true',
                       help="Process all 3 missions")
    args = parser.parse_args()

    mission_ids = [1, 2, 3] if args.all else [args.mission]

    all_results = []
    errors = []
    for mid in mission_ids:
        try:
            result = process_mission(mid)
            all_results.append(result)
        except Exception as exc:
            print(f"\n  [ERROR] Mission {mid} failed: {exc}")
            errors.append(mid)

    print("\n=== SUMMARY ===")
    for r in all_results:
        status = "PASS ✓" if r['passed'] else "FAIL ✗"
        print(f"  Mission {r['mission_id']} ({r['mission_name']}): {status} | "
              f"{r['path_length_km']:.3f} km | max slope {r['max_slope_deg']}°")
    for mid in errors:
        print(f"  Mission {mid}: ERROR (see above)")

    any_failed = errors or any(not r['passed'] for r in all_results)
    if any_failed:
        sys.exit(1)


if __name__ == '__main__':
    main()
