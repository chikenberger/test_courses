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
    AverageCourseGrade,
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
        fields = ('pk', 'email', 'password', 'is_teacher')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('pk', 'email', 'is_teacher', 'courses')





class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ('pk', 'course', 'task', 'file', 'student', 'grade')

class CommentSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Comment
        fields = ('pk', 'date', 'author', 'text', 'is_course_author', 'task')

class TaskSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    solutions = SolutionSerializer(many=True)
    class Meta:
        model = Task
        fields = ('pk', 'name', 'text', 'deadline', 'chapter', 'comments', 'solutions')


class LectureImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureImage
        fields = ('pk', 'lecture', 'image')

class LectureFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureFile
        fields = ('pk', 'lecture', 'file')

class LectureSerializer(serializers.ModelSerializer):
    images = LectureImageSerializer(many=True)
    files = LectureFileSerializer(many=True)
    class Meta:
        model = Lecture
        fields = ('pk', 'name', 'text', 'chapter', 'images', 'files')


class ChapterSerializer(serializers.ModelSerializer):
    lectures = LectureSerializer(many=True)
    tasks = TaskSerializer(many=True)
    class Meta:
        model = Chapter
        fields = ('pk', 'course', 'name', 'lectures', 'tasks')


class CourseApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseApplication
        fields = ('pk', 'course', 'student', 'approved')

class AverageCourseGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AverageCourseGrade
        fields = ('pk', 'course', 'student', 'grade')

class CourseSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True)
    applications = CourseApplicationSerializer(many=True)
    grades = AverageCourseGradeSerializer(many=True)
    class Meta:
        model = Course
        fields = ('pk', 'name', 'author', 'chapters', 'applications', 'grades')




