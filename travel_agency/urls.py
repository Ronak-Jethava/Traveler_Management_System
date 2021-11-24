from django.contrib import admin
from django.urls import path
from travel_agency import views

urlpatterns = [
    path('', views.home),
    path('display_packages', views.display_packages)
]
