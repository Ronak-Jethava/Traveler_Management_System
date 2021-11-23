from django.contrib import admin
from django.urls import path
from employee import views

urlpatterns = [
    path('', views.home),
    path('/add_traveller', views.add_traveller),
]
