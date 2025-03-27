from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer
import pyotp
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_logged_in_user(request):
    user = request.user
    return Response({
        'id': user.id,
        'email': user.email,
        'username': user.username
    })

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class GoogleLoginView(SocialLoginView):
    """Custom Google Login View with 0Auth2 Adapter."""
    adapter_class = GoogleOAuth2Adapter

# Custom Token Obtain View
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Token Refresh View
class CustomTokenRefreshView(TokenRefreshView):
    pass  # Uses the default refresh behavior

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

        return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
    
class ForgortPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"

            send_mail(
                "Reset Password", 
                f"Click here to reset your password: {reset_url}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

        return Response({"message": "If your email is registered, a reset link has been sent."})

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

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
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
            
        except:
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer  # Ensure this serializer exists

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return Response({
                'message': 'Login successful',
                'access': response.data['access'],
                'refresh': response.data['refresh']
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
