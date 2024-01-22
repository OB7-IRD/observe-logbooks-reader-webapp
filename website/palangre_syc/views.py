from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    #return HttpResponse("Hello, Cette page est la home page de la partie palangre")
    return render(request, "LL_homepage.html")