from django.shortcuts import render

from authentication.models import State
from job_posts.models import Category


def home(request):
    return render(request, 'home.html')