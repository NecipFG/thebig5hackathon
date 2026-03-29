import numpy as np
from lunar_pathfinder import load_slope_from_tif, astar_search, generate_dummy_slope

slope = generate_dummy_slope(100, 100)
obstacle_mask = slope > 20.0
path = astar_search(slope, obstacle_mask, (10, 10), (90, 90))
print(f"Path length: {len(path) if path else 'None'}")
if path:
    # verify no 90 degree turns
    for i in range(2, len(path)-1):
        prev_dr = path[i-1][0] - path[i-2][0]
        prev_dc = path[i-1][1] - path[i-2][1]
        dr = path[i][0] - path[i-1][0]
        dc = path[i][1] - path[i-1][1]
        
        # Calculate dot product
        dot = prev_dr*dr + prev_dc*dc
        # If dot product is <= 0 and vectors are not (0,0), it's a 90+ degree turn
        if not (prev_dr == 0 and prev_dc == 0) and not (dr == 0 and dc == 0):
            if dot <= 0:
                print(f"FAILED: Found sharp turn at index {i}: ({prev_dr},{prev_dc}) to ({dr},{dc})")
                exit(1)
                
    print("SUCCESS: Path generated and smoothly curves without sharp turns!")

