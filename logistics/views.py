from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Location, Delivery
from .serializers import LocationSerializer, DeliverySerializer
from donations.models import Donation


class LocationListView(generics.ListAPIView):
    queryset =Location.objects.filter(is_active=False)
    serializer_class = LocationSerializer
    permission_classes = [permissions.AllowAny]

class SchedulePickupView(generics.CreateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        donation_id = self.request.data.get('donation')
        donation = Donation.objects.get(id=donation_id)
        serializer.save(donation=donation)

class TrackDelivertView(generics.RetrieveAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'tracking_code'
