from rest_framework import serializers
from .models import (
    CourseApplication,
    MyUser,
    Course,
    Chapter,
    Lecture,
    LectureImage,
    LectureFile,
    Task,
    Comment,
    Solution,
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
        fields = ('pk', 'email', 'password', 'is_teacher', 'courses')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('pk', 'name', 'author')


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ('pk', 'name', 'course')



class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('pk', 'name', 'text', 'chapter')

class LectureImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureImage
        fields = ('pk', 'image', 'lecture')

class LectureFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureFile
        fields = ('pk', 'file', 'lecture')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('pk', 'name', 'text', 'deadline', 'chapter')


class CommentSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Comment
        fields = ('pk', 'date', 'author', 'text', 'is_course_author', 'task')


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ('pk', 'task', 'file', 'student', 'grade')


class CourseApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseApplication
        course = '__all__'