
from django.urls import path
from user_profile import views

urlpatterns = [
    path('edit_profile/employee/',views.edit_employee_profile,name='edit_employee_profile'),
    path('edit_profile/employer/',views.edit_employer_profile,name='edit_employer_profile'),
    path('test_location',views.test_location,name='test_location'),
]