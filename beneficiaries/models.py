from django.db import models
from users.models import User


class Beneficiary(models.Model):
    NEEDY_STATUS_CHIOCES = (
        ('ORPHAN', 'Orphan'),
        ('SINGLE-PARENT', 'Single Parent'),
        ('LOW_INCOME', 'Low Income Family'),

    )
    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE','Female'),
        ('OTHER', 'Other'),
    )
    EDUCATIONAL_LEVEL_CHOICES =(
        ('PRIMARY', 'Primary '),
        ('SECONDARY', 'Secondary'),
        ('TERTIARY', 'Tertiary'),
    )
    ACADEMIC_PERFORMANCE =(
        ('EXCELLENT', 'Excellent (80-100%)'),
        ('GOOD', 'Good (60-79%)'),
        ('AVERAGE', 'Average (40-59%)'),
        ('BELOW_AVERAGE', 'Below Average (20-39%)'),
        ('POOR', 'Poor (0-19%)'),
    )

    APPLICATION_STATUS =(
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')
    )
    #name= models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='beneficiary')
    needy_status = models.CharField(max_length=20, choices=NEEDY_STATUS_CHIOCES)
    institution_name = models.CharField(max_length=20, choices=EDUCATIONAL_LEVEL_CHOICES, blank=True, null=True)
    supporting_documents =models.FileField(upload_to='beneficiary_documents/', blank=True, null=True)
    age = models.PositiveBigIntegerField(default=18)
    gender = models.CharField( max_length=10,choices=GENDER_CHOICES,default='other')
    academic_performance = models.CharField(max_length=20,choices=ACADEMIC_PERFORMANCE,default='average')
    application_status = models.CharField(max_length=20, default='PENDING', choices=APPLICATION_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.needy_status}" 