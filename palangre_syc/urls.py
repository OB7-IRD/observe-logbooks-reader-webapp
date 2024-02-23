from django.urls import path

from . import views
from palangre_syc.views import checking_logbook, listing_files

urlpatterns = [
    path("", listing_files, name="listing files"),
    path("checking_logbook", checking_logbook, name="checking logbook"),
]