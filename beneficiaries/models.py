from django.db import models
from users.models import User


class Beneficiary(models.Model):
    NEEDY_STATUS_CHIOCES = (
        ('ORPHAN', 'Orphan'),
        ('SINGLE-PARENT', 'Single Parent'),
        ('LOW_INCOME', 'Low Income Family'),

    )
    EDUCATIONAL_LEVEL_CHOICES =(
        ('PRIMARY', 'Primary '),
        ('SECONDARY', 'Secondary'),
        ('TERTIARY', 'Tertiary'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='beneficiary')
    needy_status = models.CharField(max_length=20, choices=NEEDY_STATUS_CHIOCES)
    institution_name = models.CharField(max_length=20, choices=EDUCATIONAL_LEVEL_CHOICES, blank=True, null=True)
    academic_performance = models.CharField(max_length=255, blank=True, null=True)
    supporting_documents =models.FileField(upload_to='beneficiary_documents/', blank=True, null=True)
    application_status = models.CharField(max_length=20, default='PENDING', choices=(
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.needy_status}"