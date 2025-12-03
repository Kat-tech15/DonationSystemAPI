from django.db import models
from users.models import User
from donations.models import Donation
import googlemaps
from django.conf import settings
import uuid
from uuid import uuid4

def generate_tracking_code():
    return str(uuid.uuid4()).replace("-", "")[:10]


class Location(models.Model):
    name = models. CharField(max_length=255) 
    address = models. CharField(max_length=255)
    latitude = models.FloatField() 
    longitude = models.FloatField()
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name
    
class Delivery(models.Model):
    donation = models.OneToOneField(Donation, on_delete=models.CASCADE, related_name='delivery')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    pickup_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pickups')
    dropoff_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='dropoffs')
    scheduled_pickup_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=(
        ('PENDING', 'Pending'),
        ('IN_TRANSIT', 'In Transit'),
        ('DELIVERED', 'Delivered'),
    ),default='PENDING')
    tracking_code = models.CharField(max_length=100, unique=True, default=generate_tracking_code, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.tracking_code:
            self.tracking_code = str(uuid.uuid4()).replace("-", "")[:10]
        super().save(*args, **kwargs)

    def calculate_route(self):
        """Returns the driving route from pickup to drop-off using Google Maps API."""
        try:
            gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
            origin = (self.pickup_location.latitude, self.pickup_location.longitude)
            destination = (self.dropoff_location.latitude, self.dropoff_location.longitude)
            directions = gmaps.directions(origin, destination, mode='driving')

            return directions
        
        except Exception as e:
            return {"error": str(e)}

    def __str__(self):
        return f"Delivery for {self.donation.username}"


