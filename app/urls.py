from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    RegisterView, post_detail, create_post, 
    StudentListView, StudentDetailView, StudentCreateView, 
    StudentUpdateView, StudentDeleteView,
)
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/update/', views.post_update, name='post_update'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("user_profile/<int:pk>/",views.user_profile,name="profile"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path("post/<int:pk>/delete/", views.delete_post, name="delete_post"),
    path('students/', StudentListView.as_view(), name='user_lst'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('students/create/', StudentCreateView.as_view(), name='student_create'),
    path('students/<int:pk>/update/', StudentUpdateView.as_view(), name='student_update'),
    path('darslar/', views.DarsListView.as_view(), name='dars_list'),
    path('students/<int:pk>/delete/', StudentDeleteView.as_view(), name='student_delete'),

]