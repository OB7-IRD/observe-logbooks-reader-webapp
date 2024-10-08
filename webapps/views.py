from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from api_traitement import api_functions
from api_traitement.apiFunctions import *
from api_traitement.api_functions import *
# from palangre_syc import api
from .form import UserForm
from django.contrib import messages
from .models import User
import json
from zipfile import ZipFile
import os
from django.utils.translation import gettext as _

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

# def reloadToken(req, username, password):

#     user = authenticate(req, username=username,  password=password)
#     data_user = User.objects.get(username=user)

#     base_url = data_user.url
    
#     print(data_user.database)
#     if data_user.database == 'test' :
#         data_user.username = 'technicienweb'
                
#     data_user_connect = {
#         "config.login": data_user.username,
#         "config.login": data_user.username,
#         "config.password": password,
#         "config.databaseName": data_user.database,
#         "referentialLocale": data_user.ref_language,
#     }

#     return getToken(base_url, data_user_connect)

def search_in(request, allData, search="Ocean"):
    """Fonction permet d'avoir à partir des données de references les oceans ou les programmes

    Args:
        allData (json): données de references
        search (str): "Ocean" ou "Program"

    Returns:
        prog_dic (json)
    """
    if allData == []: return {}

    if request.session.get('language') == 'fr':
        if search == "Ocean":
            return { val["topiaId"] : val["label2"] for val in allData[search]}
        prog_dic = {}
        if allData == [] :
            return prog_dic

        for val in allData[search]:
            prog_dic[val["topiaId"]] = val["label2"]
        return prog_dic

    elif request.session.get('language') == 'en':
        if search == "Ocean":
            return { val["topiaId"] : val["label1"] for val in allData[search]}
        prog_dic = {}
        if allData == [] :
            return prog_dic

        for val in allData[search]:
            prog_dic[val["topiaId"]] = val["label1"]
        return prog_dic


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
            print(user)
            data_user = User.objects.get(username=user)
            print("_"*20, "user is not None and user.is_active", "_"*20)
                        
            if basename == data_user.basename.lower():
                token = ""
                allData = []
                base_url = data_user.url
                
                
                if basename == 'test-proto.ird.fr' :
                    data_user.username = 'technicienweb'
                    request.session['username'] = data_user.username
                
                print("_"*20, "base_url", "_"*20)
                
                data_user_connect = {
                    "config.login": data_user.username,
                    "config.password": password,
                    "config.databaseName": data_user.database,
                    "referentialLocale": data_user.ref_language,
                }


                try:
                    # token = "ok"
                    token = api_functions.get_token(base_url, data_user_connect)
                    print("Token: ", token)
                    print('baseURL: ', base_url)
                    allData = load_data(token=token, base_url=base_url)
                    # if allData == []:
                    #     print("="*20, "if allData == []", "="*20)

                except:
                    pass
            
                if (token != "") and (allData != []):
                    login(request, user)
                    request.session['token'] = token
                    request.session['base_url'] = base_url
                    
                    print("="*20, "if (token != "") and (allData is not [])", "="*20)
                    # print("clés présentes dans allDAta ", allData.keys())
                    datat_0c_Pr = {
                        # "ocean": search_in(request, allData),
                        "ocean": None,
                        # "senne" : allData['seine'], "palangre" : allData['longline']
                        "program" : allData["Program"]
                    }
                    request.session['data_Oc_Pr'] = datat_0c_Pr
                    request.session['table_files'] = []
                    # allData = load_data(token, base_url)
                    # print("DATA n n n : ", allData)
                    return redirect("home")
                else:
                    message = _("Impossible de se connecter au serveur verifier la connexion")
            else:
                message = _("serveur incorrect")
        else:
            message = _("username ou mot de passe incorrect")

    return render(request, "login.html", {"message": message})


@login_required
def update_data(request):
    username = request.session.get('username')
    password = request.session.get('password')
    token  = api_functions.reload_token(request, username, password)
    base_url = request.session.get('base_url')

    allData = load_data(token=token, base_url=base_url, forceUpdate=True)
    
    print("="*20, "update_data", "="*20)
    with open('allData.json', 'w', encoding='utf-8') as f:
        json.dump(allData, f, ensure_ascii=False, indent=4)
    
    datat_0c_Pr = {
        "ocean": search_in(request, allData),
        # "domains": {'senne' : allData['seine'], "palangre" : allData['longline']}
        "program": allData['Program']
    }
    request.session['data_Oc_Pr'] = datat_0c_Pr

    return redirect("home")


def deconnexion(request):
    logout(request)
    request.session['token'] = None
    request.session['username'] = None
    request.session['password'] = None
    request.session['context'] = None

    return redirect("login")


@login_required
def home(request):
    request.session['language'] = request.LANGUAGE_CODE
    return render(request, "home.html")


@login_required
def logbook(request):
    datat_0c_Pr = request.session.get('data_Oc_Pr')
    ll_context = request.session.get('context')

    try:
        file_name = "media/data/" + os.listdir('media/data')[0]
        # Opening JSON file
        f = open(file_name, encoding="utf8")
        # returns JSON object as  a dictionary
        allData = json.load(f)

        datat_0c_Pr.update({"ocean": search_in(request, allData)})
        request.session['data_Oc_Pr'] = datat_0c_Pr
        datat_0c_Pr = request.session.get('data_Oc_Pr')
    except:
        pass

    print(datat_0c_Pr['program'].keys())
    print("+"*20, "logbook datat_Oc_Pr", "+"*20) 
    # print(datat_0c_Pr)
    # print(datat_0c_Pr.keys())

    apply_conf  = request.session.get('dico_config')

    # if request.headers.get('x-requested-with') == 'XMLHttpRequest':

    if request.POST.get('submit'):
        
        message = tags = ''
        logbooks = os.listdir("media/logbooks")

        #Si validé sans fichier excel televersé
        if logbooks == []:
            print("="*10, "Validé sans fichier excel", "="*10)
            msg = _("Merci de déposer un fichier excel avant de lancer l'extraction de données !")
            messages.error(request, msg)
            tags = "error2"

            return render(request, "logbook.html",{
                "tags": tags,
                "alert_message": _("Merci de téléverser un fichier excel"),
                "ocean_data": datat_0c_Pr["ocean"],
                "ll_context" : ll_context
            })
        print(apply_conf)
        # Si le fichier pour les palangre, alors on renvoit vers 'palagre_syc'
        if apply_conf["domaine"] == "palangre":
            logbooks = os.listdir("media/logbooks")
            # print("="*20, "logbook kwargs", "="*20)
            # print(logbooks)
            # print(apply_conf)

            url = reverse('presenting previous trip')
            url = f"{url}?selected_file={logbooks}"          
            return redirect(url) 

        # sinon on a un fichier senne
        if 0 < len(logbooks) <= 1:
            if apply_conf["ty_doc"] == "ps":
                info_Navir, data_logbook, data_observateur, message = read_data("media/logbooks/"+ logbooks[0], type_doc="v21")
            if apply_conf["ty_doc"] == "ps2":
                info_Navir, data_logbook, message = read_data("media/logbooks/"+ logbooks[0], type_doc="v23")

            # Suprimer le ou les fichiers data logbooks
            os.remove("media/logbooks/"+ logbooks[0])
            # print(data_observateur)

        if message == '' and len(logbooks) > 0:
             print("len log ", len(logbooks), " messa : ", message)
             try:
                 file_name = "media/data/" + os.listdir('media/data')[0]
                 # Opening JSON file
                 f = open(file_name, encoding="utf8")
                 # returns JSON object as  a dictionary
                 allData = json.load(f)

                 if apply_conf["ty_doc"] == "ps":
                    allMessages, content_json = build_trip(allData=allData, info_bat=info_Navir, data_log=data_logbook, oce=apply_conf['ocean'], prg=apply_conf['programme'], ob=data_observateur)
                 if apply_conf["ty_doc"] == "ps2":
                    allMessages, content_json = build_trip_v23(allData=allData, info_bat=info_Navir, data_log=data_logbook, oce=apply_conf['ocean'], prg=apply_conf['programme'])

                 if os.path.exists("media/temporary_files/content_json.json"):
                     os.remove("media/temporary_files/content_json.json")
                     # creer le nouveau 
                     file_name = "media/temporary_files/content_json.json"

                     with open(file_name, 'w', encoding='utf-8') as f:
                         f.write(json.dumps(content_json, ensure_ascii=False, indent=4))
                 else:
                     # creer le nouveau content
                     file_name = "media/temporary_files/content_json.json"

                     with open(file_name, 'w', encoding='utf-8') as f:
                         f.write(json.dumps(content_json, ensure_ascii=False, indent=4))

                 if allMessages == []:
                     messages.info(request, _("Extration des données avec succès vous pouvez les soumettre maintenant."))
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
                 messages.error(request, _("Veuillez recharger la page et reprendre votre opération SVP."))
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
            "ll_context" : ll_context
        })

    # else : 
    if apply_conf is not None :
        print("="*20, "apply_conf is not None", "="*20)

        # print(apply_conf)
        # print(datat_0c_Pr['program'])

        if apply_conf['domaine'] == 'palangre' :
            return render(request, "logbook.html", context={
                "program_data": datat_0c_Pr['program']['longline'],
                "ocean_data": datat_0c_Pr["ocean"],
                "ll_context" : ll_context
            })
        elif apply_conf['domaine'] == 'senne' : 
            return render(request, "logbook.html", context={
                "program_data": datat_0c_Pr['program']['seine'],
                "ocean_data": datat_0c_Pr["ocean"],
                "ll_context" : ll_context
            })
    # print("="*20, "apply_conf is None", "="*20)
    # print(apply_conf)
    return render(request, "logbook.html", context={
                # "program_data": ll_programs,
                "program_data": datat_0c_Pr["program"],
                "ocean_data": datat_0c_Pr["ocean"],
                "ll_context" : ll_context
            })

@login_required
def getProgram(request, domaine):
    """_summary_

    Args:
        request (_type_): _description_
        domaine (_type_): _description_

    Returns:
        _type_: _description_
    """
    datat_0c_Pr = request.session.get('data_Oc_Pr')
    print('views.py getProgram domaine when domaine not selected : ', domaine)
    print(datat_0c_Pr.keys())

    # if datat_0c_Pr is not None:
    if domaine == "senne" or domaine == "palangre": 
        if domaine == "senne" :
            looking_for = "seine"
        elif domaine == "palangre":
            looking_for = "longline"

        data_0c_Pr = search_in(request, datat_0c_Pr['program'], looking_for)
        print("="*20, "datat_0c_Pr search in", "="*20)
        
        # print(datat_0c_Pr)
        dataPro = {
            "id":[],
            "value":[]
        }
        for key, value in data_0c_Pr.items():
            dataPro["id"].append(key)
            dataPro["value"].append(value)
            
        # print(dataPro)
        return JsonResponse({"dataPro": dataPro})
    else:
        return JsonResponse({})

# @login_required
def postProg_info(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        request.session['dico_config'] = {
            # 'langue': request.POST["langue"],
            'domaine': request.POST["domaine"],
            'ocean': request.POST["ocean"],
            'programme': request.POST["programme"],
            'ty_doc': request.POST["ty_doc"]
        }
        return JsonResponse({"message": "success", 
                            "domaine": request.session.get('dico_config')['domaine']})
    return JsonResponse({"message": _("Veuillez ressayer svp.")})

def logbook_del_files(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if not os.path.exists("media/logbooks"):
            os.makedirs("media/logbooks")

        logbooks_files = os.listdir("media/logbooks")

        if len(logbooks_files) > 0:
            for file in logbooks_files:
                os.remove("media/logbooks/"+ file)

            print("Suppression des logbook trouvés")
        else:
            print("Aucun logbook trouvé dans le cache")
    return JsonResponse({})

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
    token  = api_functions.reload_token(request, username, password)
    base_url = request.session.get('base_url')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        file_name = "media/temporary_files/content_json.json"
        # Opening JSON file
        f = open(file_name, encoding="utf8")
        # returns JSON object as  a dictionary
        content_json = json.load(f)
        route = '/data/ps/common/Trip'
        message, code = api_functions.send_trip(token, content_json, base_url, route)

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
    return JsonResponse({"message": _("Veuillez ressayer svp.")})

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
            print("A"*20)
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