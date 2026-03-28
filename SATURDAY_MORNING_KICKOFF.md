# 🌙 SATURDAY MORNING KICKOFF
## 9:00 AM - 12:00 PM (First 3 Hours)

**This document is for everyone. Read together before 9 AM.**

---

## ⏰ THE NEXT 36 HOURS

- **Saturday 9 AM → 8 PM:** Main work (11 hours)
- **Saturday 8 PM → 12 AM:** Final push (4 hours)
- **Saturday 12 AM → 7 AM:** SLEEP (5 hours mandatory)
- **Sunday 7 AM → 3 PM:** Final work (8 hours)
- **Sunday 3 PM → 6 PM:** Polish + present (3 hours)

**Total working time:** ~26 hours spread across 2 days

---

## 🎯 WHAT YOU'RE SHIPPING SUNDAY 6 PM

### Required (Non-negotiable):
1. ✅ **High-level summary** (1 page)
2. ✅ **Technical approach** (1-2 pages)
3. ✅ **Working demo** (interactive, shows all 3 missions)
4. ✅ **Live presentation** (5-7 minutes)

### Optional (Only if you finish early):
- Detailed results document
- Pretty slides
- Safety reports
- Metrics charts

**Strategy:** Get required stuff DONE first. Polish is bonus.

---

## 9:00 AM - 12:00 PM (First 3 Hours)

### FOR EVERYONE (30 minutes):
**9:00 - 9:30 AM**
- [ ] Read this kickoff guide
- [ ] Meet as a team
- [ ] Assign roles (confirm Person 1-5)
- [ ] Set communication channel (Slack/Discord/WhatsApp)
- [ ] Set up shared folder for deliverables
- [ ] Brief everyone on the challenge
- [ ] NO CODING YET

---

## PERSON 1: DATA & MISSION DESIGNER
**Time: 9:30 AM - 12:00 PM (2.5 hours)**

### What You Do:
1. Download lunar DEM file from NASA (takes 5-10 min)
2. Define 3 mission scenarios with real coordinates
3. Document everything so Person 2 & 3 can use it

### Detailed Steps:

**9:30 - 10:00 AM (30 min):**
- Go to: https://pds-geosciences.wustl.edu/lunar/lro_lola_edr/
- Search for: "South Pole" region (easiest, most interesting)
- Download one LOLA DEM file (~50-100 MB)
- Save to shared folder: `lunar_dem_south_pole.tif`
- Note the coordinates (latitude/longitude bounds in file)

**10:00 - 11:00 AM (60 min):**
- Open the file in QGIS (free) OR Python:
  ```python
  import rasterio
  with rasterio.open('lunar_dem_south_pole.tif') as src:
      print(src.bounds)  # Shows coordinates
      print(src.shape)   # Shows dimensions
  ```
- Identify 3 mission sites within the file:
  - **Site 1 (Easy):** Close to landing, simple terrain
  - **Site 2 (Medium):** Further, more complex
  - **Site 3 (Hard):** Very challenging terrain

- Write down for each site:
  - Latitude (e.g., -89.5°)
  - Longitude (e.g., 0°)
  - What's there? (e.g., "Shackleton Crater rim")
  - Distance from landing site (rough estimate)
  - Terrain type (flat, hilly, crater-filled)

**11:00 - 12:00 PM (60 min):**
- Create simple CSV file:
  ```
  mission_id,name,landing_lat,landing_lon,objective_lat,objective_lon,description,distance_km
  mission_1,Easy Science,−89.8,0,−89.5,0,Collect samples near Shackleton,15
  mission_2,Medium Explore,−89.8,0,−89.2,120,3 craters + temp survey,40
  mission_3,Hard Prospect,−90,0,−88.5,180,Resource-rich zone,50
  ```
- Save as: `missions.csv`
- Share with Person 2 & 3 (Slack/shared folder)
- DONE! (5 hours of work compressed to 2.5)

### What Person 2 Needs From You:
- CSV file with coordinates
- Coordinates MUST be real (check them twice)
- Distance estimate for each mission
- Brief description of each objective

### Don't do:
- ❌ Don't perfect the DEM
- ❌ Don't over-analyze terrain
- ❌ Don't make up coordinates
- ❌ Don't wait for Person 2

---

## PERSON 2: ALGORITHM DEVELOPER
**Time: 9:30 AM - 12:00 PM (2.5 hours)**

### What You Do:
1. Learn A* algorithm basics (if you don't know it)
2. Set up development environment
3. Start implementation once Person 1 shares coordinates

### Detailed Steps:

**9:30 - 10:00 AM (30 min):**
- [ ] Install Python 3.10+
- [ ] Create folder: `path_planning/`
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate it
- [ ] Install packages:
  ```bash
  pip install numpy matplotlib scipy
  ```
- [ ] Create file: `astar.py` (empty for now)

**10:00 - 11:30 AM (90 min):**
- [ ] Read A* algorithm basics (15 min):
  - It's a graph search algorithm
  - Uses heuristic (straight-line distance to goal)
  - Guarantees shortest path
  - Fast enough for real-time
  
- [ ] Wait for Person 1 to deliver `missions.csv` (should be ~10:30 AM)
- [ ] Once you have coordinates:
  - Load NASA DEM using rasterio
  - Extract region of interest around missions
  - Convert elevation map to occupancy grid (simple: slope > 20° = obstacle)

**11:30 AM - 12:00 PM (30 min):**
- [ ] Sketch implementation approach:
  - Load DEM
  - Create grid from DEM
  - Mark obstacles (craters, steep slopes)
  - Implement A* search
  - Run on first mission
  
- [ ] Don't code everything yet
- [ ] Just prepare structure

### What Person 3 & 4 Need From You (by Saturday 8 PM):
- 3 working paths (one per mission)
- Path format: list of coordinates: [(lat1, lon1), (lat2, lon2), ...]
- Metrics: path length (km), planning time (seconds)

### By Sunday 11 AM You Must Have:
- ✓ Algorithm works on all 3 missions
- ✓ All metrics collected
- ✓ Code is clean and commented
- ✓ Files saved and shared

### Don't do:
- ❌ Don't optimize yet
- ❌ Don't create beautiful visualization
- ❌ Don't overengineer
- ❌ Don't wait for perfect data

---

## PERSON 3: MISSION VALIDATOR & TERRAIN EXPERT
**Time: 9:30 AM - 12:00 PM (2.5 hours)**

### What You Do:
1. Understand what makes terrain "safe" for rovers
2. Wait for missions and paths
3. Validate them once delivered

### Detailed Steps:

**9:30 - 10:30 AM (60 min):**
- [ ] Study terrain constraints:
  - Safe slope: < 13° (basically flat)
  - Caution slope: 13-20° (rough but doable)
  - Impassable: > 20° (cliff)
  - Craters: stay 50m away minimum
  - Permanently shadowed regions: too cold, avoid if possible
  
- [ ] Create reference document:
  ```
  TERRAIN SAFETY RULES:
  - Green zone: slope < 13°
  - Yellow zone: slope 13-20°
  - Red zone: slope > 20° OR crater edge
  - Avoid permanently shadowed areas
  ```

**10:30 - 12:00 PM (90 min):**
- [ ] Wait for Person 1 to deliver missions (by 10:00 AM)
- [ ] Review missions:
  - Are coordinates real? ✓
  - Are distances reasonable? ✓
  - Is terrain described accurately? ✓
  - Are objectives clear? ✓
  
- [ ] Create simple terrain map for each mission:
  - Download DEM from Person 1
  - Calculate slope at each point
  - Create map: green (safe), yellow (risky), red (no-go)
  - Save 3 maps as images or text files
  
- [ ] Prepare validation checklist:
  ```
  Path validation checklist:
  ☐ Enters at landing site? 
  ☐ Exits at objective?
  ☐ Avoids red zones?
  ☐ Stays on green when possible?
  ☐ Path length reasonable?
  ☐ No impossible turns?
  ```

### What You'll Do Later (Sunday 7 AM):
- Receive 3 paths from Person 2
- Validate each path against safety rules
- Create 1-page validation report
- Share safety analysis with demo builder

### By Sunday 10 AM You Must Have:
- ✓ All paths validated
- ✓ Safety report written
- ✓ Terrain maps created
- ✓ Delivered to Person 4 & 5

### Don't do:
- ❌ Don't wait for algorithm to be perfect
- ❌ Don't overthink terrain rules
- ❌ Don't make up data
- ❌ Don't delay Person 2

---

## PERSON 4: VISUALIZATION & DEMO BUILDER
**Time: 9:30 AM - 12:00 PM (2.5 hours)**

### What You Do:
1. Plan visualization approach
2. Set up tools
3. Wait for data to start building

### Detailed Steps:

**9:30 - 10:00 AM (30 min):**
- [ ] Choose visualization framework (pick ONE):
  - **Easy:** Astro website + 2D maps (matplotlib/folium)
  - **Medium:** HTML5 + Canvas 3D rendering
  - **Ambitious:** Three.js for 3D terrain (most impressive)
  
- [ ] Set up project:
  - Create folder: `rover_demo/`
  - Create `index.html` (if HTML/Three.js)
  - Or create Astro project (if web framework)
  - Or create Jupyter notebook (if just Python)

**10:00 - 12:00 PM (120 min):**
- [ ] Plan visualization:
  - What do judges need to see?
    → Lunar terrain (elevation map as colors)
    → Landing site (marker)
    → Objectives (markers)
    → Rover path (line on terrain)
    → All 3 missions shown separately
  
- [ ] Sketch UI:
    → Map view
    → Mission selector (dropdown or buttons)
    → Metrics display (distance, time, safety score)
    → Play/pause animation (optional)

- [ ] Wait for data from Person 2 & 1:
  - Coordinates
  - Paths
  - Terrain data (DEM file)

### By Saturday 8 PM You Must Have:
- ✓ Terrain rendering working
- ✓ Paths visible on map
- ✓ All 3 missions selectable
- ✓ No crashes or major bugs

### By Sunday 1 PM You Must Have:
- ✓ Demo polished and beautiful
- ✓ Tested and smooth
- ✓ Ready for live presentation

### Don't do:
- ❌ Don't code before getting data
- ❌ Don't make it overly complex
- ❌ Don't overthink 3D graphics
- ❌ Don't delay starting once data arrives

---

## PERSON 5: DOCUMENTATION & PRESENTATION
**Time: 9:30 AM - 12:00 PM (2.5 hours)**

### What You Do:
1. Outline documents
2. Understand the big picture
3. Start writing high-level summary

### Detailed Steps:

**9:30 - 10:00 AM (30 min):**
- [ ] Create document structure:
  ```
  PROJECT/
  ├─ HIGH_LEVEL_SUMMARY.md (1 page)
  ├─ TECHNICAL_APPROACH.md (1-2 pages)
  ├─ RESULTS_SUMMARY.md (1 page)
  └─ PRESENTATION_SLIDES.pptx (5-7 slides)
  ```

- [ ] Create shared doc (Google Docs or Markdown):
  - Make it editable by whole team
  - Link in team chat

**10:00 - 11:30 AM (90 min):**
- [ ] Draft HIGH-LEVEL SUMMARY (1 page):
  - **Title:** "Autonomous Lunar Rover Navigation"
  - **Problem:** (What's the challenge?)
    → "Turkey is planning moon rovers"
    → "Rovers need to navigate autonomously"
    → "Current methods are manual/pre-planned"
  
  - **Solution:** (What did you build?)
    → "We built a pathfinding algorithm"
    → "Uses A* search on real lunar terrain"
    → "Finds safe routes between objectives"
  
  - **Why it matters:** (What's the impact?)
    → "Real NASA terrain data"
    → "Proven algorithm (industry standard)"
    → "3 mission scenarios tested"
  
  - **What's next:** (Where does it go?)
    → "Ready for rover implementation"
    → "Scalable to different lunar regions"

**11:30 AM - 12:00 PM (30 min):**
- [ ] Draft TECHNICAL APPROACH outline:
  - Algorithm choice: A*
  - Why A*: fast, proven, optimal
  - Terrain representation: occupancy grid
  - Safety validation: slope constraints
  - Data source: NASA LOLA DEM
  
- [ ] Don't write full documents yet
- [ ] Just outline + skeleton

### By Saturday 8 PM You Must Have:
- ✓ High-level summary drafted (rough)
- ✓ Technical outline done

### By Sunday 3 PM You Must Have:
- ✓ All 3 documents polished
- ✓ Presentation slides created
- ✓ Everything proof-read

### By Sunday 6 PM You Must Deliver:
- ✓ Slides printed/ready for live demo
- ✓ Documents submitted to judges
- ✓ Presentation practiced 2x

### Don't do:
- ❌ Don't wait for perfect data
- ❌ Don't over-write (1 page is enough)
- ❌ Don't ignore typos
- ❌ Don't forget about other people's work

---

## ✅ 12:00 PM STATUS CHECK

After first 3 hours, check these boxes:

- [ ] **Person 1:** Missions defined in CSV (shared with team)
- [ ] **Person 2:** Development environment ready, waiting for data
- [ ] **Person 3:** Terrain rules documented, validation plan ready
- [ ] **Person 4:** Demo framework set up, ready to build
- [ ] **Person 5:** Document outlines created, started drafting

**If all boxes checked:** On track. Keep going.

**If any box unchecked:** Fix it before moving on.

---

## CRITICAL POINTS

### Saturday 8 PM (MUST HAVE):
1. ✅ Algorithm works on all 3 missions (hardest deadline)
2. ✅ Missions defined and locked
3. ✅ Demo started and renders terrain
4. ✅ High-level summary drafted

### Sunday 11 AM (MUST HAVE):
1. ✅ Algorithm works (Person 2 done)
2. ✅ Paths validated (Person 3 done)
3. ✅ Demo is beautiful (Person 4 done)
4. ✅ Documents drafted (Person 5 done)

### Sunday 3 PM (MUST HAVE):
1. ✅ Everything exists and works
2. ✅ No major bugs
3. ✅ Ready to present

---

## COMMUNICATION PROTOCOL

### Daily check-ins:
- **12:00 PM (Saturday):** 15-minute standup - everyone says what they have/need
- **5:00 PM (Saturday):** 10-minute check - anyone stuck?
- **8:00 PM (Saturday):** 5-minute checkpoint - ready to sleep?
- **10:00 AM (Sunday):** 10-minute standup - what's left?

### Escalation:
- **Person 2's algorithm broken?** → Everyone helps immediately
- **Person 1 behind?** → Person 5 creates dummy missions to unblock others
- **Person 4's demo crashes?** → Simplify immediately (text output is fine)
- **Person 5 slowing down?** → Others help write docs

---

## FOOD & SLEEP STRATEGY

**Saturday Afternoon (3-8 PM):**
- Have snacks available
- Stay hydrated (water, coffee)
- Stretch every hour

**Saturday 8 PM - 12 AM:**
- Push hard but know when to quit
- Stop at midnight NO MATTER WHAT
- Go to sleep

**Saturday 12 AM - 7 AM:**
- SLEEP (non-negotiable)
- Set alarms
- Don't negotiate this

**Sunday 7 AM Onward:**
- Light breakfast
- Coffee/energy drinks OK
- Lunch around 12 PM
- Final push 3-6 PM

---

## YOU'VE GOT THIS

You have 36 hours. You have clear roles. You have a real problem to solve. You have real lunar data to use.

By Sunday 6 PM, you'll have:
- ✅ A working algorithm
- ✅ Real mission scenarios
- ✅ A beautiful demo
- ✅ Professional documentation
- ✅ A 5-minute pitch

That's a winner.

**Go start at 9 AM. Come back Sunday evening with a trophy.** 🌙🚀

---

**Last thing:** This is your playbook. Adapt it. If something isn't working, change it. If someone finishes early, they help others. If something breaks, you fix it together.

You're a team. Act like it.

Go. 🚀
