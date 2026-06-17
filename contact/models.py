from django.db import models
from django.contrib.auth.models import User
from services.models import Service


class ContactEnquiry(models.Model):

    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('responded', 'Responded'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='enquiries'
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='enquiries'
    )

    name = models.CharField(max_length=200)
    email = models.CharField(max_length=255)
    message = models.TextField()

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='new'
    )

    submitted_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f'{self.name} - {self.email}'