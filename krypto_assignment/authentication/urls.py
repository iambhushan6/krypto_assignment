from django import views
from django.contrib import admin
from django.urls import path
from authentication.views import test_view, LoginAPIView, RegisterUser

urlpatterns = [
    path('test/', test_view, name='test_view'),

    path('auth/login', LoginAPIView.as_view(), name='login'),

    path('auth/register', RegisterUser.as_view(), name='register'),
]