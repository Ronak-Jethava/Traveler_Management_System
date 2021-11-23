from django.contrib import admin
from django.urls import path
from traveller import views

urlpatterns = [
    path('', views.home),
    path('travel_history', views.travel_history),
    path('upcoming_tours', views.upcoming_tours),
]
