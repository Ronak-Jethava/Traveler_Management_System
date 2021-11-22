from django.shortcuts import render
from .models import Activities, User
import datetime

# Create your views here.

def home(requeust):
    reg_users = User.objects.all().exclude(signup_since__gte=datetime.date(2020, 12, 31)).filter(signup_since__gte=datetime.date(2019, 1, 1))
    return render(requeust, 'home.html', {'reg_users':reg_users.count})

