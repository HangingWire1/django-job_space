
from django.urls import path
from job_posts import views

urlpatterns = [

    path('search/',views.search,name='search'),
    #show townships with related states
    path('ajax/load-townships/', views.load_townships, name='ajax_load_townships'),

]