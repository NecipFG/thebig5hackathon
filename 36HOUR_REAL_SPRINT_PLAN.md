# 🌙 TUA Astro Hackathon 2026 - ACTUAL 36-HOUR SPRINT
## Saturday Morning → Sunday Evening (Real Timing)

**Reality:** You get ~36 actual working hours (not 48). Plan for sleep Sat night, power through Sun.

---

## 🎯 WHAT YOU'RE SHIPPING BY SUNDAY 6 PM

### Absolute Must-Haves (Non-Negotiable):
1. ✅ **3 Mission Scenarios** - Real lunar coordinates, defined objectives
2. ✅ **Pathfinding Algorithm** - A* working on all 3 missions
3. ✅ **Safety Validation** - Proof all paths are safe
4. ✅ **Working Demo** - Interactive visualization (doesn't need to be beautiful, just works)
5. ✅ **High-Level Summary** - 1 page explaining your solution (TUA leadership read this)
6. ✅ **Technical Approach** - 1-2 pages, algorithm explanation
7. ✅ **Live Presentation** - 5-7 minute pitch that makes sense

### Nice-to-Have (Polish if You Have Time):
- Detailed solution document (3-4 pages)
- Presentation slides
- Beautiful visualizations
- Safety reports with fancy charts

**Strategy:** Get the must-haves DONE first. Sunday morning is cleanup, not building.

---

## 📋 TEAM ASSIGNMENTS (Same 5 People, Aggressive Timeline)

### **PERSON 1: Data & Mission Designer**
**Total Time:** 12 hours (Saturday morning → afternoon → evening)

**SATURDAY 9 AM - 12 PM (3 hours)**
- Download lunar DEM for South Pole (NASA LOLA)
- Identify 3 mission sites with real coordinates
- Define objectives for each (craters, samples, etc.)
- Document in simple CSV: latitude, longitude, description

**SATURDAY 12 PM - 3 PM (3 hours)**
- Validate coordinates are real and reachable
- Create terrain descriptions (slopes, obstacles)
- Deliver to Person 2 & 3

**SATURDAY 3 PM - 8 PM (5 hours)**
- Create simple mission briefs (1 paragraph each)
- Make coordinate/terrain data available
- Standby for questions from Person 2/3

**BY SATURDAY 8 PM:** Mission scenarios LOCKED. Everyone else can work.

---

### **PERSON 2: Algorithm Developer**
**Total Time:** 18 hours (Saturday afternoon through Sunday evening)

**SATURDAY 9 AM - 12 PM (3 hours)**
- Study A* algorithm basics
- Set up development environment
- Wait for Person 1 deliverable

**SATURDAY 12 PM - 3 PM (3 hours)**
- RECEIVE missions from Person 1
- Start implementing A* pathfinding
- Test on first mission (simple grid-based version first)

**SATURDAY 3 PM - 8 PM (5 hours)**
- Get A* working on all 3 missions
- Collect basic metrics: path length, planning time
- Debug any issues

**SATURDAY 8 PM - 12 AM (4 hours)**
- Optimize algorithm if still broken
- Have 3 working paths ready
- Get some sleep (4-5 hours minimum)

**SUNDAY 7 AM - 11 AM (4 hours)**
- Wake up, test paths still work
- Final metrics collection
- Deliver to Person 4

**BY SUNDAY 11 AM:** Algorithm works. Paths exist. Done.

---

### **PERSON 3: Mission Validator & Terrain Expert**
**Total Time:** 14 hours (Saturday afternoon → evening → Sunday morning)

**SATURDAY 9 AM - 12 PM (3 hours)**
- Understand terrain constraints
- Wait for Person 1 missions

**SATURDAY 12 PM - 5 PM (5 hours)**
- RECEIVE missions
- Create simple terrain safety maps
- Validate Person 1's terrain descriptions

**SATURDAY 5 PM - 8 PM (3 hours)**
- RECEIVE paths from Person 2
- Quick validation:
  - ✓ Path avoids craters?
  - ✓ Slopes < 20°?
  - ✓ Physically possible?
- Flag any problems back to Person 2

**SATURDAY 8 PM - 12 AM (2 hours)**
- Final validation pass
- Get sleep (4-5 hours)

**SUNDAY 7 AM - 10 AM (3 hours)**
- Wake up, spot-check validation still valid
- Create simple 1-page safety report
- Deliver to Person 5 & 4

**BY SUNDAY 10 AM:** All paths validated. Safety approved. Done.

---

### **PERSON 4: Visualization & Demo Builder**
**Total Time:** 20 hours (Saturday evening → Sunday afternoon)

**SATURDAY 9 AM - 5 PM (8 hours)**
- Design visualization approach (no coding yet)
- Set up tools/framework
- Wait for Person 2 paths
- Wait for Person 1 coordinates

**SATURDAY 5 PM - 8 PM (3 hours)**
- RECEIVE paths from Person 2
- RECEIVE coordinates from Person 1
- Start building basic 3D terrain visualization
- Get terrain rendering working

**SATURDAY 8 PM - 12 AM (4 hours)**
- Overlay paths on terrain
- Make sure all 3 missions visible
- Basic interactivity (toggle missions on/off)
- Get sleep (4-5 hours)

**SUNDAY 7 AM - 1 PM (6 hours)**
- Wake up, check if demo still runs
- Polish interactions
- Add metrics display
- Final visual check

**SUNDAY 1 PM - 3 PM (2 hours)**
- Final testing, no lag
- Ready for live demo Sunday evening

**BY SUNDAY 3 PM:** Demo works. Ready to present. Done.

---

### **PERSON 5: Documentation, Strategy & Presentation**
**Total Time:** 16 hours (Saturday morning → evening → Sunday afternoon)

**SATURDAY 9 AM - 12 PM (3 hours)**
- Meet team, understand strategy
- Start outline of documents
- Collect info from everyone

**SATURDAY 12 PM - 4 PM (4 hours)**
- Write HIGH-LEVEL SUMMARY (1 page):
  - What problem? Why does Turkey need this?
  - What's your solution in plain English?
  - Why is it better?
- Make it scannable, non-technical

**SATURDAY 4 PM - 8 PM (4 hours)**
- Write TECHNICAL APPROACH (1-2 pages):
  - Which algorithm? (A*)
  - Why that algorithm?
  - How does it work on lunar terrain?
  - Simple diagram: terrain → algorithm → path
- Make it clear but technical

**SATURDAY 8 PM - 12 AM (2 hours)**
- Get sleep (4-5 hours)

**SUNDAY 7 AM - 11 AM (4 hours)**
- Wake up, collect all final results from everyone
- Write final 1-page SUMMARY OF RESULTS:
  - All 3 missions worked
  - Metrics (path length, time, safety)
  - Real data used (LOLA)

**SUNDAY 11 AM - 1 PM (2 hours)**
- Create 5-7 PRESENTATION SLIDES:
  - Slide 1: Title + problem
  - Slide 2: Your solution (A* algorithm)
  - Slide 3: 3 mission scenarios
  - Slide 4: Results (metrics table)
  - Slide 5: "Here's the demo" (transition to live)
  - Slide 6: Conclusion (why this matters for Turkey)

**SUNDAY 1 PM - 3 PM (2 hours)**
- Final polish on all documents
- Ready to present

**BY SUNDAY 3 PM:** All documents done. Presentation ready. Done.

---

## 🕐 MASTER TIMELINE (Who Works When)

### SATURDAY

```
9:00 AM - HACKATHON STARTS
│
├─ PERSON 1: Mission design (9 AM - 8 PM)
│  └─ 9-12: Download data, define 3 sites
│  └─ 12-3: Validate, document
│  └─ 3-8: Mission briefs, DELIVER ✓
│
├─ PERSON 2: Algorithm setup (9 AM - 12 AM)
│  └─ 9-12: Study, setup, wait for P1
│  └─ 12-3: RECEIVE P1, start implementation
│  └─ 3-8: Get A* working
│  └─ 8-12: Debug, optimize, DELIVER ✓
│  └─ SLEEP 12 AM - 7 AM
│
├─ PERSON 3: Terrain expert (9 AM - 12 AM)
│  └─ 9-12: Study constraints, wait
│  └─ 12-5: RECEIVE P1, terrain maps
│  └─ 5-8: RECEIVE P2 paths, validate
│  └─ 8-12: Final validation
│  └─ SLEEP 12 AM - 7 AM
│
├─ PERSON 4: Visualization (9 AM - 12 AM)
│  └─ 9-5: Design, setup, wait
│  └─ 5-8: RECEIVE P1 coords, P2 paths
│  └─ 8-12: Build terrain + paths
│  └─ SLEEP 12 AM - 7 AM
│
└─ PERSON 5: Documentation (9 AM - 12 AM)
   └─ 9-12: Strategy, outline
   └─ 12-4: High-level summary (1 page)
   └─ 4-8: Technical approach (2 pages)
   └─ 8-12: Sleep prep
   └─ SLEEP 12 AM - 7 AM

12:00 AM (MIDNIGHT)
└─ EVERYONE: Sleep 5 hours (hard stop)
```

### SUNDAY

```
7:00 AM - EVERYONE WAKES UP
│
├─ PERSON 2: Final check + metrics
│  └─ 7-11: Test algorithm, collect metrics
│  └─ 11 AM: DELIVER to P4, P5 ✓
│
├─ PERSON 3: Validation report
│  └─ 7-10: Final safety check
│  └─ 10 AM: DELIVER ✓
│
├─ PERSON 4: Demo polish
│  └─ 7-1 PM: Test, polish, optimize
│  └─ 1-3 PM: Final demo ready
│  └─ 3 PM: DELIVER ✓
│
└─ PERSON 5: Final documents + slides
   └─ 7-11: Results summary
   └─ 11-1: Presentation slides
   └─ 1-3: Polish all
   └─ 3 PM: DELIVER ✓

3:00 PM - EVERYTHING READY
│
└─ SUNDAY 3-6 PM
   ├─ REHEARSE PRESENTATION 2x
   ├─ TEST DEMO 3x
   ├─ Review all documents
   └─ Final fixes (small stuff only)

6:00 PM - SUBMISSION DEADLINE
│
└─ SUBMIT:
   ├─ High-level summary ✓
   ├─ Technical approach ✓
   ├─ Results summary ✓
   ├─ Demo (runnable) ✓
   ├─ Slides ✓
   └─ Any bonus materials
```

---

## ⚠️ CRITICAL CHECKPOINTS (DON'T MISS)

**SATURDAY 8 PM - Person 1 Must Be DONE**
- No working algorithm if missions aren't defined
- Sleep is non-negotiable after this
- Everyone else can work Sunday while P1 rests

**SATURDAY 8 PM - Person 2 Must Have Working Algorithm**
- Not pretty, but must work on all 3 missions
- Person 4 can't build demo without paths
- This is the hardest deadline

**SUNDAY 10 AM - Person 3 Must Validate**
- Person 4 needs safety data for demo
- Must happen before demo is shown to judges

**SUNDAY 1 PM - Person 5 Must Have Slides**
- Presentation is at 6 PM
- Need time to rehearse
- Slides + high-level summary are minimum

**SUNDAY 3 PM - EVERYTHING MUST EXIST**
- If anything is missing, it's too late
- Demo must run
- Documents must exist
- No exceptions

---

## 🎯 SATURDAY NIGHT DECISION POINT (8 PM)

### If Everything is On Track:
✅ Algorithm works  
✅ Missions defined  
✅ Demo skeleton started  
✅ High-level summary drafted  

→ **Go to sleep.** You'll win.

### If Algorithm is Broken:
❌ Algorithm doesn't work on all missions  

→ **STOP everything else. Everyone helps Person 2 until fixed.**
- Person 1 done anyway
- Person 3 spot-checks basics
- Person 4 waits
- Person 5 works on docs

### If Missions Aren't Defined:
❌ Person 1 still working  

→ **CRITICAL. Use generic missions to unblock Person 2.**
- Give Person 2 dummy coordinates (doesn't matter if realistic)
- Algorithm works on ANY terrain
- Person 1 fixes real missions Sunday morning
- Everyone else proceeds

---

## 📦 ABSOLUTE MINIMUM TO WIN (Sunday 6 PM)

You MUST submit:
1. ✅ **High-level summary** (1 page) - TUA reads this first
2. ✅ **Technical approach** (1 page) - How algorithm works
3. ✅ **Working demo** - Runnable, shows 3 missions, paths visible
4. ✅ **Live presentation** - 5 min pitch + demo walkthrough

**Optional but nice:**
- Detailed results document
- Presentation slides
- Safety validation report
- Metrics table

---

## 💾 DELIVERABLE CHECKLIST

### PERSON 1 - Saturday 8 PM:
- [ ] 3 mission scenarios defined
- [ ] Real lunar coordinates
- [ ] Objective descriptions
- [ ] Terrain notes (slopes, obstacles)
- [ ] Shared with Person 2 & 3

### PERSON 2 - Sunday 11 AM:
- [ ] A* algorithm implemented
- [ ] Works on all 3 missions
- [ ] Metrics collected (path length, time)
- [ ] 3 path files ready
- [ ] Shared with Person 4 & 5

### PERSON 3 - Sunday 10 AM:
- [ ] Terrain safety maps created
- [ ] All 3 paths validated
- [ ] Quick safety report (1 page)
- [ ] Shared with Person 4 & 5

### PERSON 4 - Sunday 3 PM:
- [ ] 3D terrain visualization built
- [ ] All 3 missions visible
- [ ] Paths overlay working
- [ ] Metrics displayed
- [ ] No lag, fully interactive
- [ ] Tested on demo equipment

### PERSON 5 - Sunday 3 PM:
- [ ] High-level summary (1 page)
- [ ] Technical approach (1-2 pages)
- [ ] Results summary (1 page)
- [ ] Presentation slides (5-7)
- [ ] All documents polished
- [ ] Presentation rehearsed 2x

---

## 🚨 WHAT KILLS YOU IN 36 HOURS

❌ **Overthinking:** Don't. Use real data, simple A*, basic demo.  
❌ **Waiting for perfect:** Done is better than perfect. Ship working MVP.  
❌ **Not sleeping Saturday:** 5 hours minimum or you'll crash Sunday.  
❌ **Missing checkpoints:** If Person 2's algorithm doesn't work by Saturday 8 PM, you lose.  
❌ **Skipping validation:** Person 3's safety check is NOT optional.  
❌ **No demo:** A runnable demo beats 50 pages of docs.  
❌ **Bad presentation:** Even perfect solution fails with bad pitch.

---

## ✅ WHAT WINS YOU IN 36 HOURS

✅ **Real data:** NASA LOLA (not fake)  
✅ **Working algorithm:** A* on all 3 missions (not theoretical)  
✅ **3 scenarios:** Easy + medium + hard (proves robustness)  
✅ **Safety validation:** Paths actually safe (not guessed)  
✅ **Live demo:** Interactive, clickable, judges play with it  
✅ **Clear docs:** High-level summary is 1 page, TUA leadership understands  
✅ **Good pitch:** 5-minute story that makes sense  

---

## 📍 REALISTIC EXPECTATIONS

### By Saturday 8 PM:
- Missions defined ✓
- Algorithm working ✓
- Demo started (rough) ✓
- High-level summary drafted ✓

### By Sunday 3 PM:
- Algorithm polished ✓
- Demo looks good ✓
- All docs complete ✓
- Ready to present ✓

### By Sunday 6 PM:
- SUBMIT and celebrate 🎉

---

## 🎬 PRESENTATION SCRIPT (5-7 minutes)

**Person 5 says (2 minutes):**
- "Turkey is planning to send rovers to the moon."
- "Rovers need to navigate autonomously."
- "We built an algorithm that finds safe paths."
- "It uses A* pathfinding on real lunar terrain."

**Person 4 says (3-4 minutes):**
- Demo walkthrough
- Click through all 3 missions
- Show paths on terrain
- Explain why each path is safe

**Person 5 closes (1 minute):**
- "This is mission-ready technology."
- "Real lunar data. Proven algorithm. Safe paths."
- "Turkey's rovers will navigate the moon with this."

---

## 💡 SATURDAY NIGHT PRE-SLEEP CHECKLIST

Before you sleep Saturday midnight:

- [ ] Person 1: Missions locked, shared with team
- [ ] Person 2: Algorithm works on all 3, CRITICAL
- [ ] Person 3: Validation started, terrain maps ready
- [ ] Person 4: Demo runs (rough is fine), no crashes
- [ ] Person 5: High-level summary drafted, outline done
- [ ] Everyone: Phones charging, alarms set for 7 AM
- [ ] Everyone: 4-5 hours of sleep (non-negotiable)

If ANY checkbox is unchecked → Stay up and fix it. Sleep after, not before.

---

## 🚀 YOU'VE GOT THIS

36 hours. 5 people. Clear roles. Real moon data. Working demo.

This is tight. This is real. This is how engineers actually work.

**Saturday morning:** Start strong.  
**Saturday night:** Push hard, then sleep.  
**Sunday morning:** Wake up, finish.  
**Sunday evening:** Present and win.

Go.

---

## 📞 EMERGENCY CONTACTS

**If algorithm is broken Saturday 8 PM:**
→ Everyone helps Person 2. Use dummy data if needed.

**If demo won't render Sunday morning:**
→ Simplify. Text output is fine. Static image is fine. Just works.

**If documents aren't done Sunday 2 PM:**
→ High-level summary is minimum. Everything else is bonus.

**If presentation feels weak:**
→ Keep it simple: Problem → Solution → Demo → Impact.

---

**Now go. You're starting Saturday morning. Come back Sunday 6 PM with a winner.** 🌙🚀
