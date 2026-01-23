from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    is_employer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Township(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='townships')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('state', 'name') # Prevents duplicate townships in the same state
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.state.name})"

class Location(models.Model):
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    township = models.ForeignKey(Township, on_delete=models.SET_NULL, null=True)
    detail_address = models.TextField(help_text="House No, Street Name, Ward, etc.")

    def __str__(self):
        return f"{self.detail_address}, {self.township.name}, {self.state.name}"

class Employer(models.Model):
    # Choice class for number of employees
    class EmployeeRange(models.TextChoices):
        RANGE_1_5 = '1-5', '1-5'
        RANGE_6_10 = '6-10', '6-10'
        RANGE_11_20 = '11-20', '11-20'
        RANGE_21_50 = '21-50', '21-50'
        RANGE_51_100 = '51-100', '51-100'
        RANGE_101_200 = '101-200', '101-200'
        RANGE_201_500 = '201-500', '201-500'
        RANGE_501_1000 = '501-1000', '501-1000'
        RANGE_1001_5000 = '1001-5000', '1001-5000'
        RANGE_5001_10000 = '5001-10000', '5001-10000'
        RANGE_10001_20000 = '10001-20000', '10001-20000'
        MORE_THAN_20000 = '20000+', 'More than 20000'

    # 1. Attributes
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employer_profile'
    )
    profile_photo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100)

    no_of_employee = models.CharField(
        max_length=20,
        choices=EmployeeRange.choices,
        default=EmployeeRange.RANGE_1_5
    )

    founded_at = models.DateField()

    # 2. Location (Assuming you have a Location model elsewhere)
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True
    )

    # 3. Rich Text/Description Fields
    what_we_do = models.TextField()
    why_join_us = models.TextField()
    mission_vision = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name