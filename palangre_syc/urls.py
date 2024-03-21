from django.urls import path

from . import views
from palangre_syc.views import checking_logbook, listing_files, send_logbook2Observe, presenting_previous_trip

urlpatterns = [
    path("", listing_files, name="listing files"),
    path("presenting_previous_trip", presenting_previous_trip, name = "presenting previous trip"),
    path("checking_logbook", checking_logbook, name="checking logbook"),
    path("send_logbook2bserve", send_logbook2observe, name="send logbook2Observe"),
]
