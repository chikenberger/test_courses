import json
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
import datetime

from django.contrib.auth.hashers import make_password

# average course grade
from django.utils import timezone
from django.db.models import Avg

from api.managers import MyUserManager


from .models import (
    MyUser,
    Course,
    Chapter,
    Lecture,
    LectureImage,
    LectureFile,
    Task,
    Solution,
    Comment,
    CourseApplication,
    AverageCourseGrade,
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
    SolutionSerializer,
    CommentSerializer,
    CourseApplicationSerializer,
    AverageCourseGradeSerializer,
)



# view all possibilities of this api
class ApiOverview(APIView):
    def get(self, request, format=None):
        api_urls = {
            'get jwt toknes': 'api/token/',
            'refresh jwt tokens': 'api/token/refresh/',
            'users': 'urls',
            'sign up': 'api/sign-up/',
            'list of all users': 'api/users/all/',
            'list of all students': 'api/users/students/',
            'list of all teachers': 'api/users/teachers/',
            'info about user': 'api/users/<int:user_pk>/',
            'delete user': 'api/users/<int:user_pk>/delete/',
            'update user info': 'api/users/<int:user_pk>/update/',
            'courses': 'urls',
            'list of all cousers': 'api/courses/',
            'create a new course': 'api/courses/new/',
            'view info about course': 'api/courses/<course_pk>/',
            'update course info': 'api/courses/<int:course_pk>/update/',
            'delete course': 'api/courses/<int:course_pk>/delete/',
            'chapters': 'urls',
            'create a new chapter': 'api/courses/<int:course_pk>/chapters/new/',
            'list of all chapters': 'api/courses/<int:course_pk>/chapters/',
            'get chapter info': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/',
            'update chapter info': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/update/',
            'delete chapter': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/delete/',
            'lectures': 'urls',
            'create a new lecture': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/lectures/new/',
            'list of all lectures': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/lectures/',
            'get info about lecture': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/lectures/<int:lecture_pk>/',
            'update info about lecture': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/lectures/<int:lecture_pk>/update/',
            'delete lecture': 'api/ courses/<int:course_pk>/chapters/<int:chapter_pk>/lectures/<int:lecture_pk>/delete/',
            'add image to lecture': 'api/ courses/<int:course_pk>/chapters/<int:chapter_pk>/lectures/<int:lecture_pk>/add/image/',
            'add file to lecture': 'api/ courses/<int:course_pk>/chapters/<int:chapter_pk>/lectures/<int:lecture_pk>/add/file/',
            'tasks': 'urls',
            'create a new task': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/new/',
            'list all tasks': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/',
            'get info about task': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/',
            'update task info': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/update/',
            'delete task': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/delete/',
            'comments': 'urls',
            'create a comment': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/comments/new/',
            'list all comments': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/comments/',
            'view comment': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/comments/<int:comment_pk>/',
            'update comment': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/comments/<int:comment_pk>/update/',
            'delete comment': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/comments/<int:comment_pk>/delete/',
            "solutions": 'urls',
            'create a solution': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/solutions/new/',
            'list all solutions': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/solutions/',
            'get solution info': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/solutions/<int:solution_pk>/',
            'update solution': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/solutions/<int:solution_pk>/update/',
            'delete solution': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/solutions/<int:solution_pk>/delete/',
            'rate a solution': 'api/courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/solutions/<int:solution_pk>/rate/',
            'applications': 'urls',
            'make an application': 'api/ courses/<int:course_pk>/applications/new/',
            'list all applications': 'api/ courses/<int:course_pk>/applications/',
            'get application info': 'api/ courses/<int:course_pk>/applications/<application_pk>/',
            'approve application': 'api/ courses/<int:course_pk>/applications/<application_pk>/approve/',
            'delete application': 'api/ courses/<int:course_pk>/applications/<application_pk>/delete/',
            'grades': 'urls',
            'list all average grades': 'api/courses/<int:course_pk>/grades/<int:student_pk>/',
            'count average grade for user': 'api/courses/<int:course_pk>/grades/<int:student_pk>/count/',
            'get average grade of a user': 'api/courses/<int:course_pk>/grades/',
            'delete average grade': 'api/courses/<int:course_pk>/grades/<int:student_pk>/delete/',
        }
        return Response(api_urls)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer






#
#
# USER CRUD
#
#

#sign up
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

#list all users
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

# view info of 1 user
class ViewUserInfo(APIView):
    serializer_class = UserSerializer
    def get(self, request, format=json, *args, **kwargs):
        user_pk = kwargs.get('user_pk', None)
        
        print('USER PK =', user_pk)
        print('KWARGS =', kwargs)

        user = get_object_or_404(
            MyUser,
            pk=user_pk
        )

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

#update
class UpdateUser(APIView):
    def post(self, request, format=json, *args, **kwargs):
        user_pk = kwargs.get('user_pk', None)
        
        user = get_object_or_404(
            MyUser,
            pk=user_pk
        )      

        request_data = request.data
        request_data['password'] = str(make_password(request_data['password']))

        serializer = UserRegistrationSerializer(user, data=request_data)
        if serializer.is_valid():
            # serializer['password'] = str(make_password(serializer['password']))
            serializer.save()
            return Response(
                {
                    "Message": "User modified successfuly.",
                    "user": serializer.data
                }
            )
        return Response(serializer.errors)

# delete 1 user
class DeleteUser(APIView):
    def post(self, request, format=json, *args, **kwargs):
        user_pk = kwargs.get('user_pk', None)
        user = get_object_or_404(
            MyUser,
            pk=user_pk
        )        
        user.delete()
        return Response(
            {
                "Message": "User deleted successfuly."
            }, status=status.HTTP_200_OK
        )






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







#
#
# COURSE CRUD
#
#
# create a course
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
                            "Message": f"Course '{request_body['name']}' created succesfully.",
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


# list all courses
class ListAllCourses(APIView):
    def get(self, request, format=None):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

# view course info
class ViewCourse(APIView):
    def get(self, request, format=None, *args, **kwargs):
        course_pk = kwargs.get('course_pk')

        course = get_object_or_404(
            Course,
            pk=course_pk
        )

        serializer = CourseSerializer(course, many=False)
        return Response(serializer.data)

# update course info
class UpdateCourse(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk', None)

        course = get_object_or_404(
            Course,
            pk=course_pk
        )        
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "Message": "Course modified successfuly.",
                    "course": serializer.data
                }
            )
        return Response(serializer.errors)

# delete course
class DeleteCourse(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk')
        course = get_object_or_404(
            Course,
            pk=course_pk
        )        
        course.delete()
        return Response(
            {
                "Message": "Course successfuly deleted."
            }, status=status.HTTP_200_OK
        )






#
#
#
# CHAPTER CRUD
#
#
# create a new chapter for a course
class CreateChapter(APIView):
    serializer_class = ChapterSerializer
    def post(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk', None)
        token = get_jwt_token(request)
        user = JWTAuthentication().get_user(token)
        
        is_teacher = token['is_teacher']

        if is_teacher == True:
            if token_is_valid(token):
                course = get_object_or_404(
                    Course,
                    pk=course_pk
                )                
                course_author = course.author
                if str(user) == str(course_author): 
                    request_body = request.data
                    request_body['course'] = course_pk
                    serializer = ChapterSerializer(data=request_body)
                    if (serializer.is_valid()):
                        serializer.save()
                        return Response(
                            {
                                "Message": f"Chapter '{request.data['name']}' created succesfully.",
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

# list all chapters of one course
class ListAllChapters(APIView):
    def get(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk', None)
        course = get_object_or_404(
            Course,
            pk=course_pk
        )        
        chapters = Chapter.objects.filter(course=course)
        serializer = ChapterSerializer(chapters, many=True)

        return Response(serializer.data)

# view chapter info
class ViewChapter(APIView):
    def get(self, request, format=json, *args, **kwargs):
        chapter_pk = kwargs.get('chapter_pk')
        chapter = get_object_or_404(
            Chapter,
            pk=chapter_pk
        )
        serializer = ChapterSerializer(chapter, many=False)
        return Response(serializer.data)

# update course info
class UpdateChapter(APIView):
    def post(self, request, format=json, *args, **kwargs):
        chapter_pk = kwargs.get('chapter_pk', None)
        chapter = get_object_or_404(
            Chapter,
            pk=chapter_pk
        )        
        serializer = ChapterSerializer(chapter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "Message": "Chapter modified successfuly.",
                    "chapter": serializer.data
                }
            )
        return Response(serializer.errors)

class DeleteChapter(APIView):
    def post(self, request, format=json, *args, **kwargs):
        chapter_pk = kwargs.get('chapter_pk')
        chapter = get_object_or_404(
            Chapter,
            pk=chapter_pk
        )           
        chapter.delete()
        return Response(
            {
                "Message": "Chapter successfuly deleted."
            }, status=status.HTTP_200_OK
        )







#
#
#
# LECTURE CRUD
#
#
# create a new lecture
class CreateLecture(APIView):
    serializer_class = LectureSerializer
    def post(self, request, format=json, *args, **kwargs):
        
        # pk_course для проверки является ли user автором курса
        course_pk  = kwargs.get('course_pk', None)


        # pk_chapter для добавления в request для LectureSerialzier 
        chapter_pk = kwargs.get('chapter_pk', None)

        token = get_jwt_token(request)
        user = JWTAuthentication().get_user(token)
        
        is_teacher = token['is_teacher']

        if is_teacher == True:
            if token_is_valid(token):
                course = get_object_or_404(
                    Course,
                    pk=course_pk
                )                   
                course_author = course.author
                if str(user) == str(course_author): 
                    request_body = request.data
                    request_body['chapter'] = chapter_pk
                    serializer = LectureSerializer(data=request_body)
                    if (serializer.is_valid()):
                        serializer.save()
                        return Response(
                            {
                                "Message": f"Task '{request.data['name']}' created succesfully.",
                                "Lecture": serializer.data
                            }, status=status.HTTP_201_CREATED
                        )
                    return Response(
                        {
                            "Errors": serializer.errors
                        }, status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {
                        "Error": "you can create lectures only for your courses."
                    }, status=status.HTTP_403_FORBIDDEN
                )
            return Response(
                {
                    "Error": "token is not valid.",
                }, status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            { 
                "Error": "Only teachers are allowed to create lectures.",
            }, status=status.HTTP_403_FORBIDDEN
        )

# list all lectures
class ListAllLectures(APIView):
    serializer_class = LectureSerializer
    def get(self, request, format=json, *args, **kwargs):
        chapter_pk = kwargs.get('chapter_pk', None)
        chapter = get_object_or_404(
            Chapter,
            pk=chapter_pk
        )             
        lectures = Lecture.objects.filter(chapter=chapter)
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)

# view 1 lecture
class ViewLecture(APIView):
    serializer_class = LectureSerializer
    def get(self, request, format=json, *args, **kwargs):
        lecture_pk = kwargs.get('lecture_pk', None)
        lecture = get_object_or_404(
            Lecture,
            pk=lecture_pk
        )
        serializer = LectureSerializer(lecture, many=False)
        return Response(serializer.data)

# update course info
class UpdateLecture(APIView):
    def post(self, request, format=json, *args, **kwargs):
        lecture_pk = kwargs.get('lecture_pk', None)
        lecture = get_object_or_404(
            Lecture,
            pk=lecture_pk
        )
        
        serializer = LectureSerializer(lecture, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "Message": "Lecture modified successfuly.",
                    "lecture": serializer.data
                }
            )
        return Response(serializer.errors)

# delete lecture
class DeleteLecture(APIView):
    serializer_class = LectureSerializer
    def post(self, request, format=json, *args, **kwargs):
        lecture_pk = kwargs.get('lecture_pk', None)
        lecture = get_object_or_404(
            Lecture,
            pk=lecture_pk
        )
        lecture.delete()
        return Response(
            {
                "Message": "Lecture successfuly deleted."
            }, status=status.HTTP_200_OK
        )




#
#
# LECTURE FILE/IMAGE CRUD
#
#

class LectureAddFileImage(APIView):
    def post(self, request, format=json, *args, **kwargs):
        # pk_course для проверки является ли user автором курса
        course_pk  = kwargs.get('course_pk', None)
        lecture_pk = kwargs.get('lecture_pk', None)
        file_type  = kwargs.get('file_type', None)

        token = get_jwt_token(request)
        user = JWTAuthentication().get_user(token)

        course = get_object_or_404(
            Course,
            pk=course_pk
        )
        course_author = course.author

        if str(user) == str(course_author): 
            if token_is_valid(token):
                request_body = request.data.copy()
                request_body['lecture'] = lecture_pk

                if file_type == 'image':
                    serializer = LectureImageSerializer(data=request_body)
                if file_type == 'file':
                    serializer = LectureFileSerializer(data=request_body)

                if (serializer.is_valid()):
                    serializer.save()
                    return Response(
                        {
                            "Message": f"{file_type} added succesfully.",
                            f"{file_type}": serializer.data
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
                "Error": f"you can add {file_type} only for your lectures."
            }, status=status.HTTP_403_FORBIDDEN
        )


class GetLectureFileImage(APIView):
    def get(self, request, format=json, *args, **kwargs):
        file_type   = kwargs.get('file_type', None)
        file_pk     = kwargs.get('file_pk', None)

        if file_type == 'image':
            file_instance = get_object_or_404(
                LectureImage,
                pk=file_pk
            )
            serializer = LectureImageSerializer(file_instance, many=False)
        elif file_type == 'file':
            file_instance = get_object_or_404(
                LectureFile,
                pk=file_pk
            )
            serializer = LectureFileSerializer(file_instance, many=False)
        
        return Response(serializer.data)


class UpdateLectureFileImage(APIView):
    def post(self, request, format=json, *args, **kwargs):
        file_type   = kwargs.get('file_type', None)
        file_pk     = kwargs.get('file_pk', None)

        if file_type == 'image':
            file_instance = get_object_or_404(
                LectureImage,
                pk=file_pk
            )

            serializer = LectureImageSerializer(file_instance, data=request.data)
        elif file_type == 'file':
            file_instance = get_object_or_404(
                LectureFile,
                pk=file_pk
            )
            serializer = LectureFileSerializer(file_instance, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "Message": f"{file_type} modified successfuly.",
                    f"{file_type}": serializer.data
                }, status=status.HTTP_200_OK
            )
        
        return Response(serializer.data)

class DeleteLectureFileImage(APIView):
    def post(self, request, format=json, *args, **kwargs):
        file_type   = kwargs.get('file_type', None)
        file_pk     = kwargs.get('file_pk', None)

        if file_type == 'image':
            file_instance = get_object_or_404(
                LectureImage,
                pk=file_pk
            )
        elif file_type == 'file':
            file_instance = get_object_or_404(
                LectureFile,
                pk=file_pk
            )        
        
        file_instance.delete()

        return Response(
            {
                "Message": f"{file_type} deleted successfuly."
            }, status=status.HTTP_200_OK
        )






#
#
#
# TASK CRUD
#
#
# create a new task
class CreateTask(APIView):
    serializer_class = TaskSerializer
    def post(self, request, format=json, *args, **kwargs):
        
        # pk_course для проверки является ли user автором курса
        course_pk  = kwargs.get('course_pk', None)
 
        # pk_chapter для добавления в request для TaskSerialzier
        chapter_pk = kwargs.get('chapter_pk', None)

        token = get_jwt_token(request)
        user = JWTAuthentication().get_user(token)
        
        is_teacher = token['is_teacher']

        if is_teacher == True:
            if token_is_valid(token):
                course = get_object_or_404(
                    Course,
                    pk=course_pk
                )
                course_author = course.author
                if str(user) == str(course_author): 
                    request_body = request.data
                    request_body['chapter'] = chapter_pk
                    serializer = TaskSerializer(data=request_body)
                    if (serializer.is_valid()):
                        serializer.save()
                        return Response(
                            {
                                "Message": f"Task '{request.data['name']}' created succesfully.",
                                "Task": serializer.data
                            }, status=status.HTTP_201_CREATED
                        )
                    return Response(
                        {
                            "Errors": serializer.errors
                        }, status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {
                        "Error": "you can create lectures only for your courses."
                    }, status=status.HTTP_403_FORBIDDEN
                )
            return Response(
                {
                    "Error": "token is not valid.",
                }, status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            { 
                "Error": "Only teachers are allowed to create lectures.",
            }, status=status.HTTP_403_FORBIDDEN
        )

# list all tasks
class ListAllTasks(APIView):
    serializer_class = TaskSerializer
    def get(self, request, format=json, *args, **kwargs):
        chapter_pk = kwargs.get('chapter_pk', None)
        chapter = get_object_or_404(
            Chapter,
            pk=chapter_pk
        )
        tasks = Task.objects.filter(chapter=chapter)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

# view 1 task
class ViewTask(APIView):
    serializer_class = TaskSerializer
    def get(self, request, format=json, *args, **kwargs):
        task_pk = kwargs.get('task_pk', None)
        task = get_object_or_404(
            Task,
            pk=task_pk
        )
        serializer = TaskSerializer(task, many=False)
        return Response(serializer.data)

# update course info
class UpdateTask(APIView):
    def post(self, request, format=json, *args, **kwargs):
        task_pk = kwargs.get('task_pk', None)
        task = get_object_or_404(
            Task,
            pk=task_pk
        )

        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "Message": "Task modified successfuly.",
                    "task": serializer.data
                }
            )
        return Response(serializer.errors)

# delete 1 task
class DeleteTask(APIView):
    serializer_class = TaskSerializer
    def post(self, request, format=json, *args, **kwargs):
        task_pk = kwargs.get('task_pk', None)
        task = get_object_or_404(
            Task,
            pk=task_pk
        )
        task.delete()
        return Response(
            {
                "Message": "Task deleted successfuly."
            }, status=status.HTTP_200_OK
        )







#
#
# COMMENT CRUD
#
#
# create a new comment
class CreateComment(APIView):
    serializer_class = CommentSerializer
    def post(self, request, format=json, *args, **kwargs):
        # task_pk для добавления в request для CommentSerializer
        task_pk = kwargs.get('task_pk', None)

        # если юзер писавший коммент - автор, то добавлять '(Автор)' после почты
        # course_pk для извлечения автора курса
        course_pk = kwargs.get('course_pk', None)

        course_author = get_object_or_404(
            Course,
            pk=course_pk
        )

        course_author = course_author.author

        token = get_jwt_token(request)
        user = JWTAuthentication().get_user(token)
        
        # если юзер - учитель (не обязательно автор курса)
        is_teacher = token['is_teacher']

        is_course_author = False
        if str(user) == str(course_author):
            is_course_author = True

        if token_is_valid(token):
            request_body                        = request.data
            request_body['task']                = task_pk
            request_body['author']              = str(user)
            request_body['is_course_author']    = is_course_author

            serializer = CommentSerializer(data=request_body)
            if (serializer.is_valid()):
                serializer.save()
                return Response(
                    {
                        "Message": "Comment created succesfully.",
                        "Comment": serializer.data
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

class ViewTaskComments(APIView):
    serializer_class = CommentSerializer
    def get(self, request, format=json, *args, **kwargs):
        task_pk = kwargs.get('task_pk', None)
        comments = Comment.objects.filter(task=task_pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class ViewComment(APIView):
    serializer_class = CommentSerializer
    def get(self, request, format=json, *args, **kwargs):
        comment_pk = kwargs.get('comment_pk', None)

        comment = get_object_or_404(
            Comment,
            pk=comment_pk,
        )

        serializer = CommentSerializer(comment, many=False)
        return Response(serializer.data)

class UpdateComment(APIView):
    def post(self, request, format=json, *args, **kwargs):
        comment_pk = kwargs.get('comment_pk', None)

        comment = get_object_or_404(
            Comment,
            pk=comment_pk
        )
        
        request_data = request.data
        request_data['author'] = comment.author
        serializer = CommentSerializer(comment, data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "Message": "Comment modified successfuly.",
                    "task": serializer.data
                }, status=status.HTTP_200_OK
            )
        return Response(serializer.errors)   

class DeleteComment(APIView):
    def post(self, request, format=json, *args, **kwargs):
        comment_pk = kwargs.get('comment_pk', None)
        comment = get_object_or_404(
            Comment,
            pk=comment_pk
        )
        
        comment.delete()
        return Response(
            {
                "Message": "Comment deleted successfuly."
            }, status=status.HTTP_200_OK
        )


#
#
# TASKSOLUTION CRUD
#
#
class CreateSolution(APIView):
    serializer_class = SolutionSerializer
    def post(self, request, format=json, *args, **kwargs):
        # task_pk для добавления в request для SolutionSerializer
        task_pk     = kwargs.get('task_pk', None)
        course_pk   = kwargs.get('course_pk', None)

        token = get_jwt_token(request)
        user = JWTAuthentication().get_user(token)
        

        if token_is_valid(token):
            task = get_object_or_404(
                Task,
                pk=task_pk
            )
            current_date = timezone.now()
            if current_date <= task.deadline:
                request_body            = request.data.copy()
                request_body['course']  = course_pk
                request_body['task']    = task_pk
                request_body['student'] = str(user)

                serializer = SolutionSerializer(data=request_body)
                if (serializer.is_valid()):
                    serializer.save()
                    return Response(
                        {
                            "Message": "Solution created succesfully.",
                            "Solution": serializer.data
                        }, status=status.HTTP_201_CREATED
                    )
                return Response(
                    {
                        "Errors": serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {
                        "Error": "deadline is expired."
                    }, status=status.HTTP_403_FORBIDDEN
                )
        return Response(
            {
                "Error": "token is not valid.",
            }, status=status.HTTP_401_UNAUTHORIZED
        )

class ViewAllSolutions(APIView):
    serializer_class = SolutionSerializer
    def get(self, request, format=json, *args, **kwargs):
        task_pk = kwargs.get('task_pk', None)
        solutions = Solution.objects.filter(task=task_pk)
        serializer = SolutionSerializer(solutions, many=True)
        return Response(serializer.data)

class ViewSolution(APIView):
    serializer_class = CommentSerializer
    def get(self, request, format=json, *args, **kwargs):
        solution_pk = kwargs.get('solution_pk', None)
        solution = get_object_or_404(
            Solution,
            pk=solution_pk
        )
        serializer = SolutionSerializer(solution, many=False)
        return Response(serializer.data)

class UpdateSolution(APIView):
    def post(self, request, format=json, *args, **kwargs):
        solution_pk = kwargs.get('solution_pk', None)
        course_pk   = kwargs.get('course_pk', None)
        task_pk     = kwargs.get('task_pk', None)

        solution = get_object_or_404(
            Solution,
            pk=solution_pk
        )        
        if solution.grade != 0:
            request_data            = request.data
            request_data['course']  = course_pk
            request_data['task']    = task_pk
            request_data['student'] = solution.student
            request_data['grade']   = 0

            serializer = SolutionSerializer(solution, data=request_data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "Message": "Solution modified successfuly.",
                        "solution": serializer.data
                    }, status=status.HTTP_200_OK
                )
            return Response(serializer.errors)
        else:
            return Response(
                {
                    "Error": "Your previous solution must be rated by teacher."
                }, status=status.HTTP_403_FORBIDDEN
            )

class DeleteSolution(APIView):
    def post(self, request, format=json, *args, **kwargs):
        solution_pk = kwargs.get('solution_pk', None)
        solution = get_object_or_404(
            Solution,
            pk=solution_pk
        )
        solution.delete()
        return Response(
            {
                "Message": "Solution deleted successfuly."
            }, status=status.HTTP_200_OK
        )



class RateSolution(APIView):
    def post(self, request, format=json, *args, **kwargs):
        solution_pk = kwargs.get('solution_pk', None)
        course_pk   = kwargs.get('course_pk', None)
        task_pk     = kwargs.get('task_pk', None)


        token = get_jwt_token(request)
        user = JWTAuthentication().get_user(token)      
        course = get_object_or_404(
            Course,
            pk=course_pk
        )
        if str(user) == course.author:
            solution = get_object_or_404(
                Solution,
                pk=solution_pk
            )
   
            request_data            = request.data
            request_data['file']    = solution.file
            request_data['course']  = course_pk
            request_data['task']    = task_pk
            request_data['student'] = solution.student



            serializer = SolutionSerializer(solution, data=request_data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "Message": "Solution rated successfuly.",
                        "solution": serializer.data
                    }, status=status.HTTP_200_OK
                )
            return Response(serializer.errors)

        return Response(
            {
                "Error": "Only course author can rate students solutions."
            }, status=status.HTTP_403_FORBIDDEN
        )



#
#
#
#  APPLICATION 
#
#
# make an application to a course (for students)
class ApplicateToCourse(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk', None)
        
        token = get_jwt_token(request)
        user = JWTAuthentication().get_user(token)

        if token_is_valid(token) == True:

            user_instance = get_object_or_404(
                MyUser,
                email=str(user)
            )

            request_body = {}
            request_body['course'] = course_pk
            request_body['student'] = user_instance.pk
            serializer = CourseApplicationSerializer(data=request_body)
            print('\n' * 10)
            print('USER =', user_instance)
            print('\n' * 5)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "Message": "Your application submitted successfuly.",
                        "Application": serializer.data
                    }, status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors)
        else:
            return Response(
                {
                    "Error": "token is not valid."
                }, status=status.HTTP_401_UNAUTHORIZED
            )

class ListAllApplications(APIView):
    def get(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk', None)
        applications = CourseApplication.objects.filter(course=course_pk)
        serializer = CourseApplicationSerializer(applications, many=True)
        return Response(serializer.data)

class ViewApplications(APIView):
    def get(self, request, format=json, *args, **kwargs):
        application_pk = kwargs.get('application_pk', None)
        application = get_object_or_404(
            CourseApplication,
            pk=application_pk
        )
        serializer = CourseApplicationSerializer(application)
        return Response(serializer.data)

class ApproveApplication(APIView):
    def post(self, request, format=json, *args, **kwargs):
        application_pk  = kwargs.get('application_pk', None)
        
        token = get_jwt_token(request)
        user = JWTAuthentication().get_user(token)

        application = get_object_or_404(
            CourseApplication,
            pk=application_pk
        )


        if token_is_valid(token) == True:
            if str(user) == application.course.author:
                application = get_object_or_404(
                    CourseApplication,
                    pk=application_pk
                )

                
                request_body = {}
                request_body['course']      = application.course.pk
                request_body['student']     = application.student.pk
                request_body['approved']    = True

                serializer = CourseApplicationSerializer(application, data=request_body)
                
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {
                            "Message": "Course approved successfuly.",
                            "Application": serializer.data
                        }
                    )
                else:
                    return Response(serializer.errors)
            else:
                return Response(
                    {
                        "Error": "You are not a course author."
                    }, status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                {
                    "Error": "token is not valid."
                }, status=status.HTTP_401_UNAUTHORIZED
            )

class DeleteApplication(APIView):
    def post(self, request, format=json, *args, **kwargs):
        application_pk = kwargs.get('application_pk', None)
        application = get_object_or_404(
            CourseApplication,
            pk=application_pk
        )

        application.delete()
        return Response(
            {
                "Message": "application deleted successfuly."
            }, status=status.HTTP_200_OK
        )







#
#
# COURSE GRADE
#
#

class CountAverageCourseGrade(APIView):
    def get(self, request, format=json, *args, **kwargs):
        course_pk   = kwargs.get('course_pk', None)
        student_pk  = kwargs.get('student_pk', None)



        student_course_application = get_object_or_404(
            CourseApplication,
            student=student_pk, 
            course=course_pk,
            approved=True
        )

        student_email = get_object_or_404(
            MyUser,
            pk=student_pk
        )
        student_email = student_email.email

        if student_course_application != None:

            all_student_solutions = Solution.objects.filter(
                course=course_pk,
                student=student_email
            )

            print(all_student_solutions)
            
            if all_student_solutions.exists():
                average_course_grade = all_student_solutions.aggregate(Avg('grade'))

                request_body = {}
                request_body['course']  = course_pk
                request_body['student'] = student_pk
                request_body['grade'] = average_course_grade.get('grade__avg')

                serializer = AverageCourseGradeSerializer(data=request_body)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
            else:
                raise NotFound(detail="Error 404: page not found.", code=404)
        else:
            raise NotFound(detail="Error 404: page not found.", code=404)


class GetAverageCourseGrade(APIView):
    def get(self, request, format=json, *args, **kwargs):
        course_pk   = kwargs.get('course_pk', None)
        student_pk  = kwargs.get('student_pk', None)

        course_grade = get_object_or_404(
            AverageCourseGrade,
            course=course_pk,
            student=student_pk
        )

        serializer = AverageCourseGradeSerializer(course_grade)
        
        return Response(serializer.data)

class GetAllStudentsCourseGrades(APIView):
    def get(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk', None)

        all_students_solutions = Solution.objects.filter(course=course_pk)

        serializer = AverageCourseGradeSerializer(all_students_solutions, many=True)
        return Response(serializer.data)

class DeleteAverageGrade(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk   = kwargs.get('course_pk', None)
        student_pk  = kwargs.get('student_pk', None)

        course_grade = get_object_or_404(
            AverageCourseGrade,
            course=course_pk,
            student=student_pk
        )

        course_grade.delete()

        return Response(
            {
                "Message": "average grade successfuly deleted.",
            }, status=status.HTTP_200_OK
        )