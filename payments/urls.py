from django.urls import path
from . import views 

urlpatterns = [
    path("payments/mpesa-payment/", views.MpesaPaymentView.as_view(), name="mpesa-payment"),
    path("payments/paypal-payment/", views.PayPalPaymentView.as_view(), name="paypal-payment"),
    path("payments/stripe-session/", views.StripeSessionView.as_view(), name="stripe-session"),
]