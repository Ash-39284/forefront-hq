from django.db import models
from accounts.models import UserProfile

class Order(models.Model):

    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('closed', 'Closed'),
    ]

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    confirmation_email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f'Enquiry {self.id} - {self.email}'