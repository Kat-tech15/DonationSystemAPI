from rest_framework import serializers
from .models import Beneficiary

class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = '__all__'
        read_only_fields = ('application_status', 'created_at', 'updated_at')

class BeneficiaryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = ('id', 'application_status','created_at', 'updated_at')
