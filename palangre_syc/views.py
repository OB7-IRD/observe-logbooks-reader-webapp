import time

import os
import re
import json
import datetime
import warnings


import pandas as pd
import numpy as np
import openpyxl

from django.shortcuts import render
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils import translation
# from django.http import HttpResponseRedirect, JsonResponse
# from django.utils.translation import activate
# from django.template import RequestContext
# from django.urls import reverse
# from django.utils.translation import gettext

from palangre_syc import api
from palangre_syc import json_construction


def del_empty_col(dataframe):
    """ Fonction qui supprime la colonne si elle ne contient pas d'information

    Args:
        dataframe: avec des potentielles colonnes vides (cellules mergées)

    Returns:
        dataframe: uniquement avec des éléments
    """
    colonnes_a_supprimer = [
        colonne for colonne in dataframe.columns if all(dataframe[colonne].isna())]
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
    Fonction qui prend une numpy table et ne retourne 
    que la partie avant les deux point de la colonne demandée
    '''
    return np.array([s.partition(':')[num_col].strip() for s in numpy_table[:, num_col]])


def dms_to_decimal2(degrees, minutes, direction):
    """Transforme des degrés minutes secondes en décimal

    Args:
        degrees (int), minutes (int): value
        direction (str): N S E W

    Returns:
        float: value
    """
    if degrees is None:
        return None

    # if type(degrees) is str:
    degrees = int(degrees)
    minutes = int(minutes)
    decimal_degrees = degrees + minutes / 60.0
    if direction in ['S', 'W']:
        decimal_degrees *= -1
    return decimal_degrees

def dms_to_decimal(degrees, minutes, direction):
    """Transforme des degrés minutes secondes en décimal

    Args:
        degrees (int), minutes (int): value
        direction (str): N S E W

    Returns:
        float: value
    """
    if degrees is None:
        return None

    decimal_degrees = degrees + minutes / 60.0
    decimal_degrees = np.where(direction.isin(['S', 'W']), -decimal_degrees, decimal_degrees)
    return decimal_degrees

def convert_to_time_or_text(value):
    '''
    Fonction qui convertit la cellule en time
    si elle est au format type time ou date dans le excel
    et qui laisse au format texte (cruising, in port etc) si la cellule est au format texte
    '''
    # print("heure askip : ", value)
    if isinstance(value, str):
        # print("="*3, value)
        if re.match("[0-9]{2}:[0-9]{2}:[0-9]{2}", value):
            print("first match")
            # return date_time.strftime('%H:%M:%S')
            return datetime.datetime.strptime(value, '%H:%M:%S').time().strftime('%H:%M:%S')
        elif re.match("[0-9]{2}:[0-9]{2}", value.strip()):
            # print("sd match")
            return value.strip() + ':00'
            # return date_time.strftime('%H:%M:%S')
            # return datetime.datetime.strptime(value, '%H:%M:%S').time().strftime('%H:%M:%S')
        return value
    elif isinstance(value, datetime.datetime):
        # print("="*3, value)
        # date_time = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S').time()
        date_time = value.time()
        if hasattr(date_time, 'strftime'):
            return date_time.strftime('%H:%M:%S')
        return str(date_time)
    return str(value)


def zero_if_empty(value):
    """
    Remplace par 0 quand la case est vide
    """
    if value == "None" or pd.isna(value):
        # print("value empty")
        return 0
    elif isinstance(value, str) and (value == "" or re.search(r"\S*", value)):
        # print("value blank space")
        return 0
    else:
        return int(value)


def from_topiaid_to_value(topiaid, lookingfor, label_output, domaine=None):
    """
    Fonction générale qui retourne le label output pour un topiad donné 
    dans la base common ou lognliner

    Args:
        topiad
        lookingfor: catégorie issu du WS dans laquelle on veut chercher notre topiaid
        label_output: ce qu'on veut présenter (label, nom, espèce ...)
        domaine si nécessaire (palangre, senne)

    Returns:
        nom souhaité associé au topotiad
    """
    if domaine is None:
        with open('./data_common.json', 'r', encoding='utf-8') as f:
            data_common = json.load(f)
        category = 'fr.ird.observe.entities.referential.common.' + lookingfor
        if data_common['content'][category] is not None:
            for element in data_common['content'][category]:
                if element['topiaId'] == topiaid:
                    return element[label_output]
        else:
            print("please do check the orthographe of lookingfor element")
            return None

    else:
        with open('./data_ll.json', 'r', encoding='utf-8') as f:
            data_ll = json.load(f)
        category = 'fr.ird.observe.entities.referential.ll.common.' + lookingfor
        if data_ll['content'][category] is not None:
            for element in data_ll['content'][category]:
                if element['topiaId'] == topiaid:
                    return element[label_output]
        else:
            print("please do check the orthographe of lookingfor element")
            return None



# FILE_PATH = './palangre_syc/media/Aout2022-FV GOLDEN FULL NO.168.xlsx'


def read_excel(file_path, num_page):
    ''' 
    Fonction qui prend en argument un chemin d'accès d'un document excel 
    et un numéro de page à extraire
    et qui renvoie un tableau (dataframe) des données 
    Attention -- num_page correspond au numéro de la page (1, 2 etc ...)
    '''
    classeur = openpyxl.load_workbook(filename=file_path, data_only=True)
    noms_feuilles = classeur.sheetnames
    feuille = classeur[noms_feuilles[num_page - 1]]
    df_donnees = pd.DataFrame(feuille.values)
    # fermer le classeur excel
    classeur.close()
    return df_donnees


def extract_vessel_info(df_donnees):
    """
    Extraction des cases 'Vessel Information'

    Args:
        df_donnees (df): excel p1

    Returns:
        df
    """
    df_vessel = df_donnees.iloc[7:16, 0]
    # On sépare en deux colonnes selon ce qu'il y a avant et après les ':'
    df_vessel_clean = df_vessel.str.split(':', expand=True)
    # S'assurer que toutes les valeurs sont des chaînes de caractères
    df_vessel_clean = df_vessel_clean.map(lambda x: str(x).strip() if x is not None else '')
    df_vessel_clean.columns = ['Logbook_name', 'Value']
    # On enlève les caractères spéciaux
    df_vessel_clean['Logbook_name'] = remove_spec_char_from_list(df_vessel_clean['Logbook_name'])

    return df_vessel_clean

def extract_cruise_info(df_donnees):
    """
    Extraction des cases 'Cruise Information'

    Args:
        df_donnees (df): excel p1

    Returns:
        df
    """
    # On extrait les données propres au 'Cruise information'
    df_cruise1 = df_donnees.iloc[9:10, 11:20]
    df_cruise2 = df_donnees.iloc[9:10, 20:29]

    # On supprimes les colonnes qui sont vides
    df_cruise1 = del_empty_col(df_cruise1)
    df_cruise2 = del_empty_col(df_cruise2)

    np_cruise = np.append(np.array(df_cruise1), np.array(df_cruise2), axis=0)

    # on nettoie la colonne en enlevant les espaces et les ':'
    np_cruise[:, 0] = np_removing_semicolon(np_cruise, 0)

    # On applique la fonction strip sur les cellules de la colonnes Valeur,
    # si l'élément correspond à une zone de texte
    vect = np.vectorize(strip_if_string)
    np_cruise[:, 1] = vect(np_cruise[:, 1])

    df_cruise = pd.DataFrame(np_cruise, columns=['Logbook_name', 'Value'])
    
    # Nettoyer la colonne 'Logbook_name' en enlevant les espaces et les ':'
    df_cruise['Logbook_name'] = df_cruise.iloc[:, 0].str.replace(':', '').str.strip()

    # Appliquer la fonction strip sur les cellules de la colonne 'Value' si l'élément correspond à une zone de texte
    df_cruise['Value'] = df_cruise.iloc[:, 1].apply(lambda x: x.strip() if isinstance(x, str) else x)

    # Appliquer un filtre pour les caractères spéciaux dans la colonne 'Logbook_name'
    df_cruise['Logbook_name'] = remove_spec_char_from_list(df_cruise['Logbook_name'])

    # Supprimer les espaces supplémentaires dans la colonne 'Logbook_name'
    df_cruise['Logbook_name'] = df_cruise['Logbook_name'].str.strip()
    
    return df_cruise

def extract_report_info(df_donnees):
    """
    Extraction des cases 'Report Information'

    Args:
        df_donnees (df): excel p1

    Returns:
        df
    """
    # On extrait les données 
    df_report = df_donnees.iloc[7:9, 29:35]

    # On supprime les colonnes qui sont vides
    df_report = df_report.dropna(axis=1, how='all')

    # Nettoyer la colonne 'Logbook_name' en enlevant les espaces et les ':'
    df_report.iloc[:, 0] = df_report.iloc[:, 0].str.replace(':', '').str.strip()

    # Nettoyer la colonne 'Value' en appliquant strip() si l'élément correspond à une chaîne de caractères
    df_report.iloc[:, 1] = df_report.iloc[:, 1].apply(lambda x: x.strip() if isinstance(x, str) else x)

    # Renommer les colonnes
    df_report.columns = ['Logbook_name', 'Value']

    # Appliquer un filtre pour les caractères spéciaux dans la colonne 'Logbook_name'
    df_report['Logbook_name'] = remove_spec_char_from_list(df_report['Logbook_name'])

    # Supprimer les espaces supplémentaires dans la colonne 'Logbook_name'
    df_report['Logbook_name'] = df_report['Logbook_name'].str.strip()
    
    return df_report

def extract_gear_info(df_donnees):
    """
    Extraction des cases 'Gear'

    Args:
        df_donnees (df): excel p1

    Returns:
        df
    """
     # On extrait les données 
    df_gear = df_donnees.iloc[12:16, 11:21]

    # On supprimes les colonnes qui sont vides
    df_gear = del_empty_col(df_gear)

    # Nettoyer la colonne 'Logbook_name' en enlevant les espaces et les ':'
    df_gear.iloc[:, 0] = df_gear.iloc[:, 0].str.replace(':', '').str.strip()

    # Nettoyer la colonne 'Value' en appliquant strip() si l'élément correspond à une chaîne de caractères
    df_gear.iloc[:, 1] = df_gear.iloc[:, 1].apply(lambda x: x.strip() if isinstance(x, str) else x)

    # Renommer les colonnes
    df_gear.columns = ['Logbook_name', 'Value']

    # Appliquer un filtre pour les caractères spéciaux dans la colonne 'Logbook_name'
    df_gear['Logbook_name'] = remove_spec_char_from_list(df_gear['Logbook_name'])

    # Supprimer les espaces supplémentaires dans la colonne 'Logbook_name'
    df_gear['Logbook_name'] = df_gear['Logbook_name'].str.strip()
    
    # On vérifie que les données du excel sont des entiers
    toutes_int = df_gear['Value'].apply(lambda cellule: isinstance(cellule, int)).all()
    if toutes_int:
        # Applique la fonction vect si toutes les cellules sont des entiers
        df_gear['Value'] = np.vectorize(strip_if_string)(df_gear['Value'])

    if not df_gear['Value'].apply(lambda x: isinstance(x, int)).all():
        message = _("Les données remplies dans le fichier soumis ne correspondent pas au type de données attendues. Ici on attend seulement des entiers.")
        return df_gear, message

    return df_gear

def extract_line_material(df_donnees):
    """
    Extraction des cases 'Gear'

    Args:
        df_donnees (df): excel p1

    Returns:
        df
    """
    # On extrait les données
    df_line = df_donnees.iloc[12:16, 21:29]

    # On supprimes les colonnes qui sont vides
    df_line = del_empty_col(df_line)

    # Nettoyer la colonne 'Logbook_name' en enlevant les espaces et les ':'
    df_line.iloc[:, 0] = df_line.iloc[:, 0].str.replace(':', '').str.strip()

    # Nettoyer la colonne 'Value' en appliquant strip() si l'élément correspond à une chaîne de caractères
    df_line.iloc[:, 1] = df_line.iloc[:, 1].apply(lambda x: x.strip() if isinstance(x, str) else x)
    
    # Renommer les colonnes
    df_line.columns = ['Logbook_name', 'Value']

    # Appliquer un filtre pour les caractères spéciaux dans la colonne 'Logbook_name'
    df_line['Logbook_name'] = remove_spec_char_from_list(df_line['Logbook_name'])

    # Supprimer les espaces supplémentaires dans la colonne 'Logbook_name'
    df_line['Logbook_name'] = df_line['Logbook_name'].str.strip()
    
    # Filtrer les lignes qui sont cochées
    df_line_used = df_line.loc[df_line['Value'] != "None"]

    # Traduire chaque valeur du DataFrame df_line_used
    # df_line_used['Logbook_name'] = df_line_used['Logbook_name'].apply(
    #     lambda x: _(x) if isinstance(x, str) else x)

    if len(df_line_used) > 1:
        message = _("Ici on n'attend qu'un seul matériau. Veuillez vérifier les données.")
        return df_line_used, message

    if len(df_line_used) == 0:
        message = _("La table entre les lignes 13 à 16 de la colonne 'AC' ne sont pas saisies. Veuillez vérifier les données.")
        return df_line_used, message

    return df_line_used

def extract_target_species(df_donnees):
    """
    Extraction des cases 'Target species'

    Args:
        df_donnees (df): excel p1

    Returns:
        df
    """
    # On extrait les données
    df_target = df_donnees.iloc[12:16, 29:34]

    # On supprimes les colonnes qui sont vides
    df_target = del_empty_col(df_target)

    # Nettoyer la colonne 'Logbook_name' en enlevant les espaces et les ':'
    df_target.iloc[:, 0] = df_target.iloc[:, 0].str.replace(':', '').str.strip()

    # Nettoyer la colonne 'Value' en appliquant strip() si l'élément correspond à une chaîne de caractères
    df_target.iloc[:, 1] = df_target.iloc[:, 1].apply(lambda x: x.strip() if isinstance(x, str) else x)
    
    # Renommer les colonnes
    df_target.columns = ['Logbook_name', 'Value']

    # Appliquer un filtre pour les caractères spéciaux dans la colonne 'Logbook_name'
    df_target['Logbook_name'] = remove_spec_char_from_list(df_target['Logbook_name'])

    # Supprimer les espaces supplémentaires dans la colonne 'Logbook_name'
    df_target['Logbook_name'] = df_target['Logbook_name'].str.strip()
    
    # Filtrer les lignes qui sont cochées
    df_target_used = pd.DataFrame()
    for index, row in df_target.iterrows():
        if row['Value'] is not None:
            df_target_used.loc[len(df_target_used), 'Logbook_name'] = df_target.loc[index, 'Logbook_name']
    
    return df_target_used

def extract_logbook_date(df_donnees):
    """
    Extraction des cases relatives au mois et à l'année du logbook

    Args:
        df_donnees (df): excel p1

    Returns:
        df
    """
    # On extrait les données propres au 'Vessel information'
    df_month = df_donnees.iloc[17, 5]
    df_year = df_donnees.iloc[17, 11]

    date = {'Logbook_name': ['Month', 'Year'],
            'Value': [int(df_month), int(df_year)]}
    df_date = pd.DataFrame(date)
    
    df_date['Logbook_name'] = remove_spec_char_from_list(df_date['Logbook_name'])

    return df_date

def extract_bait(df_donnees):
    """
    Extraction des cases relatives au type d'appât utilisé

    Args:
        df_donnees (df): excel p1

    Returns:
        df
    """
    # On extrait les données
    df_squid = df_donnees.iloc[19, 16]
    df_sardine = df_donnees.iloc[19, 20]
    df_mackerel = df_donnees.iloc[19, 24]
    df_muroaji = df_donnees.iloc[19, 28]
    df_other = df_donnees.iloc[19, 32]

    bait = {'Logbook_name': ['Squid', 'Sardine', 'Mackerel', 'Muroaji', 'Other'],
            'Value': [df_squid, df_sardine, df_mackerel, df_muroaji, df_other]}
    
    df_bait = pd.DataFrame(bait)
    
    # Filtrer les lignes qui sont cochées
    df_bait_used = pd.DataFrame()
    for index, row in df_bait.iterrows():
        if row['Value'] is not None:
            df_bait_used.loc[len(df_bait_used), 'Logbook_name'] = df_bait.loc[index, 'Logbook_name']
    
    return df_bait_used

def extract_positions(df_donnees):
    """
    Extraction des cases relatives aux données de position
    
    Args:
        df_donnees (df): excel p1

    Returns:
        df
    """
    data = df_donnees.iloc[24:55, :7]
    colnames = ['Day', 'Latitude_Degrees', 'Latitude_Minutes', 'Latitude_Direction',
                'Longitude_Degrees', 'Longitude_Minutes', 'Longitude_Direction']
    data.columns = colnames
    
    #  On converti les données de position en degrés décimal
    data['Latitude'] = dms_to_decimal(data['Latitude_Degrees'], data['Latitude_Minutes'], data['Latitude_Direction'])
    data['Longitude'] = dms_to_decimal(data['Longitude_Degrees'], data['Longitude_Minutes'], data['Longitude_Direction'])
    
    # Supprimer les lignes avec des valeurs nulles et conserver les colonnes d'intérêt
    data = data.dropna(subset=['Latitude', 'Longitude'])
    df_position = data[['Latitude', 'Longitude']]
    
    # for index, row in df_position.iterrows():
    #     df_position.loc[index, 'Latitude'] = round(pd.to_numeric(df_position.loc[index, 'Latitude'], errors='coerce'), 2)
    #     df_position.loc[index, 'Longitude'] = round(pd.to_numeric(df_position.loc[index, 'Longitude'], errors='coerce'), 2)
    
    df_position.reset_index(drop=True, inplace=True)

    return df_position

def get_vessel_activity_topiaid(startTimeStamp, data_ll):
    '''
    Fonction qui prend en argument une heure de depart
    et qui donne un topiaID de VesselActivity en fonction du type et du contenu de l'entrée
    cad si'il y a une heure - on est en activité de pêche,
    En revanche si c'est du texte qui contient "CRUIS" alors on est en cruise, 
    et s'il contient 'PORT' alors le bateau est au port 
    'FISHING
    '''
    if ":" in str(startTimeStamp):
        code = "FO"

    elif 'cruis' or 'no fishing' in startTimeStamp.lower():
        code = "CRUISE"

    elif 'port' in startTimeStamp.lower():
        code = "PORT"

    elif startTimeStamp is None:
        return None

    else:
        code = "OTH"

    vessel_activities = data_ll["content"]["fr.ird.observe.entities.referential.ll.common.VesselActivity"]
    for vessel_activity in vessel_activities:
        if vessel_activity.get("code") == code:
            return vessel_activity["topiaId"], vessel_activity["label1"]

    return None

def extract_time(df_donnees, data_ll):
    """
    Extraction des cases relatives aux horaires des coups de pêche
    
    Args:
        df_donnees (df): excel p1

    Returns:
        df: type horaire, sauf si le bateau est en mouvement
    """
    day = df_donnees.iloc[24:55, 0]
    df_time = df_donnees.iloc[24:55, 7:8]
    colnames = ['Time']
    df_time.columns = colnames
    df_time['Time'] = df_time['Time'].apply(convert_to_time_or_text)

    df_time.reset_index(drop=True, inplace=True)

    vessel_activities = np.empty((len(day), 1), dtype=object)
    for ligne in range(len(day)):
        vessel_activity = get_vessel_activity_topiaid(
            df_time.iloc[ligne]['Time'], data_ll)
        vessel_activities[ligne, 0] = vessel_activity[0]
    np_time = np.column_stack((day, df_time, vessel_activities))
    df_time = pd.DataFrame(np_time, columns=['Day', 'Time', 'VesselActivity'])

    return df_time

def extract_temperature(df_donnees):
    """
    Extraction des cases relatives aux températures
    
    Args:
        df_donnees (df): excel p1

    Returns:
        df
    """
    df_temp = df_donnees.iloc[24:55, 8:9]
    colnames = ['Température']
    df_temp.columns = colnames
    df_temp.reset_index(drop=True, inplace=True)
    return df_temp

def extract_fishing_effort(df_donnees):
    """
    Extraction des cases relatives aux efforts de pêche
    
    Args:
        df_donnees (df): excel p1

    Returns:
        df
    """
    df_fishing_effort = df_donnees.iloc[24:55, [0, 9, 10, 11]].copy()
    df_fishing_effort.columns = ['Day', 'Hooks per basket', 'Total hooks', 'Total lightsticks']
    df_fishing_effort['Total hooks / Hooks per basket'] = df_fishing_effort['Total hooks'] / df_fishing_effort['Hooks per basket']
    df_fishing_effort.reset_index(drop=True, inplace=True)
    return df_fishing_effort

def extract_fish_p1(df_donnees):
    """
    Extraction des cases relatives à ce qui a été pêché
    
    Args:
        df_donnees (df): excel p1

    Returns:
        df
    """
    df_fishes = df_donnees.iloc[24:55, 12:36]

    colnames = ['No RET SBF', 'Kg RET SBF',
                'No RET ALB', 'Kg RET ALB',
                'No RET BET', 'Kg RET BET',
                'No RET YFT', 'Kg RET YFT', 
                'No RET SWO', 'Kg RET SWO',
                'No RET MLS', 'Kg RET MLS',
                'No RET BUM', 'Kg RET BUM',
                'No RET BLM', 'Kg RET BLM',
                'No RET SFA', 'Kg RET SFA',
                'No RET SSP', 'Kg RET SSP', 
                'No RET OIL', 'Kg RET OIL',
                'No RET XXX', 'Kg RET XXX']
    
    df_fishes.columns = colnames
    df_fishes = df_fishes.map(zero_if_empty)
    df_fishes.reset_index(drop=True, inplace=True)
    
    return df_fishes
    
def extract_bycatch_p2(df_donnees):
    """
    Extraction des cases relatives à ce qui a été pêché mais accessoires    
    
    Args:
        df_donnees (df): excel p2

    Returns:
        df
    """
    df_bycatch = df_donnees.iloc[15:46, 1:39]

    colnames = ['No RET FAL', 'Kg RET FAL',
                'No ESC FAL', 'No DIS FAL',
                'No RET BSH', 'Kg RET BSH',
                'No ESC BSH', 'No DIS BSH',
                'No RET MAK', 'Kg RET MAK',
                'No ESC MAK', 'No DIS MAK',
                'No RET MSK', 'Kg RET MSK',
                'No ESC MSK', 'No DIS MSK', 
                'No RET SPN', 'Kg RET SPN',
                'No ESC SPN', 'No DIS SPN', 
                'No RET TIG', 'Kg RET TIG',
                'No ESC TIG', 'No DIS TIG', 
                'No RET PSK', 'Kg RET PSK',
                'No ESC PSK', 'No DIS PSK',
                'No ESC THR', 'No DIS THR',
                'No ESC OCS', 'No DIS OCS', 
                'No ESC MAM', 'No DIS MAM', 
                'No ESC SBD', 'No DIS SBD',
                'No ESC TTX', 'No DIS TTX']
    
    df_bycatch.columns = colnames
    df_bycatch = df_bycatch.map(zero_if_empty)
    df_bycatch.reset_index(drop=True, inplace=True)
    
    return df_bycatch
    
    
def extract_tunas(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les tunas 
    '''
    df_tunas = df_donnees.iloc[24:55, 12:20]
    colnames = ['No RET SBF', 'Kg RET SBF',
                'No RET ALB', 'Kg RET ALB',
                'No RET BET', 'Kg RET BET',
                'No RET YFT', 'Kg RET YFT']
    df_tunas.columns = colnames
    # print(df_tunas)
    df_tunas = df_tunas.map(strip_if_string)
    df_tunas = df_tunas.map(zero_if_empty)
    # print(df_tunas)
    df_tunas.reset_index(drop=True, inplace=True)
    return df_tunas


def extract_billfishes(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les billfishes 
    '''
    df_billfishies = df_donnees.iloc[24:55, 20:32]
    colnames = ['No RET SWO', 'Kg RET SWO',
                'No RET MLS', 'Kg RET MLS',
                'No RET BUM', 'Kg RET BUM',
                'No RET BLM', 'Kg RET BLM',
                'No RET SFA', 'Kg RET SFA',
                'No RET SSP', 'Kg RET SSP']
    df_billfishies.columns = colnames

    df_billfishies = df_billfishies.map(zero_if_empty)

    df_billfishies.reset_index(drop=True, inplace=True)
    return df_billfishies


def extract_otherfish(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les autres poissons 
    '''
    df_otherfish = df_donnees.iloc[24:55, 32:36]
    colnames = ['No RET OIL', 'Kg RET OIL',
                'No RET XXX', 'Kg RET XXX']
    df_otherfish.columns = colnames

    df_otherfish = df_otherfish.map(zero_if_empty)

    df_otherfish.reset_index(drop=True, inplace=True)
    return df_otherfish


def extract_sharksFAL(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les blacks sharks 
    '''
    df_sharksFAL = df_donnees.iloc[15:46, 1:5]
    colnames = ['No RET FAL', 'Kg RET FAL',
                'No ESC FAL', 'No DIS FAL']
    df_sharksFAL.columns = colnames

    df_sharksFAL = df_sharksFAL.map(zero_if_empty)

    df_sharksFAL.reset_index(drop=True, inplace=True)
    return df_sharksFAL


def extract_sharksBSH(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les blue sharks 
    '''
    df_sharksBSH = df_donnees.iloc[15:46, 5:9]
    colnames = ['No RET BSH', 'Kg RET BSH',
                'No ESC BSH', 'No DIS BSH']
    df_sharksBSH.columns = colnames

    df_sharksBSH = df_sharksBSH.map(zero_if_empty)

    df_sharksBSH.reset_index(drop=True, inplace=True)
    return df_sharksBSH


def extract_sharksMAK(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les Mako 
    '''
    df_sharksMAK = df_donnees.iloc[15:46, 9:13]
    colnames = ['No RET MAK', 'Kg RET MAK',
                'No ESC MAK', 'No DIS MAK']
    df_sharksMAK.columns = colnames

    df_sharksMAK = df_sharksMAK.map(zero_if_empty)

    df_sharksMAK.reset_index(drop=True, inplace=True)
    return df_sharksMAK


def extract_sharksMSK(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les hammer head sharks 
    '''
    df_sharksSPN = df_donnees.iloc[15:46, 13:17]
    colnames = ['No RET MSK', 'Kg RET MSK',
                'No ESC MSK', 'No DIS MSK']
    df_sharksSPN.columns = colnames

    df_sharksSPN = df_sharksSPN.map(zero_if_empty)

    df_sharksSPN.reset_index(drop=True, inplace=True)
    return df_sharksSPN


def extract_sharksSPN(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les hammer head sharks 
    '''
    df_sharksSPN = df_donnees.iloc[15:46, 17:21]
    colnames = ['No RET SPN', 'Kg RET SPN',
                'No ESC SPN', 'No DIS SPN']
    df_sharksSPN.columns = colnames

    df_sharksSPN = df_sharksSPN.map(zero_if_empty)

    df_sharksSPN.reset_index(drop=True, inplace=True)
    return df_sharksSPN


def extract_sharksTIG(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les tiger sharks 
    '''
    df_sharksTIG = df_donnees.iloc[15:46, 21:25]
    colnames = ['No RET TIG', 'Kg RET TIG',
                'No ESC TIG', 'No DIS TIG']
    df_sharksTIG.columns = colnames

    df_sharksTIG = df_sharksTIG.map(zero_if_empty)

    df_sharksTIG.reset_index(drop=True, inplace=True)
    return df_sharksTIG


def extract_sharksPSK(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les crocodile sharks 
    '''
    df_sharksPSK = df_donnees.iloc[15:46, 25:29]
    colnames = ['No RET PSK', 'Kg RET PSK',
                'No ESC PSK', 'No DIS PSK']

    df_sharksPSK.columns = colnames

    df_sharksPSK = df_sharksPSK.map(zero_if_empty)

    df_sharksPSK.reset_index(drop=True, inplace=True)
    return df_sharksPSK


def extract_sharksTHR(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les thresher sharks 
    '''
    df_sharksFAL = df_donnees.iloc[15:46, 29:31]
    colnames = ['No ESC THR', 'No DIS THR']
    df_sharksFAL.columns = colnames

    df_sharksFAL = df_sharksFAL.map(zero_if_empty)

    df_sharksFAL.reset_index(drop=True, inplace=True)
    return df_sharksFAL


def extract_sharksOCS(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les oceanic sharks 
    '''
    df_sharksOCS = df_donnees.iloc[15:46, 31:33]
    colnames = ['No ESC OCS', 'No DIS OCS']
    df_sharksOCS.columns = colnames

    df_sharksOCS = df_sharksOCS.map(zero_if_empty)

    df_sharksOCS.reset_index(drop=True, inplace=True)
    return df_sharksOCS


def extract_mammals(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les autres mammifères marins 
    '''
    df_mammals = df_donnees.iloc[15:46, 33:35]
    colnames = ['No ESC MAM', 'No DIS MAM']
    df_mammals.columns = colnames
    df_mammals = df_mammals.map(zero_if_empty)

    df_mammals.reset_index(drop=True, inplace=True)
    return df_mammals


def extract_seabird(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les sea birds
    '''
    df_seabird = df_donnees.iloc[15:46, 35:37]
    colnames = ['No ESC SBD', 'No DIS SBD']
    df_seabird.columns = colnames

    df_seabird = df_seabird.map(zero_if_empty)

    df_seabird.reset_index(drop=True, inplace=True)
    return df_seabird


def extract_turtles(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les infos sur les torutes 
    '''
    df_turtles = df_donnees.iloc[15:46, 37:39]
    colnames = ['No ESC TTX', 'No DIS TTX']
    df_turtles.columns = colnames

    df_turtles = df_turtles.map(zero_if_empty)

    df_turtles.reset_index(drop=True, inplace=True)
    return df_turtles


def get_list_harbours(data_common):
    """
    Args:
        data_common

    Returns:
        list: all the enabled ports (topiaId and label2)
    """
    harbours = data_common["content"]["fr.ird.observe.entities.referential.common.Harbour"]
    list_harbours = []
    for harbour in harbours:
        if harbour.get('status') == 'enabled':
            list_harbours.append({'topiaId': harbour.get(
                'topiaId'), 'label2': harbour.get('label2')})
    sorted_list_harbours = sorted(list_harbours, key=lambda x: x['label2'])
    return sorted_list_harbours

def research_dep(df_donnees_p1, data_ll, startDate):
    """
    Fonction qui recherche si 'dep' est présent dans la case à la date donnée par l'utilisateur

    Args:
        df_donnees_p1 (dataframe): _description_
        data_ll (dataframe): données de références
        startDate (date): saisie par l'utilisateur quand on créé une marée

    Returns:
        bool: True si la date saisie correspond à un departure, False si non
    """
    data = extract_time(df_donnees=df_donnees_p1, data_ll=data_ll)
    # print("#"*20, "research_dep function", "#"*20)
    day = startDate[8:10] 
    dep_rows = data[data['Time'].str.lower().str.contains('dep', case=False, na=False)]
    
    if not dep_rows.empty:
        dep_dates = dep_rows['Day']
        return str(dep_dates.values[0]) in str(day)
    else:
        return False
    

def get_previous_trip_infos2(request, df_donnees_p1, data_common):
    """Fonction qui va faire appel au WS pour :
    1) trouver l'id du trip le plus récent pour un vessel et un programme donné
    et 2) trouver les informations rattachées à ce trip

    Args:
        request (_type_): _description_
        df_donnees_p1 (_type_): _description_

    Returns:
        dictionnaire: startDate, endDate, captain
    """

    token = api.get_token()
    url_base = 'https://observe.ob7.ird.fr/observeweb/api/public'

    # les topiaid envoyés au WS doivent être avec des '-' à la place des '#'
    vessel_topiaid = json_construction.get_vessel_topiaid(
        df_donnees_p1, data_common)
    # Pour le webservice, il faut remplacer les # par des - dans les topiaid
    vessel_topiaid_ws = vessel_topiaid.replace("#", "-")
    programme_topiaid = request.session.get('dico_config')['programme']
    programme_topiaid_ws = programme_topiaid.replace("#", "-")

    print("="*20, vessel_topiaid_ws, "="*20)
    print("="*20, programme_topiaid_ws, "="*20)

    previous_trip = api.trip_for_prog_vessel(
        token, url_base, vessel_topiaid_ws, programme_topiaid_ws)
    # on récupères les informations uniquement pour le trip avec la endDate la plus récente
    parsed_previous_trip = json.loads(previous_trip.decode('utf-8'))

    if parsed_previous_trip['content'] != []:
        # Prévoir le cas ou le vessel n'a pas fait de trip avant
        trip_topiaid = parsed_previous_trip['content'][0]['topiaId'].replace(
            "#", "-")
        print("="*20, trip_topiaid, "="*20)

        # on récupère les infos du trip enregistré dans un fichier json
        api.get_one(token, url_base, trip_topiaid)

        json_previoustrip = api.load_json_file("previoustrip.json")
        # print(json_previoustrip)

        # On récupère les infos que l'on voudra afficher
        trip_info = json_previoustrip['content'][0]

        captain_name = from_topiaid_to_value(topiaid=trip_info['captain'],
                                             lookingfor='Person',
                                             label_output='lastName',
                                             domaine=None)

        vessel_name = from_topiaid_to_value(topiaid=vessel_topiaid,
                                            lookingfor='Vessel',
                                            label_output='label2',
                                            domaine=None)

        dico_trip_infos = {'startDate': trip_info['startDate'],
                           'endDate': trip_info['endDate'],
                           'captain': captain_name,
                           'vessel': vessel_name,
                           'triptopiaid': trip_topiaid}

        try:
            departure_harbour = from_topiaid_to_value(topiaid=trip_info['departureHarbour'],
                                                      lookingfor='Harbour',
                                                      label_output='label2',
                                                      domaine=None)

            dico_trip_infos.update({
                'depPort': departure_harbour,
                'depPort_topiaid': trip_info['departureHarbour'],
            })

        except KeyError:
            # departure_harbour = 'null'

            dico_trip_infos.update({
                'depPort': 'null',
                'depPort_topiaid': 'null',
            })

        return dico_trip_infos

    else:
        return None


def get_previous_trip_infos(request, df_donnees_p1, data_common):
    """Fonction qui va faire appel au WS pour :
    1) trouver l'id du trip le plus récent pour un vessel et un programme donné
    et 2) trouver les informations rattachées à ce trip

    Args:
        request (_type_): _description_
        df_donnees_p1 (_type_): _description_

    Returns:
        dictionnaire: startDate, endDate, captain
    """

    token = api.get_token()
    url_base = 'https://observe.ob7.ird.fr/observeweb/api/public'

    # les topiaid envoyés au WS doivent être avec des '-' à la place des '#'
    vessel_topiaid = json_construction.get_vessel_topiaid(df_donnees_p1, data_common)
    # Pour le webservice, il faut remplacer les # par des - dans les topiaid
    vessel_topiaid_WS = vessel_topiaid.replace("#", "-")
    programme_topiaid = request.session.get('dico_config')['programme']
    programme_topiaid_WS = programme_topiaid.replace("#", "-")

    # print("="*20, vessel_topiaid_WS, "="*20)
    # print("="*20, programme_topiaid_WS, "="*20)

    previous_trip = api.trip_for_prog_vessel(token, url_base, vessel_topiaid_WS, programme_topiaid_WS)
    
    # on récupères les informations uniquement pour le trip avec la endDate la plus récente
    parsed_previous_trip = json.loads(previous_trip.decode('utf-8'))

    if parsed_previous_trip['content'] != []:
        # Prévoir le cas ou le vessel n'a pas fait de trip avant
        print("pour ce programme et ce vessel on a : ", len(parsed_previous_trip['content']), "trip enregistrés")
        
        df_trip = pd.DataFrame(columns=["triptopiaid", "startDate", "depPort_topiad", "depPort", "endDate", "endPort_topiaid", "endPort", "ocean"])


        for num_trip in range(len(parsed_previous_trip['content'])):
            # print("boucle for, essai : ", num_trip)
            trip_topiaid = parsed_previous_trip['content'][num_trip]['topiaId'].replace("#", "-")
            # print("="*20, trip_topiaid, "="*20)
            trip_info = json.loads(api.get_trip(token, url_base, trip_topiaid).decode('utf-8'))
            # print(trip_info)
            # parsed_trip_info = json.loads(trip_info.decode('utf-8'))
            if 'departureHarbour' in trip_info['content'][0]:
                depPort = trip_info['content'][0]['departureHarbour']
                depPort_name = from_topiaid_to_value(topiaid=depPort,
                                  lookingfor='Harbour',
                                  label_output='label2',
                                  domaine=None)
            else : 
                depPort = None
                depPort_name = None
            
            if 'landingHarbour' in trip_info['content'][0]:
                endPort = trip_info['content'][0]['landingHarbour']
                endPort_name = from_topiaid_to_value(topiaid=endPort,
                                  lookingfor='Harbour',
                                  label_output='label2',
                                  domaine=None)
            else : 
                endPort = None
                endPort_name = None
            
            ocean = from_topiaid_to_value(topiaid=trip_info['content'][0]['ocean'],
                                  lookingfor='Ocean',
                                  label_output='label2',
                                  domaine=None)
        
            trip_info_row = [trip_info['content'][0]['topiaId'], 
                            trip_info['content'][0]['startDate'],
                            depPort, 
                            depPort_name, 
                            trip_info['content'][0]['endDate'],
                            endPort,
                            endPort_name,
                            ocean]
            
            df_trip.loc[num_trip] = trip_info_row
            
        ####### Optimisation GPT 
        # trips_info = []

        # for trip in parsed_previous_trip['content']:
        #     trip_topiaid = trip['topiaId'].replace("#", "-")
        #     trip_info = json.loads(api.get_trip(token, url_base, trip_topiaid).decode('utf-8'))
        #     trip_data = trip_info['content'][0]

        #     depPort = trip_data.get('departureHarbour')
        #     depPort_name = None
        #     if depPort:
        #         depPort_name = from_topiaid_to_value(topiaid=depPort,
        #                                               lookingfor='Harbour',
        #                                               label_output='label2',
        #                                               domaine=None)

        #     endPort = trip_data.get('landingHarbour')
        #     endPort_name = None
        #     if endPort:
        #         endPort_name = from_topiaid_to_value(topiaid=endPort,
        #                                               lookingfor='Harbour',
        #                                               label_output='label2',
        #                                               domaine=None)

        #     ocean = from_topiaid_to_value(topiaid=trip_data['ocean'],
        #                                   lookingfor='Ocean',
        #                                   label_output='label2',
        #                                   domaine=None)

        #     trip_info_row = [trip_data['topiaId'], 
        #                      trip_data['startDate'],
        #                      depPort, 
        #                      depPort_name, 
        #                      trip_data['endDate'],
        #                      endPort,
        #                      endPort_name,
        #                      ocean]

        #     trips_info.append(trip_info_row)

        # df_trip = pd.DataFrame(trips_info, columns=["triptopiaid", "startDate", "depPort_topiad", "depPort", "endDate", "endPort_topiaid", "endPort", "ocean"])
        
    
        return(df_trip)
    
    # else:
    #     return None



DIR = "./media/logbooks"


def presenting_previous_trip(request):


    if 'context' in request.session:
        # print("+"*50, "Avant que tout commence", "+"*50)
        # print(request.session['context'])
        # print("+"*50, "Avant que tout commence", "+"*50)
        del request.session['context'] 
        
    selected_file = request.GET.get('selected_file')
    apply_conf = request.session.get('dico_config')

    print("="*20, "presenting_previous_trip", "="*20)
    # print("apply conf : ", apply_conf)

    programme = from_topiaid_to_value(topiaid=apply_conf['programme'],
                                      lookingfor='Program',
                                      label_output='label2',
                                      domaine='palangre')

    ocean = from_topiaid_to_value(topiaid=apply_conf['ocean'],
                                  lookingfor='Ocean',
                                  label_output='label2',
                                  domaine=None)

    context = {'domaine': apply_conf['domaine'],
                'program': programme,
                'programtopiaid' : apply_conf['programme'],
                'ocean': ocean, 
                'oceantopiaid': apply_conf['ocean']}

    if selected_file is not None and apply_conf is not None:

        file_name = selected_file.strip("['']")
        file_path = DIR + "/" + file_name

        request.session['file_path'] = file_path

        print("="*20, "presenting_previous_trip selected_file", "="*20)
        print(file_path)

        df_donnees_p1 = read_excel(file_path, 1)

        with open('./data_common.json', 'r', encoding='utf-8') as f:
            data_common = json.load(f)


        try :
            start_time = time.time()
            df_previous_trip = get_previous_trip_infos(request, df_donnees_p1, data_common)
            end_time = time.time()
            
            
            print("Temps d'exécution:", end_time - start_time, "secondes")
            print("°"*20, "presenting_previous_trip - context updated", "°"*20)
            context.update({'df_previous': df_previous_trip})
        
        except :
            context.update({'df_previous': None})
            
    
    request.session['context'] = context
    return render(request, 'LL_previoustrippage.html', context)


def checking_logbook(request):
    """
    Fonction qui 
    1) affiche les données extraites du logbook soumis 
    2) vérifie et valide les données saisies par l'utilisateur

    Args:
        request 

    Returns:
        Si les données soumises ne sont pas cohérentes : on retourne la meme page avec un message d'erreur adapté 
        Si non : on envoie le logbook
    """
    
    print("="*20, "checking_logbook", "="*20)

    with open('./data_common.json', 'r', encoding='utf-8') as f:
        data_common = json.load(f)
        
    with open('./data_ll.json', 'r', encoding='utf-8') as f:
        data_ll = json.load(f)
        
    token = api.get_token()
    url_base = 'https://observe.ob7.ird.fr/observeweb/api/public'

    if request.method == 'POST':
    
        apply_conf = request.session.get('dico_config')
        print("apply_conf : ", apply_conf)
        continuetrip = request.POST.get('continuetrip')
        context = request.session.get('context')
        print("+"*50, "Juste après le post", "+"*50)
        print(context)
        print("+"*50, "END Juste après le post", "+"*50)
        
        
        #_______________________________EXTRACTION DES DONNEES__________________________________
        file_path = request.session.get('file_path')
                
        df_donnees_p1 = read_excel(file_path, 1)
        df_donnees_p2 = read_excel(file_path, 2)
        
        df_vessel = extract_vessel_info(df_donnees_p1)
        df_cruise = extract_cruise_info(df_donnees_p1)
        df_report = extract_report_info(df_donnees_p1)
        df_gear = extract_gear_info(df_donnees_p1)
        df_line = extract_line_material(df_donnees_p1)
        df_target = extract_target_species(df_donnees_p1)
        df_date = extract_logbook_date(df_donnees_p1)
        df_bait = extract_bait(df_donnees_p1)
        df_fishing_effort = extract_fishing_effort(df_donnees_p1)
        df_position = extract_positions(df_donnees_p1)
        df_time = extract_time(df_donnees_p1, data_ll)
        df_temperature = extract_temperature(df_donnees_p1)
        df_fishes = extract_fish_p1(df_donnees_p1)
        df_bycatch = extract_bycatch_p2(df_donnees_p2)


        df_activity = pd.concat([df_fishing_effort.loc[:,'Day'], df_position, df_time.loc[:, 'Time'], df_temperature,
                                df_fishing_effort.loc[:,['Hooks per basket', 'Total hooks', 'Total lightsticks']],
                                df_fishes,
                                df_bycatch],
                                axis=1)

        list_ports = get_list_harbours(data_common)
        
        data_to_homepage = {
            'df_vessel': df_vessel,
            'df_cruise': df_cruise,
            'list_ports': list_ports,
            'df_report': df_report,
            'df_gear': df_gear,
            'df_line': df_line,
            'df_target': df_target,
            'df_date': df_date,
            'df_bait': df_bait,
            'df_position': df_position,
            'df_time': df_time,
            'df_activity': df_activity,}
        #_______________________________EXTRACTION DES DONNEES__________________________________
        
        
        startDate = request.POST.get('startDate')
        depPort = request.POST.get('depPort')
        endDate = request.POST.get('endDate')
        endPort = request.POST.get('endPort')
        
        print("="*20, "data collected before validation", "="*20)
        print("startDate ", startDate)
        print("endDate ", endDate)
        print("depPort ", depPort)
        print("endPort ", endPort)
        
        ######### Si on a rempli les données demandées, on vérifie ce qui a été saisi
        if endDate is not None :
            print("+"*50, "phase de validation", "+"*50)
            print(context)
            print("+"*50, "END phase de validation", "+"*50)
            
            probleme = False
            
            logbook_month = str(df_date.loc[df_date['Logbook_name'] == 'Month', 'Value'].values[0])
            logbook_year = str(df_date.loc[df_date['Logbook_name'] == 'Year', 'Value'].values[0])
            
            
            context.update({'endDate' : json_construction.create_starttimestamp_from_field_date(endDate),
                            'endPort': endPort if endPort != '' else None})
            
            #############################
            # messages d'erreurs
            if (int(context['endDate'][5:7]) + int(context['endDate'][:4])) != (int(logbook_month) + int(logbook_year)):
                messages.error(request, _("La date de fin de trip doit être dans le mois. Saisir le dernier jour du mois dans le cas où le trip n'est pas réellement fini."))
                probleme = True
            #############################
            
            #############################
            # messages d'erreurs
            if isinstance(df_gear, tuple):
                messages.error(request, _("Les informations concernant la longueur du matériel de pêche doivent être des entiers."))
                probleme = True
            #############################
            
            
            
            if context['df_previous'] == None:
                # NOUVELLE MAREE
                context.update({'startDate': json_construction.create_starttimestamp_from_field_date(startDate), 
                                'depPort': depPort,
                                'endDate' : json_construction.create_starttimestamp_from_field_date(endDate),
                                'endPort': endPort if endPort != '' else None
                                })
                
                #############################
                is_dep_match = research_dep(df_donnees_p1, data_ll, startDate)
                print(is_dep_match)
                if is_dep_match is False:
                    messages.warning(request, _("La date de début de marée que vous avez saisie ne semble pas correspondre à une activité 'departure' du logbook. Vérifiez les données."))
                    probleme = True
                #############################
                
            else:
                # CONTINUE TRIP

                with open ('./previoustrip.json', 'r', encoding='utf-8') as f:
                    json_previoustrip = json.load(f)
                
                # On récupère la date du jour 1 au bon format
                if df_time.loc[0, 'VesselActivity'] == "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1":
                    # Si c'est une fishing operation
                    date = json_construction.create_starttimestamp(df_donnees_p1, data_ll, 0, True)
                else:
                    date = json_construction.create_starttimestamp(df_donnees_p1, data_ll, 0, False)

                #############################
                # messages d'erreurs
                if json_construction.search_date_into_json(json_previoustrip['content'], date) is True:
                    messages.warning(request, _("Le logbook soumis n'a pas pu être saisi dans la base de données car il a déjà été envoyé dans un précédent trip. Merci de vérifier sur l'application"))
                    probleme = True

                elif (int(context['df_previous']['endDate'][5:7]) + int(context['df_previous']['endDate'][:4]) + 1) != (int(logbook_month) + int(logbook_year)):
                    print(int(context['endDate'][5:7]) + int(context['endDate'][:4]) + 1, "!=", int(logbook_month) + int(logbook_year))
                    probleme = True
                    messages.warning(request, _("Le logbook soumis n'a pas pu être saisi dans la base de données car il n'est pas consécutif à la marée précédente"))
                #############################
                
                context.update({'startDate': context['df_previous']['startDate'], 
                                'depPort': context['df_previous']['depPort_topiaid'],
                                'endDate' : json_construction.create_starttimestamp_from_field_date(endDate),
                                'endPort': endPort if endPort != '' else None})

            if probleme is True:
                # on doit ajouter les infos quand meme 
                data_to_homepage.update({'programme': context['program'],
                                        'ocean': context['ocean'],})
                
                if context['df_previous'] is not None : 
                    data_to_homepage.update({'previous_trip': context['df_previous'],
                            'continuetrip': context['continuetrip'],})
                
                return render(request, 'LL_homepage.html', data_to_homepage)
            
            else :
                return send_logbook2observe(request)
                
              
        print("continue the trip : ", continuetrip)
        
        programme = from_topiaid_to_value(topiaid=apply_conf['programme'],
                                      lookingfor='Program',
                                      label_output='label2',
                                      domaine='palangre')

        ocean = from_topiaid_to_value(topiaid=apply_conf['ocean'],
                                        lookingfor='Ocean',
                                        label_output='label2',
                                        domaine=None)

        context = {'domaine': apply_conf['domaine'],
                    'program': programme,
                    'programtopiaid' : apply_conf['programme'],
                    'ocean': ocean, 
                    'oceantopiaid': apply_conf['ocean']}
        
            
        # si on contiue un trip, on récupère ses infos pour les afficher
        # if continuetrip is not None and request.POST.get('radio_previoustrip') is not None: 
        if continuetrip is not None and 'radio_previoustrip' in request.POST:    
            # si on a choisi de continuer un trip 
            triptopiaid = request.POST.get('radio_previoustrip')         
            trip_topiaid_ws = triptopiaid.replace("#", "-")
            print("="*20, trip_topiaid_ws, "="*20)

            # on récupère les infos du trip enregistré dans un fichier json
            api.get_one(token, url_base, trip_topiaid_ws)
            
            json_previoustrip = api.load_json_file("previoustrip.json")
            
            # On récupère les infos qu'on veut afficher
            trip_info = json_previoustrip['content'][0]

            captain_name = from_topiaid_to_value(topiaid=trip_info['captain'],
                                                  lookingfor='Person',
                                                  label_output='lastName',
                                                  domaine=None)

            vessel_name = from_topiaid_to_value(topiaid=trip_info['vessel'],
                                                 lookingfor='Vessel',
                                                 label_output='label2',
                                                 domaine=None)

            dico_trip_infos = {'startDate': trip_info['startDate'],
                                'endDate': trip_info['endDate'],
                                'captain': captain_name,
                                'vessel': vessel_name,
                                'triptopiaid': triptopiaid}

            try:
                departure_harbour = from_topiaid_to_value(topiaid=trip_info['departureHarbour'],
                                                        lookingfor='Harbour',
                                                        label_output='label2',
                                                        domaine=None)

                dico_trip_infos.update({
                    'depPort': departure_harbour,
                    'depPort_topiaid': trip_info['departureHarbour'],
                })

            except KeyError:
               # en théorie devrait plus y avoir ce soucis car le departure harbour sera mis en champ obligatoire 
                dico_trip_infos.update({
                    'depPort': 'null',
                    'depPort_topiaid': 'null',
                })
        
        else : 
            dico_trip_infos = None
            continuetrip = None
        
        context.update({"df_previous" : dico_trip_infos,
                        "continuetrip": continuetrip})

        print("+"*50, "A la fin de la fonction", "+"*50)
        print(context)
        print("+"*50, "END A la fin de la fonction", "+"*50)


        data_to_homepage.update({
            'programme': context['program'],
            'ocean': context['ocean'],
            'previous_trip': dico_trip_infos,
            'continuetrip': continuetrip,
        })
    
        
        return render(request, 'LL_homepage.html', data_to_homepage)

    else:
        # Gérer le cas où la méthode HTTP n'est pas POST
        pass
    return render(request, 'LL_homepage.html')

 
def send_logbook2observe(request):
    warnings.simplefilter(action='ignore', category=FutureWarning)

    if request.method == 'POST':
        print("°"*20, "POST", "°"*20)

        file_path = request.session.get('file_path')
        context = request.session.get('context')

                
        resultat = None

        print("°"*40, context)
        
    
        if os.path.exists("sample.json"):
            os.remove("sample.json")

        print("="*80)
        print("Load JSON data file")

        token = api.get_token()
        print("token :", token)
        url_base = 'https://observe.ob7.ird.fr/observeweb/api/public'

        with open('./data_common.json', 'r', encoding='utf-8') as f:
            data_common = json.load(f)
        with open('./data_ll.json', 'r', encoding='utf-8') as f:
            data_ll = json.load(f)

        print("="*80)
        print("Read excel file")
        print(file_path)

        df_donnees_p1 = read_excel(file_path, 1)
        df_donnees_p2 = read_excel(file_path, 2)


        # on extrait les données du logbook sur tout le mois si la date de fin > au mois
        # sinon on extrait jusqu'a la endDate
       
        # On transforme pour que les données soient comparables
        logbook_month = str(extract_logbook_date(df_donnees_p1).loc[extract_logbook_date(df_donnees_p1)['Logbook_name'] == 'Month', 'Value'].values[0])

        if len(logbook_month) == 1:
            logbook_month = '0' + logbook_month
            print(logbook_month, type(logbook_month))
        else:
            logbook_month = str(logbook_month)
        
        # if context['df_previous'] is not None :
        #     startDate = context['df_previous']['startDate']
        # else : 
        #     startDate = context['startDate'] 
        
        startDate = context['startDate'] 
        
        if startDate[5:7] == logbook_month:
            start_extraction = int(startDate[8:10]) - 1
            if context['endDate'][5:7] == logbook_month:
                end_extraction = int(context['endDate'][8:10])
            else:
                end_extraction = len(extract_positions(df_donnees_p1))
        else:
            start_extraction = 0
            end_extraction = int(context['endDate'][8:10])
              
        if context['continuetrip'] is None:
            # NEW TRIP
            
            print("="*80)
            print("Create Activity and Set")
            
            MultipleActivity = json_construction.create_activity_and_set(
                df_donnees_p1, df_donnees_p2,
                data_common, data_ll,
                start_extraction, end_extraction)

            print("="*80)
            print("Create Trip")
            
            trip = json_construction.create_trip(
                df_donnees_p1, MultipleActivity, data_common, context)

            print("Creation of a new trip")
            resultat = api.send_trip(token, trip, url_base)
            print("resultats : ", resultat)

        else:   
            # CONTINUE THE TRIP 
                     
            with open ('./previoustrip.json', 'r', encoding='utf-8') as f:
                json_previoustrip = json.load(f)

            MultipleActivity = json_construction.create_activity_and_set(
                df_donnees_p1, df_donnees_p2, 
                data_common, data_ll, 
                start_extraction, end_extraction)

            print("="*80)
            print("Update Trip")

            trip = json_previoustrip['content']
            # On ajoute les acitivités du nouveau logbook
            for day in range(len(MultipleActivity)):
                trip[0]['activityLogbook'].append(MultipleActivity[day])
            
            
            trip[0]["endDate"] = context['endDate']
            if context['endPort'] is not None : 
                trip[0]["landingHarbour"] = context['endPort']

            # on homogénéise les données extraites de la base, et les nouvelles données qu'on implémente :
            trip = json_construction.replace_null_false_true(trip)
            trip = json_construction.remove_keys(trip, ["topiaId", "topiaCreateDate", "lastUpdateDate"])[0]
                                
            # permet de visualiser le fichier qu'on envoie
            json_formatted_str = json.dumps(json_construction.remove_keys(trip, ["topiaId", "topiaCreateDate", "lastUpdateDate"]),
                                            indent=2,
                                            default=api.serialize)
        
            with open(file="tripupdated.json", mode="w") as outfile:
                outfile.write(json_formatted_str)
                

            resultat = api.update_trip(token=token,
                            data=trip,
                            url_base=url_base,
                            topiaid=context['df_previous']['triptopiaid'].replace("#", "-"))
    
        
        if resultat == ("Logbook inséré avec success", 1) :
            messages.success(request, _("Le logbook a bien été envoyé dans la base"))
        
        else: 
            messages.error(request, _("Il doit y avoir une erreur dedans car le logbook n'a pas été envoyé"))

        return render(request, 'LL_send_data.html')

    else:
        # ajouter une page erreur d'envoi
        return render(request, 'LL_file_selection.html')
