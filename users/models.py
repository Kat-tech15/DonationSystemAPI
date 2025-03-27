from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator

class CustomUserManager(BaseUserManager):
    """Custom user manager to handle email-based authentication."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("username", email.split("@")[0])  # Auto-generate username
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """Custom User model with email-based authentication and role-based access."""
    
    USER_ROLES = [
        ('DONOR', 'Donor'),
        ('BENEFICIARY', 'Beneficiary'),
        ('ADMIN', 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=USER_ROLES, default='DONOR')
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True, 
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', "Enter a valid phone number.")]
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # Authenticate using email instead of username
    REQUIRED_FIELDS = ["username"]  # Only email is required

    def save(self, *args, **kwargs):
        """Ensure username is auto-generated if missing."""
        if not self.username:
            self.username = self.email.split("@")[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
