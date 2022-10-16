from rest_framework import serializers
from .models import (
    MyUser,
    Course,
    Chapter,
    Lecture,
    LectureImage,
    LectureFile,
    Task,
    Grade,
    Comment,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['is_teacher'] = user.is_teacher
        
        return token


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email', 'password', 'is_teacher')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email', 'is_teacher', 'courses')

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'author')

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ('name', 'course')

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'

class LectureImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureImage
        fields = '__all__'


class LectureFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureFile
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Comment
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'