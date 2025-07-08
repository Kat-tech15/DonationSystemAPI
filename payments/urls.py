from django.urls import path
from .views import MpesaPaymentView, PayPalPaymentView, StripeSessionView, StripeWebhookView

urlpatterns = [
    path("payments/mpesa-payment/", MpesaPaymentView.as_view(), name="mpesa-payment"),
    path("payments/paypal-payment/", PayPalPaymentView.as_view(), name="paypal-payment"),
    path("payments/stripe-session/", StripeSessionView.as_view(), name="stripe-session"),
    path("payments/stripe-webhook/", StripeWebhookView.as_view(), name="stripe-webhook"),
]