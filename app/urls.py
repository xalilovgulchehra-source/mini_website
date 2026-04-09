from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("user_profile/<int:pk>/",views.user_profile,name="profile"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path("post/<int:pk>/delete/", views.delete_post, name="delete_post"),
    path('profile/edit/', views.StudentUpdateView.as_view(), name='student_update'),
]