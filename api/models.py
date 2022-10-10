from email.policy import default
from django.db import models

# custom user model
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from .managers import MyUserManager

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.title


class MyUser(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField('Email', max_length=200, unique=True, help_text = 'Your email (Required)')
    password = models.CharField(max_length=200, help_text = 'Your password (Required)')
    is_teacher = models.BooleanField(default=False, help_text = 'Mark if you are a teacher')
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def is_a_teacher(self, perm, obj=None):
        return self.is_teacher


