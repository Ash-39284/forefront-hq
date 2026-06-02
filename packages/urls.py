from django.urls import path
from . import views

urlpatterns = [
    path('packages/', views.packages, name='packages'),
    path('packages/checkout/<int:package_id>/', views.checkout, name='checkout'),
    path('packages/custom/', views.custom_package, name='custom_package'),
    path('packages/custom/summary/', views.custom_summary, name='custom_summary'),
    path('packages/custom/remove/<int:addon_id>/', views.remove_addon, name='remove_addon'),
    path('packages/custom/checkout/', views.custom_checkout, name='custom_checkout'),
    path('packages/success/', views.success, name='payment_success'),
    path('packages/webhook/', views.stripe_webhook, name='stripe_webhook'),
]