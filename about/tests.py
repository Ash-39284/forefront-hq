from django.test import TestCase, Client
from django.urls import reverse

from .models import StaffAbout


# ---------------------------------------------------------------------------
# Model Tests
# ---------------------------------------------------------------------------

# Tests for the StaffAbout model — str, defaults, ordering, and optional fields
class StaffAboutModelTest(TestCase):

    def setUp(self):
        self.member = StaffAbout.objects.create(
            name='Ashley Roberts',
            profile_img_url='https://example.com/ashley.jpg',
            job_title='Founder',
            bio_description='Ashley is the founder of Forefront HQ.',
            is_active=True,
            display_order=1,
        )

    def test_str(self):
        self.assertEqual(str(self.member), 'Ashley Roberts')

    def test_is_active_defaults_to_false(self):
        member = StaffAbout.objects.create(
            name='Draft Member',
            bio_description='Not yet active.',
            display_order=99,
        )
        self.assertFalse(member.is_active)

    def test_display_order_defaults_to_zero(self):
        member = StaffAbout.objects.create(
            name='No Order',
            bio_description='No display order set.',
        )
        self.assertEqual(member.display_order, 0)

    def test_profile_img_url_can_be_null(self):
        member = StaffAbout.objects.create(
            name='No Image',
            bio_description='No image.',
            display_order=2,
        )
        self.assertIsNone(member.profile_img_url)

    def test_job_title_can_be_null(self):
        member = StaffAbout.objects.create(
            name='No Title',
            bio_description='No job title.',
            display_order=3,
        )
        self.assertIsNone(member.job_title)

    def test_default_ordering_by_display_order(self):
        StaffAbout.objects.create(
            name='Second Member',
            bio_description='Second.',
            is_active=True,
            display_order=2,
        )
        members = list(StaffAbout.objects.all())
        self.assertEqual(members[0].name, 'Ashley Roberts')
        self.assertEqual(members[1].name, 'Second Member')


# ---------------------------------------------------------------------------
# View Tests
# ---------------------------------------------------------------------------

# Tests for the about view — status code, template, active-only filtering, and ordering
class AboutViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('about')
        self.active_member = StaffAbout.objects.create(
            name='Ashley Roberts',
            bio_description='Founder.',
            is_active=True,
            display_order=1,
        )
        self.inactive_member = StaffAbout.objects.create(
            name='Hidden Member',
            bio_description='Not shown.',
            is_active=False,
            display_order=2,
        )
        self.second_active_member = StaffAbout.objects.create(
            name='Second Member',
            bio_description='Second active member.',
            is_active=True,
            display_order=3,
        )

    def test_about_view_status_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_about_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'about/about.html')

    def test_about_view_only_shows_active_members(self):
        response = self.client.get(self.url)
        self.assertIn(self.active_member, response.context['team_members'])
        self.assertNotIn(self.inactive_member, response.context['team_members'])

    def test_about_view_shows_all_active_members(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['team_members']), 2)

    def test_about_view_ordered_by_display_order(self):
        response = self.client.get(self.url)
        members = list(response.context['team_members'])
        self.assertEqual(members[0], self.active_member)
        self.assertEqual(members[1], self.second_active_member)

    def test_about_view_accessible_without_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)