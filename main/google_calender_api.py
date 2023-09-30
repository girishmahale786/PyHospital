from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import Flow

SCOPES = ['https://www.googleapis.com/auth/calendar/event']

# You can get these credentials on Google Console
CREDENTIALS = "<Your Google OAuth Credentials>"

def confirmation():
    flow = Flow.from_client_config(CREDENTIALS, SCOPES)
    flow.redirect_uri = 'http://127.0.0.1:8000/confirm'
    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true')
    return authorization_url, state


def getCreds(state, url):
    flow = Flow.from_client_config(CREDENTIALS, SCOPES, state=state)
    flow.redirect_uri = 'http://127.0.0.1:8000/confirm'
    flow.fetch_token(authorization_response=url)
    creds = flow.credentials
    return creds

def calender_api(creds, patient, speciality, start, end, doctorEmail):
    try:
        service = build('calendar', 'v3', credentials=creds)
        event = {
            'summary': f"{patient}'s Appointment",
            'description': f"Required Speciality - {speciality}",
            'start': {
                'dateTime': f'{start}',
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': f'{end}',
                'timeZone': 'Asia/Kolkata',
            },
            'attendees': [
                {'email': f"{doctorEmail}"},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            }
        }

        event = service.events().insert(calendarId='primary',
                                        body=event, sendUpdates='all').execute()
        return event.get('htmlLink')

    except HttpError as error:
        return error
