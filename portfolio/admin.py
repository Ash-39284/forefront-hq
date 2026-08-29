from django.contrib import admin
from .models import PortfolioProject, ProjectTag, PortfolioProjectTag, PortfolioUpcoming, PortfolioUpcomingTag

class PortfolioProjectTagInline(admin.TabularInline):
    model = PortfolioProjectTag
    extra = 1

class PortfolioUpcomingTagInline(admin.TabularInline):
    model = PortfolioUpcomingTag
    extra = 1

@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'client_name', 'category', 'is_live', 'is_featured', 'completed_at']
    inlines = [PortfolioProjectTagInline]

@admin.register(PortfolioUpcoming)
class PortfolioUpcomingAdmin(admin.ModelAdmin):
    list_display = ['title', 'client_name', 'category', 'is_live', 'is_featured', 'completed_at']
    inlines = [PortfolioUpcomingTagInline]

@admin.register(ProjectTag)
class ProjectTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']