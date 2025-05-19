from django.db import models 


class ContactMessage(models.Model):
    full_name = models.CharField(max_length= 50)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.full_name}"



