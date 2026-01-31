from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def create_google_meet_event(title, start_time, end_time):
    # Authenticate with OAuth flow (example for local testing)
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES
    )
    creds = flow.run_local_server(port=0)

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': title,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'},
        'conferenceData': {
            'createRequest': {'requestId': 'sample123', 'conferenceSolutionKey': {'type': 'hangoutsMeet'}}
        },
    }

    created_event = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1
    ).execute()

    meet_link = created_event['hangoutLink']
    return meet_link
