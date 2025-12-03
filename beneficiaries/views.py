from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Beneficiary
from .serializers import BeneficiarySerializer, BeneficiaryStatusSerializer


class BeneficiaryApplyView(generics.CreateAPIView):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer
    #permission_classes = [permissions.IsAuthenticated]

    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BeneficiaryStatusView(generics.RetrieveAPIView):
    serializer_class = BeneficiaryStatusSerializer
    #permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return Beneficiary.objects.get(user=self.request.user)
    
class BeneficiaryDetailview(generics.RetrieveAPIView):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer
    #permission_classes = [permissions.IsAuthenticated]