"""
Module 2: Study Planner
Generates intelligent study plans for Data Analyst/Scientist roles
"""

from datetime import datetime, timedelta
import json
import os


class StudyPlanner:
    """Creates and manages study curriculum and schedules"""

    def __init__(self, target_date="2024-11-30"):
        self.target_date = datetime.strptime(target_date, "%Y-%m-%d")
        self.curriculum = self._create_data_analyst_curriculum()
        self.weekly_plans = {}

    def _create_data_analyst_curriculum(self):
        """
        Pre-defined curriculum for Data Analyst/Data Scientist roles
        Based on job market requirements
        """
        return {
            "sql": {
                "name": "SQL & Databases",
                "priority": "critical",
                "total_hours": 35,
                "hours_completed": 0,
                "topics": [
                    {"name": "SQL Basics (SELECT, WHERE, ORDER BY)", "hours": 4},
                    {"name": "JOINs (INNER, LEFT, RIGHT, FULL)", "hours": 5},
                    {"name": "Aggregations (GROUP BY, HAVING, COUNT, SUM, AVG)", "hours": 5},
                    {"name": "Subqueries and CTEs", "hours": 6},
                    {"name": "Window Functions (ROW_NUMBER, RANK, PARTITION BY)", "hours": 8},
                    {"name": "Query Optimization", "hours": 4},
                    {"name": "Practice Problems (LeetCode/HackerRank)", "hours": 3}
                ],
                "why_important": "Most requested skill in data analyst jobs. Used daily for data extraction."
            },
            "python": {
                "name": "Python for Data Analysis",
                "priority": "critical",
                "total_hours": 40,
                "hours_completed": 0,
                "topics": [
                    {"name": "Python Fundamentals Review", "hours": 4},
                    {"name": "Pandas: DataFrames, Series, Reading Data", "hours": 8},
                    {"name": "Data Cleaning (handling nulls, duplicates, types)", "hours": 7},
                    {"name": "Data Transformation (merge, groupby, pivot)", "hours": 8},
                    {"name": "NumPy for Numerical Operations", "hours": 4},
                    {"name": "Matplotlib & Seaborn Visualization", "hours": 6},
                    {"name": "Working with APIs and JSON", "hours": 3}
                ],
                "why_important": "Core tool for data manipulation and analysis. Essential for modern data roles."
            },
            "powerbi": {
                "name": "Power BI / Tableau",
                "priority": "critical",
                "total_hours": 30,
                "hours_completed": 0,
                "topics": [
                    {"name": "Power BI Desktop Basics", "hours": 4},
                    {"name": "Data Modeling and Relationships", "hours": 6},
                    {"name": "DAX Fundamentals (Calculated Columns, Measures)", "hours": 8},
                    {"name": "Creating Visualizations", "hours": 5},
                    {"name": "Building Interactive Dashboards", "hours": 5},
                    {"name": "Publishing and Sharing Reports", "hours": 2}
                ],
                "why_important": "Data visualization is key to communicating insights. Highly valued by employers."
            },
            "statistics": {
                "name": "Statistics & Probability",
                "priority": "high",
                "total_hours": 25,
                "hours_completed": 0,
                "topics": [
                    {"name": "Descriptive Statistics (mean, median, std dev)", "hours": 4},
                    {"name": "Probability Distributions", "hours": 5},
                    {"name": "Hypothesis Testing (t-tests, chi-square)", "hours": 6},
                    {"name": "Correlation and Regression", "hours": 5},
                    {"name": "A/B Testing Fundamentals", "hours": 5}
                ],
                "why_important": "Foundation for making data-driven decisions and interpreting results."
            },
            "excel": {
                "name": "Advanced Excel",
                "priority": "medium",
                "total_hours": 15,
                "hours_completed": 0,
                "topics": [
                    {"name": "Advanced Formulas (VLOOKUP, INDEX-MATCH, SUMIFS)", "hours": 4},
                    {"name": "Pivot Tables and Pivot Charts", "hours": 4},
                    {"name": "Power Query Basics", "hours": 4},
                    {"name": "Building Excel Dashboards", "hours": 3}
                ],
                "why_important": "Still widely used in many companies. Shows versatility."
            },
            "projects": {
                "name": "Portfolio Projects",
                "priority": "critical",
                "total_hours": 40,
                "hours_completed": 0,
                "topics": [
                    {"name": "Project 1: Sales Analytics Dashboard (SQL + Power BI)", "hours": 12},
                    {"name": "Project 2: Customer Segmentation Analysis (Python)", "hours": 10},
                    {"name": "Project 3: A/B Test Analysis (Python + Statistics)", "hours": 10},
                    {"name": "Portfolio Website Setup", "hours": 5},
                    {"name": "Resume & LinkedIn Optimization", "hours": 3}
                ],
                "why_important": "Demonstrates practical skills. Essential for interviews and job applications."
            },
            "interview_prep": {
                "name": "Interview Preparation",
                "priority": "high",
                "total_hours": 15,
                "hours_completed": 0,
                "topics": [
                    {"name": "SQL Interview Questions Practice", "hours": 5},
                    {"name": "Case Study Practice", "hours": 5},
                    {"name": "Behavioral Interview Prep", "hours": 3},
                    {"name": "Mock Interviews", "hours": 2}
                ],
                "why_important": "Bridge between skills and job offers. Critical for final stage."
            }
        }

    def calculate_available_time(self, calendar_reader):
        """
        Calculate how much study time is available from now until target date
        Accounts for calendar commitments
        """
        now = datetime.now()
        days_remaining = (self.target_date - now).days
        weeks_remaining = days_remaining / 7

        # Get calendar commitments for remaining time
        total_calendar_hours = 0
        current_date = now

        while current_date <= self.target_date:
            events = calendar_reader.get_events_for_date(current_date)
            for event in events:
                if event.get('end'):
                    duration = (event['end'] - event['start']).total_seconds() / 3600
                    total_calendar_hours += duration
            current_date += timedelta(days=1)

        # Calculate available study hours
        # Weekdays: 8am-11:30pm = 15.5h available - 2h waste = 13.5h
        # Weekends: Minimum 12h study

        weekdays_remaining = 0
        weekends_remaining = 0

        current_date = now
        while current_date <= self.target_date:
            if current_date.weekday() in [5, 6]:  # Saturday, Sunday
                weekends_remaining += 1
            else:
                weekdays_remaining += 1
            current_date += timedelta(days=1)

        max_weekday_hours = weekdays_remaining * 13.5
        max_weekend_hours = weekends_remaining * 12
        total_max_hours = max_weekday_hours + max_weekend_hours

        available_study_hours = total_max_hours - total_calendar_hours

        return {
            'days_remaining': days_remaining,
            'weeks_remaining': round(weeks_remaining, 1),
            'weekdays': weekdays_remaining,
            'weekends_days': weekends_remaining,
            'calendar_committed_hours': total_calendar_hours,
            'max_possible_hours': total_max_hours,
            'available_study_hours': available_study_hours,
            'avg_hours_per_day': available_study_hours / days_remaining if days_remaining > 0 else 0
        }

    def allocate_hours_to_curriculum(self, available_hours):
        """
        Intelligently allocate available hours to curriculum based on priority
        """
        # Calculate total needed hours
        total_needed = sum(skill['total_hours'] for skill in self.curriculum.values())

        # If we have enough time, use recommended hours
        if available_hours >= total_needed:
            print(f"✅ Good news! You have {available_hours:.0f}h available and need {total_needed}h")
            print(f"   Buffer time: {available_hours - total_needed:.0f}h for review/overflow")
            return self.curriculum

        # If time is tight, prioritize critical skills
        else:
            print(f"⚠️  Time is tight! You have {available_hours:.0f}h but curriculum needs {total_needed}h")
            print(f"   Prioritizing critical skills...")

            # Allocate hours based on priority
            critical_skills = {k: v for k, v in self.curriculum.items() if v['priority'] == 'critical'}
            high_skills = {k: v for k, v in self.curriculum.items() if v['priority'] == 'high'}

            critical_hours = sum(s['total_hours'] for s in critical_skills.values())
            high_hours = sum(s['total_hours'] for s in high_skills.values())

            # Allocate 70% to critical, 25% to high, 5% buffer
            allocated = available_hours * 0.95  # 5% buffer
            critical_allocation = allocated * 0.7
            high_allocation = allocated * 0.25

            # Scale down hours proportionally
            for skill_id, skill in self.curriculum.items():
                if skill['priority'] == 'critical':
                    scale_factor = critical_allocation / critical_hours
                    skill['total_hours'] = int(skill['total_hours'] * scale_factor)
                elif skill['priority'] == 'high':
                    scale_factor = high_allocation / high_hours
                    skill['total_hours'] = int(skill['total_hours'] * scale_factor)
                else:
                    skill['total_hours'] = int(skill['total_hours'] * 0.5)  # Cut medium priority in half

            return self.curriculum

    def generate_weekly_breakdown(self, weeks_remaining):
        """
        Break down curriculum into weekly study goals
        """
        weekly_plans = []
        skills_list = list(self.curriculum.items())

        for week_num in range(1, int(weeks_remaining) + 2):
            week_plan = {
                'week': week_num,
                'focus_skills': [],
                'total_hours': 0,
                'goals': []
            }

            # Rotate through skills, prioritizing critical ones
            # Week 1-3: Focus on SQL, Python, Power BI
            # Week 4-5: Statistics, Projects
            # Week 6+: Projects, Interview Prep

            if week_num <= 3:
                # Foundation building
                focus = ['sql', 'python', 'powerbi']
                week_plan['phase'] = 'Foundation Building'
            elif week_num <= 5:
                # Intermediate skills + project work
                focus = ['python', 'powerbi', 'statistics', 'projects']
                week_plan['phase'] = 'Skill Development & Projects'
            else:
                # Projects and interview prep
                focus = ['projects', 'interview_prep', 'sql']
                week_plan['phase'] = 'Project Sprint & Interview Prep'

            for skill_id in focus:
                if skill_id in self.curriculum:
                    skill = self.curriculum[skill_id]
                    weekly_hours = min(skill['total_hours'] - skill['hours_completed'], 10)

                    if weekly_hours > 0:
                        week_plan['focus_skills'].append({
                            'skill': skill['name'],
                            'hours': weekly_hours,
                            'topics': self._get_next_topics(skill_id, weekly_hours)
                        })
                        week_plan['total_hours'] += weekly_hours

            weekly_plans.append(week_plan)

        return weekly_plans

    def _get_next_topics(self, skill_id, hours_available):
        """Get next topics to study for a skill within available hours"""
        skill = self.curriculum[skill_id]
        topics = []
        hours_allocated = 0

        for topic in skill['topics']:
            if hours_allocated >= hours_available:
                break
            if topic['hours'] <= (hours_available - hours_allocated):
                topics.append(topic['name'])
                hours_allocated += topic['hours']

        if not topics and skill['topics']:
            topics.append(skill['topics'][0]['name'] + " (partial)")

        return topics

    def display_curriculum(self):
        """Display the full curriculum with details"""
        print("=" * 70)
        print("DATA ANALYST/SCIENTIST CURRICULUM")
        print("=" * 70)

        critical = []
        high = []
        medium = []

        for skill_id, skill in self.curriculum.items():
            if skill['priority'] == 'critical':
                critical.append((skill_id, skill))
            elif skill['priority'] == 'high':
                high.append((skill_id, skill))
            else:
                medium.append((skill_id, skill))

        total_hours = 0

        for priority_name, skills in [("CRITICAL", critical), ("HIGH PRIORITY", high), ("MEDIUM PRIORITY", medium)]:
            if skills:
                print(f"\n🎯 {priority_name} SKILLS:")
                print("-" * 70)

                for skill_id, skill in skills:
                    print(f"\n   📚 {skill['name']} ({skill['total_hours']}h)")
                    print(f"      {skill['why_important']}")
                    print(f"      Topics:")
                    for topic in skill['topics']:
                        print(f"        • {topic['name']} ({topic['hours']}h)")
                    total_hours += skill['total_hours']

        print("\n" + "=" * 70)
        print(f"TOTAL CURRICULUM HOURS: {total_hours}h")
        print("=" * 70)

    def display_weekly_plan(self, weekly_plans):
        """Display week-by-week study plan"""
        print("\n" + "=" * 70)
        print("WEEKLY STUDY PLAN")
        print("=" * 70)

        for week in weekly_plans:
            print(f"\n📅 WEEK {week['week']}: {week['phase']}")
            print(f"   Total study hours this week: {week['total_hours']}h")
            print("-" * 70)

            for skill in week['focus_skills']:
                print(f"\n   📖 {skill['skill']} ({skill['hours']}h)")
                print(f"      Topics to cover:")
                for topic in skill['topics']:
                    print(f"        • {topic}")

        print("\n" + "=" * 70)

    def save_plan(self, filename='study_plan.json'):
        """Save the study plan to file"""
        plan_data = {
            'target_date': self.target_date.strftime('%Y-%m-%d'),
            'curriculum': self.curriculum,
            'weekly_plans': self.weekly_plans,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        with open(filename, 'w') as f:
            json.dump(plan_data, f, indent=2)

        print(f"\n💾 Study plan saved to {filename}")

    def load_plan(self, filename='study_plan.json'):
        """Load existing study plan"""
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                plan_data = json.load(f)

            self.curriculum = plan_data['curriculum']
            self.weekly_plans = plan_data.get('weekly_plans', {})
            print(f"✅ Loaded study plan from {filename}")
            return True
        return False


# Standalone usage
if __name__ == "__main__":
    from calendar_reader import CalendarReader

    print("""
╔════════════════════════════════════════════╗
║   Study Plan Generator                     ║
║   Target: Data Analyst/Scientist Ready     ║
╚════════════════════════════════════════════╝
    """)

    # Initialize
    planner = StudyPlanner(target_date="2024-11-30")
    calendar = CalendarReader('calendar.ics')

    # Load calendar
    if not calendar.load_calendar():
        print("⚠️  Continuing without calendar data...")

    # Calculate available time
    print("\n📊 Calculating available study time...")
    time_available = planner.calculate_available_time(calendar)

    print(f"\n⏰ TIME ANALYSIS:")
    print(f"   Days until November 30: {time_available['days_remaining']}")
    print(f"   Weeks remaining: {time_available['weeks_remaining']}")
    print(f"   Calendar commitments: {time_available['calendar_committed_hours']:.0f}h")
    print(f"   Available for study: {time_available['available_study_hours']:.0f}h")
    print(f"   Average per day: {time_available['avg_hours_per_day']:.1f}h")

    # Allocate hours to curriculum
    print("\n🎯 Creating your personalized curriculum...")
    planner.allocate_hours_to_curriculum(time_available['available_study_hours'])

    # Display curriculum
    planner.display_curriculum()

    # Generate weekly breakdown
    print("\n📅 Generating weekly study plan...")
    weekly_plans = planner.generate_weekly_breakdown(time_available['weeks_remaining'])
    planner.display_weekly_plan(weekly_plans)

    # Save plan
    planner.save_plan()

    print("\n✅ Your study plan is ready!")
    print("   Next step: Start following the weekly plan!")