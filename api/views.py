import json
from turtle import update
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



# JWT TOKEN FUNCTIONS
def get_jwt_token(request):
    header          = JWTAuthentication().get_header(request)
    raw_token       = JWTAuthentication().get_raw_token(header)
    validated_token = JWTAuthentication().get_validated_token(raw_token)
    return validated_token

def get_user_email(token):
    user = JWTAuthentication().get_user(token)
    return str(user)

def token_is_valid(token):
    expiration_date = token.payload['exp']
    current_date    = int(datetime.datetime.now().timestamp())

    if current_date <= expiration_date:
        return True
    return False

# RESPONSE FUNCTIONS
def response_forbidden():
    return Response(
                {
                    'Message':'You are not allowed to do this.',
                }, status=status.HTTP_403_FORBIDDEN
            )
def response_token_expired():
    return Response(
                {
                    "Error": "token is not valid.",
                }, status=status.HTTP_401_UNAUTHORIZED
            )

# CRUD ADDITIONAL FUNCTIONS
def created_updated_responses(created_or_updated, serializer):
    code = status.HTTP_200_OK
    if created_or_updated == 'create':
        code = status.HTTP_201_CREATED
    return Response(
            {
                'Message': f"instance {created_or_updated}d successfuly.",
                'info': serializer.data
            }, status=code
        )

def create_or_update(create_or_update, serializer):
    if serializer.is_valid():
        serializer.save()
        return created_updated_responses(create_or_update)
    return serializer.errors()

def delete_instance(instance_pk, instance_model):
    instance = get_object_or_404(
        instance_model,
        pk=instance_pk
    )
    instance.delete()
    return Response(
        {
            "Message": "Instance deleted successfuly."
        }, status=status.HTTP_200_OK
    )


def get_instance_info(instance_model, instance_pk):
    instance = get_object_or_404(
        instance_model,
        pk=instance_pk
    )
    if instance_model == MyUser:
        serializer = UserSerializer(instance)
    elif instance_model == Course:
        serializer = CourseSerializer(instance)
    elif instance_model == Chapter:
        serializer = ChapterSerializer(instance)
    elif instance_model == Lecture:
        serializer = LectureSerializer(instance)
    elif instance_model == LectureImage:
        serializer = LectureImageSerializer(instance)
    elif instance_model == LectureFile:
        serializer = LectureFileSerializer(instance)
    elif instance_model == Task:
        serializer = TaskSerializer(instance)
    elif instance_model == Solution:
        serializer = SolutionSerializer(instance)
    elif instance_model == Comment:
        serializer = CommentSerializer(instance)
    elif instance_model == CourseApplication:
        serializer = CourseApplicationSerializer(instance)
    elif instance_model == AverageCourseGrade:
        serializer = AverageCourseGradeSerializer(instance)
    return Response(serializer.data)

def is_course_author(request, course_pk):
    token = get_jwt_token(request)
    user = get_user_email(token)

    course = Course.objects.get(pk=course_pk)
    if user == course.author:
        return True
    return False






#
#
# USER
#
#

#sign up
class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        return create_or_update('create', serializer)


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
    def get(self, request, format=json, *args, **kwargs):
        user_pk = kwargs.get('user_pk', None)
        return get_instance_info(MyUser, user_pk)

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
        return create_or_update('updated', serializer)

# delete 1 user
class DeleteUser(APIView):
    def post(self, request, format=json, *args, **kwargs):
        user_pk = kwargs.get('user_pk', None)
        return delete_instance(user_pk, MyUser)



#
#
# COURSE CRUD
#
#

# create a course
class CreateCourse(APIView):
    def post(self, request, format=json):
        token = get_jwt_token(request)
        user = get_user_email(token)
        
        is_teacher = token['is_teacher']

        if is_teacher == True:
            if token_is_valid(token):
                request_body = request.data
                request_body['author'] = user
                serializer = CourseSerializer(data=request_body)
                return create_or_update('create', serializer)
            return response_token_expired()
        return response_forbidden()

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
        return get_instance_info(Course, course_pk)

# update course info
class UpdateCourse(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk', None)
        course = get_object_or_404(
            Course,
            pk=course_pk
        )        
        serializer = CourseSerializer(course, data=request.data)
        return create_or_update('update', serializer)

# delete course
class DeleteCourse(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk')
        return delete_instance(course_pk, Course)



#
#
# CHAPTER CRUD
#
#

# create a new chapter for a course
class CreateChapter(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk', None)
        token = get_jwt_token(request)

        if is_course_author(request, course_pk):
            if token_is_valid(token):
                request_body = request.data
                request_body['course'] = course_pk
                serializer = ChapterSerializer(data=request_body)
                return create_or_update('create', serializer)
            return response_token_expired
        return response_forbidden

# list all chapters of one course
class ListAllChapters(APIView):
    def get(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk', None)
        chapters = Chapter.objects.filter(course=course_pk)
        serializer = ChapterSerializer(chapters, many=True)
        return Response(serializer.data)

# view chapter info
class ViewChapter(APIView):
    def get(self, request, format=json, *args, **kwargs):
        chapter_pk = kwargs.get('chapter_pk')
        return get_instance_info(Chapter, chapter_pk)

# update course info
class UpdateChapter(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk')
        chapter_pk = kwargs.get('chapter_pk', None)

        if is_course_author(request, course_pk):
            chapter = get_object_or_404(
                Chapter,
                pk=chapter_pk
            )
            serializer = ChapterSerializer(chapter, data=request.data)
            return create_or_update('update', serializer)
        else:
            return response_forbidden


class DeleteChapter(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk')
        chapter_pk = kwargs.get('chapter_pk')
        token = get_jwt_token(request)

        if token_is_valid(token):
            if is_course_author(request, course_pk):
                return delete_instance(Chapter, chapter_pk)
            return response_forbidden
        return response_token_expired




#
#
# LECTURE CRUD
#
#

# create a new lecture
class CreateLecture(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk')
        chapter_pk = kwargs.get('chapter_pk')
        token = get_jwt_token(request)

        if is_course_author(request, course_pk):
            if token_is_valid(token):
                request_body = request.data
                request_body['chapter'] = chapter_pk
                serializer = LectureSerializer(data=request_body)
                return create_or_update('create', serializer)
            return response_token_expired
        return response_forbidden

# list all lectures
class ListAllLectures(APIView):
    def get(self, request, format=json, *args, **kwargs):
        chapter_pk = kwargs.get('chapter_pk')
        lectures = Lecture.objects.filter(chapter=chapter_pk)
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)

# view 1 lecture
class ViewLecture(APIView):
    def get(self, request, format=json, *args, **kwargs):
        lecture_pk = kwargs.get('lecture_pk')
        return get_instance_info(Lecture, lecture_pk)

# update course info
class UpdateLecture(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk  = kwargs.get('course_pk', None)
        lecture_pk = kwargs.get('lecture_pk', None)
        token = get_jwt_token(request)

        if token_is_valid(token):
            if is_course_author(request, course_pk):
                lecture = get_object_or_404(
                    Lecture,
                    pk=lecture_pk
                )
                serializer = LectureSerializer(lecture, data=request.data)
                return create_or_update('update', serializer)
            return response_forbidden
        return response_token_expired   

# delete lecture
class DeleteLecture(APIView):
    serializer_class = LectureSerializer
    def post(self, request, format=json, *args, **kwargs):
        course_pk  = kwargs.get('course_pk', None)
        lecture_pk = kwargs.get('lecture_pk', None)
        token = get_jwt_token(request)

        if token_is_valid(token):
            if is_course_author(request, course_pk):
                return delete_instance(Lecture, lecture_pk)
            return response_forbidden
        return response_token_expired



#
#
# LECTURE FILE/IMAGE CRUD
#
#

# (create)
class LectureAddFileImage(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk  = kwargs.get('course_pk', None)
        lecture_pk = kwargs.get('lecture_pk', None)
        file_type  = kwargs.get('file_type', None)
        token = get_jwt_token(request)

        if is_course_author(request, course_pk):
            if token_is_valid(token):

                request_body = request.data.copy()
                request_body['lecture'] = lecture_pk

                if file_type == 'image':
                    serializer = LectureImageSerializer(data=request_body)
                if file_type == 'file':
                    serializer = LectureFileSerializer(data=request_body)

                serializer = LectureSerializer(data=request_body)
                return create_or_update('create', serializer)
            return response_token_expired
        return response_forbidden

class GetLectureFileImage(APIView):
    def get(self, request, format=json, *args, **kwargs):
        file_type   = kwargs.get('file_type', None)
        file_pk     = kwargs.get('file_pk', None)

        if file_type == 'image':
            return get_instance_info(LectureImage, file_pk)
        elif file_type == 'file':
            return get_instance_info(LectureFile, file_pk)

class UpdateLectureFileImage(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk   = kwargs.get('course_pk', None)
        file_type   = kwargs.get('file_type', None)
        file_pk     = kwargs.get('file_pk', None)

        token = get_jwt_token(request)

        if is_course_author(request, course_pk):
            if token_is_valid(token):

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

                return create_or_update('update', serializer)

            return response_token_expired
        return response_forbidden
        
        return Response(serializer.data)

class DeleteLectureFileImage(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk   = kwargs.get('course_pk', None)
        file_type   = kwargs.get('file_type', None)
        file_pk     = kwargs.get('file_pk', None)
        
        token = get_jwt_token(request)

        if token_is_valid(token):
            if is_course_author(request, course_pk):
                if file_type == 'image':
                    return delete_instance(LectureImage, file_pk)
                elif file_type == 'file':
                    return delete_instance(LectureFile, file_pk)
            return response_forbidden
        return response_token_expired



#
#
# TASK CRUD
#
#

# create a new task
class CreateTask(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk')
        chapter_pk = kwargs.get('chapter_pk')
        token = get_jwt_token(request)

        if token_is_valid(token):
            if is_course_author(request, course_pk):
                request_body = request.data
                request_body['chapter'] = chapter_pk
                serializer = TaskSerializer(data=request_body)
                return create_or_update('create', serializer)
            return response_forbidden
        return response_token_expired

# list all tasks
class ListAllTasks(APIView):
    serializer_class = TaskSerializer
    def get(self, request, format=json, *args, **kwargs):
        chapter_pk = kwargs.get('chapter_pk')
        tasks = Task.objects.filter(chapter=chapter_pk)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

# get task info
class ViewTask(APIView):
    serializer_class = TaskSerializer
    def get(self, request, format=json, *args, **kwargs):
        task_pk = kwargs.get('task_pk')
        return get_instance_info(Task, task_pk)

# update course info
class UpdateTask(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk')
        task_pk   = kwargs.get('task_pk')

        token = get_jwt_token(request)

        if token_is_valid(token):
            if is_course_author(request, course_pk):
                task = get_object_or_404(
                    Task,
                    pk=task_pk
                )
                serializer = TaskSerializer(task, data=request.data)
                return create_or_update('update', serializer)
            return response_forbidden
        return response_token_expired

# delete a task
class DeleteTask(APIView):
    serializer_class = TaskSerializer
    def post(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk')
        task_pk = kwargs.get('task_pk')
        token = get_jwt_token(request)

        if token_is_valid(token):
            if is_course_author(request, course_pk):
                return delete_instance(Task, task_pk)
            return response_forbidden
        return response_token_expired



#
#
# COMMENT CRUD
#
#

# create a new comment
class CreateComment(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk')
        task_pk = kwargs.get('task_pk')

        token = get_jwt_token(request)
        user  = get_user_email(token)

        if token_is_valid(token):
            user_is_course_author = False
            if is_course_author(request, course_pk):
                user_is_course_author = True

            request_body                     = request.data
            request_body['task']             = task_pk
            request_body['author']           = user
            request_body['is_course_author'] = user_is_course_author

            serializer = CommentSerializer(data=request_body)
            
            return create_or_update('create', serializer)
        return response_token_expired

class ViewTaskComments(APIView):
    def get(self, request, format=json, *args, **kwargs):
        task_pk = kwargs.get('task_pk', None)
        comments = Comment.objects.filter(task=task_pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class ViewComment(APIView):
    def get(self, request, format=json, *args, **kwargs):
        comment_pk = kwargs.get('comment_pk', None)
        return get_instance_info(Comment, comment_pk)

class UpdateComment(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk')
        comment_pk = kwargs.get('comment_pk', None)

        token = get_jwt_token(request)
        user = get_user_email(token)

        if token_is_valid(token):
            comment = get_object_or_404(
                Comment,
                pk=comment_pk
            )
            if user == comment.author or is_course_author(request, course_pk):
                request_data = request.data
                request_data['author'] = comment.author
                serializer = CommentSerializer(comment, data=request_data)
                return create_or_update('update', serializer)
            return response_forbidden
        return response_token_expired

class DeleteComment(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk')
        comment_pk = kwargs.get('comment_pk', None)
        
        token = get_jwt_token(request)
        user = get_user_email(token)

        if token_is_valid(token):
            comment = get_object_or_404(
                Comment,
                pk=comment_pk
            )
            if user == comment.author or is_course_author(request, course_pk):
                return delete_instance(Comment, comment_pk)
            return response_forbidden
        return response_token_expired



#
#
# TASKSOLUTION CRUD
#
#

#create
class CreateSolution(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk', None)
        task_pk   = kwargs.get('task_pk', None)

        token = get_jwt_token(request)
        user  = get_user_email(token)

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
                request_body['student'] = user

                serializer = SolutionSerializer(data=request_body)
                return create_or_update('create', serializer)
            return response_forbidden
        return response_token_expired

class ViewAllSolutions(APIView):
    def get(self, request, format=json, *args, **kwargs):
        task_pk = kwargs.get('task_pk', None)
        solutions = Solution.objects.filter(task=task_pk)
        serializer = SolutionSerializer(solutions, many=True)
        return Response(serializer.data)

class ViewSolution(APIView):
    def get(self, request, format=json, *args, **kwargs):
        solution_pk = kwargs.get('solution_pk', None)

        token = get_jwt_token(request)
        user = JWTAuthentication().get_user(token)

        if token_is_valid(token):
            solution = get_object_or_404(
                Solution,
                pk=solution_pk
            )
            if user == solution.student or user == solution.course.author:
                serializer = SolutionSerializer(solution, many=False)
                return Response(serializer.data)
            else:
                return response_forbidden
        else:
            return response_token_expired

class UpdateSolution(APIView):
    def post(self, request, format=json, *args, **kwargs):
        solution_pk = kwargs.get('solution_pk', None)
        course_pk   = kwargs.get('course_pk', None)
        task_pk     = kwargs.get('task_pk', None)

        solution = get_object_or_404(
            Solution,
            pk=solution_pk
        )

        current_date = timezone.now()
        if solution.grade != 0 and current_date <= solution.task.deadline:
            request_body            = request.data
            request_body['course']  = course_pk
            request_body['task']    = task_pk
            request_body['student'] = solution.student
            request_body['grade']   = 0

            serializer = SolutionSerializer(solution, data=request_body)
            return create_or_update('update', serializer)
        else:
            return response_forbidden

class DeleteSolution(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk   = kwargs.get('course_pk')
        solution_pk = kwargs.get('solution_pk')
        
        token = get_jwt_token(request)
        user = get_user_email(token)

        if token_is_valid(token):
            solution = get_object_or_404(
                Solution,
                pk=solution_pk
            )
            if user == solution.course.author:
                return delete_instance(Solution, solution_pk)
            return response_forbidden
        return response_token_expired

class RateSolution(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk   = kwargs.get('course_pk', None)
        task_pk     = kwargs.get('task_pk', None)
        solution_pk = kwargs.get('solution_pk', None)

        token = get_jwt_token(request)

        if token_is_valid(token):
            if is_course_author(request, course_pk):
                solution = get_object_or_404(
                    Solution,
                    pk=solution_pk
                )
                request_data            = request.data.copy()
                request_data['file']    = solution.file
                request_data['course']  = course_pk
                request_data['task']    = task_pk
                request_data['student'] = solution.student

                serializer = SolutionSerializer(solution, data=request_data)
                return create_or_update('create', serializer)
            return response_forbidden
        return response_token_expired



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
        user  = get_user_email(token)

        if token_is_valid(token):
            user_instance = get_object_or_404(
                MyUser,
                email=user
            )
            request_body = {}
            request_body['course'] = course_pk
            request_body['student'] = user_instance.pk
            serializer = CourseApplicationSerializer(data=request_body)
            return create_or_update('create', serializer)
        return response_token_expired

class ListAllApplications(APIView):
    def get(self, request, format=json, *args, **kwargs):
        course_pk = kwargs.get('course_pk', None)

        token = get_jwt_token(request)
        user  = get_user_email(token)

        if token_is_valid(token):
            course = get_object_or_404(
                Course,
                pk=course_pk
            )
            if user == course.author:
                applications = CourseApplication.objects.filter(course=course_pk)
                serializer = CourseApplicationSerializer(applications, many=True)
                return Response(serializer.data)
            return response_forbidden
        return response_token_expired

class ViewApplication(APIView):
    def get(self, request, format=json, *args, **kwargs):
        application_pk = kwargs.get('application_pk')

        token = get_jwt_token(request)
        user  = get_user_email(token)

        if token_is_valid(token):
            application = get_object_or_404(
                CourseApplication,
                pk=application_pk
            )
            if user == application.student.email or user == application.course.author:
                serializer = CourseApplicationSerializer(application)
                return Response(serializer.data)
            return response_forbidden
        return response_token_expired


class ApproveApplication(APIView):
    def post(self, request, format=json, *args, **kwargs):
        application_pk  = kwargs.get('application_pk', None)
        
        token = get_jwt_token(request)
        user = JWTAuthentication().get_user(token)

        application = get_object_or_404(
            CourseApplication,
            pk=application_pk
        )

        if token_is_valid(token):
            if user == application.course.author:
                request_body = {}
                request_body['course']      = application.course.pk
                request_body['student']     = application.student.pk
                request_body['approved']    = True
                serializer = CourseApplicationSerializer(application, data=request_body)
                return create_or_update('update', serializer)
            return response_forbidden
        return response_token_expired                

class DeleteApplication(APIView):
    def post(self, request, format=json, *args, **kwargs):
        application_pk = kwargs.get('application_pk', None)

        token = get_jwt_token(request)
        user  = get_user_email(token)

        if token_is_valid(token):
            application = get_object_or_404(
                CourseApplication,
                pk=application_pk
            )
            if user == application.course.author or user == application.student.email:
                return delete_instance(CourseApplication, application_pk)
            return response_forbidden
        return response_token_expired



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

        token = get_jwt_token(request)
        user = JWTAuthentication().get_user(token)

        if token_is_valid(token):
            course_pk = kwargs.get('course_pk', None)
            course = Course.objects.get(pk=course_pk)
            if course.author == str(user):
                all_students_solutions = Solution.objects.filter(course=course_pk)
                serializer = AverageCourseGradeSerializer(all_students_solutions, many=True)
                return Response(serializer.data)
            else:
                return Response(
                    {
                        'Error': 'only teachers allowed to this page.'
                    }, status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                {
                    'Error': 'token is not valid.'
                }, status=status.HTTP_401_UNAUTHORIZED
            )

class DeleteAverageGrade(APIView):
    def post(self, request, format=json, *args, **kwargs):
        course_pk   = kwargs.get('course_pk', None)
        student_pk  = kwargs.get('student_pk', None)

        token = get_jwt_token(request)
        user = JWTAuthentication().get_user(token)

        if token_is_valid(token):
            course = get_object_or_404(
                Course,
                pk=course_pk
            )
            if course.author == str(user):
                course_grade = get_object_or_404(
                    AverageCourseGrade,
                    course=course_pk,
                    student=student_pk
                )
                course_grade.delete()
            else:
                return Response(
                    {
                        'Error': 'only teachers are allowed to view this page.'
                    }, status=status.HTTP_200_OK
                )

            return Response(
                {
                    "Message": "average grade successfuly deleted.",
                }, status=status.HTTP_200_OK
            )