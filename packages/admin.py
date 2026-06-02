from django.contrib import admin
from .models import Package, PackageFeature
from .models import Package, PackageFeature, PackageAddon, CustomPackageSelection

class PackageFeatureInline(admin.TabularInline):
    model = PackageFeature
    extra = 1

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'price', 'is_recommended', 'is_active', 'display_order']
    inlines = [PackageFeatureInline]

@admin.register(PackageAddon)
class PackageAddonAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active', 'display_order']