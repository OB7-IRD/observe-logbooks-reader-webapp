# -*- coding: utf-8 -*-
""" 
Module de fonctions communes et générales à l'application. 
"""

import json
import datetime
import re
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
    if isinstance(obj, np.int64):
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