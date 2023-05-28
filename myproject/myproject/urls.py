from django.urls import path
from calendar_integration.views import GoogleCalendarInitView, GoogleCalendarRedirectView

urlpatterns = [
  path('rest/v1/calendar/init/', GoogleCalendarInitView),
  path('rest/v1/calendar/redirect/', GoogleCalendarRedirectView),
]
