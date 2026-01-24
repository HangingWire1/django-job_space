
from django.urls import path
from job_posts import views

urlpatterns = [

    path('search_jobs/',views.search_jobs,name='search_jobs'),
    #show townships with related states
    path('ajax/load-townships/', views.load_townships, name='ajax_load_townships'),
    path('job_details/<slug:job_slug>/',views.job_details,name='job_details'),
]