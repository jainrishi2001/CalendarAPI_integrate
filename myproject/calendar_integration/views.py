
from django.http import HttpResponse
from django.shortcuts import redirect
from google.oauth2 import credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os

# Get the current directory path
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the file path to client_secret.json
client_secrets_path = os.path.join(current_directory, 'myproject', 'client_secret.json')


#Step 1: Start OAuth flow and prompt user for credentials
def GoogleCalendarInitView(request):
    flow = Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=['https://www.googleapis.com/auth/calendar.readonly'],
        redirect_uri='http://your-redirect-url.com/rest/v1/calendar/redirect/'
    )

    auth_url, _ = flow.authorization_url(prompt='consent')

    return redirect(auth_url)


# Step 2: Handle redirect and obtain access token
def GoogleCalendarRedirectView(request):
    flow = Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=['https://www.googleapis.com/auth/calendar.readonly'],
        redirect_uri='http://your-redirect-url.com/rest/v1/calendar/redirect/'
    )

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    # Get access token
    credentials = flow.credentials
    access_token = credentials.token

    # Use the access token to get a list of events
    service = build('calendar', 'v3', credentials=credentials)
    events_result = service.events().list(calendarId='primary', maxResults=10).execute()
    events = events_result.get('items', [])

    # Process the events (e.g., return as JSON response)
    response_data = []
    for event in events:
        response_data.append({
            'summary': event['summary'],
            'start': event['start'].get('dateTime', event['start'].get('date')),
            'end': event['end'].get('dateTime', event['end'].get('date'))
        })

    return HttpResponse(response_data, content_type='application/json')
    