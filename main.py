import os

# os.system("pip install django")
# os.system("pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")

# Initialize Django
os.system("django-admin startproject myproject")
os.chdir("myproject")

# Create Django app
os.system("python manage.py startapp calendar_integration")

# Replace the contents of settings.py
# with open("myproject/settings.py", "w") as f:
#     f.write("""
# import os

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECRET_KEY = 'your-secret-key'

# DEBUG = True

# ALLOWED_HOSTS = []

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'calendar_integration',
# ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'myproject.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'myproject.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

# USE_I18N = True

# USE_TZ = True

# STATIC_URL = '/static/'
#     """)

# Create the required views.py file
with open("calendar_integration/views.py", "w") as f:
  f.write("""
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
    """)

# # Create the required URLs in urls.py
# with open("myproject/urls.py", "w") as f:
#     f.write("""
# from django.urls import path
# from calendar_integration.views import GoogleCalendarInitView, GoogleCalendarRedirectView

# urlpatterns = [
#     path('rest/v1/calendar/init/', GoogleCalendarInitView),
#     path('rest/v1/calendar/redirect/', GoogleCalendarRedirectView),
# ]
#     """)

# Create the required models.py file
with open("calendar_integration/models.py", "w") as f:
  f.write("""
from django.db import models

# Your models go here (if any)
    """)

# Create the required migrations
os.system("python manage.py makemigrations")
os.system("python manage.py migrate")

# # Add client_secrets.json file
# with open("client_secrets.json", "w") as f:
#     f.write("""
# {
#   "web": {
#     "client_id": "YOUR_CLIENT_ID",
#     "client_secret": "YOUR_CLIENT_SECRET",
#     "redirect_uris": ["http://your-redirect-url.com/rest/v1/calendar/redirect/"],
#     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#     "token_uri": "https://accounts.google.com/o/oauth2/token",
#     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#     "scopes": ["https://www.googleapis.com/auth/calendar.readonly"]
#   }
# }
#     """)

# Run the Django server
os.system("python manage.py runserver 0.0.0.0:3000")
