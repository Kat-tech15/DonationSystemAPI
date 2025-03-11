from django.urls import path
from  .import views
from .views import MpesaPaymentView, PaypalPaymentView, StripeSessionView, StripeWebhookView

urlpatterns = [
    path("api/mpesa-payment/", views.MpesaPaymentView, name="mpesa-payment"),
    path("api/paypal-payment/", views.PaypalPaymentView, name="paypal-payment"),
    path("api/stripe-session/", views.StripeSessionView, name="stripe-session"),
    path("api/srtipe-webhook/", views.StripeWebhookView.as_view(), name="stripe-webhook"),
]