"""
Person 1 pipeline: DEM → missions.csv + clipped DEMs + preview PNGs.

Usage:
    python -m person1.main            # download real LOLA DEM (requires internet)
    python -m person1.main --synthetic  # use synthetic DEM (offline, for testing)

Outputs:
    output/missions.csv              → consumed by Person 2 (algorithm) and Person 3
    data/dem/mission{1,2,3}.tif      → consumed by Person 2 and Person 3
    output/mission_previews/*.png    → visual confirmation for Person 1
"""
import argparse
import csv
import os
import sys

from person1.missions_data import MISSIONS
from person1.dem_fetcher import download_dem, mission_bounding_box, clip_dem_to_mission
from person1.mission_checker import check_mission
from person1.mission_plotter import plot_mission
from person1.synthetic_dem import make_synthetic_dem


MISSIONS_CSV = "output/missions.csv"
PREVIEW_DIR = "output/mission_previews"


def run(synthetic: bool = False) -> int:
    """Run the full pipeline. Returns 0 on success, 1 on any validation failure."""
    os.makedirs("data/dem", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    os.makedirs(PREVIEW_DIR, exist_ok=True)

    # ── Step 1: Get full south pole DEM ─────────────────────────────────────
    if synthetic:
        print("[main] Using SYNTHETIC DEM (pass no --synthetic flag for real data)")
        full_dem_path = None  # clip from synthetic per-mission
    else:
        try:
            full_dem_path = download_dem()
        except Exception as e:
            print(f"[main] ERROR: DEM download failed: {e}")
            print("[main] TIP: Re-run with --synthetic to use a stand-in DEM")
            return 1

    # ── Step 2: Clip DEM to each mission region ──────────────────────────────
    for m in MISSIONS:
        dem_path = m["dem_file"]
        min_lat, min_lon, max_lat, max_lon = mission_bounding_box(
            m["start_lat"], m["start_lon"],
            m["goal_lat"], m["goal_lon"],
        )

        if synthetic:
            print(f"[main] Generating synthetic DEM for mission {m['id']} ...")
            make_synthetic_dem(
                min_lat=min_lat, max_lat=max_lat,
                min_lon=min_lon, max_lon=max_lon,
                dest_path=dem_path,
                seed=m["id"] * 100,
            )
        else:
            print(f"[main] Clipping DEM for mission {m['id']} ...")
            clip_dem_to_mission(
                full_dem_path,
                min_lat=min_lat, max_lat=max_lat,
                min_lon=min_lon, max_lon=max_lon,
                dest_path=dem_path,
            )

    # ── Step 3: Validate all missions ────────────────────────────────────────
    all_valid = True
    check_results = []
    for m in MISSIONS:
        result = check_mission(
            start_lat=m["start_lat"], start_lon=m["start_lon"],
            goal_lat=m["goal_lat"], goal_lon=m["goal_lon"],
            dem_path=m["dem_file"],
        )
        status = "✓" if result["valid"] else "✗"
        print(f"[main] Mission {m['id']} ({m['name']}): {status} {result['message']}")
        if not result["valid"]:
            all_valid = False
        check_results.append(result)

    if not all_valid:
        print("[main] ERROR: One or more missions failed validation. Aborting CSV write.")
        return 1

    # ── Step 4: Write missions.csv ───────────────────────────────────────────
    fieldnames = [
        "mission_id", "name", "difficulty",
        "start_lat", "start_lon", "start_row", "start_col",
        "goal_lat", "goal_lon", "goal_row", "goal_col",
        "dem_file", "objective",
    ]
    with open(MISSIONS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for m, r in zip(MISSIONS, check_results):
            writer.writerow({
                "mission_id": m["id"],
                "name": m["name"],
                "difficulty": m["difficulty"],
                "start_lat": m["start_lat"],
                "start_lon": m["start_lon"],
                "start_row": r["start_row"],
                "start_col": r["start_col"],
                "goal_lat": m["goal_lat"],
                "goal_lon": m["goal_lon"],
                "goal_row": r["goal_row"],
                "goal_col": r["goal_col"],
                "dem_file": m["dem_file"],
                "objective": m["objective"],
            })
    print(f"[main] Wrote {MISSIONS_CSV}")

    # ── Step 5: Generate preview PNGs ───────────────────────────────────────
    for m in MISSIONS:
        preview_path = os.path.join(PREVIEW_DIR, f"mission{m['id']}_preview.png")
        plot_mission(m, m["dem_file"], preview_path)

    print("\n[main] ✓ Pipeline complete.")
    print(f"       Deliverables ready in: {MISSIONS_CSV}  data/dem/  {PREVIEW_DIR}/")
    return 0


if __name__ == "__main__":
    if os.path.basename(os.getcwd()) != "thebig5hackathon":
        print("[main] WARNING: run from the repo root (thebig5hackathon/)")

    parser = argparse.ArgumentParser(description="Person 1 mission pipeline")
    parser.add_argument(
        "--synthetic", action="store_true",
        help="Use synthetic DEM instead of downloading real LOLA data",
    )
    args = parser.parse_args()
    sys.exit(run(synthetic=args.synthetic))
