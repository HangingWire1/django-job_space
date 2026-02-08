from django.urls import path
from . import views

urlpatterns = [
    # ... other urls
    path('apply_for_job/<slug:job_slug>', views.apply_for_job, name='apply_for_job'),
    # Path for the page that lists all of a user's applications
    path('my_applications/', views.my_applications, name='my_applications'),
    # Path for the action of withdrawing an application
    path('applications/withdraw/<int:application_id>/', views.withdraw_application, name='withdraw_application'),
    path('applications/archive/<int:application_id>/', views.archive_application, name='archive_application'),
    # The main dashboard page for employers to see applicants.
    path('manage_applicants/', views.manage_applicants, name='manage_applicants'),
    # The action URL for the status change form.
    path('update-status/<int:application_id>/', views.update_application_status, name='update_application_status'),
    # ... your other urls
    path('manage-applicants/', views.manage_applicants, name='manage_applicants'),
    path('update-status/<int:application_id>/', views.update_application_status, name='update_application_status'),
    path('application-details/<int:application_id>/', views.application_details, name='application_details'),
]
