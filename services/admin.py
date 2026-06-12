from django.contrib import admin
from .models import Service

# Register your models here.
@admin.register(Service)
class Services(admin.ModelAdmin):
    list_display = ['name', 'slug', 'short_description', 'description', 'is_active', 'display_order']