import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Make sure the path to your service account key is set correctly
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
SCOPES = ["https://www.googleapis.com/auth/calendar"]

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build("calendar", "v3", credentials=credentials)

# Replace with your actual calendar ID or "primary"
CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID", "primary")

def create_calendar_event(summary, start_time_iso, attendees_emails):
    start = datetime.fromisoformat(start_time_iso)
    end = start + timedelta(hours=1)

    event = {
        'summary': summary,
        'start': {
            'dateTime': start.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'attendees': [{'email': email} for email in attendees_emails],
    }

    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event, sendUpdates="all").execute()
    return created_event.get("htmlLink")
