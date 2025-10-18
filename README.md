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

