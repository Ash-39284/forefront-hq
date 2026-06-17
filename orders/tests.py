from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import UserProfile
from packages.models import Package
from .models import Order, Payment


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def make_user(email='test@example.com', password='testpass123'):
    user = User.objects.create_user(username=email, email=email, password=password)
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return user, profile


def make_package():
    return Package.objects.create(
        name='Starter',
        code='STR',
        tier='entry',
        price=Decimal('499.00'),
        display_order=1,
        cta_label='Get Started',
        is_active=True,
        stripe_price_id='price_test_123',
    )


# ---------------------------------------------------------------------------
# Order Model Tests
# ---------------------------------------------------------------------------

# Tests for the Order model — str, status choices, field defaults, and package FK behaviour
class OrderModelTest(TestCase):

    def setUp(self):
        self.user, self.profile = make_user()
        self.package = make_package()
        self.order = Order.objects.create(
            user_profile=self.profile,
            package=self.package,
            full_name='Test Buyer',
            email='test@example.com',
            order_total=Decimal('499.00'),
            status='paid',
        )

    def test_str(self):
        self.assertEqual(str(self.order), f'Order {self.order.id} - test@example.com')

    def test_default_status_is_pending(self):
        order = Order.objects.create(
            user_profile=self.profile,
            package=self.package,
            full_name='Test Buyer',
            email='test@example.com',
            order_total=Decimal('499.00'),
        )
        self.assertEqual(order.status, 'pending')

    def test_confirmation_email_sent_defaults_to_false(self):
        order = Order.objects.create(
            user_profile=self.profile,
            package=self.package,
            full_name='Test Buyer',
            email='test@example.com',
            order_total=Decimal('499.00'),
        )
        self.assertFalse(order.confirmation_email_sent)

    def test_created_at_is_set_automatically(self):
        self.assertIsNotNone(self.order.created_at)

    def test_package_set_to_null_on_package_delete(self):
        self.package.delete()
        self.order.refresh_from_db()
        self.assertIsNone(self.order.package)

    def test_order_deleted_on_profile_delete(self):
        order_id = self.order.id
        self.profile.delete()
        self.assertFalse(Order.objects.filter(id=order_id).exists())

    def test_all_status_choices_are_valid(self):
        valid_statuses = ['pending', 'paid', 'cancelled', 'refunded']
        for status in valid_statuses:
            self.order.status = status
            self.order.save()
            self.order.refresh_from_db()
            self.assertEqual(self.order.status, status)

    def test_order_can_be_created_without_package(self):
        order = Order.objects.create(
            user_profile=self.profile,
            package=None,
            full_name='Test Buyer',
            email='test@example.com',
            order_total=Decimal('199.00'),
        )
        self.assertIsNone(order.package)

    def test_related_name_from_profile(self):
        self.assertIn(self.order, self.profile.orders.all())

    def test_related_name_from_package(self):
        self.assertIn(self.order, self.package.orders.all())


# ---------------------------------------------------------------------------
# Payment Model Tests
# ---------------------------------------------------------------------------

# Tests for the Payment model — str, field defaults, status choices, and one-to-one relationship
class PaymentModelTest(TestCase):

    def setUp(self):
        self.user, self.profile = make_user()
        self.package = make_package()
        self.order = Order.objects.create(
            user_profile=self.profile,
            package=self.package,
            full_name='Test Buyer',
            email='test@example.com',
            order_total=Decimal('499.00'),
            status='paid',
        )
        self.payment = Payment.objects.create(
            order=self.order,
            stripe_payment_intent='pi_test_123',
            stripe_customer_id='cus_test_123',
            amount=Decimal('499.00'),
            currency='gbp',
            status='succeeded',
        )

    def test_str(self):
        self.assertEqual(str(self.payment), f'Payment {self.payment.id} - test@example.com')

    def test_default_currency_is_gbp(self):
        order2 = Order.objects.create(
            user_profile=self.profile,
            package=self.package,
            full_name='Test Buyer',
            email='test@example.com',
            order_total=Decimal('499.00'),
        )
        payment = Payment.objects.create(
            order=order2,
            stripe_payment_intent='pi_test_456',
            amount=Decimal('499.00'),
        )
        self.assertEqual(payment.currency, 'gbp')

    def test_default_status_is_pending(self):
        order2 = Order.objects.create(
            user_profile=self.profile,
            package=self.package,
            full_name='Test Buyer',
            email='test@example.com',
            order_total=Decimal('499.00'),
        )
        payment = Payment.objects.create(
            order=order2,
            stripe_payment_intent='pi_test_456',
            amount=Decimal('499.00'),
        )
        self.assertEqual(payment.status, 'pending')

    def test_paid_at_is_set_automatically(self):
        self.assertIsNotNone(self.payment.paid_at)

    def test_stripe_customer_id_can_be_blank(self):
        order2 = Order.objects.create(
            user_profile=self.profile,
            package=self.package,
            full_name='Test Buyer',
            email='test@example.com',
            order_total=Decimal('499.00'),
        )
        payment = Payment.objects.create(
            order=order2,
            stripe_payment_intent='pi_test_789',
            amount=Decimal('499.00'),
        )
        self.assertIsNone(payment.stripe_customer_id)

    def test_payment_deleted_on_order_delete(self):
        payment_id = self.payment.id
        self.order.delete()
        self.assertFalse(Payment.objects.filter(id=payment_id).exists())

    def test_one_to_one_relationship_with_order(self):
        self.assertEqual(self.payment.order, self.order)
        self.assertEqual(self.order.payment, self.payment)

    def test_all_status_choices_are_valid(self):
        valid_statuses = ['pending', 'succeeded', 'failed', 'refunded']
        for status in valid_statuses:
            self.payment.status = status
            self.payment.save()
            self.payment.refresh_from_db()
            self.assertEqual(self.payment.status, status)