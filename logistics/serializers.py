from rest_framework import serializers
from .models import Location, Delivery

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'
        read_only_fields = ('tracking_code', 'status', 'created_at','updated_at')
        