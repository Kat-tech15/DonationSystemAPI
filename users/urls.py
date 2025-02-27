from django.urls import path, include
from dj_rest_auth.views import LogoutView
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleLogin
from .views import OTPLoginView, ForgotPasswordView, ResetPasswordView
from .views import UserRegistrationView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('auth/google', GoogleLogin.as_view(), name='google_login'),
    path('auth/otp-login', OTPLoginView.as_view(), name='otp_login'),
    path('auth/password-reset/', ForgotPasswordView.as_view(), name='password_reset'),
    path('auth/password-reset/confirm/', ResetPasswordView.as_view(), name='password_reset_confirm'),
]