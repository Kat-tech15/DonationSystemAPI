from django.shortcuts import render
from rest_framework import generics
from .models import Donation
from .serializers  import DonationSerializer

class DonationCreateView(generics.CreateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer

class DonationListView(generics.ListAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer

class DonationDetailView(generics.RetrieveAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
