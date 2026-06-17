from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from services.models import Service
from .models import ContactEnquiry


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_service(name='Web Design', slug='web-design', is_active=True, display_order=1):
    return Service.objects.create(
        name=name,
        slug=slug,
        short_description='A great service.',
        description='Full description.',
        is_active=is_active,
        display_order=display_order,
    )


def make_user(email='test@example.com', password='testpass123'):
    return User.objects.create_user(
        username=email, email=email, password=password
    )


# ---------------------------------------------------------------------------
# Model Tests
# ---------------------------------------------------------------------------

# Tests for the ContactEnquiry model — str, defaults, ordering, optional FKs, and cascade behaviour
class ContactEnquiryModelTest(TestCase):

    def setUp(self):
        self.user = make_user()
        self.service = make_service()
        self.enquiry = ContactEnquiry.objects.create(
            user=self.user,
            service=self.service,
            name='Ashley Roberts',
            email='ashley@example.com',
            message='I would like a new website.',
        )

    def test_str(self):
        self.assertEqual(str(self.enquiry), 'Ashley Roberts - ashley@example.com')

    def test_default_status_is_new(self):
        self.assertEqual(self.enquiry.status, 'new')

    def test_submitted_at_is_set_automatically(self):
        self.assertIsNotNone(self.enquiry.submitted_at)

    def test_responded_at_is_null_by_default(self):
        self.assertIsNone(self.enquiry.responded_at)

    def test_user_can_be_null(self):
        enquiry = ContactEnquiry.objects.create(
            user=None,
            name='Anonymous',
            email='anon@example.com',
            message='Hello.',
        )
        self.assertIsNone(enquiry.user)

    def test_service_can_be_null(self):
        enquiry = ContactEnquiry.objects.create(
            name='No Service',
            email='noservice@example.com',
            message='General enquiry.',
        )
        self.assertIsNone(enquiry.service)

    def test_user_set_to_null_on_user_delete(self):
        self.user.delete()
        self.enquiry.refresh_from_db()
        self.assertIsNone(self.enquiry.user)

    def test_service_set_to_null_on_service_delete(self):
        self.service.delete()
        self.enquiry.refresh_from_db()
        self.assertIsNone(self.enquiry.service)

    def test_all_status_choices_are_valid(self):
        for status in ['new', 'read', 'responded']:
            self.enquiry.status = status
            self.enquiry.save()
            self.enquiry.refresh_from_db()
            self.assertEqual(self.enquiry.status, status)

    def test_default_ordering_is_by_submitted_at_descending(self):
        enquiry2 = ContactEnquiry.objects.create(
            name='Second Enquiry',
            email='second@example.com',
            message='Another message.',
        )
        enquiries = list(ContactEnquiry.objects.all())
        self.assertEqual(enquiries[0], enquiry2)
        self.assertEqual(enquiries[1], self.enquiry)

    def test_related_name_from_user(self):
        self.assertIn(self.enquiry, self.user.enquiries.all())

    def test_related_name_from_service(self):
        self.assertIn(self.enquiry, self.service.enquiries.all())


# ---------------------------------------------------------------------------
# View Tests
# ---------------------------------------------------------------------------

# Tests for the contact view — GET, POST (authenticated/anonymous, with/without service), validation, and redirect
class ContactViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('contact')
        self.user = make_user()
        self.active_service = make_service(name='Web Design', slug='web-design')
        self.inactive_service = make_service(
            name='Old Service', slug='old-service', is_active=False, display_order=2
        )

    def test_get_contact_page_status_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_contact_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'contact/contact.html')

    def test_get_contact_only_shows_active_services(self):
        response = self.client.get(self.url)
        self.assertIn(self.active_service, response.context['services'])
        self.assertNotIn(self.inactive_service, response.context['services'])

    def test_get_contact_accessible_without_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_creates_enquiry(self):
        self.client.post(self.url, {
            'name': 'Ashley Roberts',
            'email': 'ashley@example.com',
            'service': self.active_service.id,
            'message': 'I would like a new website.',
        })
        self.assertEqual(ContactEnquiry.objects.count(), 1)

    def test_post_saves_correct_data(self):
        self.client.post(self.url, {
            'name': 'Ashley Roberts',
            'email': 'ashley@example.com',
            'service': self.active_service.id,
            'message': 'I would like a new website.',
        })
        enquiry = ContactEnquiry.objects.first()
        self.assertEqual(enquiry.name, 'Ashley Roberts')
        self.assertEqual(enquiry.email, 'ashley@example.com')
        self.assertEqual(enquiry.service, self.active_service)
        self.assertEqual(enquiry.message, 'I would like a new website.')

    def test_post_links_authenticated_user_to_enquiry(self):
        self.client.login(username='test@example.com', password='testpass123')
        self.client.post(self.url, {
            'name': 'Ashley Roberts',
            'email': 'ashley@example.com',
            'message': 'Logged in enquiry.',
        })
        enquiry = ContactEnquiry.objects.first()
        self.assertEqual(enquiry.user, self.user)

    def test_post_anonymous_user_enquiry_has_no_user(self):
        self.client.post(self.url, {
            'name': 'Anonymous',
            'email': 'anon@example.com',
            'message': 'Anonymous enquiry.',
        })
        enquiry = ContactEnquiry.objects.first()
        self.assertIsNone(enquiry.user)

    def test_post_without_service_creates_enquiry(self):
        self.client.post(self.url, {
            'name': 'Ashley Roberts',
            'email': 'ashley@example.com',
            'service': '',
            'message': 'General enquiry.',
        })
        enquiry = ContactEnquiry.objects.first()
        self.assertIsNone(enquiry.service)

    def test_post_with_invalid_service_id_creates_enquiry_without_service(self):
        self.client.post(self.url, {
            'name': 'Ashley Roberts',
            'email': 'ashley@example.com',
            'service': 9999,
            'message': 'Bad service ID.',
        })
        enquiry = ContactEnquiry.objects.first()
        self.assertIsNone(enquiry.service)

    def test_post_redirects_to_contact(self):
        response = self.client.post(self.url, {
            'name': 'Ashley Roberts',
            'email': 'ashley@example.com',
            'message': 'Test.',
        })
        self.assertRedirects(response, self.url)

    def test_post_shows_success_message(self):
        response = self.client.post(self.url, {
            'name': 'Ashley Roberts',
            'email': 'ashley@example.com',
            'message': 'Test.',
        }, follow=True)
        messages = list(response.context['messages'])
        self.assertTrue(any('sent' in str(m).lower() for m in messages))

    def test_enquiry_status_defaults_to_new_on_submission(self):
        self.client.post(self.url, {
            'name': 'Ashley Roberts',
            'email': 'ashley@example.com',
            'message': 'Test.',
        })
        enquiry = ContactEnquiry.objects.first()
        self.assertEqual(enquiry.status, 'new')