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
from twilio.rest import Client
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail

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
    
class ForgortPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{settings.FRONTED_URL}/reset-password/{uid}/{token}"


            send_mail(
                "Rest Password", 
                f"Click here to reset your password: {reset_url}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

        return Response({"message": "If your email is registered, a reset link has been sent."})

class ResetPasswordView(APIView):
    permission_classes =[AllowAny]

    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")


        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password reset successfully"})
            
            else:
                return Response({"error": "invalid token"}, status=status.HTTP_400_BAD_REQUEST)
            
        except:
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        
class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return Response({'message': 'Login succesful', 'access': response.data['access'], 'refresh': response.data['refresh']})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)