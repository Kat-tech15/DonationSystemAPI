from django.shortcuts import render
import requests
import paypalrestsdk
import stripe
import json
from  django.views import View
from django.conf import settings    
from .models import Transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def MpesaPaymentView(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        amount = request.POST.get("amount")

        access_token = "YOUR_ACCESS_TOKEN"
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

        headers = {"Authorization": f"Bearer {access_token}"}
        payload = {
            "BusinessShortCode": "174379",
            "Password": "ENCODED_PASSWORD",
            "Timestamp": "20211014101010",
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": "174379",
            "PhoneNumber": phone,   
            "CallBackURL": "https://yourwebsite.com/mpesa-callback",
            "AccountReference": "Donation",
            "TransactionDesc": "Donation Payment",
        }
        
        response = requests.post(api_url, json=payload, headers=headers)
        data = response.json()

        transaction = Transaction.objects.create(
            payment_method="mpesa",
            transaction_id=data.get("CheckoutRequestID"),
            amount=amount,
            status="Pending",
        )
        return JsonResponse(data)
    
paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": "YOUR_PAYPAL_CLIENT_ID",
    "client_secret": "YOUR_PAYPAL_CLIENT_SECRET",
})
@csrf_exempt
def PaypalPaymentView(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [{"amount": {"total": amount, "currency": "USD"}}],
            "redirect_urls": {
                "return_url": "https://yourwebsite.com/paypal-success",
                "cancel_url": "https://yourwebsite.com/paypal-cancel",
            },
        })

        if payment.create():
            transaction = Transaction.objects.create(
                payment_method="paypal",
                transaction_id=payment.id,
                amount=amount,
                status="Pending",
            )
            return JsonResponse({"approval_url": payment.links[1].href})
        else:
            return JsonResponse({"error": payment.error})
        
stripe.api_key = "YOUR_STRIPE_SECRET_KEY"

@csrf_exempt
def StripeSessionView(request):
    if request.method == "POST":
        amount = int(float(request.POST.get("amount")) * 100)  # Stripe uses cents

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price_data": {
                "currency": "usd",
                "product_data": {"name": "Donation"},
                "unit_amount": amount,
            }, "quantity": 1}],
            mode="payment",
            success_url="https://yourwebsite.com/stripe-success",
            cancel_url="https://yourwebsite.com/stripe-cancel",
        )

        transaction = Transaction.objects.create(
            payment_method="stripe",
            transaction_id=session.id,
            amount=request.POST.get("amount"),
            status="Pending",
        )
        return JsonResponse({"session_id": session.id, "payment_url": session.url})
    
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", None)
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError:
            return JsonResponse({"error": "Invalid payload"}, status=400)
        except stripe.error.SignatureVerificationError:
            return JsonResponse({"error": "Invalid signature"}, status=400)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            transaction_id = session["id"]
            amount = session["amount_total"] / 100 

            
            transaction = Transaction.objects.filter(transaction_id=transaction_id).first()
            if transaction:
                transaction.status = "Success"
                transaction.save()

            print(f"✅ Payment successful for Transaction ID: {transaction_id}")

        return JsonResponse({"status": "success"}, status=200)