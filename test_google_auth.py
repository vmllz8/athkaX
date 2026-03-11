import os
import pickle
from datetime import datetime, timezone

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.readonly",
]

CLIENT_SECRET_FILE = "/Users/moznali/Downloads/client_secret_173792979809-c8anittk5nf84blmdmo6b9aaupfpah46.apps.googleusercontent.com.json"
TOKEN_FILE = "token.pkl"


def get_google_credentials():
    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return creds


creds = get_google_credentials()

gmail_service = build("gmail", "v1", credentials=creds)
calendar_service = build("calendar", "v3", credentials=creds)

print("Connected to Gmail and Google Calendar.")

# Test Gmail
results = gmail_service.users().messages().list(
    userId="me",
    maxResults=5
).execute()

print("\nGmail test:")
print(results)

# Test Calendar
now = datetime.now(timezone.utc).isoformat()

events = calendar_service.events().list(
    calendarId="primary",
    timeMin=now,
    maxResults=5,
    singleEvents=True,
    orderBy="startTime"
).execute()

print("\nCalendar test:")
print(events)