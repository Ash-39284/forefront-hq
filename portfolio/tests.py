from datetime import date
from django.test import TestCase, Client
from django.urls import reverse

from .models import ProjectTag, PortfolioProject, PortfolioProjectTag


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_project(title='Test Project', slug='test-project', is_live=True,
                 is_featured=False, completed_at=date(2024, 1, 1), **kwargs):
    return PortfolioProject.objects.create(
        title=title,
        slug=slug,
        client_name='Test Client',
        category='Web Design',
        description='A test project.',
        is_live=is_live,
        is_featured=is_featured,
        completed_at=completed_at,
        **kwargs,
    )


# ---------------------------------------------------------------------------
# Model Tests
# ---------------------------------------------------------------------------

# Tests for the ProjectTag model — str representation
class ProjectTagModelTest(TestCase):

    def setUp(self):
        self.tag = ProjectTag.objects.create(name='Django', slug='django')

    def test_str(self):
        self.assertEqual(str(self.tag), 'Django')


# Tests for the PortfolioProject model — str, defaults, ordering, optional fields, and tag relationship
class PortfolioProjectModelTest(TestCase):

    def setUp(self):
        self.project = make_project()

    def test_str(self):
        self.assertEqual(str(self.project), 'Test Project')

    def test_is_live_default_is_false(self):
        project = PortfolioProject.objects.create(
            title='Draft Project',
            slug='draft-project',
            client_name='Client',
            category='Web Design',
            description='Draft.',
        )
        self.assertFalse(project.is_live)

    def test_is_featured_default_is_false(self):
        self.assertFalse(self.project.is_featured)

    def test_created_at_is_set_automatically(self):
        self.assertIsNotNone(self.project.created_at)

    def test_image_url_can_be_blank(self):
        project = make_project(title='No Image', slug='no-image', image_url=None)
        self.assertIsNone(project.image_url)

    def test_live_url_can_be_blank(self):
        project = make_project(title='No URL', slug='no-url', live_url=None)
        self.assertIsNone(project.live_url)

    def test_completed_at_can_be_blank(self):
        project = make_project(title='No Date', slug='no-date', completed_at=None)
        self.assertIsNone(project.completed_at)

    def test_slug_is_unique(self):
        with self.assertRaises(Exception):
            make_project(title='Duplicate', slug='test-project')

    def test_default_ordering_is_by_completed_at_descending(self):
        make_project(title='Older Project', slug='older-project', completed_at=date(2023, 1, 1))
        make_project(title='Newer Project', slug='newer-project', completed_at=date(2025, 1, 1))
        projects = list(PortfolioProject.objects.all())
        self.assertEqual(projects[0].title, 'Newer Project')
        self.assertEqual(projects[2].title, 'Older Project')

    def test_tags_can_be_added_via_many_to_many(self):
        tag = ProjectTag.objects.create(name='Django', slug='django')
        PortfolioProjectTag.objects.create(project=self.project, tag=tag)
        self.assertIn(tag, self.project.tags.all())

    def test_multiple_tags_can_be_added(self):
        tag1 = ProjectTag.objects.create(name='Django', slug='django')
        tag2 = ProjectTag.objects.create(name='Python', slug='python')
        PortfolioProjectTag.objects.create(project=self.project, tag=tag1)
        PortfolioProjectTag.objects.create(project=self.project, tag=tag2)
        self.assertEqual(self.project.tags.count(), 2)


# Tests for the PortfolioProjectTag through model — unique together constraint and cascade delete
class PortfolioProjectTagModelTest(TestCase):

    def setUp(self):
        self.project = make_project()
        self.tag = ProjectTag.objects.create(name='Django', slug='django')
        self.project_tag = PortfolioProjectTag.objects.create(
            project=self.project, tag=self.tag
        )

    def test_unique_together_constraint(self):
        with self.assertRaises(Exception):
            PortfolioProjectTag.objects.create(project=self.project, tag=self.tag)

    def test_project_tag_deleted_on_project_delete(self):
        project_tag_id = self.project_tag.id
        self.project.delete()
        self.assertFalse(PortfolioProjectTag.objects.filter(id=project_tag_id).exists())

    def test_project_tag_deleted_on_tag_delete(self):
        project_tag_id = self.project_tag.id
        self.tag.delete()
        self.assertFalse(PortfolioProjectTag.objects.filter(id=project_tag_id).exists())


# ---------------------------------------------------------------------------
# View Tests
# ---------------------------------------------------------------------------

# Tests for the portfolio view — status code, template, live-only filtering, ordering, and tag prefetch
class PortfolioViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('portfolio')
        self.live_project = make_project(
            title='Live Project', slug='live-project',
            is_live=True, completed_at=date(2024, 6, 1),
        )
        self.draft_project = make_project(
            title='Draft Project', slug='draft-project',
            is_live=False, completed_at=date(2024, 5, 1),
        )
        self.older_project = make_project(
            title='Older Project', slug='older-project',
            is_live=True, completed_at=date(2023, 1, 1),
        )

    def test_portfolio_view_status_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_portfolio_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'portfolio/portfolio.html')

    def test_portfolio_view_only_shows_live_projects(self):
        response = self.client.get(self.url)
        self.assertIn(self.live_project, response.context['projects'])
        self.assertNotIn(self.draft_project, response.context['projects'])

    def test_portfolio_view_shows_all_live_projects(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['projects']), 2)

    def test_portfolio_view_ordered_by_completed_at_descending(self):
        response = self.client.get(self.url)
        projects = list(response.context['projects'])
        self.assertEqual(projects[0], self.live_project)
        self.assertEqual(projects[1], self.older_project)

    def test_portfolio_view_accessible_without_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_portfolio_view_projects_have_tags_prefetched(self):
        tag = ProjectTag.objects.create(name='Django', slug='django')
        PortfolioProjectTag.objects.create(project=self.live_project, tag=tag)
        response = self.client.get(self.url)
        project = response.context['projects'][0]
        self.assertIn(tag, project.tags.all())