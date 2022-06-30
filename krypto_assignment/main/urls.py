from django.contrib import admin
from django.urls import path
from main.views import AlertsAPIView

urlpatterns = [
    path('api/alerts', AlertsAPIView.as_view(), name='alertview'),
]