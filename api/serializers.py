from rest_framework import serializers
from .models import (
    MyUser,
    Course,
    Chapter,
    Lecture,
    LectureImage,
    LectureFile,
    LectureText,
    Task,
    Grade,
    Comment,
)

# simple jwt 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from xml.dom import ValidationErr





class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("email", "password", "is_teacher")
    
    def validate(self, args):
        email = args.get('email', None)
        if MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ('ERROR: user with this EMAIL already exists.')})
        return super().validate(args)

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        # ...

        return token


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email', 'is_teacher')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'author')

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ('chapter_id', 'name', 'course')

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('lecture_id', 'name', 'chapter')

class LectureTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureText
        fields = ('text', 'lecture')

class LectureImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureImage
        fields = ('image', 'lecture')

class LectureFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureFile
        fields = ('file', 'lecture')

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('chapter', 'name', 'text', 'deadline')

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('student', 'task', 'grade')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('data', 'author', 'text', 'task')