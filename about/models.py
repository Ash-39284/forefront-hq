from django.db import models
from django.contrib.auth.models import User

class StaffAbout(models.Model):
    name = models.CharField(max_length=20, blank=True)
    profile_img = models.ImageField(default=False)
    job_title = models.CharField(max_length=25, blank=True, null=True)
    bio_description = models.TextField(max_length=255, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)

    def __str__(self):
        return self
