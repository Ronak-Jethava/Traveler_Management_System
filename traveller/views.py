from django.http.response import Http404
from django.shortcuts import render
from dummy.models import User

# Create your views here.
def home(request):
    return render(request, 'traveller_home.html')

def travel_history(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user = User.objects.get(pk=user_id)
        objs = User.objects.select_related('traveller')
        return render(request, 'get_user_id.html')
    else:
        return render(request, 'get_user_id.html')