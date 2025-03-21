from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from .models import Transaction
import stripe
from django.conf import settings
from .serializers import TransactionSerializer

class MpesaPaymentView(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(status='completed')
            return Response(serializer.data, status=status.HTTP_201_CRATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PayPalPaymentView(APIView):
    def post(self, request):
        serializer= TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(status='completed')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeSessionView(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                intent = stripe.PaymentIntent.create(
                    amount=int(serializer.validated_data['amount'] * 100),  # amount in cents
                    currency=serializer.validated_data['currency'],
                    metadata={'transaction_id': serializer.validated_data['transaction_id']}
                )
                serializer.save(status='pending')
                return Response({'client_secret': intent.client_secret}, status=status.HTTP_201_CREATED)
            except stripe.error.StripeError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           
class StripeWebhookView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except (ValueError, stripe.error.signatureVerificationError) as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        if event['type'] == 'payment_intent.suceeded':
            payment_intent = event['data']['object']
            transaction_id = payment_intent['metadata']['transaction_id']

            try:
                transaction = Transaction.objects.get(transaction_id=transaction_id)
                transaction.status= 'completed'
                transaction.save()
            
            except Transaction.DoesNotExist:
                pass
        return Response(status=status.HTTP_200_OK)