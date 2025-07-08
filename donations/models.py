from django.db import models
from users.models import User
from rest_framework import viewsets, serializers

class Donation(models.Model):
    DONATION_TYPES = (
        ('MONEY', 'Money'),
        ('STATIONERY', 'Stationary'),
        ('FOOD', 'Food'),
        ('FURNITURE', 'Furniture'),
    )
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
    )
    PAYMENT_METHODS = (
        ('MPESA', 'M-Pesa'),
        ('BANK', 'Bank Transfer'),
        ('PAYPAL', 'PayPal'),
        ('CASH', 'Cash'),
    )
    donor = models. ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    item_name = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    payment_method = models.CharField(max_length=50,  choices=PAYMENT_METHODS, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='PENDING')
    gps_location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.donor.username} - {self.donation_type}"

