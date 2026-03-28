# 📋 FRIDAY NIGHT PREP CHECKLIST
## Before You Sleep Tonight (Friday)

**Do these things TONIGHT so you're ready Saturday 9 AM.**

---

## 👥 TEAM LOGISTICS

- [ ] Confirm all 5 team members are attending Saturday (phone/message them NOW)
- [ ] Assign roles (Person 1-5) - get confirmation from each person
- [ ] Create communication channel (Slack, Discord, WhatsApp group chat)
- [ ] Share all documents with team:
  - `36HOUR_REAL_SPRINT_PLAN.md`
  - `SATURDAY_MORNING_KICKOFF.md`
  - `QUICK_REFERENCE_CARD.md` (print this one)
  - This checklist
- [ ] Set Saturday morning alarm for 8:30 AM (be early)
- [ ] Share venue/meeting location with everyone

---

## 💻 TECHNICAL SETUP (Each Person Does Their Part)

### PERSON 1 (Data & Mission Designer):
- [ ] Download and install QGIS (free, takes 10 min)
  → https://qgis.org/download/
- [ ] OR make sure you have Python 3.10+ with rasterio library installed
  ```bash
  pip install rasterio numpy
  ```
- [ ] Test you can read GeoTIFF files (practice on a sample)
- [ ] Have a text editor ready for CSV creation
- [ ] Bring: laptop with 100GB+ free disk space (DEM files are large)

### PERSON 2 (Algorithm Developer):
- [ ] Install Python 3.10+ (if not already)
- [ ] Install required packages:
  ```bash
  pip install numpy scipy matplotlib
  ```
- [ ] Create a GitHub or shared folder for code
- [ ] Familiarize yourself with A* algorithm (15 min YouTube video)
  → Search "A* pathfinding algorithm explained"
- [ ] Have a code editor ready (VS Code, PyCharm, etc.)
- [ ] Test you can run Python code from terminal

### PERSON 3 (Mission Validator):
- [ ] Understand terrain constraints (read the section in documents)
- [ ] Download QGIS or matplotlib (to visualize terrain maps)
- [ ] Prepare a spreadsheet template for validation:
  ```
  mission,slope_check,crater_check,distance_ok,energy_ok,validated
  mission_1,✓,✓,✓,✓,YES
  mission_2,✓,✓,✓,✓,YES
  mission_3,?,?,?,?,pending
  ```
- [ ] Have terrain reference guide ready

### PERSON 4 (Visualization & Demo Builder):
- [ ] Decide on visualization technology (Three.js, matplotlib, or canvas)
- [ ] Install necessary tools:
  - If Three.js: Node.js + npm
  - If matplotlib: Python 3.10+
  - If Astro: Node.js + npm
- [ ] Create a Hello World demo in your chosen tech
  - Make sure it runs without errors
  - Test on your laptop
- [ ] Bring: charger for laptop (you'll need it)

### PERSON 5 (Documentation & Presentation):
- [ ] Set up document system (Google Docs or Markdown repo)
- [ ] Create template documents:
  - High-level summary (1 page template)
  - Technical approach (outline)
  - Results summary (outline)
  - Presentation slides (5-7 blank slides)
- [ ] Share links with team
- [ ] Install a markdown editor if using Markdown (VS Code, Obsidian)
- [ ] Practice what a good 5-minute pitch sounds like (watch TED talk example)

---

## 🗺️ DATA PREP

### To know before Saturday:
- [ ] Where is the hackathon venue? (address, how to get there)
- [ ] Will there be WiFi? (check upload/download speeds)
- [ ] Is there food/coffee provided?
- [ ] What time do judging presentations start?
- [ ] Can you submit files online or in-person?

### Resources you should bookmark:
- [ ] NASA LOLA DEM download: https://pds-geosciences.wustl.edu/lunar/lro_lola_edr/
- [ ] SLDEM2015 alternative: https://pgda.gsfc.nasa.gov/products/54
- [ ] Python rasterio docs: https://rasterio.readthedocs.io/
- [ ] A* algorithm reference: https://en.wikipedia.org/wiki/A*_search_algorithm

---

## 📱 COMMUNICATION

- [ ] Add everyone to chat group NOW (test that messages send/receive)
- [ ] Have phone numbers of all 4 teammates in your phone
- [ ] Set group chat name: "🌙 TUA Astro Hackathon Team"
- [ ] Pin important info (venue, deadline, contacts)
- [ ] Agree on check-in schedule:
  - Saturday 12 PM: First standup
  - Saturday 5 PM: Mid-day check
  - Saturday 8 PM: Before sleep check
  - Sunday 10 AM: Wake up check

---

## 🎯 MINDSET PREP

- [ ] Read the challenge description one more time
- [ ] Watch one A* algorithm explanation video (15 min)
- [ ] Believe in your team
- [ ] Remember: Done > Perfect
- [ ] You're building for a real space agency, not school
- [ ] This is real work, real data, real problem

---

## 🛏️ FRIDAY NIGHT

**By Friday 11 PM:**
- [ ] Get 7-8 hours of sleep
- [ ] Set your alarm for 8:30 AM Saturday
- [ ] Prepare your laptop and charger
- [ ] Have a good breakfast planned for Saturday morning
- [ ] Know how you're getting to the venue

**Saturday morning (8:30 AM):**
- [ ] Wake up early
- [ ] Eat breakfast (fuel for long day)
- [ ] Check all your tools work (Python, QGIS, editor, etc.)
- [ ] Arrive at venue 15 minutes early
- [ ] Have team gather 5 minutes before 9 AM start

---

## ✅ FINAL CHECKLIST BEFORE SLEEP

### Person 1:
- [ ] QGIS or Python + rasterio installed and tested
- [ ] Know how to load GeoTIFF files
- [ ] Have CSV template ready
- [ ] Laptop has space for DEM files

### Person 2:
- [ ] Python 3.10+ installed
- [ ] numpy, scipy installed
- [ ] Watched A* explanation video
- [ ] Know the basic algorithm flow
- [ ] Code editor ready

### Person 3:
- [ ] Understand 5 terrain safety rules
- [ ] Have validation checklist template
- [ ] QGIS or visualization tool ready
- [ ] Know how to read terrain maps

### Person 4:
- [ ] Visualization framework chosen and working
- [ ] Hello World demo runs without error
- [ ] Know what you're building (3 missions on map)
- [ ] Laptop fully charged and ready

### Person 5:
- [ ] Document templates created
- [ ] Shared with team
- [ ] Know the story you're telling
  - Problem: Autonomous lunar navigation
  - Solution: A* algorithm
  - Proof: 3 mission scenarios
  - Impact: Real space mission tech
- [ ] Markdown editor or Google Docs accessible

### EVERYONE:
- [ ] Confirmed attending Saturday 9 AM? ✓
- [ ] Team chat joined? ✓
- [ ] Have all documents? ✓
- [ ] Know your role? ✓
- [ ] Laptop + charger ready? ✓
- [ ] Alarm set for 8:30 AM? ✓
- [ ] Getting 7-8 hours sleep? ✓

---

## 🎬 SATURDAY 9 AM

Walk into that hackathon room and:

1. **Gather as a team (9:00-9:30 AM)**
   - Review kickoff guide together
   - Confirm roles
   - Set communication rules
   - Review critical checkpoints

2. **Person 1 starts immediately**
   - Download lunar DEM
   - Define missions

3. **Everyone else waits for data**
   - Study your responsibilities
   - Set up your tools
   - Get ready to build

4. **12:00 PM first standup**
   - What do we have?
   - What do we need?
   - Any blockers?

---

## 🏆 WINNING FORMULA

**Real Data** (NASA LOLA)  
+ **Proven Algorithm** (A*)  
+ **3 Mission Scenarios** (easy, medium, hard)  
+ **Safety Validation** (Person 3 proves it works)  
+ **Beautiful Demo** (Person 4 makes judges say wow)  
+ **Professional Docs** (Person 5 tells the story)  
+ **Good Presentation** (5 min pitch that lands)  

= **TROPHY** 🏆

---

## 💪 YOU'VE GOT THIS

By this time tomorrow (Saturday 11 PM), you'll have:
- ✅ Missions defined
- ✅ Algorithm working
- ✅ Paths validated
- ✅ Demo built
- ✅ Docs drafted

By Sunday 6 PM, you'll be submitting a winner.

Sleep well tonight. You earned it. Tomorrow you show what you're made of.

**See you Saturday morning. 🚀🌙**

---

**Questions?** Ask them NOW. Don't wait until Saturday.

**Last minute help?** Reach out to Claude or your team lead NOW.

**Ready?** Yes. You're ready.

Go.
