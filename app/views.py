from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Post
from .forms import StudentForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, PostForm

User = get_user_model()

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'myapp/register.html'
    success_url = reverse_lazy('login')

def user_profile(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    user_posts = user_obj.posts.all().order_by('-created_at')
    
    context = {
        'user_obj': user_obj,
        'user_posts': user_posts,
    }
    return render(request, 'myapp/user_profile.html', context)

def user_lst(request):
    userlar = CustomUser.objects.all()
    return render(request, 'myapp/userlar.html', {'users': userlar})

class StudentListView(ListView):
    model = CustomUser
    template_name = 'myapp/userlar.html'
    context_object_name = 'users'

class StudentDetailView(DetailView):
    model = CustomUser
    template_name = 'myapp/ad.html'
    context_object_name = 'user'

class StudentCreateView(CreateView):
    model = CustomUser
    form_class = StudentForm
    template_name = 'myapp/student_form.html'
    success_url = reverse_lazy('user_lst')

class StudentUpdateView(UpdateView):
    model = CustomUser
    form_class = StudentForm
    template_name = 'myapp/student_form.html'
    success_url = reverse_lazy('user_lst')

class StudentDeleteView(DeleteView):
    model = CustomUser
    template_name = 'myapp/student_confirm_delete.html'
    success_url = reverse_lazy('user_lst')
    context_object_name = 'user'
    
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('profile', pk=request.user.id)

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect('profile', pk=request.user.id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=request.user.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'app/edit_post.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'app/post_detail.html', {'post': post})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
    return redirect('profile', pk=request.user.id)