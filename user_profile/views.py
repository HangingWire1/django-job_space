from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from authentication.models import Employee, Employer, Location
from .forms import EmployeeProfileForm, EmployerProfileForm, LocationForm


@login_required
def edit_employee_profile(request):
    """
    Show and edit the logged-in user's Employee profile.
    Only users with is_employee=True can access this view.
    """
    # Ensure only employee users can access
    if not getattr(request.user, 'is_employee', False):
        messages.error(request, "Only employee accounts can edit an employee profile.")
        return redirect('home')  # change to an appropriate URL

    # Get or create the employee instance (create only if user.is_employee True)
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        # Safe to auto-create because we already checked is_employee
        employee = Employee.objects.create(user=request.user)

    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('home')  # adjust as needed
        # else:
        #     messages.error(request, "Please correct the errors below.")
    else:
        form = EmployeeProfileForm(instance=employee)

    # Pass Python objects (lists/dicts) to template for json_script hydration
    context = {
        'form': form,
        'employee': employee,
        'experience_json': employee.experience or [],
        'education_json': employee.education or [],
        'skills_json': employee.skills or [],
        'social_json': employee.social_media or {},
    }
    return render(request, 'user_profile/edit_profile.html', context)

def test_location(request):
    context = {
        "location_form": LocationForm(),
    }
    return render(request, "user_profile/includes/edit_employer_profile.html", context)


@login_required
def edit_employer_profile(request):
    employer = Employer.objects.get(user=request.user)

    # 🔥 Get or create location for this employer
    location, created = Location.objects.get_or_create(
        employer=employer,
        defaults={
            "detail_address": ""
        }
    )

    if request.method == "POST":
        form = EmployerProfileForm(
            request.POST,
            request.FILES,
            instance=employer
        )
        location_form = LocationForm(
            request.POST,
            instance=location
        )

        if form.is_valid() and location_form.is_valid():
            employer = form.save()
            location = location_form.save(commit=False)
            location.employer = employer
            location.save()

            messages.success(request, "Your profile has been updated successfully!")
            return redirect("home")

    else:
        form = EmployerProfileForm(instance=employer)
        location_form = LocationForm(instance=location)

    return render(request, "user_profile/edit_profile.html", {
        "form": form,
        "location_form": location_form,
        "employer": employer,
        "profile_type": "employer"
    })
