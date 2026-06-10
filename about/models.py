from django.db import models


class StaffAbout(models.Model):
    name = models.CharField(max_length=100)
    profile_img_url = models.URLField(max_length=500, blank=True, null=True)
    job_title = models.CharField(max_length=50, blank=True, null=True)
    bio_description = models.TextField(null=True)
    is_active = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.name




