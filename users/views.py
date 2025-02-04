from django.shortcuts import render
from rest_framework import generics,permissions
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class =UserRegistrationSerializer
    permission_classes =[permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

def home_view(request):
    return HttpResponse("<h1>Welcome to Donations System App!</h1>")