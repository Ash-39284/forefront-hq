from django.test import TestCase, Client
from django.urls import reverse

from .models import Service


# ---------------------------------------------------------------------------
# Model Tests
# ---------------------------------------------------------------------------

# Tests for the Service model — str representation, default ordering, and is_active default
class ServiceModelTest(TestCase):

    def setUp(self):
        self.service = Service.objects.create(
            name='Web Design',
            slug='web-design',
            short_description='Beautiful websites.',
            description='We build beautiful, responsive websites.',
            is_active=True,
            display_order=1,
        )

    def test_str(self):
        self.assertEqual(str(self.service), 'Web Design')

    def test_is_active_default(self):
        service = Service.objects.create(
            name='SEO',
            slug='seo',
            short_description='Search engine optimisation.',
            description='Full SEO audit and setup.',
            display_order=2,
        )
        self.assertTrue(service.is_active)

    def test_default_ordering(self):
        Service.objects.create(
            name='Social Media',
            slug='social-media',
            short_description='Social setup.',
            description='Full social media setup.',
            is_active=True,
            display_order=2,
        )
        services = list(Service.objects.all())
        self.assertEqual(services[0].name, 'Web Design')
        self.assertEqual(services[1].name, 'Social Media')

    def test_slug_is_unique(self):
        with self.assertRaises(Exception):
            Service.objects.create(
                name='Web Design Duplicate',
                slug='web-design',
                short_description='Duplicate slug.',
                description='This should fail.',
                display_order=99,
            )


# ---------------------------------------------------------------------------
# View Tests
# ---------------------------------------------------------------------------

# Tests for the services view — status code, template, active-only filtering, and ordering
class ServicesViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('services')
        self.active_service = Service.objects.create(
            name='Web Design',
            slug='web-design',
            short_description='Beautiful websites.',
            description='We build beautiful, responsive websites.',
            is_active=True,
            display_order=1,
        )
        self.inactive_service = Service.objects.create(
            name='Old Service',
            slug='old-service',
            short_description='No longer offered.',
            description='This service is retired.',
            is_active=False,
            display_order=2,
        )
        self.second_active_service = Service.objects.create(
            name='SEO',
            slug='seo',
            short_description='Search engine optimisation.',
            description='Full SEO audit and setup.',
            is_active=True,
            display_order=3,
        )

    def test_services_view_status_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_services_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'services/services.html')

    def test_services_view_only_shows_active_services(self):
        response = self.client.get(self.url)
        self.assertIn(self.active_service, response.context['services'])
        self.assertNotIn(self.inactive_service, response.context['services'])

    def test_services_view_shows_all_active_services(self):
        response = self.client.get(self.url)
        self.assertIn(self.second_active_service, response.context['services'])
        self.assertEqual(len(response.context['services']), 2)

    def test_services_view_ordered_by_display_order(self):
        response = self.client.get(self.url)
        services = list(response.context['services'])
        self.assertEqual(services[0], self.active_service)
        self.assertEqual(services[1], self.second_active_service)

    def test_services_view_accessible_without_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)