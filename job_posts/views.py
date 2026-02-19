from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from applications.models import Application
from authentication.models import Township, State, Location, Employer, Employee
from job_posts.forms import JobPostForm
from job_posts.models import JobPost


def load_townships(request):
    state_id = request.GET.get('state_id')
    townships = Township.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'township_dropdown_list_options.html', {'townships': townships})

def search_jobs(request):
    # Start with a clean queryset
    queryset = JobPost.objects.all()

    # 1. HARD FILTERS (Explicit matches - Very Fast)
    # We narrow the pool from 1,000,000 jobs to maybe 500 in a specific area
    state_id = request.GET.get('state')
    township_id = request.GET.get('township')
    category_id = request.GET.get('category')

    if state_id:
        # This "hops" from JobPost -> Location -> state_id
        queryset = queryset.filter(location__state_id=state_id)
    if township_id:
        # This "hops" from JobPost -> Location -> township_id
        queryset = queryset.filter(location__township_id=township_id)
    if category_id:
        queryset = queryset.filter(category_id=category_id)

    # 2. SOFT FILTER (Keyword search - Expensive)
    # Now we only search keywords within those 500 narrowed results
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    context = {
        'jobs': queryset,
    }
    return render(request, 'job_posts/searched_jobs.html', context)

def job_details(request, job_slug):
    job = JobPost.objects.get(slug=job_slug)

    user_has_applied = False
    if request.user.is_authenticated and request.user.is_employee:
        try:
            # Step 1: Get the Employee profile linked to the User
            employee_profile = request.user.employee

            # Step 2: Use the Employee profile to filter applications
            user_has_applied = Application.objects.filter(
                job=job,
                employee=employee_profile
            ).exclude(status='withdrawn').exists()

        except Employee.DoesNotExist:
            # This is a safety check. It handles cases where a user might be marked
            # as an employee but doesn't have an Employee profile object created yet.
            user_has_applied = False

    context = {
        'job': job,
        'user_has_applied': user_has_applied,
    }
    return render(request, 'job_posts/job_details.html', context)

@login_required
def post_job(request):
    # Find employer profile for the logged in user.
    employer = getattr(request.user, 'employer', None)
    if employer is None:
        # try a different lookup if your Employer model uses a foreign key 'user'
        try:
            employer = Employer.objects.get(user=request.user)
        except (Employer.DoesNotExist, Employer.MultipleObjectsReturned):
            messages.error(request, "You need an Employer profile to post jobs. Please create one first.")
            # Replace 'employer_profile_create' with the actual URL name where employers create their profile.
            return redirect('user_registration')

    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            loc, created = Location.objects.get_or_create(
                state=form.cleaned_data['state'],
                township=form.cleaned_data['township'],
                detail_address=form.cleaned_data['detail_address']
            )
            job.location = loc
            job.employer = employer
            job.save()
            print(job.location.state, job.location.township,job.location.detail_address),
            messages.success(request, "Job posted successfully.")
            # redirect to job detail or job list — change 'job_detail' to your route name
            # return redirect('job_detail', slug=job.slug)
            return redirect('home')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = JobPostForm()

    context = {
        'form': form,
    }
    return render(request, 'job_posts/edit_job.html',context)

@login_required
def jobs_list(request):
    employer = request.user.employer  # adjust if your relation is different
    jobs = JobPost.objects.filter(employer=employer)

    return render(request, 'job_posts/jobs_list.html', {'jobs': jobs})

@login_required
def delete_job(request, slug):
    employer = request.user.employer
    job = get_object_or_404(JobPost, slug=slug, employer=employer)

    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect('jobs_list')

    return render(request, 'jobs_list', {'job': job})

@login_required
def edit_job(request, slug):
    employer = request.user.employer
    job = get_object_or_404(JobPost, slug=slug, employer=employer)

    location = job.location  # existing location

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)

        if form.is_valid():
            job = form.save(commit=False)

            # Update Location manually
            state = form.cleaned_data['state']
            township = form.cleaned_data['township']
            detail_address = form.cleaned_data['detail_address']

            location.state = state
            location.township = township
            location.detail_address = detail_address
            location.save()

            job.location = location
            job.save()

            messages.success(request, "Job updated successfully.")
            return redirect('jobs_list')
    else:
        # Pre-fill manual fields
        form = JobPostForm(instance=job, initial={
            'state': location.state,
            'township': location.township,
            'detail_address': location.detail_address,
        })

    return render(request, 'job_posts/edit_job.html', {'form': form, 'job': job})