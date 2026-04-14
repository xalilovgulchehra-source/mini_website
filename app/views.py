from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Post,Dars,Alo
from .forms import StudentForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, PostForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Post

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
    userlar = Alo.objects.all()
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
    
class DarsListView(ListView):
    model = Dars
    template_name = 'myapp/dars_list.html' # Darslar ko'rinadigan html fayl
    context_object_name = 'darslar'
    
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/list.html', {'posts': posts})


# 🔍 DETAIL (bitta post)
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/detail.html', {'post': post})


# ➕ CREATE
@login_required
def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        image = request.FILES.get('image')

        Post.objects.create(
            author=request.user,
            title=title,
            body=body,
            image=image
        )
        return redirect('post_list')

    return render(request, 'posts/create.html')


# ✏️ UPDATE
@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # faqat owner edit qilsin
    if post.author != request.user:
        return redirect('post_list')

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.body = request.POST.get('body')

        if request.FILES.get('image'):
            post.image = request.FILES.get('image')

        post.save()
        return redirect('post_detail', pk=post.pk)

    return render(request, 'posts/update.html', {'post': post})


# ❌ DELETE
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # faqat owner delete qilsin
    if post.author != request.user:
        return redirect('post_list')

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(request, 'posts/delete.html', {'post': post})