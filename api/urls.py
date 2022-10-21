from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('', views.ApiOverview.as_view(), name='api-overview'),

    #jwt tokens
    path('token/', views.MyTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),

    # user
    path('sign-up/', views.UserRegistrationView.as_view(), name='sign-up'),
    path('users/<int:user_pk>/', views.ViewUserInfo.as_view(), name='view-user-info'),
    path('users/<int:user_pk>/delete/', views.DeleteUser.as_view(), name='delete-user'),
    path('users/<int:user_pk>/update/', views.UpdateUser.as_view(), name='update-user'),
    path('users/<str:users_type>/', views.ListRequestedUsers.as_view(), name='list-of-all-users'),

    # course
    path('courses/new/', views.CreateCourse.as_view(), name='create-new-course'),
    path('courses/', views.ListAllCourses.as_view(), name='list-all-courses'),
    path('courses/<int:course_pk>/', views.ViewCourse.as_view(), name='view-course'),
    path('courses/<int:course_pk>/update/', views.UpdateCourse.as_view(), name='update-course'),
    path('courses/<int:course_pk>/delete/', views.DeleteCourse.as_view(), name='delete-course'),

    # chapter
    path('courses/<int:course_pk>/chapters/new/',\
         views.CreateChapter.as_view(), name='create-new-chapter'),
    path('courses/<int:course_pk>/chapters/', \
        views.ListAllChapters.as_view(), name='list-all-chapters'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/',\
         views.ViewChapter.as_view(), name='view-chapter'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/update/',\
         views.UpdateChapter.as_view(), name='update-chapter'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/delete/',\
         views.DeleteChapter.as_view(), name='delete-chapter'),

    # lecture
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/lectures/new/', \
        views.CreateLecture.as_view(), name='create-new-lecture'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/lectures/', \
        views.ListAllLectures.as_view(), name='list-all-lectures'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/lectures/<int:lecture_pk>/', \
        views.ViewLecture.as_view(), name='view-lecture'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/lectures/<int:lecture_pk>/update/', \
        views.UpdateLecture.as_view(), name='update-lecture'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/lectures/<int:lecture_pk>/delete/', \
        views.DeleteLecture.as_view(), name='delete-lecture'),

    # lecture file/image
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/lectures/<int:lecture_pk>/<str:file_type>/new/', \
        views.LectureAddFileImage.as_view(), name='create-lecture-file-or-image'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/lectures/<int:lecture_pk>/<str:file_type>/<int:file_pk>/get/', \
        views.GetLectureFileImage.as_view(), name='get-lecture-file-or-image'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/lectures/<int:lecture_pk>/<str:file_type>/<int:file_pk>/update/', \
        views.UpdateLectureFileImage.as_view(), name='update-lecture-file-or-image'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/lectures/<int:lecture_pk>/<str:file_type>/<int:file_pk>/delete/', \
        views.DeleteLectureFileImage.as_view(), name='delete-lecture-file-or-image'),

    # task
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/new/', \
        views.CreateTask.as_view(), name='create-new-task'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/', \
        views.ListAllTasks.as_view(), name='list-all-tasks'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/', \
        views.ViewTask.as_view(), name='view-task'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/update/', \
        views.UpdateTask.as_view(), name='update-task'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/delete/', \
        views.DeleteTask.as_view(), name='delete-task'),
    
    # comment
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/comments/new/', \
        views.CreateComment.as_view(), name='create-comment'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/comments/', \
        views.ViewTaskComments.as_view(), name='view-task-comments'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/comments/<int:comment_pk>/', \
        views.ViewComment.as_view(), name='view-comment'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/comments/<int:comment_pk>/update/',\
        views.UpdateComment.as_view(), name='change-comment'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/comments/<int:comment_pk>/delete/', \
        views.DeleteComment.as_view(), name='delete-comment'),

    # solutions
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/solutions/new/', \
        views.CreateSolution.as_view(), name='create-solution'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/solutions/', \
        views.ViewAllSolutions.as_view(), name='view-all-solutions'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/solutions/<int:solution_pk>/', \
        views.ViewSolution.as_view(), name='view-solution'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/solutions/<int:solution_pk>/update/',\
        views.UpdateSolution.as_view(), name='change-solution'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/solutions/<int:solution_pk>/delete/', \
        views.DeleteSolution.as_view(), name='delete-solution'),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/tasks/<int:task_pk>/solutions/<int:solution_pk>/rate/',\
        views.RateSolution.as_view(), name='rate-solution'),
    
    # applications
    path('courses/<int:course_pk>/applications/new/', \
        views.ApplicateToCourse.as_view(), name='applicate-to-course'),
    path('courses/<int:course_pk>/applications/', \
        views.ListAllApplications.as_view(), name='list-all-applications'),
    path('courses/<int:course_pk>/applications/<application_pk>/', \
        views.ViewApplication.as_view(), name='view-application'),
    path('courses/<int:course_pk>/applications/<application_pk>/approve/', \
        views.ApproveApplication.as_view(), name='approve-application'),
    path('courses/<int:course_pk>/applications/<application_pk>/delete/', \
        views.DeleteApplication.as_view(), name='delete-application'),
    
    # course grade
    path('courses/<int:course_pk>/grades/<int:student_pk>/', \
        views.GetAverageCourseGrade.as_view(), name='get-course-grade'),
    path('courses/<int:course_pk>/grades/<int:student_pk>/count/', \
        views.CountAverageCourseGrade.as_view(), name='count-course-grade'),
    path('courses/<int:course_pk>/grades/', \
        views.GetAllStudentsCourseGrades.as_view(), name='all-students-course-grade'),
    path('courses/<int:course_pk>/grades/<int:student_pk>/delete/', \
        views.DeleteAverageGrade.as_view(), name='delete-average-grade'),
]