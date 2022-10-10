from rest_framework import serializers
from .models import Task, MyUser

# simple jwt 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

#registration
from xml.dom import ValidationErr




class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'



class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email', 'is_teacher')




class RegistrationSerializer(serializers.ModelSerializer):


    class Meta:
        model = MyUser
        fields = ("email", "password", "is_teacher")
    
    def validate(self, args):
        email = args.get('email', None)
        if MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ('ERROR: user with this EMAIL already exists.')})
        return super().validate(args)

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        # ...

        return token
