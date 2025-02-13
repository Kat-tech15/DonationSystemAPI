from django.urls import path
from .views import LocationListView, SchedulePickupView, TrackDelivertView


urlpatterns = [
    path('locations/', LocationListView.as_view(), name='location-list'),
    path('schedule_pickup/', SchedulePickupView.as_view(), name='schedule-pickup'),
    path('track/<str:tracking_code>/', TrackDelivertView.as_view(), name='track-delivery'),
]

