from django.contrib import admin
from django.urls import path
from employee import views

urlpatterns = [
    path('', views.home),
]
