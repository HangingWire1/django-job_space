from django.db import models
from django.conf import settings
from job_posts.models import JobPost
from authentication.models import Employee

# In your models.py

class Application(models.Model):
    # --- Status Choices and Core Relationships ---
    # (These remain the same)
    STATUS_CHOICES = [
        ('waited', 'Waited'),
        ('to_interview', 'To_interview'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    # We still keep the link to the original employee for reference
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='applications')

    # --- SNAPSHOT FIELDS ---
    # These fields are copied from the Employee model at the time of application.
    # This ensures that the application record is a permanent, unchangeable snapshot.

    # Basic Info Snapshot
    employee_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    # File Snapshot
    # IMPORTANT: Use a different upload_to path to keep application files separate!
    cv_file = models.FileField(upload_to='application_cvs/', null=True, blank=True)

    # Career Info Snapshot
    salary_expect = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    experience = models.JSONField(default=list)
    education = models.JSONField(default=list)
    skills = models.JSONField(default=list)

    # --- Application Metadata ---
    # (These remain the same)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waited')
    cover_letter = models.TextField(blank=True, null=True)
    # This will be our "soft delete" or "archive" flag.
    is_archived_by_user = models.BooleanField(default=False)

    class Meta:
        unique_together = ('job', 'employee')
        ordering = ['-applied_at']

    def __str__(self):
        # We can use the snapshotted name now
        return f"{self.employee_name} applied for {self.job.title}"



