from unittest.mock import patch, MagicMock

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from allauth.account.models import EmailAddress
from accounts.models import UserProfile


# ---------------------------------------------------------------------------
# Model Tests
# ---------------------------------------------------------------------------

# Tests for the UserProfile model — str representation and field defaults
class UserProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='testpass123',
        )
        self.profile, _ = UserProfile.objects.get_or_create(user=self.user)

    def test_str(self):
        self.assertEqual(str(self.profile), 'test@example.com profile')

    def test_profile_fields_blank_by_default(self):
        self.assertIsNone(self.profile.phone)
        self.assertIsNone(self.profile.company_name)
        self.assertIsNone(self.profile.stripe_customer_id)

    def test_one_to_one_relationship(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.user.profile, self.profile)


# ---------------------------------------------------------------------------
# View Tests — Home
# ---------------------------------------------------------------------------

# Tests for the home view — status code and correct template
class HomeViewTest(TestCase):

    def test_home_status_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')


# ---------------------------------------------------------------------------
# View Tests — Login
# ---------------------------------------------------------------------------

# Tests for the login view — GET, POST success/failure, email verification, and redirect handling
class LoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('login')
        self.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='testpass123',
        )
        self.profile, _ = UserProfile.objects.get_or_create(user=self.user)

    def test_get_login_page_status_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_login_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_authenticated_user_redirected_from_login(self):
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(self.url)
        self.assertRedirects(response, '/')

    def test_authenticated_user_redirected_to_next(self):
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(self.url + '?next=/packages/')
        self.assertRedirects(response, '/packages/')

    def test_login_with_verified_email_succeeds(self):
        EmailAddress.objects.create(
            user=self.user, email=self.user.email, primary=True, verified=True
        )
        response = self.client.post(self.url, {
            'email': 'test@example.com',
            'password': 'testpass123',
        })
        self.assertRedirects(response, '/')
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_with_unverified_email_blocked(self):
        EmailAddress.objects.create(
            user=self.user, email=self.user.email, primary=True, verified=False
        )
        response = self.client.post(self.url, {
            'email': 'test@example.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        messages = list(response.context['messages'])
        self.assertTrue(any('verify' in str(m).lower() for m in messages))

    def test_login_no_email_address_record_allowed(self):
        # Google OAuth users have no EmailAddress record — should be let through
        response = self.client.post(self.url, {
            'email': 'test@example.com',
            'password': 'testpass123',
        })
        self.assertRedirects(response, '/')
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_wrong_password_fails(self):
        response = self.client.post(self.url, {
            'email': 'test@example.com',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        messages = list(response.context['messages'])
        self.assertTrue(any('invalid' in str(m).lower() for m in messages))

    def test_login_unknown_email_fails(self):
        response = self.client.post(self.url, {
            'email': 'nobody@example.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_redirects_to_next_url(self):
        EmailAddress.objects.create(
            user=self.user, email=self.user.email, primary=True, verified=True
        )
        response = self.client.post(self.url + '?next=/packages/', {
            'email': 'test@example.com',
            'password': 'testpass123',
            'next': '/packages/',
        })
        self.assertRedirects(response, '/packages/')

    def test_login_page_passes_next_to_context(self):
        response = self.client.get(self.url + '?next=/packages/')
        self.assertEqual(response.context['next'], '/packages/')


# ---------------------------------------------------------------------------
# View Tests — Register
# ---------------------------------------------------------------------------

# Tests for the register view — GET, validation errors, successful registration, and email confirmation
class RegisterViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('register')

    def test_get_register_page_status_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_register_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_authenticated_user_redirected_from_register(self):
        user = User.objects.create_user(
            username='existing@example.com',
            email='existing@example.com',
            password='testpass123',
        )
        self.client.login(username='existing@example.com', password='testpass123')
        response = self.client.get(self.url)
        self.assertRedirects(response, '/')

    def test_passwords_do_not_match(self):
        response = self.client.post(self.url, {
            'email': 'new@example.com',
            'password1': 'testpass123',
            'password2': 'different123',
        })
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertTrue(any('match' in str(m).lower() for m in messages))
        self.assertEqual(User.objects.filter(email='new@example.com').count(), 0)

    def test_duplicate_email_rejected(self):
        User.objects.create_user(
            username='taken@example.com',
            email='taken@example.com',
            password='testpass123',
        )
        response = self.client.post(self.url, {
            'email': 'taken@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertTrue(any('already exists' in str(m).lower() for m in messages))

    def test_short_password_rejected(self):
        response = self.client.post(self.url, {
            'email': 'new@example.com',
            'password1': 'short',
            'password2': 'short',
        })
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertTrue(any('8 characters' in str(m).lower() for m in messages))
        self.assertEqual(User.objects.filter(email='new@example.com').count(), 0)

    @patch('allauth.account.models.EmailAddress.send_confirmation')
    def test_successful_registration_creates_user(self, mock_send):
        self.client.post(self.url, {
            'email': 'new@example.com',
            'password1': 'strongpass123',
            'password2': 'strongpass123',
        })
        self.assertTrue(User.objects.filter(email='new@example.com').exists())

    @patch('allauth.account.models.EmailAddress.send_confirmation')
    def test_successful_registration_creates_unverified_email_address(self, mock_send):
        self.client.post(self.url, {
            'email': 'new@example.com',
            'password1': 'strongpass123',
            'password2': 'strongpass123',
        })
        email_address = EmailAddress.objects.get(email='new@example.com')
        self.assertTrue(email_address.primary)
        self.assertFalse(email_address.verified)

    @patch('allauth.account.models.EmailAddress.send_confirmation')
    def test_successful_registration_sends_confirmation_email(self, mock_send):
        self.client.post(self.url, {
            'email': 'new@example.com',
            'password1': 'strongpass123',
            'password2': 'strongpass123',
        })
        mock_send.assert_called_once()

    @patch('allauth.account.models.EmailAddress.send_confirmation')
    def test_successful_registration_redirects_to_verification_sent(self, mock_send):
        response = self.client.post(self.url, {
            'email': 'new@example.com',
            'password1': 'strongpass123',
            'password2': 'strongpass123',
        })
        self.assertRedirects(response, reverse('account_email_verification_sent'))

    @patch('allauth.account.models.EmailAddress.send_confirmation')
    def test_successful_registration_does_not_log_user_in(self, mock_send):
        response = self.client.post(self.url, {
            'email': 'new@example.com',
            'password1': 'strongpass123',
            'password2': 'strongpass123',
        }, follow=True)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    @patch('allauth.account.models.EmailAddress.send_confirmation')
    def test_register_passes_next_to_context(self, mock_send):
        response = self.client.get(self.url + '?next=/packages/')
        self.assertEqual(response.context['next'], '/packages/')


# ---------------------------------------------------------------------------
# View Tests — Logout
# ---------------------------------------------------------------------------

# Tests for the logout view — logs out the user, shows a success message, and redirects home
class LogoutViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('logout')
        self.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='testpass123',
        )

    def test_logout_redirects_to_home(self):
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('home'))

    def test_logout_logs_user_out(self):
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(self.url, follow=True)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_shows_success_message(self):
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(self.url, follow=True)
        messages = list(response.context['messages'])
        self.assertTrue(any('logged out' in str(m).lower() for m in messages))

    def test_logout_works_for_anonymous_user(self):
        # Logging out when not logged in should still redirect cleanly
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('home'))