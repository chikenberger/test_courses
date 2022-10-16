import json
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
import datetime
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
from .serializers import (
    CourseSerializer,
    MyTokenObtainPairSerializer, 
    UserRegistrationSerializer,
    UserSerializer,
    CourseSerializer,
    ChapterSerializer,
    LectureSerializer,
    LectureImageSerializer,
    LectureFileSerializer,
    TaskSerializer,
    GradeSerializer,
    CommentSerializer,
)



# view all possibilities of this api (at localhost:8000/api/)
class ApiOverview(APIView):
    def get(self, request, format=None):
        api_urls = {
            'Sign up': 'api/sign-up/',
            'Get jwt tokens': '/api/token/',
            'Refresh jwt tokens': '/api/token/refresh/',
            'List of all users': '/api/all-users/',
        }
        return Response(api_urls)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#sign up (localhost:8000/api/sign-up)
class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
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

#list all users (localhost:8000/api/users/all)
class ListRequestedUsers(APIView):
    def get(self, request, users_type, format=None):
        if users_type == 'all':
            requested_objects = MyUser.objects.all()
        elif users_type == 'students':
            requested_objects = MyUser.objects.filter(is_teacher=False)
        elif users_type == 'teachers':
            requested_objects = MyUser.objects.filter(is_teacher=True)
        else:
            raise NotFound(detail="Error 404: page not found.", code=404)
        
        serializer = UserSerializer(requested_objects, many=True)
        
        return Response(serializer.data)

# list all courses (localhost:8000/api/courses/)
class ListAllCourses(APIView):
    def get(self, request, format=None):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)

        return Response(serializer.data)

def get_jwt_token(request):
    header          = JWTAuthentication().get_header(request)
    raw_token       = JWTAuthentication().get_raw_token(header)
    jwt_token       = JWTAuthentication().get_validated_token(raw_token)
    
    return jwt_token


def token_is_valid(token):
    expiration_date = token.payload['exp']
    current_date    = int(datetime.datetime.now().timestamp())

    if current_date <= expiration_date:
        return True
    return False

# create a course (localhost:8000/api/courses/new)
class CreateCourse(APIView):
    serializer_class = CourseSerializer
    def post(self, request, format=json):
        token = get_jwt_token(request)
        user = JWTAuthentication().get_user(token)
        
        is_teacher = token['is_teacher']
        
        if is_teacher == True:
            if token_is_valid(token):
                request_body = request.data
                request_body['author'] = str(user)
                serializer = CourseSerializer(data=request_body)
                if (serializer.is_valid()):
                    serializer.save()
                    return Response(
                        {
                            "Message": f"Course \"{request_body['name']}\" created succesfully.",
                            "Course": serializer.data
                        }, status=status.HTTP_201_CREATED
                    )
                return Response(
                    {
                        "Errors": serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {
                    "Error": "token is not valid.",
                }, status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            { 
                "Error": "Only teachers are allowed to create courses.",
            }, status=status.HTTP_403_FORBIDDEN
        )

# list all chapters of one course (localhost:8000/api/courses/<pk>/chapters)
class ListAllChapters(APIView):
    def get(self, request, format=json, *args, **kwargs):
        pk = kwargs.get('pk', None)
        course = Course.objects.get(pk=pk)
        chapters = Chapter.objects.filter(course=course)
        serializer = ChapterSerializer(chapters, many=True)

        return Response(serializer.data)

# create a new chapter for one course (localhost:8000/api/courses/<pk>/chapter/new)
class CreateChapter(APIView):
    serializer_class = ChapterSerializer
    def post(self, request, format=json, *args, **kwargs):
        pk = kwargs.get('pk', None)
        token = get_jwt_token(request)
        user = JWTAuthentication().get_user(token)
        
        is_teacher = token['is_teacher']

        if is_teacher == True:
            if token_is_valid(token):
                course = Course.objects.get(pk=pk)
                course_author = course.author
                if str(user) == str(course_author): 
                    # request_body = {}
                    request_body = request.data
                    request_body['course'] = pk
                    serializer = ChapterSerializer(data=request_body)
                    if (serializer.is_valid()):
                        serializer.save()
                        return Response(
                            {
                                "Message": f"Chapter \"{request.data['name']}\" created succesfully.",
                                "Chapter": serializer.data
                            }, status=status.HTTP_201_CREATED
                        )
                    return Response(
                        {
                            "Errors": serializer.errors
                        }, status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {
                        "Error": "you can create chapters only for your courses."
                    }, status=status.HTTP_403_FORBIDDEN
                )
            return Response(
                {
                    "Error": "token is not valid.",
                }, status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            { 
                "Error": "Only teachers are allowed to create chaptes.",
            }, status=status.HTTP_403_FORBIDDEN
        )