from django.db import models
from users.models import User

class Donation(models.Model):
    DONATION_TYPES = (
        ('MONEY', 'Money'),
        ('SCHOOL_ITEMS', 'School Items'),
        ('FOOD', 'Food'),
        ('FURNITURE', 'Furniture'),
    )
    donor = models. ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    item_type = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='PENDING')
    gps_location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.donor.username} - {self.donation_type}"

