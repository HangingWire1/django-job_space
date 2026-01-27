
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Employee, Employer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def sync_user_profiles(sender, instance, created, **kwargs):
    """
    Syncs profile existence and active status based on the User's role flags.
    """

    # --- 1. HANDLE EMPLOYEE ROLE ---
    if instance.is_employee:
        # get_or_create returns (object, created_bool).
        # We use _ because we don't need to know if it was just created.
        profile, _ = Employee.objects.get_or_create(user=instance)

        # Ensure it is active if the flag is checked
        if not profile.is_active:
            profile.is_active = True
            profile.save()
    else:
        # .filter().update() is safe even if the profile doesn't exist (no crash)
        Employee.objects.filter(user=instance).update(is_active=False)

    # --- 2. HANDLE EMPLOYER ROLE ---
    if instance.is_employer:
        # Ensure EmployerProfile exists
        emp_profile, _ = Employer.objects.get_or_create(user=instance)

        # Ensure it is active
        if not emp_profile.is_active:
            emp_profile.is_active = True
            emp_profile.save()
    else:
        # Deactivate if flag is unchecked
        Employer.objects.filter(user=instance).update(is_active=False)