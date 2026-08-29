from django.db import models


class ProjectTag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PortfolioProject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    client_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    live_url = models.CharField(max_length=500, blank=True, null=True)
    is_live = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    completed_at = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(ProjectTag, through='PortfolioProjectTag', blank=True)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        return self.title


class PortfolioProjectTag(models.Model):
    project = models.ForeignKey(PortfolioProject, on_delete=models.CASCADE)
    tag = models.ForeignKey(ProjectTag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('project', 'tag')


class PortfolioUpcoming(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    client_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='portfolio/upcoming/', blank=True, null=True)
    live_url = models.CharField(max_length=500, blank=True, null=True)
    is_live = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    completed_at = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(ProjectTag, through='PortfolioUpcomingTag', blank=True)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        return self.title


class PortfolioUpcomingTag(models.Model):
    upcoming = models.ForeignKey(PortfolioUpcoming, on_delete=models.CASCADE)
    tag = models.ForeignKey(ProjectTag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('upcoming', 'tag')

    def __str__(self):
        return f"{self.upcoming} - {self.tag}"