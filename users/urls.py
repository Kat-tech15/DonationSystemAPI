from django.urls import path, include
from dj_rest_auth.views import LogoutView, LoginView
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from .views import OTPLoginView, ForgortPasswordView, ResetPasswordView
from .views import UserRegistrationView, CustomTokenObtainPairView

urlpatterns = [
    path('api/register/', UserRegistrationView.as_view(),name='register'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/google/', LoginView.as_view(), name='google_login'),
    path('api/auth/otp-login/', OTPLoginView.as_view(), name='otp_login'),
    path('api/auth/password-reset/', ForgortPasswordView.as_view(), name='password_reset'),
    path('api/auth/password-reset/confirm/', ResetPasswordView.as_view(), name='password_reset_confirm'),
    path('api/auth/', include('allauth.socialaccount.urls')),
]