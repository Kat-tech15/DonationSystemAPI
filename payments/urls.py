from django.urls import path
from  .import views
from .views import MpesaPaymentView, PaypalPaymentView, StripeSessionView, StripeWebhookView

urlpatterns = [
    path("api/payments/mpesa-payment/", views.MpesaPaymentView, name="mpesa-payment"),
    path("api/payments/paypal-payment/", views.PaypalPaymentView, name="paypal-payment"),
    path("api/payments/stripe-session/", views.StripeSessionView, name="stripe-session"),
    path("api/payments/srtipe-webhook/", views.StripeWebhookView.as_view(), name="stripe-webhook"),
]