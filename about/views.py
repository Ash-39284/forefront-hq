from django.shortcuts import render
from .models import StaffAbout

def about(request):
    team_members = StaffAbout.objects.filter(is_active=True).order_by('display_order')
    return render(request, 'about/about.html', {'team_members': team_members})