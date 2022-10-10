from django.urls import path
from . import views

# jwt tokens
from .serializers import MyTokenObtainPairSerializer, RegistrationSerializer
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
"""
from .views import (
    MyTokenObtainPairView,
    UserRegistrationView,
)

"""



urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('sign-up/', views.UserRegistrationView.as_view(), name='sign-up'),
    path('token/', views.TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]

"""
path('task-list/', views.taskList, name='task-list'),
path('task-detail/<str:pk>/', views.taskDetail, name='task-detail'),
path('task-create/', views.taskCreate, name='task-create'),
path('task-update/<str:pk>/', views.taskUpdate, name='task-update'),
path('task-delete/<str:pk>/', views.taskDelete, name='task-delete'),
"""