# My AI Study Scheduler Agent

**How I'm Balancing My MSc AI Studies with Becoming a Data Analyst**

I built this automated AI-powered scheduling system to help me manage my MSc AI coursework while preparing for a data analyst career. It reads my calendar, understands my university commitments, and generates perfectly balanced daily study plans to help me become job-ready by December 2024.

---

## 🎯 What This Does for Me

- **📅 Reads My Calendar** - Automatically syncs with my Outlook calendar
- **🎓 Understands My MSc** - Analyzes my courses once and remembers them forever
- **🤖 Generates My Daily Schedule** - Creates balanced 50/50 MSc + Career prep plans
- **🔔 Sends Me Notifications** - Windows notifications throughout the day with sound
- **💬 I Can Chat With It** - Ask questions, get study tips, adjust my plans
- **📊 Tracks My Progress** - Monitors my journey to career readiness

---

## ✨ Key Features I Built In

### Intelligent Course Analysis (One-Time)
- Detects my MSc courses from my calendar
- Identifies overlap with Data Analyst skills I need
- Focuses my self-study on gaps (SQL, Power BI, Excel - things not covered in my MSc)
- Saves the analysis - never needs to run again

### My Daily Automated Schedule
- **7:00 AM**: Generates my balanced daily schedule
- **Throughout the day**: Sends me reminders for lectures, labs, and study sessions
- **50/50 Balance**: Equal time for my MSc work and career preparation
- **Smart Planning**: Works around my commitments, optimal time allocation

### Pre-Loaded Data Analyst Curriculum I Need
- **SQL** (35h) - From basics to window functions
- **Python** (40h) - Pandas, NumPy, data analysis
- **Power BI** (30h) - Dashboards and DAX
- **Statistics** (25h) - Hypothesis testing, A/B tests
- **Excel** (15h) - Advanced formulas, pivot tables
- **Portfolio Projects** (40h) - Real-world projects for my resume
- **Interview Prep** (15h) - Technical and behavioral preparation

---

## 🚀 How I Set This Up

### What I Needed
- Python 3.8 or higher
- Windows 10/11 (for notifications)
- My Outlook calendar
- Anthropic API key (Claude AI)

### My Installation Steps

1. **Created My Project Folder**
```bash
mkdir study-scheduler
cd study-scheduler
```

2. **Set Up Virtual Environment**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Installed Required Packages**
```bash
pip install anthropic python-dotenv win10toast schedule
```

4. **Created My .env File**

I created a `.env` file with my API key:
```
ANTHROPIC_API_KEY=sk-ant-my-key-here
```

I got my API key from: https://console.anthropic.com/

5. **Exported My Calendar**

From Outlook:
- File → Open & Export → Import/Export
- Export to a file → Choose format
- Saved as `calendar.ics`

I placed `calendar.ics` in my project folder.

6. **Generated My Study Plan**
```bash
python study_planner.py
```

This created my personalized `study_plan.json` file.

7. **Started My Agent**
```bash
python ai_agent.py
```

I chose mode 1 (Daemon mode) so it runs all day and sends me notifications.

---

## 📁 My Project Structure

```
study-scheduler/
├── calendar_reader.py          # Module 1: Reads my calendar
├── study_planner.py            # Module 2: Generates my curriculum
├── ai_agent.py                 # Module 3: My AI scheduling assistant
├── calendar.ics                # My exported Outlook calendar
├── .env                        # My API keys (private)
├── study_plan.json             # My personalized study plan
├── msc_overlap_analysis.json   # One-time analysis of my MSc courses
├── schedule_YYYY-MM-DD.json    # My daily schedules
└── README.md                   # This file
```

---

## 🎓 How This Works for Me

### First Run (One-Time Setup)
```
🎓 FIRST-TIME SETUP
Analyzing my MSc courses...

Detected courses:
• Programming for Data Analysis
• Research Methods
• Graph and AI

🔄 Adjusting curriculum...
✓ Python: My MSc covers 70% → I'll focus on advanced topics only
✓ Statistics: My MSc covers 60% → I'll focus on business applications
🎯 PURE GAPS: SQL, Power BI, Excel (not in my MSc)

💾 Saved! Won't run again.
```

### My Daily Operation

**7:00 AM - My Morning Routine**
```
🌅 Good morning, Banda!
📋 Generating your balanced schedule...

Today's Schedule:
• 11:00-13:00: Research Methods (lecture)
• 15:00-17:00: Programming for Data Analysis (lab)

⏱️ Available study time: 6.5 hours
Target: 3.25h MSc + 3.25h Data Analyst (50/50)

✅ Schedule generated
I'll send you notifications throughout the day
```

**Throughout My Day - Notifications I Get**

**10:50 AM**
```
📅 Upcoming: Research Methods
In 10 minutes
11:00 - 13:00
```

**15:30 PM**
```
📚 Time to Study: SQL
Window Functions: ROW_NUMBER and RANK

• Start with ROW_NUMBER basics
• Practice RANK vs DENSE_RANK
```

**20:00 PM**
```
📚 Time to Study: Power BI
Building Interactive Dashboards

• Create 3 visualizations
• Add slicers and filters
```

---

## 💬 How I Chat With My Agent

```bash
python ai_agent.py
→ I choose: 2 (or 3 for daemon + chat)
```

**Example Conversations I Have:**

```
Me: Why is SQL scheduled at 8am?

Agent: Morning is best for SQL because window functions 
require focused thinking, Banda. Your brain is freshest then, 
and it doesn't overlap with your MSc courses!

Me: What if I'm too tired today?

Agent: Then take it easier, Banda. Maybe do lighter topics 
like Excel instead. Consistency matters more than perfection.

Me: How many hours of SQL do I have left?

Agent: You have about 28 hours of SQL remaining, Banda. At your 
current pace, you'll finish in 3 weeks. On track!
```

---

## 🔧 My Configuration

### My Schedule Settings (in `ai_agent.py`)

```python
self.wake_time = "07:00"          # I wake up at 7am
self.sleep_time = "00:00"         # I sleep at midnight
self.daily_waste_hours = 2        # Meals, breaks, transitions
self.break_minutes_per_hour = 10  # I take 10-min breaks every hour
```

### My Target Date (in `study_planner.py`)

```python
target_date = "2025-11-30"  # When I start my job search
```

---

## 📊 Why I Use 50/50 Balance

I need to make equal progress on both my MSc and my career:

**My MSc Work (50%)**
- MSc assignments
- Lecture review
- Exam preparation
- MSc projects

**My Career Prep (50%)**
- SQL (not in my MSc - pure gap)
- Power BI (not in my MSc - pure gap)
- Excel (not in my MSc - pure gap)
- Portfolio projects for my resume
- Interview preparation

**Why This Works for Me:**
- ✅ I'll graduate successfully (MSc covered)
- ✅ I'll be job-ready by December (skills covered)
- ✅ No wasted time on duplication (agent knows what my MSc teaches)
- ✅ Balanced progress (not neglecting either goal)

---

## 🐛 Problems I've Solved

### "Failed to generate schedule"
**What I check:**
- ✅ My `calendar.ics` exists in project folder
- ✅ My `study_plan.json` exists (I run `study_planner.py` first)
- ✅ My `.env` has correct `ANTHROPIC_API_KEY`
- ✅ My API key is valid and has credits

**How I debug:**
My agent shows detailed logs. I look for:
```
   Sending request to Claude...
   ✓ Got response from Claude
   ✓ Found JSON in response
   ✓ Parsed JSON successfully
```

### "schedule module has no attribute 'every'"
**My fix:**
```bash
pip uninstall schedule -y
pip install schedule
```

I also check for conflicting files named `schedule.py` in my folder.

### "Notifications not appearing"
**What I check:**
- My Windows notifications are enabled (Settings → Notifications)
- `win10toast` is installed: `pip install win10toast`
- I run as administrator if needed

---

## 📅 My Daily Workflow

**Every Morning:**
1. My agent automatically generates my schedule at 7:00 AM
2. I receive a morning summary notification
3. Throughout the day: I get notifications for my events and study sessions

**My Routine:**
- I run my agent in **daemon mode** (option 1)
- I let it run in background all day
- I follow the notification reminders
- I check console for detailed logs

**Weekly:**
- I review my `schedule_*.json` files to see my progress
- I adjust if I'm falling behind (I chat with my agent)
- I update my calendar with new events

---

## 🎯 How I Track My Success

My agent tracks:
- **Hours I've completed** per skill
- **Topics I've mastered** in my curriculum
- **Projects I've finished** for my portfolio
- **Days remaining** until December
- **My balance ratio** (MSc vs Career)

By December, I'll have:
- ✅ My MSc coursework completed
- ✅ 3-5 portfolio projects for my resume
- ✅ SQL, Power BI, Excel proficiency
- ✅ Interview-ready skills
- ✅ My resume and LinkedIn optimized

---



---

## 💡 Tips I've Learned

1. **I'm Consistent** - I run the agent every day
2. **I Follow Notifications** - They're optimally timed for me
3. **I Take Breaks** - 10 minutes per hour is built in
4. **I Chat When Stuck** - I ask my agent for help
5. **I Update My Calendar** - I keep it current for accurate planning
6. **I Review My Progress** - I check completed vs remaining hours
7. **I Stay Flexible** - Life happens, my agent adapts

---

## 📚 Resources I'm Using

My agent recommends these resources:

**SQL:**
- Mode Analytics SQL Tutorial
- LeetCode SQL problems
- HackerRank SQL track

**Python:**
- Pandas documentation
- Kaggle Learn courses
- Real datasets for practice

**Power BI:**
- Microsoft Learn
- Power BI Community
- Sample dashboards


## 🎓 About Me & This Project

I'm an MSc AI student working toward becoming a data analyst by December 2025. I built this system because I realized I needed:
- ✅ Smart planning (not just hard work)
- ✅ Balance between my MSc and career prep
- ✅ Automation (so I can focus on learning, not planning)
- ✅ Accountability (notifications keep me on track)

**My Philosophy:** Let AI handle my scheduling, I focus on learning.

**My Goal:** Graduate with my MSc while becoming job-ready for data analyst roles.

---

## 📞 If You're Using This

If you're another student trying to balance studies with career prep:
1. Follow my setup instructions
2. Adjust the configuration for your schedule
3. Stay consistent with the daily routine
4. Trust the 50/50 balance
5. Chat with your agent when you need help

---




