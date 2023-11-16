from django.shortcuts import render


# Create your views here.
def index(request):
    # return render(request, "index.html")
    # return render(request, "index_page_logb.html")
    return render(request, "index_log.html")
    # return render(request, "../../theme/templates/base.html")
    # return render(request, "index_old.html")
