from django.shortcuts import render
from rest_framework import generics
from .models import Donation
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from .serializers  import DonationSerializer

class DonationCreateView(generics.CreateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(donor=self.request.user)
        else:
            raise serializer.ValidationError({"error": "User must be authenticated to make a donation."})

class DonationListView(generics.ListAPIView):
    queryset = Donation.objects.all().order_by('-timestamp')
    serializer_class = DonationSerializer

class DonationDetailView(generics.RetrieveAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer