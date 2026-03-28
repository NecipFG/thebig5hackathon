# 🌙 QUICK REFERENCE - WHO DOES WHAT

## 5 PEOPLE. 48 HOURS. ONE WINNING SOLUTION.

---

## 👤 PERSON 1: DATA & MISSION DESIGNER
**When:** Starts FIRST (Thursday evening)  
**Hours:** 16 total (distributed)  
**Key Output:** Mission coordinates + terrain maps

```
YOUR JOB:
1. Download NASA lunar data (South Pole region)
2. Define 3 mission scenarios with REAL coordinates:
   - Scenario 1 (Easy): 15km, 1 waypoint
   - Scenario 2 (Medium): 40km, 3 waypoints  
   - Scenario 3 (Hard): Complex terrain, constraints
3. Create terrain analysis for each mission

DELIVERABLE FOR PERSON 2:
→ CSV: Landing site + objective coordinates
→ Document: Safety requirements, constraints

DELIVERABLE FOR PRESENTATION:
→ Map visualization of all 3 missions
→ 1-paragraph mission briefs
```

**Checkpoint:** Friday 9 AM (must be DONE)

---

## 🤖 PERSON 2: ALGORITHM DEVELOPER
**When:** Starts Thursday, main work Friday  
**Hours:** 20 total (concentrated Friday morning-afternoon)  
**Key Output:** Working pathfinding algorithm

```
YOUR JOB:
1. Understand A* algorithm (study, don't code yet)
2. Implement A* pathfinding
3. Run on all 3 missions from Person 1
4. Collect metrics: distance, time, safety score

DELIVERABLE FOR PERSON 4:
→ 3 complete paths (one per mission)
→ Metrics table (path length, planning time, etc.)

DELIVERABLE FOR PRESENTATION:
→ Algorithm explanation diagram
→ Performance metrics
→ 1-2 minute tech explanation
```

**Checkpoint:** Friday 3 PM (all 3 paths must work)

---

## 🗺️ PERSON 3: MISSION VALIDATOR & TERRAIN EXPERT
**When:** Parallel with Persons 1 & 2  
**Hours:** 14 total (Thursday evening + Friday)  
**Key Output:** Safety validation reports

```
YOUR JOB:
1. Understand terrain constraints (slopes, craters, etc.)
2. Create "safety maps" for each mission (green/yellow/red zones)
3. Validate all 3 paths from Person 2:
   ✓ Avoid craters?
   ✓ Slopes < 20°?
   ✓ Physically possible?
4. Calculate risk metrics

DELIVERABLE FOR PERSON 4:
→ Terrain maps (safe/unsafe zones)
→ Safety validation reports (1 per mission)
→ Risk metrics for all 3 paths

DELIVERABLE FOR PRESENTATION:
→ "Why this route is safe" analysis
→ Difficulty comparison chart
→ 1-minute safety briefing
```

**Checkpoint:** Friday 4 PM (all validations done)

---

## 🎨 PERSON 4: VISUALIZATION & DEMO BUILDER
**When:** Friday morning → Saturday morning  
**Hours:** 18 total (main work Friday)  
**Key Output:** Interactive web demo that judges play with

```
YOUR JOB:
1. Build beautiful 3D visualization of lunar terrain
2. Show all 3 mission paths on the map
3. Make it INTERACTIVE:
   - Toggle missions on/off
   - Show metrics on screen
   - Hover for details
   - (Optional) Rover animation
4. Polish design (professional look)

DELIVERABLE FOR PRESENTATION:
→ Live interactive demo (runnable on laptop)
→ All 3 scenarios visible
→ Metrics displayed
→ Mobile-friendly

INPUTS FROM:
← Person 1: Coordinates + terrain data
← Person 2: Final paths + metrics
← Person 3: Safety maps + validation results
```

**Checkpoint:** Friday 6 PM (demo is interactive + beautiful)

---

## 📝 PERSON 5: DOCUMENTATION, STRATEGY & PRESENTATION
**When:** Parallel with everyone (big push Friday afternoon)  
**Hours:** 15 total  
**Key Output:** 3 required documents + presentation slides

```
YOUR JOB:
1. Write HIGH-LEVEL SUMMARY (1-2 pages)
   → What problem? Why? What's your solution?
   → Audience: TUA leadership (non-technical)

2. Write TECHNICAL APPROACH (2-3 pages)
   → Which algorithm? Why? How does it work?
   → Diagrams showing flow

3. Write DETAILED SOLUTION (3-4 pages)
   → All 3 mission results
   → Performance data
   → Real data sources used

4. Create PRESENTATION SLIDES (5-7 slides)
   → Title → Problem → Solution → Results → Demo → Conclusion

REQUIRED DELIVERABLES:
→ High-Level Summary ✅
→ Technical Approach ✅
→ Detailed Solution ✅

BONUS DELIVERABLES:
→ Presentation slides ✅
→ Cohesive story ✅

INPUTS FROM:
← Everyone (collect all their work, tell the story)
```

**Checkpoint:** Friday 8 PM (all documents drafted)

---

## 📅 WHO WORKS WHEN

```
THURSDAY 6 PM - MIDNIGHT (First 6 hours)
├─ Person 1: START HERE (mission design)
├─ Person 2: Learn algorithm
├─ Person 3: Meet Person 1, understand constraints
├─ Person 4: Plan visualization approach
└─ Person 5: Strategy meeting, outline docs

FRIDAY 8 AM - 1 PM (Hours 6-17)
├─ Person 1: DELIVER mission scenarios ✓
├─ Person 2: Implement algorithm
├─ Person 3: Create terrain maps
├─ Person 4: Build 3D visualization
└─ Person 5: Write high-level + technical docs

FRIDAY 1 PM - 7 PM (Hours 17-29)
├─ Person 1: Done (standby)
├─ Person 2: Test all 3 missions, collect metrics
├─ Person 3: Validate all paths
├─ Person 4: Add interactive features
└─ Person 5: Write detailed solution, prep slides

FRIDAY 7 PM - MIDNIGHT (Hours 29-42)
├─ Everyone: Final polish
├─ Person 2: Algorithm optimization if needed
├─ Person 3: Final safety checks
├─ Person 4: Design perfection
└─ Person 5: Presentation slides + final review

SATURDAY 8 AM - 1 PM (Hours 42-48)
├─ Everyone: QA & testing
├─ Person 5: Final document polish
└─ All: REHEARSE PRESENTATION 3 TIMES
```

---

## ✅ CRITICAL CHECKPOINTS

**FRIDAY 9 AM**
- ☑ Person 1: All 3 missions defined with REAL coordinates
- ☑ Person 1: Terrain analysis complete

**FRIDAY 3 PM**
- ☑ Person 2: Algorithm works on all 3 missions
- ☑ Person 2: Metrics collected

**FRIDAY 4 PM**
- ☑ Person 3: All paths validated as SAFE
- ☑ Person 3: Safety reports complete

**FRIDAY 6 PM**
- ☑ Person 4: Demo is interactive + beautiful
- ☑ Person 4: All 3 missions visible

**FRIDAY 8 PM**
- ☑ Person 5: All 3 documents drafted
- ☑ Person 5: Presentation slides created

**FRIDAY MIDNIGHT**
- ☑ ALL: Polish in progress
- ☑ ALL: No major missing pieces
- ☑ If any checkpoint failed → FIX IT NOW

**SATURDAY NOON**
- ☑ ALL: Everything ready
- ☑ ALL: Rehearsed presentation 3 times
- ☑ ALL: Demo tested on judge's equipment

---

## 🎯 WHAT JUDGES ARE LOOKING FOR

| Judges Want | Your Answer |
|---|---|
| **Real Data?** | ✅ NASA LOLA DEM from actual lunar terrain |
| **Works?** | ✅ Algorithm tested on all 3 missions, results proven |
| **Safe?** | ✅ Person 3 validated every path against real constraints |
| **Scope?** | ✅ Not just pathfinding—3 complete mission scenarios |
| **Polish?** | ✅ Beautiful demo judges can interact with |
| **Clear?** | ✅ 3 documents explain everything TUA needs to know |

---

## 🚀 WORKLOAD REALITY CHECK

**Person 1:** 16 hours (front-loaded, then standby) ← EARLIEST DEADLINE  
**Person 2:** 20 hours (concentrated Friday morning/afternoon)  
**Person 3:** 14 hours (parallel with others)  
**Person 4:** 18 hours (Friday main push, Saturday polish)  
**Person 5:** 15 hours (distributed, big Friday afternoon push) ← LATEST DEADLINE  

**Total team effort:** ~82 hours spread across 5 people = **TOTALLY DOABLE**

---

## 💡 SUCCESS FORMULA

```
PERSON 1 defines: WHERE the rover goes (real coordinates)
        ↓
PERSON 2 plans: HOW it gets there (algorithm path)
        ↓
PERSON 3 validates: IS IT SAFE? (safety checks)
        ↓
PERSON 4 shows: HERE'S WHAT IT LOOKS LIKE (beautiful demo)
        ↓
PERSON 5 explains: HERE'S WHY THIS MATTERS (presentation)
        
        JUDGES IMPRESSED → YOU WIN 🏆
```

---

## ❌ THINGS THAT KILL YOU

- ❌ Fake/synthetic data (judges know)
- ❌ Algorithm doesn't work on all 3 missions
- ❌ No safety validation (rover gets stuck = fail)
- ❌ Bad presentation (can't explain in 7 minutes)
- ❌ Missing any of 3 required documents
- ❌ Running out of time Saturday (too late to fix)

---

## ✅ THINGS THAT WIN YOU

- ✅ Real NASA data
- ✅ 3 mission scenarios (not just 1)
- ✅ Proven safe paths
- ✅ Beautiful interactive demo
- ✅ Clear professional documentation
- ✅ Coherent 7-minute story
- ✅ Everything polished and finished

---

**PRINT THIS. READ IT. EXECUTE IT.**

🌙 **Now go build the future of lunar exploration.** 🚀
