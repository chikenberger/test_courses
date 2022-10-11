from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status

from .serializers import (
    MyTokenObtainPairSerializer, 
    RegistrationSerializer,
    MyUserSerializer,


)

from .models import MyUser

# Create your views here. 



@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        
        'Sign up':'api/sign-up/',
        'Get jwt tokens': '/api/token',
        'Refresh jwt tokens': '/api/token/refresh',
    }

    return Response(api_urls)


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
