from django.contrib import admin
from django.urls import path
from home import views

import dummy

urlpatterns = [
    path('', views.home),
]
