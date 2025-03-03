from django.shortcuts import render
from rest_framework import generics,serializers
from .models import Donation
from rest_framework.generics import RetrieveAPIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
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
            raise serializers.ValidationError({"error": "User must be authenticated to make a donation."})

class DonationListView(generics.ListAPIView):
    queryset = Donation.objects.all().order_by('-timestamp')
    serializer_class = DonationSerializer
    permission_classes= [AllowAny]

class DonationDetailView(generics.RetrieveAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer

    def get_object(self):
        obj = get_object_or_404(Donation, pk=self.kwargs.get('pk'))
        return obj