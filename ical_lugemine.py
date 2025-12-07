from icalendar import Calendar
import recurring_ical_events
import requests
from pathlib import Path
import datetime


def saa_ical(self):
    '''Loob ühenduse icaliga'''
    url = "https://ois2.ut.ee/api/timetable/personal/link/9b43407acc5f4ed48ca53057ad9c39b5/et"

    try:
        response = requests.get(url)
        response.raise_for_status()
        cal = Calendar.from_ical(response.content)

        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)

        events = recurring_ical_events.of(
            cal).between(start_of_week, end_of_week)

        return events
    except Exception as e:
        print(f"Error loading calendar: {e}")


def saa_rida(event):
    '''arvutab mis real event on'''
    start = event.get('DTSTART').dt

    if event.get('DTEND'):
        end = event.get('DTEND').dt
        duration = end - start
    elif event.get('DURATION'):
        duration = event.get('DURATION').dt
        end = start + duration

    start = start.hour

    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600

    rida = start - 8
    return [rida, hours]
