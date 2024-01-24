from django.shortcuts import render
import requests

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
    Fonction qui récupère le référentiel longliners 
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
    Fonction qui récupère le référentiel common 
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

def np_removing_semicolon(numpy_table, num_col):
    '''
    Fonction qui prend une numpy table et ne retourne que la partie avant les deux point de la colonne demandée
    '''
    return np.array([s.partition(':')[num_col].strip() for s in numpy_table[:, num_col]])

def dms_to_decimal(degrees, minutes, direction):
    decimal_degrees = degrees + minutes / 60.0
    if direction in ['S', 'W']:
        decimal_degrees *= -1
    return decimal_degrees

#file_path = './palangre_syc/media/Août2023-FV GOLDEN FULL NO.168.xlsx'
file_path = './palangre_syc/media/july2022-FV GOLDEN FULL NO.168.xlsx'


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
    
def extract_vesselInfo_LL(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les données relatives au bateau 'Vessel information'
    '''    
    num_page = 1
    df_donnees = read_excel(file_path, num_page)
    
    # On extrait les données propres au 'Vessel information' 
    df_vessel = df_donnees.iloc[7:16,0]
    np_vessel = np.array(df_vessel)

    # On sépare en deux colonnes selon ce qu'il y a avant et après les ':'
    entries = [(item.split(":")[0].strip(), item.split(":")[1].strip() if ':' in item else '') for item in np_vessel]
    np_vessel_clean = np.array(entries, dtype=[('Logbook_name', 'U50'), ('Value', 'U50')])
    df_vessel = pd.DataFrame(np_vessel_clean)
    
    return df_vessel

def extract_cruiseInfo_LL(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les données relatives à la marée
    '''    
    num_page = 1
    df_donnees = read_excel(file_path, num_page)
    
    # On extrait les données propres au 'Vessel information' 
    df_cruise1 = df_donnees.iloc[7:10,11:20]
    df_cruise2 = df_donnees.iloc[7:10,20:29]

    # On supprimes les colonnes qui sont vides
    df_cruise1 = suppression_colonnes_vides(df_cruise1) 
    df_cruise2 = suppression_colonnes_vides(df_cruise2)

    np_cruise = np.append(np.array(df_cruise1), np.array(df_cruise2), axis = 0)
    
    # on nettoie la colonne en enlevant les espaces et les ':'
    np_cruise[:, 0] = np_removing_semicolon(np_cruise, 0)
    
    # On applique la fonction strip sur les cellules de la colonnes Valeur, si l'élément correspond à une zone de texte
    vect = np.vectorize(strip_if_string)    
    np_cruise[:, 1] = vect(np_cruise[:, 1])
    
    df_cruise = pd.DataFrame(np_cruise, columns = ['Logbook_name', 'Value'])

    return df_cruise

def extract_gearInfo_LL(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les données relatives à l'équipement
    '''    
    num_page = 1
    df_donnees = read_excel(file_path, num_page)
    
    # On extrait les données propres au 'Vessel information' 
    df_gear = df_donnees.iloc[12:16,11:21]

    # On supprimes les colonnes qui sont vides
    df_gear = suppression_colonnes_vides(df_gear) 

    np_gear = np.array(df_gear)
    
    # on nettoie la colonne en enlevant les espaces et les ':'
    np_gear[:, 0] = np_removing_semicolon(np_gear, 0)
    
    # On applique la fonction strip sur les cellules de la colonnes Valeur, si l'élément correspond à une zone de texte
    vect = np.vectorize(strip_if_string)    
    np_gear[:, 1] = vect(np_gear[:, 1])
    
    df_gear = pd.DataFrame(np_gear, columns = ['Logbook_name', 'Value'])
    
    return df_gear

def extract_lineMaterial_LL(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les données relatives aux matériel des lignes
    '''    
    num_page = 1
    df_donnees = read_excel(file_path, num_page)
    
    # On extrait les données propres au 'Vessel information' 
    df_line = df_donnees.iloc[12:16,21:29]

    # On supprimes les colonnes qui sont vides
    df_line = suppression_colonnes_vides(df_line) 
    
    np_line = np.array(df_line)
    
    # On applique la fonction strip sur les cellules de la colonnes Valeur, si l'élément correspond à une zone de texte
    vect = np.vectorize(strip_if_string)    
    np_line[:,0:1] = vect(np_line[:,0:1])
    
    df_line = pd.DataFrame(np_line, columns = ['Logbook_name', 'Value'])
    
    return df_line

def extract_target_LL(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les données relatives aux target spécifiques
    '''    
    num_page = 1
    df_donnees = read_excel(file_path, num_page)
    
    # On extrait les données propres au 'Vessel information' 
    df_target = df_donnees.iloc[12:16,29:34]

    # On supprimes les colonnes qui sont vides
    df_target = suppression_colonnes_vides(df_target) 

    np_target = np.array(df_target)
        
    np_target[:, 0] = np_removing_semicolon(np_target, 0)
    # On applique la fonction strip sur les cellules de la colonnes Valeur, si l'élément correspond à une zone de texte
    vect = np.vectorize(strip_if_string)    
    np_target[:,0:1] = vect(np_target[:,0:1])
    
    df_target = pd.DataFrame(np_target, columns = ['Logbook_name', 'Value'])
    
    return df_target

def extract_logbookDate(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe le mois et l'année du logbook
    '''    
    num_page = 1
    df_donnees = read_excel(file_path, num_page)
    
    # On extrait les données propres au 'Vessel information' 
    df_month = df_donnees.iloc[17,5]
    df_year = df_donnees.iloc[17,11]

    np_date = np.array([('Month', df_month), ('Year', df_year)], 
                       dtype = [('Logbook_name', 'U10'), ('Value', int)])
    df_date = pd.DataFrame(np_date)
    
    return df_date

      
def extract_positions(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les position de chaque coup de peche par jour 
    en type float (C'EST QUEL SYSTEME ?)
    '''    
    num_page = 1
    df_donnees = read_excel(file_path, num_page)
    
    df_lat_dms = df_donnees.iloc[24:54, 1:4]
    print(df_lat_dms)
    np_lat_dms = np.array(df_lat_dms)
    
#    split_data = np.char.split(np_lat_dms)
#    np_lat_dms = np.array(split_data.tolist(), dtype=[('Degree', int), ('Minut', int), ('Direction', 'U10')])



    #df_lat_dec['Latitute'] = df_lat_dms.apply(dms_to_decimal, axis = 0)
#    print(np_lat_dms)
    
    print('DONC JUST UNE LIGNE')
#    print(np_lat_dms[3,])
#    for row in range(len(np_lat_dms)):
#        np_lat_dms[row, 'Latitute'] = dms_to_decimal(np_lat_dms[row, 0], np_lat_dms[row, 1], np_lat_dms[row, 2])
    
    df_lat_dec = pd.DataFrame(np_lat_dms)
    
    return df_lat_dec


def index(request):
    file_path = './palangre_syc/media/july2022-FV GOLDEN FULL NO.168.xlsx'
    df_vessel = extract_vesselInfo_LL(file_path)
    df_cruise = extract_cruiseInfo_LL(file_path)
    df_gear = extract_gearInfo_LL(file_path)
    df_line = extract_lineMaterial_LL(file_path)
    df_target = extract_target_LL(file_path)
    df_date = extract_logbookDate(file_path)
    
    df_position = extract_positions(file_path)

    if request.method == 'POST':
        
        token = get_token()
        data_ref_ll = get_referential_ll()
        data_ref_common = get_referential_common()

        context = {
            'token': token, 
            'data_ref_ll': data_ref_ll, 
            'data_ref_common' : data_ref_common, 
            'df_vessel' : df_vessel, 
            'df_cruise' : df_cruise, 
            'df_gear' : df_gear, 
            'df_line' : df_line, 
            'df_target' : df_target, 
            'df_date' : df_date, 
            
            'df_position' : df_position
        }
        
    else : 
        context = { 
            'df_vessel' : df_vessel, 
            'df_cruise' : df_cruise, 
            'df_gear' : df_gear, 
            'df_line' : df_line, 
            'df_target' : df_target, 
            'df_date' : df_date, 
            
            'df_position' : df_position
        }
    
    return render(request, 'LL_homepage.html', context)

 