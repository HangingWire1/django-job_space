from django.shortcuts import render

from authentication.models import State
from job_posts.models import Category


def home(request):
    states = State.objects.all().order_by('name')
    categories = Category.objects.all().order_by('name')
    context = {
        'states': states,
        'categories': categories
    }
    return render(request, 'home.html', context)