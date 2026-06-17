import json
import time
import hmac
import hashlib
from decimal import Decimal
from unittest.mock import patch, MagicMock

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from accounts.models import UserProfile
from orders.models import Order, Payment
from .models import Package, PackageFeature, PackageAddon, CustomPackageSelection


# ---------------------------------------------------------------------------
# Model Tests
# ---------------------------------------------------------------------------

# Tests for the Package model — str representation, default ordering, and field defaults
class PackageModelTest(TestCase):

    def setUp(self):
        self.package = Package.objects.create(
            name='Starter',
            code='STR',
            tier='entry',
            price=Decimal('499.00'),
            is_recommended=False,
            is_active=True,
            display_order=1,
            cta_label='Get Started',
            stripe_price_id='price_test_123',
        )

    def test_str(self):
        self.assertEqual(str(self.package), 'Starter')

    def test_default_ordering(self):
        Package.objects.create(
            name='Pro', code='PRO', tier='mid', price=Decimal('999.00'),
            display_order=2, cta_label='Go Pro', is_active=True,
        )
        packages = list(Package.objects.all())
        self.assertEqual(packages[0].name, 'Starter')
        self.assertEqual(packages[1].name, 'Pro')

    def test_is_active_default(self):
        p = Package.objects.create(
            name='Draft', code='DFT', tier='entry', price=Decimal('0.00'),
            cta_label='Draft', display_order=99,
        )
        self.assertTrue(p.is_active)

    def test_is_recommended_default(self):
        self.assertFalse(self.package.is_recommended)


# Tests for the PackageFeature model — str representation, related name access, and ordering
class PackageFeatureModelTest(TestCase):

    def setUp(self):
        self.package = Package.objects.create(
            name='Starter', code='STR', tier='entry', price=Decimal('499.00'),
            display_order=1, cta_label='Get Started', is_active=True,
        )
        self.feature = PackageFeature.objects.create(
            package=self.package,
            feature_text='5 pages included',
            display_order=1,
        )

    def test_str(self):
        self.assertEqual(str(self.feature), 'Starter - 5 pages included')

    def test_related_name(self):
        self.assertIn(self.feature, self.package.features.all())

    def test_ordering(self):
        f2 = PackageFeature.objects.create(
            package=self.package, feature_text='SEO setup', display_order=2
        )
        features = list(self.package.features.all())
        self.assertEqual(features[0], self.feature)
        self.assertEqual(features[1], f2)


# Tests for the PackageAddon model — str representation, default ordering, and is_active default
class PackageAddonModelTest(TestCase):

    def setUp(self):
        self.addon = PackageAddon.objects.create(
            name='Logo Design',
            description='Professional logo creation',
            price=Decimal('150.00'),
            is_active=True,
            display_order=1,
        )

    def test_str(self):
        self.assertEqual(str(self.addon), 'Logo Design - £150.00')

    def test_default_ordering(self):
        addon2 = PackageAddon.objects.create(
            name='SEO Audit', description='Full SEO audit',
            price=Decimal('75.00'), display_order=2,
        )
        addons = list(PackageAddon.objects.all())
        self.assertEqual(addons[0], self.addon)
        self.assertEqual(addons[1], addon2)

    def test_is_active_default(self):
        self.assertTrue(self.addon.is_active)


# Tests for CustomPackageSelection — str with user/session key, and get_total() with and without addons
class CustomPackageSelectionModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123'
        )
        self.addon1 = PackageAddon.objects.create(
            name='Logo Design', description='Logo', price=Decimal('150.00'), display_order=1
        )
        self.addon2 = PackageAddon.objects.create(
            name='SEO Audit', description='SEO', price=Decimal('75.00'), display_order=2
        )
        self.selection = CustomPackageSelection.objects.create(user=self.user)
        self.selection.addons.set([self.addon1, self.addon2])

    def test_str_with_user(self):
        self.assertIn('testuser', str(self.selection))

    def test_str_with_session_key(self):
        sel = CustomPackageSelection.objects.create(session_key='abc123')
        self.assertIn('abc123', str(sel))

    def test_get_total(self):
        self.assertEqual(self.selection.get_total(), Decimal('225.00'))

    def test_get_total_no_addons(self):
        sel = CustomPackageSelection.objects.create(user=self.user)
        self.assertEqual(sel.get_total(), Decimal('0'))


# ---------------------------------------------------------------------------
# View Tests
# ---------------------------------------------------------------------------

# Tests for the packages listing view — status code, template, and active-only filtering
class PackagesViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.active_package = Package.objects.create(
            name='Starter', code='STR', tier='entry', price=Decimal('499.00'),
            display_order=1, cta_label='Get Started', is_active=True,
        )
        self.inactive_package = Package.objects.create(
            name='Hidden', code='HID', tier='entry', price=Decimal('99.00'),
            display_order=2, cta_label='Hidden', is_active=False,
        )
        self.addon = PackageAddon.objects.create(
            name='Logo Design', description='Logo', price=Decimal('150.00'),
            is_active=True, display_order=1,
        )

    def test_packages_view_status_200(self):
        response = self.client.get(reverse('packages'))
        self.assertEqual(response.status_code, 200)

    def test_packages_view_uses_correct_template(self):
        response = self.client.get(reverse('packages'))
        self.assertTemplateUsed(response, 'packages/packages.html')

    def test_packages_view_only_shows_active_packages(self):
        response = self.client.get(reverse('packages'))
        self.assertIn(self.active_package, response.context['packages'])
        self.assertNotIn(self.inactive_package, response.context['packages'])

    def test_packages_view_shows_active_addons(self):
        response = self.client.get(reverse('packages'))
        self.assertIn(self.addon, response.context['addons'])


# Tests for the checkout view — login protection, Stripe redirect, metadata, and 404 handling
class CheckoutViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123'
        )
        self.package = Package.objects.create(
            name='Starter', code='STR', tier='entry', price=Decimal('499.00'),
            display_order=1, cta_label='Get Started', is_active=True,
            stripe_price_id='price_test_123',
        )

    def test_checkout_redirects_anonymous_user(self):
        response = self.client.get(reverse('checkout', args=[self.package.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    @patch('packages.views.stripe.checkout.Session.create')
    def test_checkout_redirects_to_stripe(self, mock_create):
        mock_session = MagicMock()
        mock_session.url = 'https://checkout.stripe.com/test'
        mock_create.return_value = mock_session

        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('checkout', args=[self.package.id]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'https://checkout.stripe.com/test')

    @patch('packages.views.stripe.checkout.Session.create')
    def test_checkout_passes_correct_metadata(self, mock_create):
        mock_session = MagicMock()
        mock_session.url = 'https://checkout.stripe.com/test'
        mock_create.return_value = mock_session

        self.client.login(username='testuser', password='testpass123')
        self.client.get(reverse('checkout', args=[self.package.id]))

        call_kwargs = mock_create.call_args[1]
        self.assertEqual(call_kwargs['metadata']['package_id'], self.package.id)
        self.assertEqual(call_kwargs['metadata']['user_id'], self.user.id)

    def test_checkout_404_for_invalid_package(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('checkout', args=[9999]))
        self.assertEqual(response.status_code, 404)


# Tests for the payment success view — status code and correct template
class SuccessViewTest(TestCase):

    def test_success_view_status_200(self):
        response = self.client.get(reverse('payment_success'))
        self.assertEqual(response.status_code, 200)

    def test_success_view_uses_correct_template(self):
        response = self.client.get(reverse('payment_success'))
        self.assertTemplateUsed(response, 'packages/success.html')


# Tests for the payment cancel view — redirect to packages and error message
class CancelViewTest(TestCase):

    def test_cancel_redirects_to_packages(self):
        response = self.client.get(reverse('payment_cancel'))
        self.assertRedirects(response, reverse('packages'))

    def test_cancel_adds_error_message(self):
        response = self.client.get(reverse('payment_cancel'), follow=True)
        messages = list(response.context['messages'])
        self.assertTrue(any('cancelled' in str(m).lower() for m in messages))


# Tests for the custom package builder view — status code, template, and addon context
class CustomPackageViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.addon = PackageAddon.objects.create(
            name='Logo Design', description='Logo', price=Decimal('150.00'),
            is_active=True, display_order=1,
        )

    def test_custom_package_view_status_200(self):
        response = self.client.get(reverse('custom_package'))
        self.assertEqual(response.status_code, 200)

    def test_custom_package_uses_correct_template(self):
        response = self.client.get(reverse('custom_package'))
        self.assertTemplateUsed(response, 'packages/custom_package.html')

    def test_custom_package_shows_active_addons(self):
        response = self.client.get(reverse('custom_package'))
        self.assertIn(self.addon, response.context['addons'])


# Tests for the custom summary view — POST stores session, GET renders, and total is calculated correctly
class CustomSummaryViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.addon = PackageAddon.objects.create(
            name='Logo Design', description='Logo', price=Decimal('150.00'),
            is_active=True, display_order=1,
        )

    def test_post_stores_addons_in_session(self):
        response = self.client.post(reverse('custom_summary'), {
            'addons': [str(self.addon.id)],
            'addon_pages': '0',
        })
        self.assertRedirects(response, reverse('custom_summary'))
        self.assertIn(str(self.addon.id), self.client.session['selected_addons'])

    def test_get_renders_summary(self):
        session = self.client.session
        session['selected_addons'] = [str(self.addon.id)]
        session['selected_pages'] = 0
        session.save()

        response = self.client.get(reverse('custom_summary'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'packages/custom_summary.html')

    def test_total_calculated_correctly(self):
        session = self.client.session
        session['selected_addons'] = [str(self.addon.id)]
        session['selected_pages'] = 0
        session.save()

        response = self.client.get(reverse('custom_summary'))
        self.assertEqual(response.context['total'], Decimal('150.00'))


# Tests for the remove addon view — removes correct addon from session and redirects
class RemoveAddonViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.addon = PackageAddon.objects.create(
            name='Logo Design', description='Logo', price=Decimal('150.00'),
            is_active=True, display_order=1,
        )

    def test_remove_addon_from_session(self):
        session = self.client.session
        session['selected_addons'] = [str(self.addon.id), '999']
        session.save()

        self.client.get(reverse('remove_addon', args=[self.addon.id]))
        self.assertNotIn(str(self.addon.id), self.client.session['selected_addons'])
        self.assertIn('999', self.client.session['selected_addons'])

    def test_remove_addon_redirects_to_summary(self):
        session = self.client.session
        session['selected_addons'] = []
        session.save()
        response = self.client.get(reverse('remove_addon', args=[self.addon.id]))
        self.assertRedirects(response, reverse('custom_summary'))


# Tests for the update pages view — increment/decrement, boundary limits (1–30), and redirect
class UpdatePagesViewTest(TestCase):

    def test_increase_pages(self):
        session = self.client.session
        session['selected_pages'] = 2
        session.save()

        self.client.post(reverse('update_pages'), {'action': 'increase'})
        self.assertEqual(self.client.session['selected_pages'], 3)

    def test_decrease_pages(self):
        session = self.client.session
        session['selected_pages'] = 3
        session.save()

        self.client.post(reverse('update_pages'), {'action': 'decrease'})
        self.assertEqual(self.client.session['selected_pages'], 2)

    def test_cannot_increase_above_30(self):
        session = self.client.session
        session['selected_pages'] = 30
        session.save()

        self.client.post(reverse('update_pages'), {'action': 'increase'})
        self.assertEqual(self.client.session['selected_pages'], 30)

    def test_cannot_decrease_below_1(self):
        session = self.client.session
        session['selected_pages'] = 1
        session.save()

        self.client.post(reverse('update_pages'), {'action': 'decrease'})
        self.assertEqual(self.client.session['selected_pages'], 1)

    def test_redirects_to_summary(self):
        response = self.client.post(reverse('update_pages'), {'action': 'increase'})
        self.assertRedirects(response, reverse('custom_summary'))


# Tests for the remove pages view — resets selected_pages to zero and redirects to summary
class RemovePagesViewTest(TestCase):

    def test_remove_pages_sets_to_zero(self):
        session = self.client.session
        session['selected_pages'] = 5
        session.save()

        self.client.get(reverse('remove_pages'))
        self.assertEqual(self.client.session['selected_pages'], 0)

    def test_remove_pages_redirects(self):
        response = self.client.get(reverse('remove_pages'))
        self.assertRedirects(response, reverse('custom_summary'))


# Tests for the custom checkout view — login protection, empty addon guard, and Stripe redirect
class CustomCheckoutViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123'
        )
        self.addon = PackageAddon.objects.create(
            name='Logo Design', description='Logo', price=Decimal('150.00'),
            is_active=True, display_order=1,
        )

    def test_custom_checkout_requires_login(self):
        response = self.client.get(reverse('custom_checkout'))
        self.assertEqual(response.status_code, 302)

    def test_custom_checkout_redirects_if_no_addons(self):
        self.client.login(username='testuser', password='testpass123')
        session = self.client.session
        session['selected_addons'] = []
        session['selected_pages'] = 0
        session.save()

        response = self.client.get(reverse('custom_checkout'))
        self.assertRedirects(response, reverse('custom_package'))

    @patch('packages.views.stripe.checkout.Session.create')
    def test_custom_checkout_redirects_to_stripe(self, mock_create):
        mock_session = MagicMock()
        mock_session.url = 'https://checkout.stripe.com/custom'
        mock_create.return_value = mock_session

        self.client.login(username='testuser', password='testpass123')
        session = self.client.session
        session['selected_addons'] = [str(self.addon.id)]
        session['selected_pages'] = 0
        session.save()

        response = self.client.get(reverse('custom_checkout'))
        self.assertEqual(response.status_code, 302)


# ---------------------------------------------------------------------------
# Webhook Tests
# ---------------------------------------------------------------------------

def _build_stripe_event(payload_dict, secret):
    """Helper: build a signed Stripe webhook payload."""
    payload = json.dumps(payload_dict).encode('utf-8')
    timestamp = int(time.time())
    signed_payload = f'{timestamp}.{payload.decode()}'
    signature = hmac.new(
        secret.encode('utf-8'),
        signed_payload.encode('utf-8'),
        hashlib.sha256,
    ).hexdigest()
    sig_header = f't={timestamp},v1={signature}'
    return payload, sig_header


# Tests for the Stripe webhook — order/payment creation, email sending, edge cases, and error handling
class StripeWebhookTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.webhook_url = reverse('stripe_webhook')
        self.webhook_secret = 'whsec_testsecret'

        self.user = User.objects.create_user(
            username='buyer', email='buyer@example.com',
            first_name='Test', last_name='Buyer', password='testpass123',
        )
        self.profile, _ = UserProfile.objects.get_or_create(user=self.user)
        self.package = Package.objects.create(
            name='Starter', code='STR', tier='entry', price=Decimal('499.00'),
            display_order=1, cta_label='Get Started', is_active=True,
            stripe_price_id='price_test_123',
        )

    def _post_event(self, event_dict):
        """Post a mock Stripe event to the webhook endpoint."""
        payload = json.dumps(event_dict).encode('utf-8')
        # Use a dummy sig header — we'll mock construct_event to bypass verification
        return self.client.post(
            self.webhook_url,
            data=payload,
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='t=0,v1=dummy',
        )

    def _checkout_session_event(self, package_id=None, user_id=None, custom=False):
        return {
            'type': 'checkout.session.completed',
            'data': {
                'object': {
                    'metadata': {
                        'package_id': str(package_id or self.package.id),
                        'user_id': str(user_id or self.user.id),
                        'custom_package': 'true' if custom else 'false',
                    },
                    'amount_total': 49900,
                    'customer_email': 'buyer@example.com',
                    'payment_intent': 'pi_test_123',
                    'customer': 'cus_test_123',
                }
            }
        }

    @patch('packages.views.stripe.Webhook.construct_event')
    def test_webhook_returns_200_on_valid_event(self, mock_construct):
        event = self._checkout_session_event()
        mock_construct.return_value = event
        response = self._post_event(event)
        self.assertEqual(response.status_code, 200)

    @patch('packages.views.stripe.Webhook.construct_event')
    def test_webhook_creates_order(self, mock_construct):
        event = self._checkout_session_event()
        mock_construct.return_value = event

        with patch('packages.views.send_mail'):
            self._post_event(event)

        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.email, 'buyer@example.com')
        self.assertEqual(order.order_total, Decimal('499.00'))
        self.assertEqual(order.status, 'paid')

    @patch('packages.views.stripe.Webhook.construct_event')
    def test_webhook_creates_payment(self, mock_construct):
        event = self._checkout_session_event()
        mock_construct.return_value = event

        with patch('packages.views.send_mail'):
            self._post_event(event)

        self.assertEqual(Payment.objects.count(), 1)
        payment = Payment.objects.first()
        self.assertEqual(payment.stripe_payment_intent, 'pi_test_123')
        self.assertEqual(payment.status, 'succeeded')
        self.assertEqual(payment.amount, Decimal('499.00'))

    @patch('packages.views.stripe.Webhook.construct_event')
    def test_webhook_sends_confirmation_email(self, mock_construct):
        event = self._checkout_session_event()
        mock_construct.return_value = event

        with patch('packages.views.send_mail') as mock_mail:
            self._post_event(event)

        mock_mail.assert_called_once()
        call_kwargs = mock_mail.call_args[1]
        self.assertIn('buyer@example.com', call_kwargs['recipient_list'])

    @patch('packages.views.stripe.Webhook.construct_event')
    def test_webhook_marks_confirmation_email_sent(self, mock_construct):
        event = self._checkout_session_event()
        mock_construct.return_value = event

        with patch('packages.views.send_mail'):
            self._post_event(event)

        order = Order.objects.first()
        self.assertTrue(order.confirmation_email_sent)

    @patch('packages.views.stripe.Webhook.construct_event')
    def test_webhook_saves_stripe_customer_id_to_profile(self, mock_construct):
        event = self._checkout_session_event()
        mock_construct.return_value = event

        with patch('packages.views.send_mail'):
            self._post_event(event)

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.stripe_customer_id, 'cus_test_123')

    @patch('packages.views.stripe.Webhook.construct_event')
    def test_webhook_handles_custom_package(self, mock_construct):
        event = self._checkout_session_event(custom=True)
        mock_construct.return_value = event

        with patch('packages.views.send_mail'):
            self._post_event(event)

        order = Order.objects.first()
        self.assertIsNone(order.package)

    @patch('packages.views.stripe.Webhook.construct_event')
    def test_webhook_returns_200_without_user_id(self, mock_construct):
        """Webhook should return 200 but skip order creation if no user_id."""
        event = {
            'type': 'checkout.session.completed',
            'data': {
                'object': {
                    'metadata': {},
                    'amount_total': 49900,
                    'customer_email': 'nobody@example.com',
                    'payment_intent': 'pi_xyz',
                    'customer': '',
                }
            }
        }
        mock_construct.return_value = event
        response = self._post_event(event)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 0)

    @patch('packages.views.stripe.Webhook.construct_event',
           side_effect=ValueError('invalid payload'))
    def test_webhook_returns_400_on_invalid_payload(self, mock_construct):
        response = self._post_event({})
        self.assertEqual(response.status_code, 400)

    @patch('packages.views.stripe.Webhook.construct_event')
    def test_webhook_ignores_non_checkout_events(self, mock_construct):
        event = {'type': 'payment_intent.created', 'data': {'object': {}}}
        mock_construct.return_value = event
        response = self._post_event(event)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 0)