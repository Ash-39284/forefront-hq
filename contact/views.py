from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Service, ContactEnquiry

def contact(request):
    services = Service.objects.filter(is_active=True)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        service_id = request.POST.get('service')
        message = request.POST.get('message')

        service = None
        if service_id:
            try:
                service = Service.objects.get(id=service_id)
            except Service.DoesNotExist:
                pass

        ContactEnquiry.objects.create(
            user=request.user if request.user.is_authenticated else None,
            service=service,
            name=name,
            email=email,
            message=message,
        )

        messages.success(request, 'Your message has been sent. We\'ll be in touch within 24 hours.')
        return redirect('contact')

    return render(request, 'contact/contact.html', {'services': services})