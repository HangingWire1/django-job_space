# applications/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import JobPost, Application, Employee
from .forms import EmployeeApplicationForm

@login_required
def apply_for_job(request, job_slug):
    job = get_object_or_404(JobPost, slug=job_slug)

    if not request.user.is_employee:
        messages.error(request, "Only registered employees can apply for jobs.")
        # Make sure your redirect URL name is correct, e.g., 'job_details'
        return redirect('job_details', job_slug=job_slug)

    employee = request.user.employee

    # Check if they have already applied (no changes needed here)
    # if Application.objects.filter(job=job, employee=employee).exists():
    #     messages.warning(request, "You have already applied for this job.")
    #     return redirect('job_details', job_slug=job_slug)

    if request.method == 'POST':
        # NOTE: We bind the form to the instance to handle file uploads easily.
        form = EmployeeApplicationForm(request.POST, request.FILES, instance=employee)

        if form.is_valid():
            # Get the submitted data from the form
            cleaned_data = form.cleaned_data

            # --- 1. CREATE THE APPLICATION SNAPSHOT FIRST ---
            # This ensures the snapshot always has exactly what the user submitted.
            # This is how you would correctly structure the update_or_create call

            application, created = Application.objects.update_or_create(
                # 1. LOOKUP: These fields are used to find the existing application.
                # These MUST match your database's UNIQUE constraint.
                job=job,
                employee=employee,

                # 2. DEFAULTS: If a record is found, these fields will be UPDATED.
                # If no record is found, a NEW record will be CREATED with all these values.
                defaults={
                    'status': 'waited',  # you might want to update this too
                    'employee_name': form.cleaned_data.get('employee_name'),
                    'email': form.cleaned_data.get('email'),
                    'phone': form.cleaned_data.get('phone'),
                    'cv_file': form.cleaned_data.get('cv_file'),
                    'salary_expect': form.cleaned_data.get('salary_expect'),
                    'cover_letter': form.cleaned_data.get('cover_letter'),
                    'experience': employee.experience,
                    'education': employee.education,
                    'skills': employee.skills,
                }
            )

            # --- 2. NOW, CONDITIONALLY UPDATE THE EMPLOYEE PROFILE ---
            # This logic will "fill in the blanks" on the main profile.

            profile_needs_saving = False

            # For each field, check if the profile has a value. If not, update it.
            if not employee.employee_name and cleaned_data.get('employee_name'):
                employee.employee_name = cleaned_data.get('employee_name')
                profile_needs_saving = True

            if not employee.email and cleaned_data.get('email'):
                employee.email = cleaned_data.get('email')
                profile_needs_saving = True

            if not employee.phone and cleaned_data.get('phone'):
                employee.phone = cleaned_data.get('phone')
                profile_needs_saving = True

            # For the CV file
            if not employee.cv_file and cleaned_data.get('cv_file'):
                employee.cv_file = cleaned_data.get('cv_file')
                profile_needs_saving = True

            # For salary, we might want to update it if they've never set one
            if not employee.salary_expect and cleaned_data.get('salary_expect'):
                employee.salary_expect = cleaned_data.get('salary_expect')
                profile_needs_saving = True

            # Only hit the database if a change was actually made
            if profile_needs_saving:
                employee.save()

            messages.success(request, f"You have successfully applied for the job: {job.title}")
            return redirect('job_details', job_slug=job_slug)
    else:
        # GET request logic remains the same
        form = EmployeeApplicationForm(instance=employee)

    context = {
        'job': job,
        'form': form,
    }
    return render(request, 'applications/apply_template.html', context)

@login_required
def my_applications(request):
    """
    Displays a list of all job applications submitted by the currently
    logged-in employee.
    """
    if not request.user.is_employee:
        messages.error(request, "This page is only available for employees.")
        return redirect('home') # Redirect to your homepage

    # THE QUERY IS UPDATED HERE:
    applications = request.user.employee.applications.filter(
        is_archived_by_user=False
    ).order_by('-applied_at')

    context = {
        'applications': applications
    }
    return render(request, 'applications/my_applications.html', context)


@require_POST  # This decorator makes the view only accept POST requests, which is safer
@login_required
def withdraw_application(request, application_id):
    """
    Handles the logic for an employee to withdraw an application.
    """
    # Security Check: Get the application and ensure it belongs to the current user
    application = get_object_or_404(Application, id=application_id, employee=request.user.employee)

    # Business Rule: You can only withdraw applications that are pending
    if application.status in ['waited', 'to_interview']:
        application.status = 'withdrawn'
        application.save()
        messages.success(request, f"You have successfully withdrawn your application for '{application.job.title}'.")
    else:
        messages.warning(request, "This application cannot be withdrawn as it is no longer pending.")

    return redirect('my_applications')

# In applications/views.py

@require_POST
@login_required
def archive_application(request, application_id):
    """
    Handles the logic for a user to archive (soft delete) an application.
    """
    # Security Check: Ensure the application belongs to the current user
    application = get_object_or_404(Application, id=application_id, employee=request.user.employee)

    # Business Rule: You can only archive applications that are withdrawn or rejected
    if application.status in ['withdrawn', 'rejected']:
        application.is_archived_by_user = True
        application.save()
        messages.success(request, f"The application for '{application.job.title}' has been archived and hidden from this list.")
    else:
        messages.warning(request, "This application cannot be archived at this time.")

    return redirect('my_applications')

@login_required
def manage_applicants(request):
    """
    This is the main view for the employer's applicant dashboard.
    It handles filtering applications based on the status provided
    in the URL query parameter.
    """
    # Security check: Ensure the user is an employer.
    if not hasattr(request.user, 'employer'):
        messages.error(request, "You are not authorized to view this page.")
        return redirect('home')  # Or your main landing page

    # --- Filtering Logic ---
    # Get the status from the URL (e.g., ?status=accepted)
    # Default to 'waited' if no status is provided. This shows "New Applications" by default.
    status_filter = request.GET.get('status', 'waited')

    # --- Data Retrieval & Security ---
    # Filter applications where the job post belongs to the currently logged-in employer.
    # This is a CRUCIAL security measure.
    applications = Application.objects.filter(
        job__employer=request.user.employer,
        status=status_filter
    ).order_by('-applied_at')

    # A dictionary to get a nice, human-readable title for the page.
    status_titles = {
        'waited': 'New Applications',
        'to_interview': 'To Interview',
        'accepted': 'Accepted Applicants',
        'rejected': 'Rejected Applicants',
        'withdrawn': 'Withdrawn Applications',
    }

    context = {
        'applications': applications,
        'current_status': status_filter,  # For highlighting the active menu item
        'status_title': status_titles.get(status_filter, 'Applicants')  # Safely get the title
    }
    return render(request, 'applications/manage_applicants.html', context)


@require_POST  # Ensures this view can only be accessed via a POST request
@login_required
def update_application_status(request, application_id):
    """
    Handles the form submission from the dropdown to change an application's status.
    """
    # --- Security Check ---
    # Get the specific application, but also ensure it belongs to the logged-in employer.
    # If an employer tries to change an application that isn't theirs, this will raise a 404 error.
    application = get_object_or_404(
        Application,
        id=application_id,
        job__employer=request.user.employer
    )

    # Get the new status from the submitted form's <select> element.
    new_status = request.POST.get('new_status')

    # --- Validation ---
    # Get a list of all valid status keys (e.g., 'waited', 'accepted', etc.)
    valid_statuses = [choice[0] for choice in Application.STATUS_CHOICES]

    if new_status in valid_statuses:
        application.status = new_status
        application.save()
        messages.success(request,
                         f"Status for {application.employee_name} updated to '{application.get_status_display()}'.")
    else:
        messages.error(request, "Invalid status selected.")

    # --- Redirect Back ---
    # Redirect the user back to the page they were just on. This is great UX, as it
    # returns them to the list they were viewing (e.g., the "To Interview" list).
    return redirect(request.META.get('HTTP_REFERER', 'manage_applicants'))

@login_required
def application_details(request, application_id):
    """
    Displays the full details of a single application, including all the
    snapshotted data.
    """
    # --- CRUCIAL SECURITY CHECK ---
    # Fetches the application, but ONLY if the related job post belongs to the
    # currently logged-in employer. Prevents unauthorized access.
    application = get_object_or_404(
        Application,
        id=application_id,
        job__employer=request.user.employer
    )

    context = {
        'application': application
    }

    return render(request, 'applications/application_details.html', context)



