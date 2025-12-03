from rest_framework.response import Response
from rest_framework import status, permissions, generics
from drf_yasg.utils import swagger_auto_schema
from .models import Transaction
import stripe
from django.conf import settings
from .serializers import TransactionSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

class MpesaPaymentView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer

    @swagger_auto_schema(request_body=TransactionSerializer, responses={201: TransactionSerializer})
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(status='completed')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PayPalPaymentView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer

    @swagger_auto_schema(request_body=TransactionSerializer, responses={201: TransactionSerializer})
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(status='completed')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StripeSessionView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer

    @swagger_auto_schema(request_body=TransactionSerializer)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                intent = stripe.PaymentIntent.create(
                    amount=int(serializer.validated_data['amount'] * 100),  # cents
                    currency=serializer.validated_data['currency'],
                    metadata={'transaction_id': serializer.validated_data['transaction_id']}
                )
                serializer.save(status='pending')
                return Response({'client_secret': intent.client_secret}, status=status.HTTP_201_CREATED)
            except stripe.error.StripeError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
