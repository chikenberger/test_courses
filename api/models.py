from email.policy import default
from django.db import models

# custom user model
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from .managers import MyUserManager


# Create your models here.


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



class Course(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    chapter_id = models.SmallIntegerField(default=1)
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Lecture(models.Model):
    lecture_id = models.IntegerField(default=1)
    name = models.CharField(max_length=100)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class LectureText(models.Model):
    text = models.TextField(blank=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class LectureImage(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

    image_upload_path = f'courses/{lecture.name}/files/images/'
    image = models.ImageField(upload_to=image_upload_path)

    def __str__(self):
        return self.image

class LectureFile(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    file_upload_path = f'courses/{lecture.name}/files/'
    file = models.FileField(upload_to=file_upload_path)

    def __str__(self):
        return self.file



class Task(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    text = models.TextField()
    deadline = models.DateField()
    
    def __str__(self):
        return self.name

class Grade(models.Model):
    student = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    grade = models.SmallIntegerField(default=0)


class Comment(models.Model):
    data = models.DateField()
    author = models.EmailField()
    text = models.CharField(max_length=200)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)