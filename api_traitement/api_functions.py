#######################################################
#
# A mon sens le fichier api_functions devrait être ainsi, 
# seules les fonctions relatives à la connexion à l'api devraient être présentes
#
#######################################################

import json
import requests

# from api_traitement.json_fonctions import *
from api_traitement.apiFunctions import pretty_print, serialize, errorFilter

from webapps.models import User
from django.contrib.auth import authenticate



########### Token ###########

def getToken(baseUrl, data):
    """
    Adelphe
    data = {
            "config.login": "username",
            "config.password": "password",
            "config.databaseName": "database",
            "referentialLocale": "FR"}
    """

    url = baseUrl + "/init/open"
    response = requests.get(url, params=data)
    print(response.url)
    token = response.json()['authenticationToken']

    return token


def is_valid(token):
    """ 
    Clem
    Fonction booléenne qui test si le token est encore valide
    Args:
        token (str): _description_
    """
    api_base = 'https://observe.ob7.ird.fr/observeweb/api/public/init/information?'
    # Constitution du lien url pour accéder à l'API et fermer la connexion
    api_url = api_base + 'authenticationToken=' + token
    response = requests.get(api_url)
    print("reponse of is valid function ", response.status_code)
    return response.status_code == 200


def reload_token(req, username, password):

    user = authenticate(req, username=username,  password=password)
    data_user = User.objects.get(username=user)

    baseUrl = data_user.url
    
    print("data_user.database",data_user.database)
    if data_user.database == 'test' :
        data_user.username = 'technicienweb'
                
    data_user_connect = {
        "config.login": data_user.username,
        "config.login": data_user.username,
        "config.password": password,
        "config.databaseName": data_user.database,
        "referentialLocale": data_user.ref_language,
    }

    return getToken(baseUrl, data_user_connect)


def get_all_referential_data(token, module, baseUrl):
    url = baseUrl + "/referential/" + module + "?authenticationToken=" + token
    ac_cap = requests.get(url)
    if ac_cap.status_code == 200:
        dicoModule = {}
        for val in json.loads(ac_cap.text)["content"]:
            vals = val.rsplit('.', 1)[1]
            dicoModule[vals] = []

            for valin in json.loads(ac_cap.text)["content"][val]:
                dicoModule[vals].append(valin)
        print("="*20, "get_all_referential_data", "="*20)
        print(dicoModule)
        return dicoModule
    else:
        return "Problème de connexion pour recuperer les données"

########### Fonctions faisant appel au le web service ###########
def getId_Data(token, url, moduleName, argment, route):
    """
    Permet de retourner un id en fonction du module et de la route envoyé
    """
    headers = {
        "Content-Type": "application/json",
        'authenticationToken': token
    }

    urls = url + route + moduleName + "?filters." + argment
    rep = requests.get(urls, headers=headers)

    # print(rep.url)

    if rep.status_code == 200:
        return json.loads(rep.text)["content"][0]["topiaId"]
    else:
        return json.loads(rep.text)["message"]


def check_trip(token, content, url_base):
    """
    Permet de verifier si la marée a inserer existe déjà dans la base de donnée
    """
    start = content["startDate"].replace("T00:00:00.000Z", "")
    end = content["endDate"].replace("T00:00:00.000Z", "")

    vessel_id = content["vessel"].replace("#", "-")

    # print(start, end, vessel_id)

    id_ = ""
    ms_ = True

    try:
        id_ = getId_Data(token, url=url_base, moduleName="Trip", route="/data/ps/common/",
                        argment="startDate=" + start + "&filters.endDate=" + end + "&filters.vessel_id=" + vessel_id)
    except:
        ms_ = False

    return id_, ms_

    
def get_one_from_ws(token, url_base, route, topiaid):
    """ Fonction qui interroge le web service (ws) pour récupérer toutes les données relatives à une route et un topiaid

    Args:
        token (str): token
        url_base: chemin d'accès à la connexion ('https://observe.ob7.ird.fr/observeweb/api/public')
        route: chemin d'accès plus précis (par ex : '/data/ll/common/Trip/')
        topiaid: topiaid avec des '-' à la place des '#'

    Returns:
        file.json: informations relatives au topiaid fourni
    """
    
    headers = {
        'authenticationToken': token, 
    }
    
    params = {
        'config.recursive' : 'true', 
    }
    
    url = url_base + route + topiaid
    
    response = requests.get(url, headers=headers, params = params, timeout=15)

    if response.status_code == 200 :
        # with open(file = "media/temporary_files/previoustrip.json", mode = "w") as outfile:
        #     outfile.write(response.text)
        return response.content
    
    else:
        return None
    
def trip_for_prog_vessel(token, url_base, route, vessel_id, programme_topiaid):
    """
    Pour un navire et un programme donnée, renvoie le topiaid du dernier trip saisi

    Args:
        token
        url_base: 'https://observe.ob7.ird.fr/observeweb/api/public'
        vessel_id: topiaid du navire (avec les '-')
        programme_topiaid: topiaid du programme choisi (avec les '-')

    Returns:
        trip topiaid
    """
    # api_base = 'https://observe.ob7.ird.fr/observeweb/api/'
    api_trip = '?authenticationToken='

    api_vessel_filter = '&filters.vessel_id='
    api_programme_filter = '&filters.logbookProgram_id='
    api_ordeer_filter = '&orders.endDate=DESC'

    api_trip_request = url_base + route + api_trip + token + api_vessel_filter + vessel_id + api_programme_filter + programme_topiaid + api_ordeer_filter
    response = requests.get(api_trip_request, timeout=15)
    return response.content


def send_trip(token, data, url_base, route):
    """ Fonction qui ajoute un trip (marée) dans la base

    Args:
        token (str): token
        data (json): json file (trip) que l'on envoie dans la base
        url_base (str): 'https://observe.ob7.ird.fr/observeweb/api/public' base de connexion à l'api
        route (str):  '/data/ps/common/Trip' ou '/data/ll/common/Trip'
    Returns:
        le json inséré dans le temporary_files 
        text message: logbook bien inséré, ou bien un json d'erreur
    """

    data_json = json.dumps(data)

    headers = {
        "Content-Type": "application/json",
        'authenticationToken': token
    }

    url = url_base + route

    print("Post")
    pretty_print(data)
    
    response = requests.post(url, data=data_json, headers=headers)

    print(response.status_code, "\n")

    if response.status_code == 200:
        # return json.loads(res.text)
        return ("Logbook inséré avec success", 1)
    else:
        with open(file = "media/temporary_files/error.json", mode = "w") as outfile:
            outfile.write(response.text)
        try:
            return (errorFilter(response.text), 2)
            # return json.loads(res.text), 2
        except KeyError:
            # Faire une fonction pour mieux traiter ce type d'erreur
            # print("Message d'erreur: ", json.loads(res.text)["exception"]["result"]["nodes"]) # A faire
            print("Message d'erreur: ", json.loads(response.text)) # A faire
            return ("L'insertion de cet logbook n'est pas possible. Désolé veuillez essayer un autre", 3)


def update_trip(token, data, url_base, topiaid):
    """
    Fonction qui met à jour un trip dans la base de données, donc supprime le trip existant pour insérer le nouveau data_json sous le même topiaid

    Args:
        token (str): token
        data (json): json file qu'on envoie dans la base
        url_base (str): 'https://observe.ob7.ird.fr/observeweb/api/public' base de connexion à l'api
        topiaid du trip que l'on veut update (l'ancienne version sera supprimée)
    Returns:
    """

    data_json = json.dumps(data, default=serialize)

    headers = {
        "Content-Type": "application/json",
        'authenticationToken': token,}

    url = url_base + '/data/ll/common/Trip/' + topiaid

    pretty_print(data)
    response = requests.put(url, data=data_json, headers=headers, timeout=15)
    
    print("Code resultat de la requete", response.status_code)
    
    if response.status_code == 200:
        return ("Logbook inséré avec success", 1)
    else:
        with open(file = "media/temporary_files/errorupdate.json", mode = "w") as outfile:
            outfile.write(response.text)
