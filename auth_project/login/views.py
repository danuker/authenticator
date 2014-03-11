from django.shortcuts import render
from django.template.loader import get_template

# Create your views here.
def home(request):
    return render(request, 'home.html')