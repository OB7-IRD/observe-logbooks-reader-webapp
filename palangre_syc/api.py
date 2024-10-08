import datetime
import json
import numpy as np
import requests
import yaml
from json import dump

# from palangre_syc.json_construction import pretty_print
# from json_construction import pretty_print
# from api_traitement.apiFunctions import errorFilter

# def is_valid(token):
#     """ Fonction qui teste si le token est encore valide
#     Args:
#         token (str): _description_
#     """
#     api_base = 'https://observe.ob7.ird.fr/observeweb/api/public/init/information?'
#     # Constitution du lien url pour accéder à l'API et fermer la connexion
#     api_url = api_base + 'authenticationToken=' + token
#     response = requests.get(api_url)
#     print("reponse of is valid function ", response.status_code)
#     return response.status_code == 200


# def get_token():
#     """ Fonction qui regarde s'il existe un token, s'il est valide, ou en créé un le cas échéant
    
#     Returns:
#         str: valid token
#     """
#     try:
#         with open('token.yml', 'r') as file :
#             data = yaml.safe_load(file)
#         token = data['token']
#     except:
#         token = None
#     if not is_valid(token):
#         print("Token not valid", token)
#         api_base = 'https://observe.ob7.ird.fr/observeweb/api/public/init/open?'
#         api_modelVersion = 'config.modelVersion=9.2.3&'
#         api_login = 'config.login=technicienweb&'
#         api_password = 'config.password=wpF3NITE&'
#         api_databaseName = 'config.databaseName=test&'
#         api_referential = 'referentialLocale=FR'
        
#         # Constitution du lien url pour accéder à l'API et donc générer un token
#         api_url = api_base + api_modelVersion + api_login + api_password + api_databaseName + api_referential
        
#         response = requests.get(api_url)
        
#         # si la réponse est un succès, on extrait que le Token
#         if response.status_code == 200:
#             data_from_api = response.json()
#             token = data_from_api['authenticationToken']
#         else:
#             token = None
        
#         data = {'token' : token}
        
#         with open('token.yml', 'w') as outfile:
#             yaml.dump(data, outfile, default_flow_style=False)        
    
#     return token

# def get_referential_ll():
#     """ Fonction qui récupère les données issues du référentiel de palangre

#     Returns:
#         json: referentiel palangre
#     """

#     api_base = 'https://observe.ob7.ird.fr/observeweb/api/public/referential/ll?'
#     api_token = 'authenticationToken=' + get_token() +'&'
#     api_infos = 'config.loadReferential=&config.recursive=&config.prettyPrint=true&config.serializeNulls=&referentialLocale='
    
#     # Constitution du lien url pour accéder à l'API et donc générer un token
#     api_url = api_base + api_token + api_infos
#     response = requests.get(api_url, timeout=15)
    
#     # si la réponse est un succès, on extrait que le Token
#     if response.status_code == 200:
#         data_ref_ll = response.json()
#         with open('data_ll.json', 'w', encoding='utf-8') as f:
#             dump(data_ref_ll, f, ensure_ascii=False, indent=4)
#     else:
#         data_ref_ll = None

#     return data_ref_ll
    
# def get_referential_common():
#     """ fonction qui récupères les données issues du référentiel commun
    
#     Returns:
#         json: referentiel commun 
#     """
#     api_base = 'https://observe.ob7.ird.fr/observeweb/api/public/referential/common?'
#     api_Token = 'authenticationToken=' + get_token() +'&'
#     api_infos = 'config.loadReferential=&config.recursive=&config.prettyPrint=true&config.serializeNulls=&referentialLocale='
        
#     # Constitution du lien url pour accéder à l'API et donc générer un token
#     api_url = api_base + api_Token + api_infos
#     response = requests.get(api_url, timeout=15)
        
#     # si la réponse est un succès, on extrait que le Token
#     if response.status_code == 200:
#         data_ref_common = response.json()
#         with open('data_common.json', 'w', encoding='utf-8') as f:
#             dump(data_ref_common, f, ensure_ascii=False, indent=4)
#     else:
#         data_ref_common = None
    
#     return data_ref_common
    

# def close(token):
#     """
#     Fonction qui fmer un token
#     """
#     api_base = 'https://observe.ob7.ird.fr/observeweb/api/public/init/close?'
    
#     # Constitution du lien url pour accéder à l'API et fermer la connexion
#     api_url = api_base + 'authenticationToken=' + token
#     response = requests.get(api_url, timeout=15)
#     print("reponse of close function ", response.status_code)
#     return response.status_code
        
        
def serialize(obj): 
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    if isinstance(obj, np.int64):
        return int(obj)
    return str(obj)
    # raise TypeError("Type not serializable")
    
# def get_one(token, url_base, route, topiaid):
#     """ Fonction qui interroge la base de données pour récupérer toutes les données relatives à un topiaid et une route 

#     Args:
#         token (str): token
#         url_base: chemin d'accès à la connexion ('https://observe.ob7.ird.fr/observeweb/api/public')
#         route: chemin d'accès plus précis (par ex : '/data/ll/common/Trip/')
#         topiaid: topiaid avec des '-' à la place des '#'

#     Returns:
#         file.json: informations relatives au topiaid fourni
#     """
    
#     headers = {
#         'authenticationToken': token, 
#     }
    
#     params = {
#         'config.recursive' : 'true', 
#     }
    
#     url = url_base + route + topiaid
    
#     response = requests.get(url, headers=headers, params = params, timeout=15)
#     # response.raise_for_status()  # Lève une exception en cas d'erreur HTTP

#     if response.status_code == 200 :
#         with open(file = "media/temporary_files/previoustrip.json", mode = "w") as outfile:
#             outfile.write(response.text)
#         return response.content
    
#     else:
#         return None
    
# def get_trip(token, url_base, topiaid):
    
#     headers = {
#         'authenticationToken': token, 
#     }
    
#     params = {
#         'config.recursive' : 'true', 
#     }
    
#     url = url_base + '/data/ll/common/Trip/' + topiaid
    
#     response = requests.get(url, headers=headers, params = params, timeout=15)
#     # response.raise_for_status()  # Lève une exception en cas d'erreur HTTP

#     if response.status_code == 200 :
#         # print("response status == 200 so tempfile created")
#         # with open(file = "previoustrip.json", mode = "w") as outfile:
#         #     outfile.write(response.text)
#         return response.content
    
#     else:
#         return None
    

def update_trip(token, data, url_base, topiaid):
    """Fonction qui met à jour un trip dans la base de données, donc supprime le trip existant pour insérer le nouveau data_json sous le même topiaid

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
        'authenticationToken': token, 
    }

    url = url_base + '/data/ll/common/Trip/' + topiaid

    print("PUT for updating the data")
    # pretty_print(data)
    response = requests.put(url, data=data_json, headers=headers, timeout=15)
    
    print("Code resultat de la requete", response.status_code)
    print("url envoyé : ", url)

    if response.status_code == 200:
        return ("Logbook inséré avec success", 1)
    else:
        with open(file = "media/temporary_files/errorupdate.json", mode = "w") as outfile:
            outfile.write(response.text)


# def send_trip(token, data, url_base):
#     """_summary_

#     Args:
#         token (str): token valide
#         data (json): json file
#         url_base (str): 'https://observe.ob7.ird.fr/observeweb/api/public' base de connexion à l'api

#     Returns:
#         text message: logbook bien inséré, ou bien un json d'erreur
#     """

#     data_json = json.dumps(data, default=serialize)

#     headers = {
#         "Content-Type": "application/json",
#         'authenticationToken': token
#     }

#     url = url_base + '/data/ll/common/Trip'

#     print("Post")
#     # pretty_print(data)
#     res = requests.post(url, data=data_json, headers=headers, timeout=30)

#     print("Code resultat de la requete", res.status_code)
#     print("url envoyé : ", url)

#     if res.status_code == 200:
#         return ("Logbook inséré avec success", 1)
#     else:
#         with open(file = "media/temporary_files/error.json", mode = "w") as outfile:
#             outfile.write(res.text)


def trip_for_prog_vessel(token, url_base, vessel_id, programme_topiaid):
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
    api_trip = '/data/ll/common/Trip?authenticationToken='

    api_vessel_filter = '&filters.vessel_id='
    api_programme_filter = '&filters.logbookProgram_id='
    api_ordeer_filter = '&orders.endDate=DESC'

    api_trip_request = url_base + api_trip + token + api_vessel_filter + vessel_id + api_programme_filter + programme_topiaid + api_ordeer_filter
    response = requests.get(api_trip_request, timeout=15)
    return response.content

# def table_trip(token, url_base, vessel_id, programme_topiaid):
#     """
#     Pour un navire et un programme donnée, renvoie le topiaid du dernier trip saisi

#     Args:
#         token
#         url_base: 'https://observe.ob7.ird.fr/observeweb/api/public'
#         vessel_id: topiaid du navire (avec les '-')
#         programme_topiaid: topiaid du programme choisi (avec les '-')

#     Returns:
#         trip topiaid
#     """
#     # api_base = 'https://observe.ob7.ird.fr/observeweb/api/'
#     api_trip = '/data/ll/common/Trip?authenticationToken='

#     api_vessel_filter = '&filters.vessel_id='
#     api_programme_filter = '&filters.logbookProgram_id='
#     api_ordeer_filter = '&orders.endDate=DESC'

#     api_trip_request = url_base + api_trip + token + api_vessel_filter + vessel_id + api_programme_filter + programme_topiaid + api_ordeer_filter
#     response = requests.get(api_trip_request, timeout=15)
#     return response.content


# def load_json_file(file_path):
#     try:
#         with open(file_path, 'r') as file:
#             # a voir s'il faut ajouter '.decode('utf8')'    
#             data = json.load(file)
#             return data
#     except FileNotFoundError:
#         print(f"File '{file_path}' not found.")
#         return None
#     except json.JSONDecodeError as e:
#         print(f"Error decoding JSON file '{file_path}': {e}")
#         return None
    
