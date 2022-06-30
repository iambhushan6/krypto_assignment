
from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from authentication import models
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=60, min_length=6, write_only=True)

    class Meta:
        model = models.User
        fields = ['email', 'password', 'username', 'id']

    def validate(self, attrs):
        email = attrs.get('email','')
        username = attrs.get('username','')
        id = attrs.get('id','')
        _id = attrs.get('_id','')

        return attrs 

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):


    email = serializers.CharField()
    password = serializers.CharField(max_length = 68, min_length = 6, write_only = True)
    authToken = serializers.CharField(max_length = 68, min_length = 6, read_only=True)


    class Meta:
        model = models.User
        fields = ['email', 'password', 'authToken']

    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        user = auth.authenticate( email= email, password= password)

        if not user:
            raise AuthenticationFailed("Invalid Credentials")

        return {  
            "email": user.email,
            # "username": user.username,
            'authToken': user.tokens
        }
        return super().validate(attrs)