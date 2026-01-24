from django.db import models
from django.template.defaultfilters import slugify

from authentication.models import Employer,Location

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class JobPost(models.Model):
    # Job Type Options
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
    ]

    # Relationships
    employer = models.ForeignKey('authentication.Employer', on_delete=models.CASCADE, related_name='job_posts')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='jobs')
    location = models.ForeignKey('authentication.Location', on_delete=models.CASCADE, related_name='job_listings')

    # Basic Info
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')

    #company info
    company_name = models.CharField(max_length=255)
    detail_address = models.TextField(
        blank=True,
        null=True,
        help_text="Enter the specific building number, street, or directions."
    )

    # Details
    description = models.TextField()
    requirements = models.TextField()

    # Contact & Metadata
    contact_email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-create slug if it's empty
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} at {self.employer}"

    class Meta:
        ordering = ['-created_at']
