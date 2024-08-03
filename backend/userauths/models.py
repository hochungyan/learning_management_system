from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=30, blank=True)
    otp = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
 
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]
        if not self.full_name:
            self.full_name = self.username
        super().save(*args, **kwargs)