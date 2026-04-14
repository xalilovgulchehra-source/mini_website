from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings

# 1. Manager birinchi turishi kerak
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Telefon raqami kiritilishi shart!')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(phone_number, password, **extra_fields)

# 2. Keyin Model kelishi kerak
class CustomUser(AbstractUser):
    username = None 
    phone_number = models.CharField(max_length=15, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default="profile_pics/default.jpg", blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = [] 

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number

# 3. Va boshqa modellar (FK uchun settings.AUTH_USER_MODEL ishlating)
class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='posts'
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Dars(models.Model):
    nomi = models.CharField(max_length=200)
    haqida = models.TextField() 
    sana = models.DateTimeField(auto_now_add=True)
    video_fayl = models.FileField(upload_to='media/videos')

    def __str__(self):
        return self.nomi
    
class Alo(models.Model):
    ism = models.CharField(max_length=100)
    familiya = models.CharField(max_length=100)
    pic = models.ImageField(upload_to='media/profile_pics')
