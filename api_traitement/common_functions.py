# -*- coding: utf-8 -*-
""" 
#######################################################
#
# Module de fonctions communes et générales à l'application indépendamment de la pêcherie. 
#
#######################################################
"""
import json
import datetime
import re
import openpyxl
import pandas as pd
import numpy as np

def load_json_file(file_path):
    """ Fonction qui charge un fichier json enregistré dans un dossier donné en argument et le renvoie

    Args:
        file_path
        
    Returns:
        dict: fichier json en format dictionnaire
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file '{file_path}': {e}")
        return None
    
def serialize(obj): 
    """ 
    Serialize obj dans un format json de type date, int ou str.
    """
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    if isinstance(obj, np.int64) or isinstance(obj, np.int32):
        return int(obj)
    return str(obj)
    # raise TypeError("Type not serializable")

def pretty_print(json_data, file="media/temporary_files/created_json_file.json", mode="a"):
    """ Fonction qui affiche le fichier json avec les bonnes indentations un fichier json

    Args:
        json_data (json): Données json en entrée
        file (str, optional): Nom de fichier json de sortie "created_json_file.json".
        mode (str, optional): Defaults to "a" pour "append" - "w" pour "write"
    """

    json_formatted_str = json.dumps(
        json_data, indent=2, default=serialize)
    with open(file, mode) as outfile:
        outfile.write(json_formatted_str)


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
    """
    Fonction qui applique la fonction python strip() si l'élement est bien de type texte
    """
    return element.strip() if isinstance(element, str) else element

def remove_spec_char_from_list(char_list):
    """
    Fonction qui applique remove_spec_char à chaque élément d'une liste de chaînes
    """
    return [re.sub("[^A-Z ]", "", str(item), 0, re.IGNORECASE) for item in char_list]

def convert_to_time_or_text(value):
    """
    Fonction qui converti la cellule en time si elle est au format type time ou date dans le excel
    et qui laisse au format texte (cruising, in port etc) si la cellule est au format texte
    """
    if isinstance(value, str):
        # print("="*3, value)
        if re.match("[0-9]{2}:[0-9]{2}:[0-9]{2}", value):
            #print("first match")
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


def np_removing_semicolon(numpy_table, num_col):
    """
    Fonction qui prend une numpy table et ne retourne que la partie avant les deux point (:) de la colonne demandée
    """
    return np.array([s.partition(':')[num_col].strip() for s in numpy_table[:, num_col]])

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


def read_excel(logbook_file_path, num_page):
    """ 
    Fonction qui extrait les informations d'un fichier excel en dataframe

    Args:
        logbook_file_path: lien vers le fichier contenant le logbook
        num_page (int): numéro de page à extraire (1, 2 etc ...)

    Returns:
        (dataframe): du fichier excel
    """
    classeur = openpyxl.load_workbook(filename=logbook_file_path, data_only=True)
    noms_feuilles = classeur.sheetnames
    feuille = classeur[noms_feuilles[num_page - 1]]
    df_donnees = pd.DataFrame(feuille.values)
    classeur.close()
    return df_donnees


def get_list_harbours(allData):
    """
    Args:
        allData

    Returns:
        list: all the enabled ports (topiaId and label2)
    """

    harbours = allData["Harbour"]
    sorted_list_harbours = [{'topiaId': harbour.get('topiaId'), 'label2': harbour.get('label2')} 
                        for harbour in harbours if harbour.get('status') == 'enabled']
    sorted_list_harbours.sort(key=lambda x: x['label2'])

    return sorted_list_harbours


def from_topiaid_to_value(topiaid, lookingfor, label_output, allData, domaine=None):
    """
    Fonction générale qui retourne le label output pour un topiad donné 
    dans la base common ou longliner

    Args:
        topiad
        lookingfor: catégorie issu du WS dans laquelle on veut chercher notre topiaid
        label_output: ce qu'on veut présenter (label, nom, espèce ...)
        domaine si nécessaire (palangre, senne)

    Returns:
        nom souhaité associé au topotiad
    """
    
    if lookingfor == 'VesselActivity' or lookingfor == 'Program':
        if domaine is None :
            print("Error il faut préciser un domaine")
            return None
        else :
            if domaine == 'palangre':
                domaine_en = str('longline')
            else:
                domaine_en = str('seine')
            
            for element in allData[lookingfor][domaine_en]: 
                if element['topiaId'] == topiaid:
                    return element[label_output]
        
    else:
        if allData[lookingfor] is not None:
            for element in allData[lookingfor]:
                if element['topiaId'] == topiaid:
                    return element[label_output]
        else:
            print("please do check the orthographe of looking for element")
            return None


