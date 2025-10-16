"""
Module 3: AI Study Agent v3.0 - Fully Automated
Runs silently, generates schedules, sends notifications throughout the day
Good morning, Banda!
"""

import os
from datetime import datetime, timedelta, time as dt_time
from anthropic import Anthropic
from dotenv import load_dotenv
import json
from win10toast import ToastNotifier
import schedule
import time
import threading

from calendar_reader import CalendarReader
from study_planner import StudyPlanner

# Load environment
load_dotenv('.env')

# Initialize Windows notification system
toaster = ToastNotifier()


class AutomatedStudyAgent:
    """
    Fully automated agent that:
    - Runs silently in background
    - Generates schedules automatically
    - Sends notifications for calendar events and study sessions
    - No interaction needed unless you want to chat
    """

    def __init__(self, calendar_file='calendar.ics', study_plan_file='study_plan.json'):
        self.claude = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.calendar = CalendarReader(calendar_file)
        self.planner = StudyPlanner()
        self.study_plan_file = study_plan_file
        self.overlap_file = 'msc_overlap_analysis.json'

        # User constraints
        self.wake_time = "07:00"
        self.sleep_time = "00:00"
        self.daily_waste_hours = 2
        self.break_minutes_per_hour = 10

        # Load data
        self.calendar.load_calendar()
        self.planner.load_plan(study_plan_file)

        # Load or create overlap analysis (ONE TIME)
        self.overlap_analysis = self.load_overlap_analysis()

        # Track today's schedule
        self.todays_schedule = None
        self.notified_events = set()  # Track what we've already notified

    def load_overlap_analysis(self):
        """Load saved MSc overlap analysis if it exists"""
        if os.path.exists(self.overlap_file):
            with open(self.overlap_file, 'r') as f:
                analysis = json.load(f)
            return analysis
        return None

    def save_overlap_analysis(self, analysis):
        """Save MSc overlap analysis for future use"""
        with open(self.overlap_file, 'w') as f:
            json.dump(analysis, f, indent=2)

    def setup_first_time(self):
        """One-time setup: Analyze MSc courses"""
        print("\n" + "=" * 70)
        print("🎓 FIRST-TIME SETUP")
        print("=" * 70)
        print("Analyzing your MSc courses... This will only happen once!")

        self.overlap_analysis = self.analyze_msc_curriculum_overlap()

        if self.overlap_analysis:
            self.adjust_curriculum_for_overlap(self.overlap_analysis)
            self.save_overlap_analysis(self.overlap_analysis)
            self.planner.save_plan()

            print("\n✅ Setup complete!")
            print("💾 Saved your MSc course analysis")
            print("\nFrom now on:")
            print("  • I'll generate your daily schedule automatically")
            print("  • Send you notifications throughout the day")
            print("  • No need to interact unless you want to chat")
            print("=" * 70)

    def analyze_msc_curriculum_overlap(self):
        """Analyze MSc courses from calendar"""
        all_events = self.calendar.all_events
        course_titles = set()

        for event in all_events:
            title = event['title'].lower()
            if any(keyword in title for keyword in ['lecture', 'lab', 'tutorial', 'seminar', 'workshop']):
                course_name = title.split(';')[0].strip() if ';' in title else title
                course_titles.add(course_name)

        print(f"\n   Detected {len(course_titles)} MSc courses:")
        for course in sorted(course_titles):
            print(f"   • {course}")

        curriculum_simple = {
            k: {'name': v['name'], 'topics': [t['name'] for t in v['topics']]}
            for k, v in self.planner.curriculum.items()
        }

        context = f"""
Analyze MSc AI curriculum overlap with Data Analyst skills.

MSc COURSES: {json.dumps(list(course_titles), indent=2)}
DATA ANALYST CURRICULUM: {json.dumps(curriculum_simple, indent=2)}

Return JSON:
{{
  "covered_by_msc": {{
    "skill_id": {{"coverage_percentage": 0-100, "msc_course": "course name", "what_needs_self_study": "gaps"}}
  }},
  "pure_gaps": ["sql", "powerbi", "excel"],
  "recommendation": "Balance advice"
}}
"""

        try:
            message = self.claude.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=2000,
                messages=[{"role": "user", "content": context}]
            )

            response_text = message.content[0].text
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx != -1:
                return json.loads(response_text[start_idx:end_idx])

        except Exception as e:
            print(f"⚠️  Error: {e}")

        return None

    def adjust_curriculum_for_overlap(self, overlap_analysis):
        """Adjust curriculum based on MSc overlap"""
        if not overlap_analysis:
            return

        covered = overlap_analysis.get('covered_by_msc', {})
        pure_gaps = overlap_analysis.get('pure_gaps', [])

        for skill_id, coverage_info in covered.items():
            if skill_id in self.planner.curriculum:
                coverage_pct = coverage_info.get('coverage_percentage', 0)
                original_hours = self.planner.curriculum[skill_id]['total_hours']
                reduction_factor = (100 - coverage_pct) / 100
                new_hours = int(original_hours * reduction_factor)
                self.planner.curriculum[skill_id]['total_hours'] = new_hours

        print(f"\n   🎯 Focus areas (gaps in MSc): {', '.join(pure_gaps)}")

    def calculate_daily_available_time(self, date):
        """Calculate available study time"""
        events = self.calendar.get_events_for_date(date)

        calendar_hours = sum(
            (e['end'] - e['start']).total_seconds() / 3600
            for e in events if e.get('end')
        )

        total_awake_hours = 17
        available_hours = total_awake_hours - self.daily_waste_hours - calendar_hours
        effective_study_hours = available_hours * 0.83

        return {
            'calendar_blocked': calendar_hours,
            'effective_study_hours': effective_study_hours,
            'calendar_events': events
        }

    def generate_daily_schedule(self, date=None):
        """Generate balanced daily schedule"""
        if date is None:
            date = datetime.now()

        time_info = self.calculate_daily_available_time(date)
        curriculum_status = json.dumps(self.planner.curriculum, indent=2)

        msc_context = ""
        if self.overlap_analysis:
            msc_context = f"""
MSc Coverage: {json.dumps(self.overlap_analysis.get('covered_by_msc', {}), indent=2)}
Pure Gaps: {json.dumps(self.overlap_analysis.get('pure_gaps', []), indent=2)}
"""

        context = f"""
Generate Banda's balanced daily schedule for {date.strftime('%A, %B %d, %Y')}.

TIME AVAILABLE:
- Effective study hours: {time_info['effective_study_hours']:.1f}h
- Calendar events: {json.dumps([{{'title': e['title'], 'start': e['start'].strftime('%H:%M'), 'end': e['end'].strftime('%H:%M') if e.get('end') else 'N/A'}} for e in time_info['calendar_events']], indent=2)}

CURRICULUM: {curriculum_status}
{msc_context}

REQUIREMENTS:
1. 50/50 split: {time_info['effective_study_hours'] / 2:.1f}h MSc + {time_info['effective_study_hours'] / 2:.1f}h Data Analyst gaps
2. Work around calendar events
3. Start after 7am, end before 11:30pm
4. Specific topics with 3 bullet points each
5. 1.5-2.5 hour blocks with breaks

Return JSON:
{{
  "date": "{date.strftime('%Y-%m-%d')}",
  "summary": "Brief overview",
  "total_study_hours": 0.0,
  "schedule": [
    {{
      "start_time": "08:00",
      "end_time": "10:00",
      "subject": "SQL",
      "specific_topic": "Window Functions",
      "study_guidance": ["Point 1", "Point 2", "Point 3"],
      "resources": "Resources to use",
      "why_now": "Reason for timing"
    }}
  ]
}}
"""

        try:
            print("   Sending request to Claude...")
            message = self.claude.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=4000,
                messages=[{"role": "user", "content": context}]
            )

            response_text = message.content[0].text
            print("   ✓ Got response from Claude")

            # Debug: Show part of response
            print(f"   Response preview: {response_text[:200]}...")

            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx != -1:
                schedule_json = response_text[start_idx:end_idx]
                print("   ✓ Found JSON in response")
                schedule = json.loads(schedule_json)
                print("   ✓ Parsed JSON successfully")

                # Save schedule
                filename = f"schedule_{date.strftime('%Y-%m-%d')}.json"
                with open(filename, 'w') as f:
                    json.dump(schedule, f, indent=2)
                print(f"   ✓ Saved to {filename}")

                return schedule
            else:
                print("   ❌ No JSON found in Claude's response")
                print(f"   Full response:\n{response_text}")
                return None

        except json.JSONDecodeError as e:
            print(f"   ❌ JSON parsing error: {e}")
            print(f"   Attempted to parse: {response_text[start_idx:start_idx + 200]}...")
            return None
        except Exception as e:
            print(f"   ❌ Error generating schedule: {e}")
            import traceback
            traceback.print_exc()
            return None

    def send_notification(self, title, message, duration=10):
        """Send Windows system notification with sound"""
        try:
            # win10toast automatically handles Windows notification center
            # threaded=True prevents blocking
            toaster.show_toast(
                title,
                message,
                duration=duration,
                threaded=True,
                icon_path=None  # Uses default Windows icon
            )
            print(f"🔔 Sent: {title}")
        except Exception as e:
            print(f"⚠️  Notification error: {e}")
            print(f"   {title}: {message}")

    def notify_calendar_event(self, event, minutes_before=10):
        """Send notification for upcoming calendar event"""
        event_id = f"{event['start'].strftime('%H:%M')}-{event['title']}"

        if event_id not in self.notified_events:
            title = f"📅 Upcoming: {event['title']}"
            start = event['start'].strftime('%H:%M')
            end = event['end'].strftime('%H:%M') if event.get('end') else '?'
            message = f"In {minutes_before} minutes\n{start} - {end}"

            self.send_notification(title, message)
            self.notified_events.add(event_id)
            print(f"🔔 Notified: {event['title']} at {start}")

    def notify_study_session(self, session):
        """Send notification for study session"""
        session_id = f"{session['start_time']}-{session['subject']}"

        if session_id not in self.notified_events:
            title = f"📚 Time to Study: {session['subject']}"

            # Create informative message
            message = f"{session['specific_topic']}\n\n"

            # Add first 2 guidance points
            guidance = session.get('study_guidance', [])
            if len(guidance) >= 1:
                message += f"• {guidance[0]}\n"
            if len(guidance) >= 2:
                message += f"• {guidance[1]}"

            self.send_notification(title, message, duration=15)
            self.notified_events.add(session_id)
            print(f"🔔 Study reminder sent: {session['subject']} at {session['start_time']}")

    def check_and_notify(self):
        """Check current time and send appropriate notifications"""
        now = datetime.now()
        current_time = now.strftime('%H:%M')

        if not self.todays_schedule:
            return

        # Check calendar events (notify 10 min before)
        time_info = self.calculate_daily_available_time(now)
        for event in time_info['calendar_events']:
            event_time = event['start']
            time_until = (event_time - now).total_seconds() / 60

            # Notify 10 minutes before
            if 8 <= time_until <= 12:
                self.notify_calendar_event(event, minutes_before=10)

        # Check study sessions (notify at start time)
        for session in self.todays_schedule.get('schedule', []):
            session_time = session['start_time']

            # If it's time for this session (within 2 minutes)
            session_dt = datetime.strptime(session_time, '%H:%M').replace(
                year=now.year, month=now.month, day=now.day
            )
            time_diff = (session_dt - now).total_seconds() / 60

            if -2 <= time_diff <= 2:
                self.notify_study_session(session)

    def morning_routine(self):
        """Morning routine: Generate schedule and send summary"""
        today = datetime.now()

        # Generate today's schedule
        print(f"\n🌅 Good morning, Banda! {today.strftime('%A, %B %d, %Y')}")
        print("📋 Generating your balanced schedule...")

        self.todays_schedule = self.generate_daily_schedule(today)

        if self.todays_schedule:
            # Send morning summary
            summary = self.todays_schedule.get('summary', 'Your day is planned')
            total_hours = self.todays_schedule.get('total_study_hours', 0)
            num_sessions = len(self.todays_schedule.get('schedule', []))

            message = f"Good morning, Banda!\n\n{summary}\n\n{num_sessions} study sessions planned\nTotal: {total_hours:.1f} hours\n\nYou'll get reminders throughout the day!"

            self.send_notification("🌅 Today's Schedule Ready", message, duration=20)

            print(f"✅ Schedule generated")
            print(f"   {num_sessions} study sessions, {total_hours:.1f} hours")
            print(f"   Windows notifications will be sent throughout the day")
        else:
            print("❌ Failed to generate schedule")

        # Reset notification tracking for new day
        self.notified_events.clear()

    def run_daemon(self):
        """Run as background daemon - sends notifications all day"""
        print("\n" + "=" * 70)
        print("🤖 AI STUDY AGENT - DAEMON MODE")
        print("=" * 70)
        print("Running in background...")
        print("Will send notifications throughout the day")
        print("Press Ctrl+C to stop")
        print("=" * 70)

        # Schedule morning routine at 7:00 AM
        schedule.every().day.at("07:00").do(self.morning_routine)

        # Check for notifications every minute
        schedule.every(1).minutes.do(self.check_and_notify)

        # Run morning routine now if after 7 AM and no schedule yet
        now = datetime.now()
        if now.time() >= dt_time(7, 0) and not self.todays_schedule:
            self.morning_routine()

        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds

    def chat_mode(self):
        """Interactive chat mode"""
        print("\n💬 Chat Mode - Ask me anything!")
        print("Type 'exit' to quit\n")

        while True:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\nAgent: Good luck, Banda! 🚀")
                break

            # Generate response using Claude
            context = f"""
You are Banda's AI study coach. Help with questions about the schedule, study tips, motivation.

USER: {user_input}

Respond conversationally, briefly (2-3 sentences), and supportively.
"""

            try:
                message = self.claude.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=500,
                    messages=[{"role": "user", "content": context}]
                )
                print(f"\nAgent: {message.content[0].text}\n")
            except Exception as e:
                print(f"\nAgent: Sorry, I had trouble with that: {e}\n")


# Main entry point
if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════╗
║   AI Study Agent v3.0                     ║
║   Fully Automated - Banda's Edition       ║
╚════════════════════════════════════════════╝
    """)

    agent = AutomatedStudyAgent(
        calendar_file='calendar.ics',
        study_plan_file='study_plan.json'
    )

    # First-time setup if needed
    first_run = not os.path.exists('msc_overlap_analysis.json')

    if first_run:
        agent.setup_first_time()
        print("\n✅ Setup complete! Starting automated mode...\n")

    print("\nChoose mode:")
    print("1. Daemon mode (runs all day, sends automatic notifications)")
    print("2. Chat mode (ask questions, get advice)")
    print("3. Both (daemon in background + chat)")

    choice = input("\nYour choice (1/2/3): ").strip()

    if choice == '1':
        # Pure daemon mode
        agent.run_daemon()

    elif choice == '2':
        # Pure chat mode
        agent.chat_mode()

    elif choice == '3':
        # Both: daemon in background thread, chat in foreground
        print("\n🤖 Starting daemon in background...")
        daemon_thread = threading.Thread(target=agent.run_daemon, daemon=True)
        daemon_thread.start()

        time.sleep(2)  # Let daemon initialize

        print("\n💬 Starting chat mode (daemon running in background)...")
        agent.chat_mode()

    else:
        print("\n⚠️  Invalid choice. Run again and choose 1, 2, or 3")