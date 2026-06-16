
from django.urls import path
from dashboard import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # category crud
    path('categories/',views.categories, name='categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
    # blog post crud
    path('posts/', views.posts, name='posts'),
    path('posts/add/',views.add_post, name='add_post'),
    path('posts/edit/<int:pk>/',views.edit_post, name='edit_post'),
    path('posts/delete/<int:pk>/',views.delete_post, name='delete_post'),
    #users crud
    path('users/',views.users, name='users'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/edit/<int:pk>/',views.edit_user, name='edit_user'),
    path('users/delete/<int:pk>/',views.delete_user, name='delete_user'),
    # location/states
    path('states/',views.states, name='states'),
    path('states/add/', views.add_state, name='add_state'),
    path('states/edit/<int:pk>/', views.edit_state, name='edit_state'),
    path('states/delete/<int:pk>', views.delete_state, name='delete_state'),
    # location/townships
    path('townships/<int:state_id>/', views.townships, name='townships'),
    path('township/add/<int:state_id>/', views.add_township, name='add_township'),
    path('township/edit/<int:state_id>/<int:pk>/', views.edit_township, name='edit_township'),
    path('township/delete/<int:state_id>/<int:pk>', views.delete_township, name='delete_township'),
]