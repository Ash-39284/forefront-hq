from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

def enquiry(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        message = request.POST.get('message', '')

        order = Order.objects.create(
            user_profile=getattr(request.user, 'userprofile', None) if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            message=message,
        )

        send_mail(
            subject='New Enquiry Received',
            message=f'Thanks {full_name}, we\'ve received your enquiry and will be in touch shortly.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )
        order.confirmation_email_sent = True
        order.save()

        messages.success(request, 'Your enquiry has been sent — we\'ll be in touch soon.')
        return redirect('enquiry')

    return render(request, 'orders/enquiry.html')