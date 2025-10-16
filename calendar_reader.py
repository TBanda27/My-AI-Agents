"""
Module 1: Calendar Reader
Reads calendar events from ICS file and provides them to other modules
"""

from datetime import datetime, timedelta
from collections import defaultdict
import re


class CalendarReader:
    """Handles reading and parsing calendar events from ICS files"""

    def __init__(self, calendar_file='calendar.ics'):
        self.calendar_file = calendar_file
        self.all_events = []

    def load_calendar(self):
        """Load and parse the ICS calendar file"""
        try:
            with open(self.calendar_file, 'r', encoding='utf-8') as f:
                content = f.read()

            self.all_events = self._parse_ics_content(content)
            print(f"✅ Loaded {len(self.all_events)} events from {self.calendar_file}")
            return True

        except FileNotFoundError:
            print(f"❌ File '{self.calendar_file}' not found!")
            return False

        except Exception as e:
            print(f"❌ Error reading calendar: {e}")
            return False

    def _parse_ics_content(self, content):
        """Parse ICS content and extract events"""
        events = []
        event_blocks = content.split('BEGIN:VEVENT')

        for block in event_blocks[1:]:
            if 'END:VEVENT' not in block:
                continue

            event = self._extract_event_data(block)
            if event and 'title' in event and 'start' in event:
                events.append(event)

        return events

    def _extract_event_data(self, block):
        """Extract event data from VEVENT block"""
        event = {}

        # Extract SUMMARY (title)
        summary_match = re.search(r'SUMMARY:(.+?)(?:\n[A-Z]|\nEND:VEVENT)', block, re.DOTALL)
        if summary_match:
            event['title'] = summary_match.group(1).strip().replace('\n ', '')

        # Extract DTSTART (start time)
        dtstart_match = re.search(r'DTSTART[^:]*:(\d{8}T\d{6})', block)
        if dtstart_match:
            event['start'] = self._parse_datetime(dtstart_match.group(1))

        # Extract DTEND (end time)
        dtend_match = re.search(r'DTEND[^:]*:(\d{8}T\d{6})', block)
        if dtend_match:
            event['end'] = self._parse_datetime(dtend_match.group(1))

        # Extract LOCATION
        location_match = re.search(r'LOCATION:(.+?)(?:\n[A-Z]|\nEND:VEVENT)', block, re.DOTALL)
        if location_match:
            event['location'] = location_match.group(1).strip().replace('\n ', '')
        else:
            event['location'] = ''

        return event

    def _parse_datetime(self, dt_string):
        """Parse ICS datetime format: 20250922T110000 -> datetime object"""
        try:
            return datetime.strptime(dt_string, '%Y%m%dT%H%M%S')
        except:
            return None

    def get_events_for_date(self, date):
        """Get all events for a specific date"""
        date_str = date.strftime('%Y-%m-%d')
        events = []

        for event in self.all_events:
            event_date_str = event['start'].strftime('%Y-%m-%d')
            if event_date_str == date_str:
                events.append(event)

        return sorted(events, key=lambda x: x['start'])

    def get_events_for_week(self, start_date=None):
        """Get all events for the current week (Sunday to Saturday)"""
        if start_date is None:
            start_date = datetime.now()

        # Find the Sunday of this week
        days_since_sunday = (start_date.weekday() + 1) % 7  # Convert Monday=0 to Sunday=0
        week_start = start_date - timedelta(days=days_since_sunday)
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)

        # Week ends on Saturday
        week_end = week_start + timedelta(days=7)

        events = []
        for event in self.all_events:
            if week_start <= event['start'] < week_end:
                events.append(event)

        return sorted(events, key=lambda x: x['start'])

    def get_events_by_date(self, days=7):
        """Get events grouped by date for the current week (Sunday-Saturday)"""
        events = self.get_events_for_week(datetime.now())

        events_by_date = defaultdict(list)
        for event in events:
            date_key = event['start'].strftime('%Y-%m-%d')
            events_by_date[date_key].append(event)

        return dict(events_by_date)

    def get_current_week_range(self):
        """Get the Sunday-Saturday range for current week"""
        now = datetime.now()
        days_since_sunday = (now.weekday() + 1) % 7
        week_start = now - timedelta(days=days_since_sunday)
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)

        return {
            'start': week_start,
            'end': week_end,
            'start_str': week_start.strftime('%A, %B %d'),
            'end_str': week_end.strftime('%A, %B %d')
        }

    def calculate_free_hours(self, date):
        """Calculate free hours for a given date"""
        # Assume working hours: 08:00 - 23:30 (15.5 hours available)
        total_available = 15.5

        events = self.get_events_for_date(date)

        scheduled_hours = 0
        for event in events:
            if event.get('end'):
                duration = (event['end'] - event['start']).total_seconds() / 3600
                scheduled_hours += duration

        free_hours = total_available - scheduled_hours
        return {
            'total_available': total_available,
            'scheduled': scheduled_hours,
            'free': free_hours
        }

    def get_week_summary(self):
        """Get summary statistics for the current week (Sunday-Saturday)"""
        week_range = self.get_current_week_range()
        events = self.get_events_for_week()

        total_hours = 0
        lectures = 0
        labs = 0
        other = 0

        for event in events:
            if event.get('end'):
                duration = (event['end'] - event['start']).total_seconds() / 3600
                total_hours += duration

            title_lower = event['title'].lower()
            if 'lecture' in title_lower:
                lectures += 1
            elif 'lab' in title_lower:
                labs += 1
            else:
                other += 1

        return {
            'week_start': week_range['start_str'],
            'week_end': week_range['end_str'],
            'total_events': len(events),
            'total_hours': total_hours,
            'lectures': lectures,
            'labs': labs,
            'other': other
        }

    def display_events(self, events=None, title="CALENDAR EVENTS"):
        """Display events in a formatted way"""
        if events is None:
            events = self.get_events_for_week()
            week_range = self.get_current_week_range()
            title = f"THIS WEEK ({week_range['start_str']} - {week_range['end_str']})"

        if not events:
            print("No events to display")
            return

        # Group by date
        events_by_date = defaultdict(list)
        for event in events:
            date_key = event['start'].strftime('%Y-%m-%d')
            events_by_date[date_key].append(event)

        print("=" * 70)
        print(title)
        print("=" * 70)

        for date in sorted(events_by_date.keys()):
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%A, %B %d, %Y')

            days_away = (date_obj.date() - datetime.now().date()).days
            if days_away == 0:
                day_label = "TODAY"
            elif days_away == 1:
                day_label = "TOMORROW"
            else:
                day_label = f"In {days_away} days"

            print(f"\n📅 {formatted_date} ({day_label})")
            print("-" * 70)

            for event in events_by_date[date]:
                start_time = event['start'].strftime('%H:%M')

                if event.get('end'):
                    end_time = event['end'].strftime('%H:%M')
                    duration = (event['end'] - event['start']).total_seconds() / 3600
                    print(f"   {start_time} - {end_time}  ({duration:.1f}h)")
                else:
                    print(f"   {start_time}")

                print(f"   📌 {event['title']}")

                if event['location']:
                    print(f"   📍 {event['location']}")

                print()

        print("=" * 70)


# Standalone usage
if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════╗
║   Calendar Reader Module                   ║
╚════════════════════════════════════════════╝
    """)

    reader = CalendarReader('calendar.ics')

    if reader.load_calendar():
        # Display upcoming events
        reader.display_events(title="YOUR UPCOMING CALENDAR")

        # Show summary
        summary = reader.get_week_summary()
        print(f"\n📊 Week Summary ({summary['week_start']} - {summary['week_end']}):")
        print(f"   Events: {summary['total_events']}")
        print(f"   Scheduled hours: {summary['total_hours']:.1f}h")
        print(f"   Lectures: {summary['lectures']}, Labs: {summary['labs']}, Other: {summary['other']}")