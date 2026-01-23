
from django.shortcuts import render, redirect
from django.http import JsonResponse
from authentication.models import Township

def load_townships(request):
    state_id = request.GET.get('state_id')
    townships = Township.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'job_posts/township_dropdown_list_options.html', {'townships': townships})

def search(request):
    pass
