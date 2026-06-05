import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Package, PackageAddon
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


stripe.api_key = settings.STRIPE_SECRET_KEY

def packages(request):
    packages = Package.objects.filter(is_active=True)
    addons = PackageAddon.objects.filter(is_active=True)
    return render(request, 'packages/packages.html', {
        'packages': packages,
        'addons': addons,
    })

@login_required
def checkout(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': package.stripe_price_id,
            'quantity': 1,
        }],
        mode='payment',
        customer_email=request.user.email,
        success_url=request.build_absolute_uri('/packages/success/'),
        cancel_url=request.build_absolute_uri('/packages/'),
        metadata={
            'package_id': package.id,
            'user_id': request.user.id,
        }
    )

    return redirect(checkout_session.url, code=303)

def success(request):
    return render(request, 'packages/success.html')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        package_id = session['metadata']['package_id']
        user_id = session['metadata']['user_id']
        amount = session['amount_total']
        email = session['customer_email'] or ''
        payment_intent = session['payment_intent'] or ''
        customer_id = session['customer'] or ''

        try:
            from django.contrib.auth.models import User
            from accounts.models import UserProfile
            from orders.models import Order, Payment

            user = User.objects.get(id=user_id)
            user = User.objects.get(id=user_id)
            profile, created = UserProfile.objects.get_or_create(user=user)
            package = Package.objects.get(id=package_id)

            order = Order.objects.create(
                user_profile=profile,
                package=package,
                full_name=user.get_full_name() or email,
                email=email,
                order_total=amount / 100,
                status='paid'
            )

            Payment.objects.create(
                order=order,
                stripe_payment_intent=payment_intent,
                stripe_customer_id=customer_id or '',
                amount=amount / 100,
                currency='gbp',
                status='succeeded'
            )

            print(f'Order {order.id} created for {email}')

        except Exception as e:
            print(f'Webhook error: {e}')

    return HttpResponse(status=200)

def custom_package(request):
    addons = PackageAddon.objects.filter(is_active=True)
    selected_addon_ids = request.session.get('selected_addons', [])
    selected_pages = request.session.get('selected_pages', 0)
    return render(request, 'packages/custom_package.html', {
        'addons': addons,
        'selected_addon_ids': [str(id) for id in selected_addon_ids],
        'selected_pages': selected_pages,
    })


def custom_summary(request):
    if request.method == 'POST':
        selected_addon_ids = request.POST.getlist('addons')
        selected_pages = int(request.POST.get('addon_pages', 0))
        request.session['selected_addons'] = selected_addon_ids
        request.session['selected_pages'] = selected_pages
        return redirect('custom_summary')

    selected_addon_ids = request.session.get('selected_addons', [])
    selected_pages = request.session.get('selected_pages', 0)
    addons = PackageAddon.objects.filter(id__in=selected_addon_ids)
    
    # Get page addon price
    page_addon = PackageAddon.objects.filter(name='Additional Page').first()
    page_total = page_addon.price * selected_pages if page_addon and selected_pages else 0
    
    total = sum(addon.price for addon in addons) + page_total

    return render(request, 'packages/custom_summary.html', {
        'addons': addons,
        'total': total,
        'selected_pages': selected_pages,
        'page_addon': page_addon,
        'page_total': page_total,
    })


def remove_addon(request, addon_id):
    selected_addons = request.session.get('selected_addons', [])
    selected_addons = [a for a in selected_addons if a != str(addon_id)]
    request.session['selected_addons'] = selected_addons
    return redirect('custom_summary')
        
@login_required
def custom_checkout(request):
    selected_addon_ids = request.session.get('selected_addons', [])
    selected_pages = request.session.get('selected_pages', 0)
    addons = PackageAddon.objects.filter(id__in=selected_addon_ids)

    line_items = []

    # Add regular addons
    for addon in addons:
        line_items.append({
            'price_data': {
                'currency': 'gbp',
                'product_data': {
                    'name': addon.name,
                },
                'unit_amount': int(addon.price * 100),
            },
            'quantity': 1,
        })

    # Add additional pages if selected
    if selected_pages and selected_pages > 0:
        page_addon = PackageAddon.objects.filter(name='Additional Page').first()
        if page_addon:
            line_items.append({
                'price_data': {
                    'currency': 'gbp',
                    'product_data': {
                        'name': f'Additional Pages (x{selected_pages})',
                    },
                    'unit_amount': int(page_addon.price * 100),
                },
                'quantity': selected_pages,
            })

    if not line_items:
        return redirect('custom_package')

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        customer_email=request.user.email,
        success_url=request.build_absolute_uri('/packages/success/'),
        cancel_url=request.build_absolute_uri('/packages/'),
        metadata={
            'user_id': request.user.id,
            'custom_package': 'true',
            'addon_ids': ','.join(selected_addon_ids),
            'selected_pages': selected_pages,
        }
    )

    return redirect(checkout_session.url, code=303)

def remove_pages(request):
    request.session['selected_pages'] = 0
    return redirect('custom_summary')

def update_pages(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        current = request.session.get('selected_pages', 0)
        if action == 'increase' and current < 30:
            request.session['selected_pages'] = current + 1
        elif action == 'decrease' and current > 1:
            request.session['selected_pages'] = current - 1
    return redirect('custom_summary')