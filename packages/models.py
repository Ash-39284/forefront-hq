from django.db import models
from django.contrib.auth.models import User

class Package(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    tier = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_recommended = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    cta_label = models.CharField(max_length=100)
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.name
    
class PackageFeature(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='features')
    feature_text = models.CharField(max_length=255)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f'{self.package.name} - {self.feature_text}'

class PackageAddon(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f'{self.name} - £{self.price}'


class CustomPackageSelection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='custom_selections')
    session_key = models.CharField(max_length=255, blank=True, null=True)
    addons = models.ManyToManyField(PackageAddon, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        return sum(addon.price for addon in self.addons.all())

    def __str__(self):
        return f'Custom selection - {self.user or self.session_key}'