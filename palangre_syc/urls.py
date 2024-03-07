from django.urls import path

from palangre_syc.views import checking_logbook, send_logbook2Observe, presenting_previous_trip

urlpatterns = [
    # path("", listing_files, name="listing files"),
    path("presenting_previous_trip", presenting_previous_trip, name = "presenting previous trip"),
    path("checking_logbook", checking_logbook, name="checking logbook"),
    path("send_logbook2Observe", send_logbook2Observe, name="send logbook2Observe"),
    # path("../logbook", return_to_logbook),
]
