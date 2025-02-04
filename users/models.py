from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_ROLES = [
        ('DONOR', 'Donor'),
        ('BENEFICIARY', 'Beneficiary'),
        ('ADMIN', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=USER_ROLES, default='donor')
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
