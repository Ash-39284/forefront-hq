from django.shortcuts import render
from .models import Service

def services(request):
    services = Service.objects.filter(is_active=True).order_by('display_order')
    return render(request, 'services/services.html', {'services': services})
