from django.shortcuts import render
from rest_framework import generics,permissions
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer
import pyotp
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.conf import settings
from twilio.rest import client


User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class =UserRegistrationSerializer
    permission_classes =[permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

def home_view(request):
    return HttpResponse("<h1>Welcome to Donations System App!</h1>")

class OTPLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        totp = pyotp.TOTP(pyotp.random_base32())
        otp_code = totp.now()

        device, created = TOTPDevice.objects.get_or_create(user=user, name="default")
        device.confirmed = True
        device.save()

        send_mail(
            "Your OTP Code",
            f"Your OTP code is: {otp_code}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False
        )

        return Response({"message": "OTP send succesfully"}, status=status.HTTP_200_OK)