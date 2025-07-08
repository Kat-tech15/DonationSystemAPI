from django.urls import path
from .views import LocationListView, SchedulePickupView, TrackDelivertView


urlpatterns = [
    path('logistics/locations/', LocationListView.as_view(), name='location-list'),
    path('logistics/schedule_pickup/', SchedulePickupView.as_view(), name='schedule-pickup'),
    path('logistics/track/<str:tracking_code>/', TrackDelivertView.as_view(), name='track-delivery'),
]

