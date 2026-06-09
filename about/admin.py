from django.contrib import admin
from .models import StaffAbout

@admin.register(StaffAbout)
class StaffAboutAdmin(admin.ModelAdmin):
    list_display = ['name', 'profile_img', 'job_title', 'bio_description', 'display_order']