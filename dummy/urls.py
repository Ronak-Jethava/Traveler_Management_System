from django.contrib import admin
from django.urls import path
from dummy import views as dummy_views

import dummy

urlpatterns = [
    path('', dummy_views.home),
]
