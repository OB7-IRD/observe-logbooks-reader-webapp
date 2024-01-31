"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from blog.views import index
from webapps.views import auth_login, deconnexion, home, logbook, register, file_upload_view, update_data, getProgram, postProg_info, domaineSelect, sendData

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', auth_login, name="login"),
    # path('register', register, name="register"),
    path('logout', deconnexion, name="logout"),
    path('', home, name="home"),
    path('logbook', logbook, name="logbook"),
    path('upload', file_upload_view, name="upload_view"),
    path('update', update_data, name="update"),
    path('<str:domaine>', getProgram, name="getProgram"),
    path('logbook/apply', postProg_info, name="postProg_info"),
    path('logbook/domainselect', domaineSelect, name="domaineSelect"),
    path('logbook/sendData', sendData, name="sendData"),
    
    # j'importe l'ensemble des urls qui seront déclinées dans mon app palangre syc
    path("palangre_syc/", include("palangre_syc.urls")),
]

handler404 = 'website.views.error_page.error_404_view'