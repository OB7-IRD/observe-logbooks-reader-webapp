from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from api_traitement.apiFunctions import *
from .form import UserForm
from django.contrib import messages
from .models import User
import json
from zipfile import ZipFile
import os

# Create your views here.
def register(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            #messages.success(request, " Vous etes enregistrer")
            return redirect("login")
        else:
            messages.error(request, form.errors)
    return render(request, "register.html", {"form": form})

def relordToken(req, username, password):

    user = authenticate(req, username=username,  password=password)
    data_user = User.objects.get(username=user)

    baseUrl = data_user.url
    
    print(data_user.database)
    if data_user.database == 'test' :
        data_user.username = 'technicienweb'
                
    data_user_connect = {
        "config.login": data_user.username,
        "config.password": password,
        "config.databaseName": data_user.database,
        "referentialLocale": data_user.ref_language,
    }

    return getToken(baseUrl, data_user_connect)

def auth_login(request):
    message = ""
    if request.method == "POST":
        basename = request.POST['base']
        username = request.POST['username']
        password = request.POST['password']

        request.session['username'] = username
        request.session['password'] = password
        
        user = authenticate(request, username=username,  password=password)

        print("="*20, "auth_login", "="*20)        

        if user is not None and user.is_active:
            data_user = User.objects.get(username=user)
            print("_"*20, "user is not None and user.is_active", "_"*20)
                        
            if basename == data_user.basename.lower():
                token = ""
                allData = []
                baseUrl = data_user.url
                
                
                if basename == 'test-proto.ird.fr' :
                    data_user.username = 'technicienweb'
                    print(user , data_user)
                
                print("_"*20, "baseUrl", "_"*20)
                
                data_user_connect = {
                    "config.login": data_user.username,
                    "config.password": password,
                    "config.databaseName": data_user.database,
                    "referentialLocale": data_user.ref_language,
                }


                try:
                    # token = "ok"
                    token = getToken(baseUrl, data_user_connect)
                    print("Token: ", token)
                    print('baseURL: ', baseUrl)
                    allData = load_data(token=token, baseUrl=baseUrl)
                    # if allData == []:
                    #     print("="*20, "if allData == []", "="*20)

                except:
                    pass
            
                
                if (token != "") and (allData != []):
                    login(request, user)
                    request.session['token'] = token
                    request.session['baseUrl'] = baseUrl
                    
                    print("="*20, "if (token != "") and (allData is not [])", "="*20)
                    
                    datat_0c_Pr = {
                        "ocean": search_in(allData),
                        "senne" : allData['seine'], "palangre" : allData['longline']
                    }
                    request.session['data_Oc_Pr'] = datat_0c_Pr
                    request.session['table_files'] = []
                    # allData = load_data(token, baseUrl)
                    # print("DATA n n n : ", allData)
                    return redirect("home")
                else:
                    message = "Impossible de se connecter au serveur verifier la connexion"
            else:
                message = "serveur incorrect"
        else:
            message = "username ou mot de passe incorrect"

    return render(request, "login.html", {"message": message})


@login_required
def update_data(request):
    username = request.session.get('username')
    password = request.session.get('password')
    token  = relordToken(request, username, password)
    baseUrl = request.session.get('baseUrl')

    allData = load_data(token=token, baseUrl=baseUrl, forceUpdate=True)
    print("="*20, "update_data", "="*20)
    datat_0c_Pr = {
        "ocean": search_in(allData),
        "domains": {'senne' : allData['seine'], "palangre" : allData['longline']}
    }
    request.session['data_Oc_Pr'] = datat_0c_Pr

    return redirect("home")


def deconnexion(request):
    logout(request)
    request.session['token'] = None
    request.session['username'] = None
    request.session['password'] = None

    return redirect("login")


# @login_required
def home(request):
    return render(request, "home.html")


@login_required
def logbook(request):
    datat_0c_Pr = request.session.get('data_Oc_Pr')
    print("+"*20, "logbook datat_Oc_Pr", "+"*20) 
    # print(datat_0c_Pr)
    
    ll_programs = search_in(datat_0c_Pr["palangre"], search="Program")
    apply_conf  = request.session.get('dico_config')

    # if request.headers.get('x-requested-with') == 'XMLHttpRequest':

    if request.POST.get('submit'):
        
        message = tags = ''
        logbooks = os.listdir("media/logbooks")
        
        # Si le fichier pour les palangre, alors on renvoit vers 'palagre_syc'
        if apply_conf["domaine"] == "palangre":
            logbooks = os.listdir("media/logbooks")
            # print("="*20, "logbook kwargs", "="*20)
            # print(logbooks)
            # print(apply_conf)

            url = reverse('checking logbook')
            url = f"{url}?selected_file={logbooks}"          
            return redirect(url) 
                         
                         

        # sinon on a un fichier senne
        if 0 < len(logbooks) <= 1:
            info_Navir, data_logbook, data_observateur, message = read_data("media/logbooks/"+ logbooks[0])

            # Suprimer le ou les fichiers data logbooks
            os.remove("media/logbooks/"+ logbooks[0])

        if message == '' and len(logbooks) > 0:
            print("len log ", len(logbooks), " messa : ", message)
            try:
                file_name = "media/data/" + os.listdir('media/data')[0]
                # Opening JSON file
                f = open(file_name, encoding="utf8")
                # returns JSON object as  a dictionary
                allData = json.load(f)

                allMessages, content_json = build_trip(allData=allData, info_bat=info_Navir, data_log=data_logbook, oce=apply_conf['ocean'], prg=apply_conf['programme'], ob=data_observateur)

                # print(content_json,'\n')

                if os.path.exists("media/content_json/content_json.json"):
                    os.remove("media/content_json/content_json.json")
                    # creer le nouveau content
                    file_name = "media/content_json/content_json.json"

                    with open(file_name, 'w', encoding='utf-8') as f:
                        f.write(json.dumps(content_json, ensure_ascii=False, indent=4))
                else:
                    # creer le nouveau content
                    file_name = "media/content_json/content_json.json"

                    with open(file_name, 'w', encoding='utf-8') as f:
                        f.write(json.dumps(content_json, ensure_ascii=False, indent=4))

                if allMessages == []:
                    messages.info(request, "Extration des données avec succès vous pouvez les soumettre maintenant.")
                else:
                    for msg in allMessages:
                        messages.error(request, msg)
                        tags = "error"

                    # Mettre les messages d'erreurs dans un fichier log
                    file_log_name = "media/log/log.txt"

                    with open(file_log_name, 'w', encoding='utf-8') as f_log:
                        log_mess = "\r\r".join(allMessages)
                        f_log.write(log_mess)
            except UnboundLocalError:
                messages.error(request, "Veuillez recharger la page et reprendre votre opération SVP.")
                tags = "error2"

                logbooks = os.listdir("media/logbooks")

                for logbook in logbooks:
                    os.remove("media/logbooks/"+ logbook)


        else:
            messages.error(request, message)
            tags = "error"

        return render(request, "logbook.html",{
            "tags": tags,
            "ocean_data": datat_0c_Pr["ocean"],
        })

    # else : 
    if apply_conf is not None :
        print("="*20, "apply_conf is not None", "="*20)
        print(apply_conf)
        if apply_conf['domaine'] == 'palangre' :
            return render(request, "logbook.html", context={
                "program_data": datat_0c_Pr['palangre']['Program'],
                "ocean_data": datat_0c_Pr["ocean"]
            })
        elif apply_conf['domaine'] == 'senne' : 
            return render(request, "logbook.html", context={
                "program_data": datat_0c_Pr['senne']['Program'],
                "ocean_data": datat_0c_Pr["ocean"]
            })
    # print("="*20, "apply_conf is None", "="*20)
    # print(apply_conf)
    return render(request, "logbook.html", context={
                "program_data": ll_programs,
                "ocean_data": datat_0c_Pr["ocean"]
            })

@login_required
def getProgram(request, domaine):
    datat_0c_Pr = request.session.get('data_Oc_Pr')
    
    if datat_0c_Pr != None:

        datat_0c_Pr = search_in(datat_0c_Pr[domaine], "Program")
        print("="*20, "datat_0c_Pr search in", "="*20)
        # print(datat_0c_Pr)
        dataPro = {
            "id":[],
            "value":[]
        }
        for key, value in datat_0c_Pr.items():
            # print(key, value)
            dataPro["id"].append(key)
            dataPro["value"].append(value)
            print("="*20, "dataPro", "="*20)
            # print(datat_0c_Pr)
        # print(dataPro)
        return JsonResponse({"dataPro": dataPro})
    else:
        return JsonResponse({})

# @login_required
def postProg_info(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        request.session['dico_config'] = {
            'langue': request.POST["langue"],
            'domaine': request.POST["domaine"],
            'ocean': request.POST["ocean"],
            'programme': request.POST["programme"],
            'ty_doc': request.POST["ty_doc"]
        }
        # print(request.session.get('dico_config'))
        return JsonResponse({"message": "success", 
                             "domaine": request.session.get('dico_config')['domaine']})
    return JsonResponse({"message": "Veuillez ressayer svp."})

@login_required
def domaineSelect(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        logbooks = os.listdir("media/logbooks")

        for logbook in logbooks:
            os.remove("media/logbooks/"+ logbook)

        return JsonResponse({"domaine": request.session.get('dico_config')['domaine']})

@login_required
def sendData(request):
    username = request.session.get('username')
    password = request.session.get('password')
    token  = relordToken(request, username, password)
    baseUrl = request.session.get('baseUrl')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        file_name = "media/content_json/content_json.json"
        # Opening JSON file
        f = open(file_name, encoding="utf8")
        # returns JSON object as  a dictionary
        content_json = json.load(f)

        message, code = add_trip(token, content_json, baseUrl)

        if code == 1:
            messages.success(request, message)
            print(1, message)
        elif code == 2:
            for msg in message:
                messages.error(request, msg)
            print(2, message)
        else:
            messages.warning(request, message)
            print(3, message)

        return JsonResponse({"message": "Success", "code": code, "msg": message})
    return JsonResponse({"message": "Veuillez ressayer svp."})

def extract_data(my_file):
    with ZipFile(my_file, 'r') as zip:
        # afficher tout le contenu du fichier zip
        zip.printdir()
        print('extraction...')
        # extraire tous les fichiers
        # zip.extractall()
        # extraire tous les fichiers vers un autre répertoire
        zip.extractall("zipfiles")
        print('Terminé!')

    # Extraire un seul fichier zip
    # zip = ZipFile(my_file)
    # zip.extract('*.xlsx', "../media/zipfiles")
    # zip.extract('*.xlsm', "../media/zipfiles")
    # zip.close()
    #request.SESSION['files'] = files


files = []
def file_upload_view2(request):
    m_file = []
    if files is not []:
         files.clear()
    #print(request.FILES)

    if request.method == "POST":
        my_file = request.FILES.get('file')

        # files.append(my_file)
        #print(my_file)
        m_file = my_file
        a = str(my_file)

        read_data(my_file)

    # print(my_file, " => ", a.split(".")[1])

        if a.split(".")[1] == "zip":
            extract_data(my_file)
            dat = os.listdir("media/zipfiles")
            res = "zipfiles"+ "/" + str(dat[0])
            dat = os.listdir(res)
            m_file = dat
            # supprimer le contenu
            # shutil.rmtree("../media/zipfiles/")
            print(m_file)
        else:
            print("AAAAAAAAAAAAAAAAAAAAAAA")
    return render(request, "logbook.html",{"files": m_file})


def file_upload_view(request):

    if request.method == "POST":

        file = request.FILES['file']
        fs = FileSystemStorage()

        if (file.name not in os.listdir("media/logbooks")):
            #To copy data to the base folder
            filename = fs.save("logbooks/"+file.name, file)
            uploaded_file_url = fs.url(filename)                 #To get the file`s url

            print(uploaded_file_url)

        # print("Contenu", request.session['table_files'])
    return render(request, "logbook.html")


def get_data_extract(request):

    #_, data, _, messages = read_data(request.FILES.get('file'))

    # request.session.get('table_files').append(data.to_dict())
    # request.session['table_files'] = request.session.get('table_files')

    # dat = os.listdir("../media/zipfiles")

    if request.POST.get('submit'):

        messages = ''

        logbooks = os.listdir("media/logbooks")

        print(logbooks)

        # _, data, _, messages = read_data(request.FILES.get('file'))

        # m_file = request.session.get('table_files')
        # print("Submit: ", len(m_file))

        # request.session['table_files'] = []

        return render(request, "logbook.html",{"files": messages })
#"""
#    if request.method == "POST":
#
#        print("Appliquer: ", request.POST)
#        return render(request, "logbook.html",{"files": "appliquer"})
#
#"""


def error_404_view(request, exception):
    return render(request, "404.html")