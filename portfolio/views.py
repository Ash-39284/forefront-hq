from django.shortcuts import render
from .models import PortfolioProject

def portfolio(request):
    projects = PortfolioProject.objects.filter(is_live=True).prefetch_related('tags').order_by('-completed_at')
    return render(request, 'portfolio/portfolio.html', {'projects': projects})

