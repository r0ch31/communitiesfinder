from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


def generate_unique_slug(instance, field_value=None, slug_field_name='slug'):
    """
    Generate a unique slug for a model instance.
    If field_value is provided, use it as the base; otherwise, use instance.name.
    Appends a number if the slug already exists.
    """
    if not field_value:
        field_value = getattr(instance, 'name', '')
    slug_base = slugify(field_value)
    slug = slug_base
    ModelClass = instance.__class__
    counter = 1

    while ModelClass.objects.filter(**{slug_field_name: slug}).exists():
        slug = f"{slug_base}-{counter}"
        counter += 1

    return slug


# ----------------------
# Category Model
# ----------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', args=[self.slug])


# ----------------------
# Location Model
# ----------------------
class Location(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        unique_together = ('name', 'region', 'country')
        ordering = ["country", "region", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            # Create base string including name, region, and country
            slug_base = self.name
            if self.region:
                slug_base += f"-{self.region}"
            slug_base += f"-{self.country}"
            self.slug = generate_unique_slug(self, field_value=slug_base)
        super().save(*args, **kwargs)

    def __str__(self):
        parts = [self.name]
        if self.region:
            parts.append(self.region)
        parts.append(self.country)
        return ", ".join(parts)

    def get_absolute_url(self):
        return reverse('location_detail', args=[self.slug])


# ----------------------
# Community Model
# ----------------------
class Community(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="communities")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="communities")
    founded_date = models.DateField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    website = models.URLField(max_length=200, blank=True, null=True)
    facebook_page = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-added_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('community_detail', args=[self.slug])


# ----------------------
# Community Submission Model
# ----------------------
class CommunitySubmission(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="submissions")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="submissions")
    founded_date = models.DateField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    facebook_page = models.URLField(blank=True, null=True)
    submitted_at = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)
    community = models.OneToOneField(
        Community,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="submission"
    )

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Submission: {self.name}"

    def approve_submission(self):
        """Approve submission and create corresponding Community if not exists."""
        if not self.community:
            self.community = Community.objects.create(
                name=self.name,
                description=self.description,
                category=self.category,
                location=self.location,
                founded_date=self.founded_date,
                website=self.website,
                facebook_page=self.facebook_page,
                approved=True,
                status='approved'
            )
        self.approved = True
        self.save()


# ----------------------
# News/Event Model
# ----------------------
class NewsEvent(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    published_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['-published_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, field_value=self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.slug])
