from django.shortcuts import render
import requests

from json import dump

import openpyxl 
import pandas as pd
import numpy as np
import re
import datetime

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
    
def del_empty_col(dataframe):
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

def remove_spec_char(char):
    '''
    Fonction qui élimine les caractères non ascii
    '''
    return re.sub("[^A-Z ]", "", str(char), 0, re.IGNORECASE)

def remove_spec_char_from_list(char_list):
    '''
    Applique remove_spec_char à chaque élément d'une liste de chaînes
    '''
    return [remove_spec_char(item) for item in char_list]

def np_removing_semicolon(numpy_table, num_col):
    '''
    Fonction qui prend une numpy table et ne retourne que la partie avant les deux point de la colonne demandée
    '''
    return np.array([s.partition(':')[num_col].strip() for s in numpy_table[:, num_col]])

def dms_to_decimal(degrees, minutes, direction):
    if degrees is None : 
        return None
    
    # if type(degrees) is str:
    degrees = int(degrees)
    minutes = int(minutes)
    decimal_degrees = degrees + minutes / 60.0
    if direction in ['S', 'W']:
        decimal_degrees *= -1
    return decimal_degrees

def convert_to_time_or_text(value):
    '''
    Fonction qui convertit la cellule en time - si elle est au format type time ou type date dans le excel
    et qui laisse au format texte (cruising, in port etc) si la cellule est au format texte
    '''
    try:
        if ' ' in value or ':' in value:
            date_time = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S').time()
            if hasattr(date_time, 'strftime'): 
                return date_time.strftime('%H:%M:%S')  
            return str(date_time)
        else :
            if re.match("%H:%M:%S", value):
                # return date_time.strftime('%H:%M:%S')  
                return datetime.datetime.strptime(value, '%H:%M:%S').time().strftime('%H:%M:%S')
            return value  
        
    except (ValueError, TypeError):
        if hasattr(value, 'strftime'): 
            return value.strftime('%H:%M:%S')  
        return str(value)

def zero_if_empty(value):
    if value == "None" or pd.isna(value):
        return 0
    else :
        return int(value)

# FILE_PATH = './palangre_syc/media/Août2023-FV GOLDEN FULL NO.168.xlsx'
FILE_PATH = './palangre_syc/media/july2022-FV GOLDEN FULL NO.168.xlsx'
# FILE_PATH = './palangre_syc/media/S 08-TORNG TAY NO.1-MAR2021.xlsx'

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
    # On applique un filtre pour les caractères spéciaux
    np_vessel_clean['Logbook_name'] = remove_spec_char_from_list(np_vessel_clean['Logbook_name'] )
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
    df_cruise1 = del_empty_col(df_cruise1) 
    df_cruise2 = del_empty_col(df_cruise2)

    np_cruise = np.append(np.array(df_cruise1), np.array(df_cruise2), axis = 0)
    
    # on nettoie la colonne en enlevant les espaces et les ':'
    np_cruise[:, 0] = np_removing_semicolon(np_cruise, 0)
    
    # On applique la fonction strip sur les cellules de la colonnes Valeur, si l'élément correspond à une zone de texte
    vect = np.vectorize(strip_if_string)    
    np_cruise[:, 1] = vect(np_cruise[:, 1])
    
    df_cruise = pd.DataFrame(np_cruise, columns = ['Logbook_name', 'Value'])
    df_cruise['Logbook_name'] = remove_spec_char_from_list(df_cruise['Logbook_name'] )

    return df_cruise

def extract_reportInfo_LL(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les données relatives aux info de report
    '''    
    num_page = 1
    df_donnees = read_excel(file_path, num_page)
    
    # On extrait les données propres au 'Vessel information' 
    df_report = df_donnees.iloc[7:9,29:35]

    # On supprimes les colonnes qui sont vides
    df_report = del_empty_col(df_report) 
    np_report = np.array(df_report)
    
    # On applique la fonction strip sur les cellules de la colonnes Valeur, si l'élément correspond à une zone de texte
    vect = np.vectorize(strip_if_string)    
    np_report[:,0:1] = vect(np_report[:,0:1])
    
    df_report = pd.DataFrame(np_report, columns = ['Logbook_name', 'Value'])
    df_report['Logbook_name'] = remove_spec_char_from_list(df_report['Logbook_name'] )

    return df_report

def extract_gearInfo_LL(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les données relatives à l'équipement
    '''    
    num_page = 1
    df_donnees = read_excel(file_path, num_page)
    
    # On extrait les données propres au 'Vessel information' 
    df_gear = df_donnees.iloc[12:16,11:21]

    # On supprimes les colonnes qui sont vides
    df_gear = del_empty_col(df_gear) 

    np_gear = np.array(df_gear)
    
    # on nettoie la colonne en enlevant les espaces et les ':'
    np_gear[:, 0] = np_removing_semicolon(np_gear, 0)
    
    # On applique la fonction strip sur les cellules de la colonnes Valeur, si l'élément correspond à une zone de texte
    vect = np.vectorize(strip_if_string)    
    np_gear[:, 1] = vect(np_gear[:, 1])
    
    df_gear = pd.DataFrame(np_gear, columns = ['Logbook_name', 'Value'])
    df_gear['Logbook_name'] = remove_spec_char_from_list(df_gear['Logbook_name'] )

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
    df_line = del_empty_col(df_line) 
    
    np_line = np.array(df_line)
    
    # On applique la fonction strip sur les cellules de la colonnes Valeur, si l'élément correspond à une zone de texte
    vect = np.vectorize(strip_if_string)    
    np_line[:,0:1] = vect(np_line[:,0:1])
    
    df_line = pd.DataFrame(np_line, columns = ['Logbook_name', 'Value'])
    df_line['Logbook_name'] = remove_spec_char_from_list(df_line['Logbook_name'] )

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
    df_target = del_empty_col(df_target) 

    np_target = np.array(df_target)
        
    np_target[:, 0] = np_removing_semicolon(np_target, 0)
    # On applique la fonction strip sur les cellules de la colonnes Valeur, si l'élément correspond à une zone de texte
    vect = np.vectorize(strip_if_string)    
    np_target[:,0:1] = vect(np_target[:,0:1])
    
    df_target = pd.DataFrame(np_target, columns = ['Logbook_name', 'Value'])
    df_target['Logbook_name'] = remove_spec_char_from_list(df_target['Logbook_name'] )
    
    return df_target

def extract_logbookDate_LL(file_path):
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
    df_date['Logbook_name'] = remove_spec_char_from_list(df_date['Logbook_name'] )
    
    return df_date

def extract_bait_LL(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe le type de d'appat utilisé
    '''    
    num_page = 1
    df_donnees = read_excel(file_path, num_page)
    
    # On extrait les données propres au 'Vessel information' 
    df_squid = df_donnees.iloc[19,16]
    df_sardine = df_donnees.iloc[19,20]
    df_mackerel = df_donnees.iloc[19,24]
    df_muroaji = df_donnees.iloc[19,28]
    df_other = df_donnees.iloc[19,32]

    np_bait = np.array([('Squid', df_squid), 
                        ('Sardine', df_sardine),
                        ('Mackerel', df_mackerel),
                        ('Muroaji', df_muroaji),
                        ('Orther', df_other),], 
                       dtype = [('Logbook_name', 'U10'), ('Value', 'U10')])
    df_bait = pd.DataFrame(np_bait)
   # df_date['Logbook_name'] = remove_spec_char_from_list(df_date['Logbook_name'] )
    
    return df_bait

def extract_positions(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les position de chaque coup de peche par jour 
    en décimal type float
    '''    
    num_page = 1
    df_donnees = read_excel(file_path, num_page)
    
    day = df_donnees.iloc[24:55, 0]
    df_lat_dms = df_donnees.iloc[24:55, 1:4]
    df_long_dms = df_donnees.iloc[24:55, 4:7]
    colnames = ['Degrees', 'Minutes', 'Direction']
    df_lat_dms.columns = colnames
    df_long_dms.columns = colnames
    
    df_lat_dms['Latitute'] = df_lat_dms.apply(lambda row: dms_to_decimal(row['Degrees'], row['Minutes'], row['Direction']), axis=1)
    Latitute = round(df_lat_dms['Latitute'], 2).values
    
    df_long_dms['Longitude'] = df_long_dms.apply(lambda row: dms_to_decimal(row['Degrees'], row['Minutes'], row['Direction']), axis=1)
    Longitude = round(df_long_dms['Longitude'], 2).values
    
    np_position = np.column_stack((day, Latitute, Longitude))
    df_position = pd.DataFrame(np_position, columns=['Day', 'Latitute', 'Longitude'])
    
    return df_position

def extract_time(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les horaires des coups de pêche 
    Elle retourne un champ type horaire, sauf si le bateau est en mouvement
    '''    
    num_page = 1
    df_donnees = read_excel(file_path, num_page)

    df_time = df_donnees.iloc[24:55, 7:8]
    colnames = ['Time']
    df_time.columns = colnames
    df_time['Time'] = df_time['Time'].apply(convert_to_time_or_text)
    
    df_time.reset_index(drop=True, inplace=True)
    return df_time

def extract_temperature(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les horaires des coups de pêche 
    Elle retourne un champ type horaire, sauf si le bateau est en mouvement
    '''    
    num_page = 1
    df_donnees = read_excel(file_path, num_page)

    df_temp = df_donnees.iloc[24:55, 8:9]
    colnames = ['Température']
    df_temp.columns = colnames
    
    df_temp.reset_index(drop=True, inplace=True)
    return df_temp

def extract_fishingEffort(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les efforts de peche
    '''    
    num_page = 1
    df_donnees = read_excel(file_path, num_page)

    df_fishingEffort = df_donnees.iloc[24:55, 9:12]
    colnames = ['Hooks', 'Total hooks', 'Total lightsticks']
    df_fishingEffort.columns = colnames
    
    df_fishingEffort.reset_index(drop=True, inplace=True)
    return df_fishingEffort

def extract_tunas(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les tunas 
    '''    
    num_page = 1
    df_donnees = read_excel(file_path, num_page)

    df_tunas = df_donnees.iloc[24:55, 12:20]
    colnames = ['No SBF', 'Kg SBF', 
                'No ALB', 'Kg ALB', 
                'No BET', 'Kg BET', 
                'No YFT', 'Kg YFT']
    df_tunas.columns = colnames
    
    df_tunas = df_tunas.map(zero_if_empty)

    df_tunas.reset_index(drop=True, inplace=True)
    return df_tunas

def extract_billfishes(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les billfishes 
    '''    
    num_page = 1
    df_donnees = read_excel(file_path, num_page)

    df_billfishies = df_donnees.iloc[24:55, 20:32]
    colnames = ['No SWO', 'Kg SWO', 
                'No MLS', 'Kg MLS', 
                'No BLZ', 'Kg BLZ', 
                'No BLM', 'Kg BLM',
                'No SFA', 'Kg SFA', 
                'No SSP', 'Kg SSP']
    df_billfishies.columns = colnames
    
    df_billfishies = df_billfishies.map(zero_if_empty)

    df_billfishies.reset_index(drop=True, inplace=True)
    return df_billfishies

def extract_otherfish(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les autres poissons 
    '''    
    num_page = 1
    df_donnees = read_excel(file_path, num_page)

    df_otherfish = df_donnees.iloc[24:55, 32:36]
    colnames = ['No oil fish', 'Kg oil fish', 
                'No other species', 'Kg other species']
    df_otherfish.columns = colnames
    
    df_otherfish = df_otherfish.map(zero_if_empty)

    df_otherfish.reset_index(drop=True, inplace=True)
    return df_otherfish

def extract_sharksFAL(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les blacks sharks 
    '''    
    num_page = 2
    df_donnees = read_excel(file_path, num_page)

    df_sharksFAL = df_donnees.iloc[15:46, 1:5]
    colnames = ['FAL No Retained', 'FAL Kg Retained', 
                'FAL No Released alive', 'FAL No Discarded dead']
    df_sharksFAL.columns = colnames
    
    df_sharksFAL = df_sharksFAL.map(zero_if_empty)

    df_sharksFAL.reset_index(drop=True, inplace=True)
    return df_sharksFAL

def extract_sharksBSH(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les blue sharks 
    '''    
    num_page = 2
    df_donnees = read_excel(file_path, num_page)

    df_sharksBSH = df_donnees.iloc[15:46, 5:9]
    colnames = ['BSH No Retained', 'BSH Kg Retained', 
                'BSH No Released alive', 'BSH No Discarded dead']
    df_sharksBSH.columns = colnames
    
    df_sharksBSH = df_sharksBSH.map(zero_if_empty)

    df_sharksBSH.reset_index(drop=True, inplace=True)
    return df_sharksBSH

def extract_sharksMAK(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les Mako 
    '''    
    num_page = 2
    df_donnees = read_excel(file_path, num_page)

    df_sharksMAK = df_donnees.iloc[15:46, 9:13]
    colnames = ['MAK No Retained', 'MAK Kg Retained', 
                'MAK No Released alive', 'MAK No Discarded dead']
    df_sharksMAK.columns = colnames
    
    df_sharksMAK = df_sharksMAK.map(zero_if_empty)

    df_sharksMAK.reset_index(drop=True, inplace=True)
    return df_sharksMAK

def extract_sharksSPN(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les hammer head sharks 
    '''    
    num_page = 2
    df_donnees = read_excel(file_path, num_page)

    df_sharksSPN = df_donnees.iloc[15:46, 13:17]
    colnames = ['SPN No Retained', 'SPN Kg Retained', 
                'SPN No Released alive', 'SPN No Discarded dead']
    df_sharksSPN.columns = colnames
    
    df_sharksSPN = df_sharksSPN.map(zero_if_empty)

    df_sharksSPN.reset_index(drop=True, inplace=True)
    return df_sharksSPN

def extract_sharksTIG(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les tiger sharks 
    '''    
    num_page = 2
    df_donnees = read_excel(file_path, num_page)

    df_sharksTIG = df_donnees.iloc[15:46, 17:21]
    colnames = ['TIG No Retained', 'TIG Kg Retained', 
                'TIG No Released alive', 'TIG No Discarded dead']
    df_sharksTIG.columns = colnames
    
    df_sharksTIG = df_sharksTIG.map(zero_if_empty)

    df_sharksTIG.reset_index(drop=True, inplace=True)
    return df_sharksTIG

def extract_sharksPSK(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les crocodile sharks 
    '''    
    num_page = 2
    df_donnees = read_excel(file_path, num_page)

    df_sharksPSK = df_donnees.iloc[15:46, 21:25]
    colnames = ['PSK No Retained', 'PSK Kg Retained', 
                'PSK No Released alive', 'PSK No Discarded dead']
    df_sharksPSK.columns = colnames
    
    df_sharksPSK = df_sharksPSK.map(zero_if_empty)

    df_sharksPSK.reset_index(drop=True, inplace=True)
    return df_sharksPSK

def extract_sharksTHR(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les thresher sharks 
    '''    
    num_page = 2
    df_donnees = read_excel(file_path, num_page)

    df_sharksFAL = df_donnees.iloc[15:46, 25:27]
    colnames = ['THR No Released alive', 'THR No Discarded dead']
    df_sharksFAL.columns = colnames
    
    df_sharksFAL = df_sharksFAL.map(zero_if_empty)

    df_sharksFAL.reset_index(drop=True, inplace=True)
    return df_sharksFAL

def extract_sharksOCS(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les oceanic sharks 
    '''    
    num_page = 2
    df_donnees = read_excel(file_path, num_page)

    df_sharksOCS = df_donnees.iloc[15:46, 27:29]
    colnames = ['OCS No Released alive', 'OCS No Discarded dead']
    df_sharksOCS.columns = colnames
    
    df_sharksOCS = df_sharksOCS.map(zero_if_empty)

    df_sharksOCS.reset_index(drop=True, inplace=True)
    return df_sharksOCS

def extract_mammals(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les autres mammifères marins 
    '''    
    num_page = 2
    df_donnees = read_excel(file_path, num_page)

    df_mammals = df_donnees.iloc[15:46, 29:31]
    colnames = ['Mammals No Released alive', 'Mammals No Discarded dead']
    df_mammals.columns = colnames
    
    df_mammals = df_mammals.map(zero_if_empty)

    df_mammals.reset_index(drop=True, inplace=True)
    return df_mammals

def extract_seabird(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les sea birds
    '''    
    num_page = 2
    df_donnees = read_excel(file_path, num_page)

    df_seabird = df_donnees.iloc[15:46, 31:33]
    colnames = ['Seabird No Released alive', 'Seabird No Discarded dead']
    df_seabird.columns = colnames
    
    df_seabird = df_seabird.map(zero_if_empty)

    df_seabird.reset_index(drop=True, inplace=True)
    return df_seabird

def extract_turtles(file_path):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les torutes 
    '''    
    num_page = 2
    df_donnees = read_excel(file_path, num_page)

    df_turtles = df_donnees.iloc[15:46, 33:35]
    colnames = ['Turtles No Released alive', 'Turtles No Discarded dead']
    df_turtles.columns = colnames
    
    df_turtles = df_turtles.map(zero_if_empty)

    df_turtles.reset_index(drop=True, inplace=True)
    return df_turtles




def index(request):
    fp = FILE_PATH

    df_vessel = extract_vesselInfo_LL(fp)
    df_cruise = extract_cruiseInfo_LL(fp)
    df_report = extract_reportInfo_LL(fp)
    df_gear = extract_gearInfo_LL(fp)
    df_line = extract_lineMaterial_LL(fp)
    df_target = extract_target_LL(fp)
    df_date = extract_logbookDate_LL(fp)
    df_bait = extract_bait_LL(fp)
    df_fishingEffort = extract_fishingEffort(fp)
    
    df_position = extract_positions(fp)
    df_time = extract_time(fp)
    df_temperature = extract_temperature(fp)
    df_tunas = extract_tunas(fp)
    df_billfishes = extract_billfishes(fp)
    df_otherfish = extract_otherfish(fp)
    df_sharksFAL = extract_sharksFAL(fp)
    df_sharksBSH = extract_sharksBSH(fp)
    df_sharksMAK = extract_sharksMAK(fp)
    df_sharksSPN = extract_sharksSPN(fp)
    df_sharksTIG = extract_sharksTIG(fp)
    df_sharksPSK = extract_sharksPSK(fp)
    df_sharksTHR = extract_sharksTHR(fp)
    df_sharksOCS = extract_sharksOCS(fp)
    df_mammals = extract_mammals(fp)
    df_seabirds = extract_seabird(fp)
    df_turtles = extract_turtles(fp)
    
    
    
    df_activity = pd.concat([df_position, df_time, df_temperature, 
                             df_fishingEffort, df_tunas, df_billfishes, df_otherfish, 
                             df_sharksFAL, df_sharksBSH, df_sharksMAK, 
                             df_sharksSPN, df_sharksTIG, df_sharksPSK, 
                             df_sharksTHR, df_sharksOCS, 
                             df_mammals, df_seabirds, df_turtles],
                            axis = 1)
    
        
    if request.method == 'POST':
        
        token = get_token()
        data_ref_ll = get_referential_ll()
        data_ref_common = get_referential_common()

        context = {
            'token': token, 
            'data_ref_ll': data_ref_ll, 
            'data_ref_common' : data_ref_common, 
        }
        
    else : 
        context = { 
            'df_vessel' : df_vessel, 
            'df_cruise' : df_cruise, 
            'df_report' : df_report,
            'df_gear' : df_gear, 
            'df_line' : df_line, 
            'df_target' : df_target, 
            'df_date' : df_date, 
            'df_bait' : df_bait,
            
            'df_position' : df_position,   
            'df_time' : df_time,       
            'df_activity' : df_activity, 
        }
    
    return render(request, 'LL_homepage.html', context)

 