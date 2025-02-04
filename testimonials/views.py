from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from donations.models  import Donation
from beneficiaries.models import Beneficiary
from rest_framework import generics, permissions
from .models import Testimonial
from .serializers import TestimonialSerializer



class TestimonialListView(generics.ListAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.AllowAny]


class TestimonialCreateView(generics.CreateAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(beneficiary=self.request.user)
    
class ImpactMerticsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        total_donations = Donation.objects.count()
        total_beneficiaries = Beneficiary.objects.filter(application_status='APPROVED').count()
        success_rate = (total_beneficiaries / Beneficiary.objects.count()) * 100 if Beneficiary.objects.count() > 0 else 0

        metrics = {
            'total_donations_received': total_donations,
            'total_students_and_institutions_supported': total_beneficiaries,
            'success_rate': f"{success_rate:.2f}"
        }
        return Response(metrics, status=status.HTTP_200_OK)

