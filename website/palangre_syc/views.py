from django.shortcuts import render
import requests

from django.http import HttpResponse
from json import dump

import openpyxl 
import pandas as pd
import numpy as np

from .forms import MyForm


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

def strip_if_string(element):
    '''
    Fonction qui applique la fonction python strip() si l'élement est bien de type texte
    '''
    return element.strip() if isinstance(element, str) else element


file_path = './palangre_syc/media/Août2023-FV GOLDEN FULL NO.168.xlsx'

def read_excel(file_path, num_page): 
    '''
    Fonction qui prend en argument un chemin d'accès d'un document excel et un numéro de page à extraire
    et qui renvoie un tableau (dataframe) des données 
    Attention -- num_page correspond au numéro de la page (1, 2, 3 etc ...)
    '''
    classeur = openpyxl.load_workbook(filename = file_path, data_only=True)
    noms_feuilles = classeur.sheetnames
    feuille = classeur[noms_feuilles[num_page - 1]]
    df_donnees = pd.DataFrame(feuille.values)
    # fermer le classeur excel 
    classeur.close()
    
    return df_donnees
    
    
def extract_vesselInfo_LL():
    '''
    Fonction qui extrait et présente dans un dataframe les données relatives au bateau 'Vessel information'
    '''    
    num_page = 1
    file_path =  './palangre_syc/media/Août2023-FV GOLDEN FULL NO.168.xlsx'
    df_donnees = read_excel(file_path, num_page)
    
    # On extrait les données propres au 'Vessel information' 
    df_vessel = df_donnees.iloc[7:16,0]
    np_vessel = np.array(df_vessel)

    # On sépare en deux colonnes selon ce qu'il y a avant et après les ':'
    entries = [(item.split(":")[0].strip(), item.split(":")[1].strip() if ':' in item else '') for item in np_vessel]
    np_vessel_clean = np.array(entries, dtype=[('Logbook_name', 'U50'), ('Value', 'U50')])
    df_vessel = pd.DataFrame(np_vessel_clean)
    
    return df_vessel


def extract_cruiseInfo_LL():
    '''
    Fonction qui extrait et présente dans un dataframe les données relatives à la marée
    '''    
    num_page = 1
    file_path =  './palangre_syc/media/Août2023-FV GOLDEN FULL NO.168.xlsx'
    df_donnees = read_excel(file_path, num_page)
    
    # On extrait les données propres au 'Vessel information' 
    df_cruise1 = df_donnees.iloc[7:10,11:20]
    df_cruise2 = df_donnees.iloc[7:10,20:29]

    # On supprimes les colonnes qui sont vides
    df_cruise1 = suppression_colonnes_vides(df_cruise1) 
    df_cruise2 = suppression_colonnes_vides(df_cruise2)

    np_cruise = np.append(np.array(df_cruise1), np.array(df_cruise2), axis = 0)
    
    # on nettoie la colonne en enlevant les espaces et les ':'
    Logbook_name = np.array([s.partition(':')[0].strip() for s in np_cruise[:, 0]])
    np_cruise[:, 0] = Logbook_name
    
    # On applique la fonction strip sur les cellules de la colonnes Valeur, si l'élément correspond à une zone de texte
    vect = np.vectorize(strip_if_string)    
    np_cruise[:, 1] = vect(np_cruise[:, 1])
    
    df_cruise = pd.DataFrame(np_cruise, columns = ['Logbook_name', 'Value'])

    return df_cruise

    
    


      


def index(request):
    
    df_vessel = extract_vesselInfo_LL()
    df_cruise = extract_cruiseInfo_LL()

    if request.method == 'POST':
        
        token = get_token()
        data_ref_ll = get_referential_ll()
        data_ref_common = get_referential_common()

        context = {
            'token': token, 
            'data_ref_ll': data_ref_ll, 
            'data_ref_common' : data_ref_common, 
            'df_vessel' : df_vessel, 
            'df_cruise' : df_cruise
        }
        
    else : 
        context = { 
            'df_vessel' : df_vessel, 
            'df_cruise' : df_cruise
        }
    
    return render(request, 'LL_homepage.html', context)

 