from django.shortcuts import render

# Create your views here.
def home(requeust):
    return render(requeust, 'home.html')

