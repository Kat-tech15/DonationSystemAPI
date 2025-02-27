from django.urls import path
from .views import LocationListView, SchedulePickupView, TrackDelivertView


urlpatterns = [
    path('api/logistics/locations/', LocationListView.as_view(), name='location-list'),
    path('api/logistics/schedule_pickup/', SchedulePickupView.as_view(), name='schedule-pickup'),
    path('api/logistics/track/<str:tracking_code>/', TrackDelivertView.as_view(), name='track-delivery'),
]

