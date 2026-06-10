from django.contrib import admin
from .models import StaffAbout

@admin.register(StaffAbout)
class StaffAboutAdmin(admin.ModelAdmin):
    list_display = ['name', 'job_title', 'is_active', 'display_order']