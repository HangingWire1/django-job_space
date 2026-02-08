from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_employer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    # def __str__(self):
    #     return self.email

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

class Employer(models.Model):
    is_active = models.BooleanField(default=True)
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
        related_name='employer',
        limit_choices_to = {'is_employer': True}
    )
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    company_name = models.CharField(max_length=255,null=True, blank=True)
    industry = models.CharField(max_length=100,null=True, blank=True)

    no_of_employee = models.CharField(
        max_length=20,
        choices=EmployeeRange.choices,
        default=EmployeeRange.RANGE_1_5
    )

    founded_at = models.DateField(null=True, blank=True)

    contact_email = models.EmailField(null=True, blank=True)
    # 3. Rich Text/Description Fields
    what_we_do = models.TextField(null=True, blank=True)
    why_join_us = models.TextField(null=True, blank=True)
    mission_vision = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Prevent saving if the linked user isn't marked as an employer
        if self.user and not getattr(self.user, 'is_employer', False):
            raise ValidationError("The selected user must have is_employer=True.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensures clean() is called before saving
        super().save(*args, **kwargs)

    def __str__(self):
            return self.user.email

class Employee(models.Model):
    # Linking to the built-in User model
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employee',  # Access via user.employee_profile
        limit_choices_to={'is_employee': True}
    )

    employee_name = models.CharField(
        max_length=100, blank=True, null=True
    )

    # Basic Contact
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20,null=True, blank=True)

    # Location
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    township = models.ForeignKey(Township, on_delete=models.SET_NULL, null=True, blank=True)

    # Files
    profile_pic = models.ImageField(upload_to='employee/profiles/pics/', null=True, blank=True)
    cv_file = models.FileField(upload_to='employee/profiles/cvs/', null=True, blank=True)

    # Career Info
    salary_expect = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Complex Data (JSON)
    # Note: Requires a database like PostgreSQL for full functionality,
    # but works as text in SQLite.
    experience = models.JSONField(default=list, blank=True)
    education = models.JSONField(default=list, blank=True)
    skills = models.JSONField(default=list, blank=True)
    social_media = models.JSONField(default=dict, blank=True)

    def clean(self):
        # Prevent saving if the linked user isn't marked as an employee
        if self.user and not getattr(self.user, 'is_employee', False):
            raise ValidationError("The selected user must have is_employee=True.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensures clean() is called before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email

class Location(models.Model):
    employer = models.OneToOneField(
        Employer,
        on_delete=models.CASCADE,
        related_name='location',
        null = True,
        blank = True
    )
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    township = models.ForeignKey(Township, on_delete=models.SET_NULL, null=True)
    detail_address = models.TextField(help_text="House No, Street Name, Ward, etc.")

    def __str__(self):
        # This prevents the NoneType error by providing fallbacks for everything
        addr = self.detail_address if self.detail_address else "No Address"
        town = self.township.name if self.township else "No Township"
        stat = self.state.name if self.state else "No State"
        return f"{addr}, {town}, {stat}"


