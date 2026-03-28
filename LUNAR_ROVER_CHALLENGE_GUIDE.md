# 🌙 TUA Astro Hackathon 2026 - Autonomous Route Optimization for Lunar Surface
## Complete Challenge Breakdown & Data Resources

---

## 1. CHALLENGE DECODED ✅

### What You're Actually Building:
A **pathfinding algorithm** that enables Turkey's lunar rover to:
- ✅ Autonomously determine safe routes on the lunar surface
- ✅ Avoid craters, obstacles, and dangerous terrain
- ✅ Navigate from a start point to goal objectives
- ✅ Optimize for "safety" (minimize risks, avoid steep slopes)

### Key Questions Answered:

| Question | Answer |
|----------|--------|
| **Where does it land?** | You define the landing site (use real lunar coordinates) |
| **Where does it go?** | You set mission objectives (science targets, resource sites) |
| **Route or route-maker?** | **BOTH** - Build the algorithm that generates routes dynamically |
| **Autonomy?** | The rover figures out paths itself (not pre-programmed) |

### Deliverables Required:
1. ✅ High-level summary (what your solution does)
2. ✅ Detailed solution (how it works)
3. ✅ Technical approach (algorithms, implementation)

---

## 2. DATA SOURCES YOU CAN USE 🛰️

### NASA/Public Lunar Data (FREE):

#### **A. Terrain Data - Digital Elevation Models (DEMs)**
- **LOLA (Lunar Orbiter Laser Altimeter)**: High-resolution elevation data
  - Resolution: 5m per pixel at lunar poles
  - Source: NASA Planetary Data System
  - Download: https://pds-geosciences.wustl.edu/lunar/lro_lola_edr/
  
- **SLDEM2015**: Combined LOLA + Kaguya terrain map
  - Best available lunar topography
  - 512 pixels per degree resolution
  - Source: NASA PGDA

#### **B. Satellite Imagery**
- **LROC NAC** (Lunar Reconnaissance Orbiter Camera): High-res surface photos
- **Kaguya TC**: Stereo images covering 99% of lunar surface

#### **C. Pre-made Datasets for Path Planning**
- **MoonPlanBench**: 36 occupancy grids from lunar poles
  - Already converted to navigable maps
  - Paper: "Planetary Terrain Datasets and Benchmarks for Rover Path Planning"
  - GitHub: Check recent arxiv releases
  
- **LuSNAR Dataset**: Lunar segmentation with semantic labels
  - Available on Kaggle
  - 9,766 realistic rendered images
  - Includes rock/crater labels

---

## 3. ALGORITHM SELECTION 🤖

### What Works Best for Lunar Rovers:

#### **Graph-Based Algorithms (BEST FOR PLANETARY ROVERS)**
**Dijkstra's Algorithm**
- ✅ Guarantees shortest path
- ✅ Fastest computation among graph methods
- ✅ Used by NASA Mars rovers
- ❌ Requires full terrain mapping
- Performance: ~263m path length, 54s planning time

**A* (A-Star)**
- ✅ 35% faster than Dijkstra
- ✅ 11% shorter paths than Dijkstra
- ✅ Heuristic-guided search (smarter)
- ✅ Industry standard
- Performance: ~235m path, 35s planning

**Theta*** (Angle-Optimized A*)
- ✅ Smoother paths (fewer turns)
- ✅ Better for rover kinematics
- ✅ Similar speed to A*

#### **Sampling-Based Algorithms (FAST, NON-OPTIMAL)**
**RRT (Rapidly-exploring Random Tree)**
- ✅ Explores space quickly
- ✅ Works in high dimensions
- ✅ Handles complex terrain
- ❌ Slower (675s+), non-optimal paths
- ❌ Lots of turns/instability

**RRT* (RRT with optimization)**
- ✅ Asymptotically optimal
- ❌ Still slower than Dijkstra for 2D
- ✅ Good for 3D with terrain

### 🏆 RECOMMENDATION FOR YOUR TEAM:
**START WITH: A* or Theta***
- Simple to implement
- Proven on lunar terrains
- NASA-validated
- Fast enough for real-time operations

**OPTIMIZE WITH: RRT* (if terrain complexity is high)**
- Better for rough 3D surfaces
- Add traversability constraints

---

## 4. TECHNICAL APPROACH FRAMEWORK 🔧

### Your Solution Should Include:

#### **Step 1: Environment Representation**
```
Input: Digital Elevation Model (DEM) from lunar data
Process:
  - Convert DEM to occupancy grid
  - Define traversability thresholds:
    * Slope < 13° = safe
    * Slope 13-20° = caution zone
    * Slope > 20° = impassable
  - Mark craters/obstacles as obstacles
Output: 2D navigation map for algorithm
```

#### **Step 2: Start & Goal Definition**
```
Input: 
  - Rover landing coordinates (latitude/longitude)
  - Mission objective coordinates
Process:
  - Convert to map coordinates
  - Define safety margins around obstacles
Output: Start node, Goal node for pathfinding
```

#### **Step 3: Path Planning Algorithm**
```
Input: Navigation map, start, goal
Algorithm: A* or Theta*
Process:
  - Build search graph from occupancy map
  - Apply heuristic (straight-line distance to goal)
  - Expand nodes in order of f(n) = g(n) + h(n)
    * g(n) = actual cost from start
    * h(n) = estimated cost to goal
  - Return path when goal reached
Output: Sequence of waypoints
```

#### **Step 4: Path Optimization (Optional)**
```
- Remove redundant waypoints
- Smooth path with Bézier curves
- Add velocity constraints for rover physics
```

#### **Step 5: Safety Validation**
```
- Verify no segment crosses obstacle
- Calculate slope along entire path
- Estimate power consumption
- Generate risk metrics
```

---

## 5. DATA WORKFLOW FOR YOUR TEAM 📊

```
🌍 Step 1: Download Real Lunar Data
   └─> Get SLDEM2015 or LOLA DEM
   └─> For region: Lunar South Pole (mission focus)

📐 Step 2: Parse & Preprocess
   └─> Convert GeoTIFF to Python array
   └─> Extract region of interest (e.g., 50km x 50km)
   └─> Normalize elevation values

🗺️ Step 3: Create Navigation Map
   └─> Calculate slope at each pixel
   └─> Create occupancy grid (walkable = 0, obstacle = 1)
   └─> Set traversability thresholds

📍 Step 4: Define Test Cases
   └─> Choose 3-5 mission scenarios:
       * Short distance (5km)
       * Medium distance (20km) 
       * High-complexity terrain
       * Multiple waypoints
   └─> Set start/goal for each

🔍 Step 5: Run Algorithm
   └─> Input: occupancy map + start + goal
   └─> Output: path as waypoint sequence
   └─> Metrics: path length, planning time, safety score

📈 Step 6: Validate & Visualize
   └─> Plot path on original DEM
   └─> Show slope profile along path
   └─> Compare with baseline algorithms
```

---

## 6. TEAM ROLE ALLOCATION (5 People) 👥

### Role 1: **Data Engineer**
- Download lunar datasets
- Parse GeoTIFF/DEM files
- Create navigation maps
- Tools: Python, GDAL, numpy

### Role 2: **Algorithm Developer**
- Implement A* / Theta* 
- Handle graph construction
- Optimize search heuristics
- Tools: Python, C++, or custom

### Role 3: **Terrain & Validation**
- Define traversability rules
- Validate paths (no cliff crossing)
- Calculate safety metrics
- Tools: Python, matplotlib

### Role 4: **Visualization & Demo**
- Plot paths on lunar maps
- Create interactive visualizer
- 3D terrain rendering (if time)
- Tools: Python, Three.js, or WebGL

### Role 5: **Documentation Lead**
- Write high-level summary
- Create technical documentation
- Prepare presentation slides
- Tools: Markdown, Diagrams, PowerPoint

---

## 7. QUICK START: CODE SKELETON 🚀

### Basic A* Implementation
```python
import heapq
import numpy as np

def a_star(grid, start, goal):
    """
    grid: 2D array (0=free, 1=obstacle)
    start: (row, col)
    goal: (row, col)
    """
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    h_score = lambda pos: abs(pos[0]-goal[0]) + abs(pos[1]-goal[1])
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            # Reconstruct path
            path = [goal]
            while path[-1] in came_from:
                path.append(came_from[path[-1]])
            return path[::-1]
        
        # Check 4-neighbors (or 8 with diagonals)
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            neighbor = (current[0]+dr, current[1]+dc)
            
            # Check bounds and obstacles
            if not (0 <= neighbor[0] < grid.shape[0]):
                continue
            if not (0 <= neighbor[1] < grid.shape[1]):
                continue
            if grid[neighbor] == 1:
                continue
            
            tentative_g = g_score[current] + 1
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + h_score(neighbor)
                heapq.heappush(open_set, (f_score, neighbor))
    
    return None  # No path found
```

### Load & Preprocess DEM
```python
import rasterio
import numpy as np
from scipy import ndimage

# Load DEM
with rasterio.open('lunar_dem.tif') as src:
    dem = src.read(1)  # Read first band

# Calculate slope
gradient_x = np.gradient(dem, axis=1)
gradient_y = np.gradient(dem, axis=0)
slope = np.sqrt(gradient_x**2 + gradient_y**2)

# Create navigable map
threshold = 0.2  # slope threshold
nav_map = (slope > threshold).astype(int)

# Dilate obstacles (add safety margin)
nav_map = ndimage.binary_dilation(nav_map, iterations=3)

# Run A*
start = (100, 100)  # lunar coordinates
goal = (300, 300)
path = a_star(nav_map, start, goal)
```

---

## 8. RESOURCES & LINKS 🔗

### Data Downloads:
- NASA PDS LOLA: https://pds-geosciences.wustl.edu/lunar/lro_lola_edr/
- SLDEM2015: https://pgda.gsfc.nasa.gov/products/54
- LuSNAR Dataset: https://kaggle.com/datasets/...

### Key Papers (FREE on arXiv):
- "Planetary Terrain Datasets and Benchmarks" (2024)
- "Building Lunar Maps for Terrain Relative Navigation" (NASA)
- "A Comprehensive Review of Path-Planning Algorithms for Planetary Rovers" (2025)

### Tools:
- GDAL: Geospatial data handling
- QGIS: Visualize DEMs
- Python: rasterio, matplotlib, numpy
- ROS: Robotics framework (optional)

---

## 9. SUCCESS METRICS 📊

Judges will likely look for:
- ✅ **Algorithm correctness**: Finds valid paths without crossing obstacles
- ✅ **Safety optimization**: Minimizes slopes, crater proximity
- ✅ **Efficiency**: Fast planning (< 1 second for 50km² map)
- ✅ **Real data**: Uses actual lunar terrain (not synthetic)
- ✅ **Documentation**: Clear explanation of approach
- ✅ **Scalability**: Works for different map sizes
- ✅ **Visualization**: Nice demo/presentation

---

## 10. NEXT STEPS 🎯

### Before you code:
1. ✅ Download one lunar DEM (start small: 20km x 20km)
2. ✅ Visualize it in QGIS or Python
3. ✅ Choose A* as your primary algorithm
4. ✅ Define 3 test scenarios with real coordinates
5. ✅ Sketch your system architecture

### Divvy up work:
- **Data Engineer**: Download & parse DEM (2-3 hours)
- **Algorithm Dev**: Implement A* (4-6 hours)
- **Terrain**: Create nav maps & metrics (3-4 hours)
- **Viz**: Build demo/plots (3-4 hours)
- **Docs**: Write summaries (2-3 hours)

### MVP (Minimum Viable Product):
- A* finds path on real lunar DEM
- Path avoids craters/obstacles
- Visualized on map with slope profile
- One-page summary + code explanation

---

## Let's Go! 🚀

You've got this. The data exists, the algorithms are proven, and your team has 5 smart people. Focus on:
1. Real data (don't fake it)
2. Clean algorithm implementation
3. Safety validation
4. Good documentation

**Questions? Ask away!**
