from django.shortcuts import render
import requests

from django.http import HttpResponse

def index(request):
    
    
    return render(request, "LL_homepage.html")



