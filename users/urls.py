from django.urls import path, include
from dj_rest_auth.views import LogoutView
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    OTPLoginView, 
    GoogleLoginView,
    ForgortPasswordView, 
    ResetPasswordView, 
    get_logged_in_user, 
    UserRegistrationView, 
    CustomTokenObtainPairView, 
    CustomTokenRefreshView
)

urlpatterns = [
    # User registration
    path('auth/register/', UserRegistrationView.as_view(), name='register'),

    # Authentication (JWT & OTP)
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/google/', GoogleLoginView.as_view(), name='google_login'),
    path('auth/otp-login/', OTPLoginView.as_view(), name='otp_login'),

    # Password reset
    path('auth/password-reset/', ForgortPasswordView.as_view(), name='password_reset'),
    path('auth/password-reset/confirm/', ResetPasswordView.as_view(), name='password_reset_confirm'),

    # JWT Token Management
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    # User profile
    path('auth/me/', get_logged_in_user, name='get_logged_in_user'),

    # Social authentication (AllAuth)
    path('auth/', include('allauth.socialaccount.urls')),
]
