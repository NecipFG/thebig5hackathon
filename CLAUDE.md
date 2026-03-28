# The Big 5 - TUA Astro Hackathon

## Project Overview
Lunar rover autonomous pathfinding system for the TUA (Turkish Aerospace Agency) Astro Hackathon 2026. A 5-person team building A* pathfinding on real NASA LOLA lunar terrain data.

## Challenge Goal
Find safe, traversable paths for a lunar rover across 3 mission scenarios at the Moon's South Pole, using real elevation data.

## Core Technical Stack
- **Algorithm**: A* pathfinding on lunar DEM grid
- **Data source**: NASA LOLA (Lunar Orbiter Laser Altimeter) - South Pole DEM
- **Safety constraint**: Slopes < 20°, avoid craters/permanently shadowed regions
- **Visualization**: 3D terrain with overlaid paths (3 missions)

## Team Roles
| Person | Role | Key Deliverable |
|--------|------|-----------------|
| 1 | Data & Mission Designer | 3 mission scenarios with real lunar coordinates |
| 2 | Algorithm Developer | A* working on all 3 missions + metrics |
| 3 | Terrain & Validation Expert | Safety maps + validated paths report |
| 4 | Visualization & Demo Builder | Interactive 3D demo |
| 5 | Documentation & Presentation | 1-page summary, tech doc, 5-7 slides |

## Required Deliverables (Sunday 6 PM)
1. High-level summary (1 page, non-technical)
2. Technical approach (1-2 pages, algorithm explanation)
3. Working demo (runnable, 3 missions visible, interactive)
4. Live presentation (5-7 min pitch + demo walkthrough)

## Key Files
- `36HOUR_REAL_SPRINT_PLAN.md` — master timeline and per-person task breakdown
- `LUNAR_ROVER_CHALLENGE_GUIDE.md` — challenge rules, A* reference implementation, deliverable requirements
- `QUICK_REFERENCE_CARD.md` — condensed who-does-what reference
- `SATURDAY_MORNING_KICKOFF.md` — detailed first-3-hours guide
- `FRIDAY_NIGHT_PREP.md` — pre-hackathon team logistics checklist

## Critical Path
Person 1 (missions) → Person 2 (algorithm) → Person 3 (validation) + Person 4 (demo) → Person 5 (docs wrap-up)

Person 2's working algorithm by Saturday 8 PM is the hardest and most critical deadline.

## No existing code yet
All files are planning/strategy documents. Implementation starts Saturday morning.
