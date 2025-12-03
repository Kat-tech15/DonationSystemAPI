from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'amount', 'currency']  
        read_only_fields = ['status', 'created_at', 'updated_at', 'user']  
