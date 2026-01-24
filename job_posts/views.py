from django.db.models import Q
from django.shortcuts import render, redirect
from authentication.models import Township, State, Location
from job_posts.models import JobPost


def load_townships(request):
    state_id = request.GET.get('state_id')
    townships = Township.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'job_posts/township_dropdown_list_options.html', {'townships': townships})

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
    return render(request, 'job_posts/job_details.html', {'job': job})