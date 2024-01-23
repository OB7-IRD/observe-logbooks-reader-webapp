from django.shortcuts import render
import requests

from django.http import HttpResponse
from json import dump

import openpyxl 
import pandas as pd


def get_token():
    '''
    Fonction qui sort un Token 
    Amélioration : on passe en entrée les données, obtenues à partir du formulaire de connexion 
    '''
    api_base = 'https://observe.ob7.ird.fr/observeweb/api/public/init/open?'
    api_modelVersion = 'config.modelVersion=9.2.1&'
    api_login = 'config.login=technicienweb&'
    api_password = 'config.password=wpF3NITE&'
    api_databaseName = 'config.databaseName=test&'
    api_referential = 'referentialLocale=FR'
    
    # Constitution du lien url pour accéder à l'API et donc générer un token
    api_url = api_base + api_modelVersion + api_login + api_password + api_databaseName + api_referential
    response = requests.get(api_url)
    
    # si la réponse est un succès, on extrait que le Token
    if response.status_code == 200:
        data_from_api = response.json()
        token = data_from_api['authenticationToken']
    else:
        token = None

    return token

def get_referential_ll():
    '''
    Fonction qui affiche le référentiel longliners 
    ''' 
    api_base = 'https://observe.ob7.ird.fr/observeweb/api/public/referential/ll?'
    api_Token = 'authenticationToken=' + get_token() +'&'
    api_infos = 'config.loadReferential=&config.recursive=&config.prettyPrint=true&config.serializeNulls=&referentialLocale='
    
    # Constitution du lien url pour accéder à l'API et donc générer un token
    api_url = api_base + api_Token + api_infos 
    response = requests.get(api_url)
    
    # si la réponse est un succès, on extrait que le Token
    if response.status_code == 200:
        data_ref_ll = response.json()
    #    with open('data_ll.json', 'w', encoding='utf-8') as f:
    #        dump(data_ref_ll, f, ensure_ascii=False, indent=4)
    else:
        data_ref_ll = None

    return data_ref_ll
    
def get_referential_common():
    '''
    Fonction qui affiche le référentiel common 
    ''' 
    api_base = 'https://observe.ob7.ird.fr/observeweb/api/public/referential/common?'
    api_Token = 'authenticationToken=' + get_token() +'&'
    api_infos = 'config.loadReferential=&config.recursive=&config.prettyPrint=true&config.serializeNulls=&referentialLocale='
        
    # Constitution du lien url pour accéder à l'API et donc générer un token    
    api_url = api_base + api_Token + api_infos 
    response = requests.get(api_url)
        
    # si la réponse est un succès, on extrait que le Token
    if response.status_code == 200:
        data_ref_common = response.json()
    #    with open('data_common.json', 'w', encoding='utf-8') as f:
    #        dump(data_ref_common, f, ensure_ascii=False, indent=4)
    else:
        data_ref_common = None
    
    return data_ref_common
    
def suppression_colonnes_vides(dataframe):
    '''
    Fonction qui supprime une colonne si elle est vide ('None')
    '''
    colonnes_a_supprimer = [colonne for colonne in dataframe.columns if all(dataframe[colonne].isna())]
    dataframe.drop(columns=colonnes_a_supprimer, inplace=True)
    return dataframe  

def read_excel(): 
    '''
    Fonction qui lit un doc excel de palangre seychellois (version 17.6) placé dans le dossier media de l'appli
    et qui renvoie un tableau (dataframe) des données concernant le trip, et un concernant les activités sur le mois
    '''
    file_path = './palangre_syc/media/Août2023-FV GOLDEN FULL NO.168.xlsx'
    classeur = openpyxl.load_workbook(filename = file_path, data_only=True)
    noms_feuilles = classeur.sheetnames

    # Page 1    
    feuille = classeur[noms_feuilles[0]]

    df_donnees = pd.DataFrame(feuille.values)
    df_donnees.drop(index=range(6), inplace = True)
    df_trip = df_donnees.iloc[1:11]
    df_activity = df_donnees.iloc[22:56]
    
    df_trip = suppression_colonnes_vides(df_trip)
    df_activity = suppression_colonnes_vides(df_activity)
    
    df_trip_propre = pd.DataFrame({'data_obs' : ['startDate', 'endDate', 'noOfCrewMembers'],
                                   'data_lb' : ['', '', ''],
                                   'value' : ['', '', '']})
    
    
   # df_trip_propre = df_trip_propre.to_dict('records')
    return df_trip, df_activity


# fermer le classeur excel 
#classeur.close()

      


def index(request):
    token = get_token()
    data_ref_ll = get_referential_ll()
    data_ref_common = get_referential_common()
    df_trip, df_activity = read_excel()
    context = {
        'token': token, 
        'data_ref_ll': data_ref_ll, 
        'data_ref_common' : data_ref_common, 
        'df_trip' : df_trip, 
        'df_activity' : df_activity
    }
    return render(request, 'LL_homepage.html', context)

 