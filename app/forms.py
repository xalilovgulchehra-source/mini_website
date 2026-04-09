# app/forms.py
from django import forms
from .models import CustomUser,Post

class CustomUserCreationForm(forms.ModelForm):
    # Bu ro'yxatdan o'tish uchun
    class Meta:
        model = CustomUser
        fields = ('phone_number',)

class StudentForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'birth_date', 'profile_picture']
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image']