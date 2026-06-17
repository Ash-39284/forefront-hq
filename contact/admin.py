from django.contrib import admin
from .models import ContactEnquiry

@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'service', 'status', 'submitted_at']
    list_filter = ['status']
