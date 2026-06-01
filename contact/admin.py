from django.contrib import admin
from .models import Service, ContactEnquiry

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'display_order']

@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'service', 'status', 'submitted_at']
    list_filter = ['status']
