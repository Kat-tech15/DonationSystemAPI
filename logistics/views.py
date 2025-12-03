from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Location, Delivery
from .serializers import LocationSerializer, DeliverySerializer
from donations.models import Donation


class LocationListView(generics.ListAPIView):
    """View to list all active donation drop-off points."""
    queryset =Location.objects.filter(is_active=True)
    serializer_class = LocationSerializer
    permission_classes = [permissions.AllowAny]

class SchedulePickupView(generics.CreateAPIView):
    """"View to schedule a donation pickup."""
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        donation_id = self.request.data.get('donation')
        pickup_location_id = self.request.data.get('pickup_location')
        dropoff_location_id = self.request.data.get('dropoff_location')
        scheduled_pickup_time = self.request.data.get('scheduled_pickup_time')

        if not (donation_id and pickup_location_id and dropoff_location_id and scheduled_pickup_time):
            return Response({"message": "Please provide all required fields."}, status=status.HTTP_400_BAD_REQUEST)
        
        donation = get_object_or_404(Donation, id=donation_id)

        serializer.save(user=self.request.user, donation=donation)
        return Response({"message": "Pickup scheduled succesfully!"}, status=status.HTTP_201_CREATED )

class TrackDelivertView(generics.RetrieveAPIView):
    """View to track a donation delivery using a tracking code."""
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'tracking_code'

    def get_object(self):
        tracking_code = self.kwargs.get('tracking_code')
        return get_object_or_404(Delivery, tracking_code=tracking_code)
