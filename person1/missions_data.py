"""
Mission definitions for the TUA Astro Hackathon 2026.

3 scenarios at the Lunar South Pole using real named crater landmarks.
Coordinates are geographic (latitude/longitude in degrees).

Mission 1 — Shackleton Rim (Easy, ~6 km)
  Shackleton crater sits at -89.67°, nearly at the pole itself.
  The rim receives near-continuous sunlight and is a prime target.

Mission 2 — de Gerlache Basin (Medium, ~22 km)
  de Gerlache crater at -88.55°, 274.7° — a large south pole basin.
  Path crosses mixed terrain with moderate slopes.

Mission 3 — Haworth to Nobile (Hard, ~38 km)
  Haworth crater at -87.47°, 4.58° to the Nobile region.
  Longest traverse; crosses permanently shadowed region boundaries.
"""

MISSIONS = [
    {
        "id": 1,
        "name": "Shackleton Rim",
        "difficulty": "easy",
        "start_lat": -89.68,
        "start_lon": 0.00,
        "goal_lat": -89.50,
        "goal_lon": 45.00,
        "dem_file": "data/dem/mission1.tif",
        "objective": "Crater rim surface sample survey",
    },
    {
        "id": 2,
        "name": "de Gerlache Basin",
        "difficulty": "medium",
        "start_lat": -88.55,
        "start_lon": 274.70,
        "goal_lat": -87.80,
        "goal_lon": 265.00,
        "dem_file": "data/dem/mission2.tif",
        "objective": "Solar wind deposit sampling",
    },
    {
        "id": 3,
        "name": "Haworth to Nobile",
        "difficulty": "hard",
        "start_lat": -87.47,
        "start_lon": 4.58,
        "goal_lat": -85.50,
        "goal_lon": 45.00,
        "dem_file": "data/dem/mission3.tif",
        "objective": "Permanently shadowed region boundary survey",
    },
]
