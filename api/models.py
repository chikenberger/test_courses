from xml.dom.pulldom import START_DOCUMENT
from django.db import models

# custom user model
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import MyUserManager
from django.utils import timezone






class Course(models.Model):
    name        = models.CharField(max_length=100)
    author      = models.EmailField(blank=False)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    name        = models.CharField(max_length=100)
    course      = models.ForeignKey(Course, related_name='chapters', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    chapter     = models.ForeignKey(Chapter, related_name='tasks', on_delete=models.CASCADE, null=True)
    name        = models.CharField(max_length=100)
    text        = models.TextField(blank=False)
    deadline    = models.DateTimeField(blank=False)

    def __str__(self):
        return self.name


class Lecture(models.Model):
    chapter     = models.ForeignKey(Chapter, related_name='lectures', on_delete=models.CASCADE, null=True)
    name        = models.CharField(max_length=100)
    text        = models.TextField(blank=True)

    def __str__(self):
        return self.name

class LectureImage(models.Model):
    image = models.ImageField()
    lecture = models.ForeignKey(Lecture, related_name='images', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.image

class LectureFile(models.Model):
    file = models.FileField()
    lecture = models.ForeignKey(Lecture, related_name='files', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.file


class Comment(models.Model):
    task                = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE, null=True)
    date                = models.DateTimeField(default=timezone.now)
    author              = models.EmailField()
    is_course_author    = models.BooleanField(default=False)
    text                = models.CharField(max_length=200)

    def __str__(self):
        return self.author




"""
class Grade(models.Model):
    course      = models.ForeignKey(Course, related_name='grades', on_delete=models.CASCADE, null=True)
    task        = models.ForeignKey(Task, related_name='grades', on_delete=models.CASCADE, null=True)
    student     = models.EmailField(blank=False, null=True)
    grade       = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.grade
"""




class Solution(models.Model):
    course  = models.ForeignKey(Course, null=True, related_name='solutions', on_delete=models.CASCADE)
    task    = models.ForeignKey(Task, null=True, related_name='solutions', on_delete=models.CASCADE)
    file    = models.FileField()
    student = models.EmailField(null=True)
    grade   = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.student


class MyUser(AbstractUser, PermissionsMixin):
    username     = None
    email        = models.EmailField('Email', max_length=200, unique=True, help_text = 'Your email (Required)')
    password     = models.CharField(max_length=200, help_text = 'Your password (Required)')
    is_teacher   = models.BooleanField(default=False)
    
    courses      = models.ManyToManyField(Course, related_name='courses', blank=True)

    is_staff     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return self.email