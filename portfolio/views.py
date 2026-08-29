from django.shortcuts import render
from .models import PortfolioProject, PortfolioUpcoming

def portfolio(request):
    projects = PortfolioProject.objects.filter(is_live=True).prefetch_related('tags').order_by('-completed_at')
    upcoming_projects = PortfolioUpcoming.objects.prefetch_related('tags').order_by('-completed_at')
    return render(request, 'portfolio/portfolio.html', {
        'projects': projects,
        'upcoming_projects': upcoming_projects,
    })