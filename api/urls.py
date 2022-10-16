from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('', views.ApiOverview.as_view(), name='api-overview'),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),

    path('sign-up/', views.UserRegistrationView.as_view(), name='sign-up'),
    path('users/<str:users_type>/', views.ListRequestedUsers.as_view(), name='list-of-all-users'),
    path('courses/', views.ListAllCourses.as_view(), name='list-all-courses'),

    path('courses/new', views.CreateCourse.as_view(), name='create-new-course'),
    path('courses/<int:pk>/chapters/new', views.CreateChapter.as_view(), name='create-new-chapter'),
    path('courses/<int:pk>/chapters', views.ListAllChapters.as_view(), name='list-all-chapters'),
]