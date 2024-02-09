import datetime
import json
import numpy as np
import requests
from json_construction import pretty_print
# from api_traitement.apiFunctions import errorFilter

def close(token):
    api_base = 'https://observe.ob7.ird.fr/observeweb/api/public/init/close?'
    # api_modelVersion = 'config.modelVersion=9.2.1&'
    # api_login = 'config.login=technicienweb&'
    # api_password = 'config.password=wpF3NITE&'
    # api_databaseName = 'config.databaseName=test&'
    # api_referential = 'referentialLocale=FR'
    
    # Constitution du lien url pour accéder à l'API et fermer la connexion
    api_url = api_base + token
    response = requests.get(api_url)
    
    return response.status_code
        
def serialize(obj): 
    if isinstance(obj, datetime.datetime): 
        return obj.isoformat() 
    if isinstance(obj, np.int64):
        return int(obj)
    raise TypeError("Type not serializable") 

def send_trip(token, data, url_base):
    """_summary_

    Args:
        token (_type_): _description_
        data (_type_): _description_
        url_base (_type_): _description_

    Returns:
        _type_: _description_
    """

    # dict = content
    data_json = json.dumps(data, default=serialize)

    headers = {
        "Content-Type": "application/json",
        'authenticationToken': token
    }

    url = url_base + '/data/ll/common/Trip'

    print("Post")
    pretty_print(data)
    res = requests.post(url, data=data_json, headers=headers)

    print("Code resultat de la requete", res.status_code)

    if res.status_code == 200:
        # return json.loads(res.text)
        return ("Logbook inséré avec success", 1)
    else:
        with open(file = "error.json", mode = "w") as outfile:
            outfile.write(res.text)
        # pretty_print(res.text, file = "error.json", mode = "w")

def errorFilter(response):
    """
    Permet de simplifier l'afficharge des erreurs dans le programme lors de l'insertion des données
    """
    error = json.loads(response)
    # print(error)
    lati_long_date_ref = []
    msg = []
    comp = 0
    comp2 = 0
    for val in error['exception']['result']['data']:
        for i in range(len(val['messages'])):

            if (val['messages'][i]['fieldName'] == 'latitude') or (val['messages'][i]['fieldName'] == 'longitude') or (
                    val['messages'][i]['fieldName'] == 'quadrant'):
                temp = ""
                try:
                    temp = val['reference']['content']['date'].replace("T00:00:00.000Z", ""), \
                        val['reference']['content']['time'].replace(":00.000Z", "").replace('1970-01-01T', '')

                except:
                    temp2 = " *** champs erreur: " + str(
                        val['messages'][i]['fieldName']) + " \n ****** Message Erreur: " + str(
                        val['messages'][i]['message'])
                    if temp2 not in msg:
                        comp += 1
                        msg.append(temp2)

                if temp != "":
                    if temp not in lati_long_date_ref:
                        lati_long_date_ref.append(temp)
            else:
                temp2 = " *** champs erreur: " + str(
                    val['messages'][i]['fieldName']) + " \n ****** Message Erreur: " + str(
                    val['messages'][i]['message'])
                if temp2 not in msg:
                    msg.append(temp2)

            if temp2 in msg:
                comp2 += 1

    all_message = []
    for val_m in msg:
        all_message.append(val_m)

    if comp != 0:
        all_message.append(" *** nombre d'occurence sur longitude et latitude: " + str(comp))

    if comp2 != 0:
        all_message.append(" *** Nombre total d'erreurs tout types confondus: " + str(comp2))

    for vals in lati_long_date_ref:
        all_message.append(" *** Erreur sur la longitude et la latitude le " + str(vals[0]) + " à " + str(vals[1]))

    return all_message

