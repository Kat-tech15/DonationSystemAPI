from django.urls import path
from .views import MpesaPaymentView, PaypalPaymentView, StripeSessionView, StripeWebhookView

urlpatterns = [
    path("api/payments/mpesa-payment/", MpesaPaymentView.as_view(), name="mpesa-payment"),
    path("api/payments/paypal-payment/", PaypalPaymentView.as_view(), name="paypal-payment"),
    path("api/payments/stripe-session/", StripeSessionView.as_view(), name="stripe-session"),
    path("api/payments/srtipe-webhook/", StripeWebhookView.as_view(), name="stripe-webhook"),
]