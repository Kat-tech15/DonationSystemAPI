from rest_framework import serializers
from .models import Donation




class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.donation_type == 'money':
            return{k: data[k] for k in ['id', 'donor', 'donation_type', 'amount', 'payment_method', 'status', 'gps_location', 'timestamp']}
        elif instance.donation_type == 'food':
            return{k: data[k] for k in ['id', 'donor', 'donation_type', 'item_name', 'quantity', 'gps_location', 'timestamp']}
        elif instance.donation_type == 'school_items':
            return{k: data[k] for k in ['id', 'donor', 'donation_type', 'material_type', 'quantity', 'gps_location', 'timestamp']}
        elif instance.donation_type == 'furniture':
            return{k: data[k] for k in ['id', 'donor', 'donation_type', 'material_type', 'quantity', 'gps_location', 'timestamp']}
        
        return data if data else {}