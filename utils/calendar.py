import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build 
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/calendar']


from datetime import datetime, timedelta

def create_event(summary, description, start_dt, end_dt, attendees, service):
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_dt.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_dt.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'attendees': [{'email': email} for email in attendees],
    }

    event_result = service.events().insert(calendarId='primary', body=event).execute()
    return event_result


def get_calendar_service():
    creds = None
    if os.path.exists("credentials.json"):
        creds = Credentials.from_authorized_user_file("credentials.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # <-- THIS LINE NEEDS `Request` imported
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)
