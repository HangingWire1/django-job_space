# jobs/context_processors.py
from authentication.models import State
from job_posts.models import Category

def job_search_data(request):
    """
    Makes states and categories globally available across all templates.
    """
    return {
        'states': State.objects.all().order_by('name'),
        'categories': Category.objects.all().order_by('name'),
    }