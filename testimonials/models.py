from django.db import models
from  users.models import User

class Testimonial(models.Model):
    beneficiary = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials')
    story = models.TextField()
    image = models.ImageField(upload_to='testimonial_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Testimonial by {self.beneficiary.username}"


