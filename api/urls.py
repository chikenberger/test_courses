from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('sign-up/', views.UserRegistrationView.as_view(), name='sign-up'),
    path('token/', views.TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('all-users/', views.ListAllUsers.as_view(), name='list-of-all-users'),
    path('all-students/', views.ListAllStudents.as_view(), name='list-of-all-students')

]
