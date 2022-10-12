from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.views import APIView

from .models import (
    MyUser,
    Course,
    Chapter,
    Lecture,
    LectureText,
    LectureImage,
    LectureFile,
    Task,
    Grade,
    Comment,
)

from .serializers import (
    MyTokenObtainPairSerializer, 
    RegistrationSerializer,
    MyUserSerializer,
    CourseSerializer,
    ChapterSerializer,
    LectureSerializer,
    LectureTextSerializer,
    LectureImageSerializer,
    LectureFileSerializer,
    TaskSerializer,
    GradeSerializer,
    CommentSerializer,
)


# Create your views here. 



@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Sign up': 'api/sign-up/',
        'Get jwt tokens': '/api/token/',
        'Refresh jwt tokens': '/api/token/refresh/',
        'List of all users': '/api/all-users/',
    }

    return Response(api_urls)


class ListAllUsers(APIView):
    def get(self, request, format=None):
        users = MyUser.objects.all()
        serializer = MyUserSerializer(users, many=True)

        return Response(serializer.data)

class ListAllStudents(APIView):
    def get(self, request, format=None):
        students = MyUser.objects.filter(is_teacher=False)
        serializer = MyUserSerializer(students, many=True)

        return Response(serializer.data)








class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserRegistrationView(generics.GenericAPIView):

    serializer_class = RegistrationSerializer

    def post(self, request):
        
        serializer = self.get_serializer(data = request.data)
        
        if (serializer.is_valid()):
            serializer.save()
            response = Response(
                {
                    "Message": "User created succesfully.",
                    "User": serializer.data
                }, status=status.HTTP_201_CREATED
            )
            return response

        return Response({"Errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

