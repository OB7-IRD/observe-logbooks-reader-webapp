from django.urls import path

from . import views
from palangre_syc.views import index

urlpatterns = [
    path("", index, name="index"),
]