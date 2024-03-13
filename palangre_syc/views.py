from django.template import RequestContext
from django.urls import reverse
from django.utils import translation
import os
import re
import json
import datetime
import warnings
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.translation import activate

from django.utils.translation import gettext as _
from django.utils.translation import gettext


import pandas as pd
import numpy as np
import openpyxl

from django.shortcuts import redirect, render
from django.contrib import messages

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

    # if type(degrees) is str:
    degrees = int(degrees)
    minutes = int(minutes)
    decimal_degrees = degrees + minutes / 60.0
    if direction in ['S', 'W']:
        decimal_degrees *= -1
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


def from_topiad_to_value2(topiad, domaine=None):
    """
    Fonction qui retourne le label 1 pour un topiad donné 
    dans la base common si un domaine n'est pas précisé

    Args:
        topiad
        domaine si nécessaire (palangre, senne)

    Returns:
        label1
    """
    if domaine is None:
        with open('./data_common.json', 'r', encoding='utf-8') as f:
            data_common = json.load(f)
        for element in data_common['content']['fr.ird.observe.entities.referential.common.Ocean']:
            if element['topiaId'] == topiad:
                return element['label2']

    else:
        with open('./data_ll.json', 'r', encoding='utf-8') as f:
            data_ll = json.load(f)

        for element in data_ll['content']['fr.ird.observe.entities.referential.ll.common.Program']:
            if element['topiaId'] == topiad:
                return element['label2']


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
        for element in data_ll['content'][category]:
            if element['topiaId'] == topiaid:
                return element[label_output]


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


def extract_vesselInfo_LL(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe 
    les données relatives au bateau 'Vessel information'
    '''
    # On extrait les données propres au 'Vessel information'
    df_vessel = df_donnees.iloc[7:16, 0]
    np_vessel = np.array(df_vessel)

    # On sépare en deux colonnes selon ce qu'il y a avant et après les ':'
    entries = [(item.split(":")[0].strip(), item.split(":")[
                1].strip() if ':' in item else '') for item in np_vessel]
    np_vessel_clean = np.array(
        entries, dtype=[('Logbook_name', 'U50'), ('Value', 'U50')])
    # On applique un filtre pour les caractères spéciaux
    np_vessel_clean['Logbook_name'] = remove_spec_char_from_list(
        np_vessel_clean['Logbook_name'])
    df_vessel = pd.DataFrame(np_vessel_clean)
    df_vessel['Logbook_name'] = df_vessel['Logbook_name'].apply(
        lambda x: x.strip())

    return df_vessel


def extract_cruiseInfo_LL(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les données relatives à la marée
    '''
    # On extrait les données propres au 'Vessel information'
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
    df_cruise['Logbook_name'] = remove_spec_char_from_list(
        df_cruise['Logbook_name'])
    df_cruise['Logbook_name'] = df_cruise['Logbook_name'].apply(
        lambda x: x.strip())

    return df_cruise

def extract_reportInfo_LL(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les données
    relatives aux info de report
    '''
    # On extrait les données propres au 'Vessel information'
    df_report = df_donnees.iloc[7:9, 29:35]

    # On supprimes les colonnes qui sont vides
    df_report = del_empty_col(df_report)
    np_report = np.array(df_report)

    # On applique la fonction strip sur les cellules de la colonnes Valeur,
    # si l'élément correspond à une zone de texte
    vect = np.vectorize(strip_if_string)
    np_report[:, 0:1] = vect(np_report[:, 0:1])

    df_report = pd.DataFrame(np_report, columns=['Logbook_name', 'Value'])
    df_report['Logbook_name'] = remove_spec_char_from_list(
        df_report['Logbook_name'])

    return df_report


def extract_gearInfo_LL(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les données relatives à l'équipement
    '''
    # On extrait les données propres au 'Vessel information'
    df_gear = df_donnees.iloc[12:16, 11:21]

    # On supprimes les colonnes qui sont vides
    df_gear = del_empty_col(df_gear)

    np_gear = np.array(df_gear)
    # on nettoie la colonne en enlevant les espaces et les ':'
    np_gear[:, 0] = np_removing_semicolon(np_gear, 0)

    # On applique la fonction strip sur les cellules de la colonnes Valeur,
    # si l'élément correspond à une zone de texte

    # vect = np.vectorize(strip_if_string)
    # np_gear[:, 1] = vect(np_gear[:, 1])
    # if not np_gear[:, 1].apply(lambda x: isinstance(x, int))

    df_gear = pd.DataFrame(np_gear, columns=['Logbook_name', 'Value'])

    # Vérifie si toutes les cellules de la colonne sont des entiers
    toutes_int = df_gear['Value'].apply(
        lambda cellule: isinstance(cellule, int)).all()
    # print("toutes int ? ", toutes_int)
    if toutes_int:
        # Applique la fonction vect si toutes les cellules sont des entiers
        df_gear['Value'] = np.vectorize(strip_if_string)(df_gear['Value'])
    # print("df_gear ? ", df_gear)

    df_gear['Logbook_name'] = remove_spec_char_from_list(
        df_gear['Logbook_name'])
    df_gear['Logbook_name'] = df_gear['Logbook_name'].apply(
        lambda x: x.strip())

    if not df_gear['Value'].apply(lambda x: isinstance(x, int)).all():
        message = _(
            "Les données remplies dans le fichier soumis ne correspondent pas au type de données attendues. Ici on attend seulement des entiers.")
        return df_gear, message

    return df_gear


def extract_lineMaterial_LL(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les données 
    relatives aux matériel des lignes
    '''
    # On extrait les données propres au 'Vessel information'
    df_line = df_donnees.iloc[12:16, 21:29]

    # On supprimes les colonnes qui sont vides
    df_line = del_empty_col(df_line)

    np_line = np.array(df_line)

    # On applique la fonction strip sur les cellules de la
    # colonnes Valeur, si l'élément correspond à une zone de texte
    vect = np.vectorize(strip_if_string)
    np_line[:, 0:1] = vect(np_line[:, 0:1])

    df_line = pd.DataFrame(np_line, columns=['Logbook_name', 'Value'])
    df_line['Logbook_name'] = remove_spec_char_from_list(
        df_line['Logbook_name'])
    df_line['Logbook_name'] = df_line['Logbook_name'].apply(
        lambda x: x.strip())

    df_line_used = df_line.loc[df_line['Value'] != "None"]

    # print(df_line_used)

    # Traduire chaque valeur du DataFrame df_line_used
    df_line_used['Logbook_name'] = df_line_used['Logbook_name'].apply(
        lambda x: gettext(x) if isinstance(x, str) else x)
    # print(df_line_used['Logbook_name'])

    if len(df_line_used) > 1:
        message = _(
            "Ici on n'attend qu'un seul matériau. Veuillez vérifier les données.")
        return df_line_used, message

    if len(df_line_used) == 0:
        message = _(
            "La table entre les lignes 13 à 16 de la colonne 'AC' ne sont pas saisies. Veuillez vérifier les données.")
        return df_line_used, message

    # df_line_used = [[_(valeur) for valeur in ligne] for ligne in df_line_used]

    return df_line_used


def extract_target_LL(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les données relatives aux target spécifiques
    '''
    # On extrait les données propres au 'Vessel information'
    df_target = df_donnees.iloc[12:16, 29:34]

    # On supprimes les colonnes qui sont vides
    df_target = del_empty_col(df_target)

    np_target = np.array(df_target)

    np_target[:, 0] = np_removing_semicolon(np_target, 0)
    # On applique la fonction strip sur les cellules de
    # la colonnes Valeur, si l'élément correspond à une zone de texte
    vect = np.vectorize(strip_if_string)
    np_target[:, 0:1] = vect(np_target[:, 0:1])

    df_target = pd.DataFrame(np_target,
                             columns=['Logbook_name', 'Value'])
    df_target['Logbook_name'] = remove_spec_char_from_list(
        df_target['Logbook_name'])
    df_target['Logbook_name'] = df_target['Logbook_name'].apply(
        lambda x: x.strip())

    # for element in df_target['Value']:
    #     print(element, type(element))

    # df_targeted = df_target.loc[df_target['Value'] == None]
    # print(df_targeted)
    # filtered = [row['Logbook_name'] for row in df_target if row['Value'] != 'None']
    # Supposons que df_target est votre DataFrame pandas
    # filtered = df_target.loc[df_target['Value'] == 'P', 'Logbook_name']

    # filtered = [row for row in df_target if row['Value'] is not None]
    # print(filtered)

    return df_target


def extract_logbookDate_LL(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe le mois et l'année du logbook
    '''
    # On extrait les données propres au 'Vessel information'
    df_month = df_donnees.iloc[17, 5]
    df_year = df_donnees.iloc[17, 11]

    np_date = np.array([('Month', df_month), ('Year', df_year)],
                       dtype=[('Logbook_name', 'U10'), ('Value', int)])
    df_date = pd.DataFrame(np_date)
    df_date['Logbook_name'] = remove_spec_char_from_list(
        df_date['Logbook_name'])

    return df_date


def extract_bait_LL(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe le type de d'appat utilisé
    '''
    # On extrait les données propres au 'Vessel information'
    df_squid = df_donnees.iloc[19, 16]
    df_sardine = df_donnees.iloc[19, 20]
    df_mackerel = df_donnees.iloc[19, 24]
    df_muroaji = df_donnees.iloc[19, 28]
    df_other = df_donnees.iloc[19, 32]

    np_bait = np.array([('Squid', df_squid),
                        ('Sardine', df_sardine),
                        ('Mackerel', df_mackerel),
                        ('Muroaji', df_muroaji),
                        ('Other', df_other),],
                       dtype=[('Logbook_name', 'U10'), ('Value', 'U10')])
    df_bait = pd.DataFrame(np_bait)

    df_bait_used = df_bait.loc[df_bait['Value'] != "None"]

    return df_bait_used


def extract_positions(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe 
    les position de chaque coup de peche par jour 
    en décimal type float
    '''
    day = df_donnees.iloc[24:55, 0]
    df_lat_dms = df_donnees.iloc[24:55, 1:4]
    df_long_dms = df_donnees.iloc[24:55, 4:7]
    colnames = ['Degrees', 'Minutes', 'Direction']
    df_lat_dms.columns = colnames
    df_long_dms.columns = colnames

    df_lat_dms['Latitude'] = np.where(df_lat_dms.isnull().any(axis=1), np.nan,
                                      df_lat_dms.apply(lambda row: dms_to_decimal(row['Degrees'], row['Minutes'], row['Direction']), axis=1))

    df_long_dms['Longitude'] = np.where(df_long_dms.isnull().any(axis=1), np.nan,
                                        df_long_dms.apply(lambda row: dms_to_decimal(row['Degrees'], row['Minutes'], row['Direction']), axis=1))

    df_position = pd.DataFrame({'Day': day,
                                'Latitude': df_lat_dms['Latitude'],
                                'Longitude': df_long_dms['Longitude']})

    df_position = df_position.dropna()

    df_position['Latitude'] = df_position['Latitude'].round(2)
    df_position['Longitude'] = df_position['Longitude'].round(2)

    df_position.reset_index(drop=True, inplace=True)

    return df_position


def get_VesselActivity_topiaID(startTimeStamp, data_ll):
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

    VesselActivities = data_ll["content"]["fr.ird.observe.entities.referential.ll.common.VesselActivity"]
    for VesselActivity in VesselActivities:
        if VesselActivity.get("code") == code:
            return VesselActivity["topiaId"], VesselActivity["label1"]

    return None


def extract_time(df_donnees, data_ll):
    '''
    Fonction qui extrait et présente dans un dataframe les horaires des coups de pêche 
    Elle retourne un champ type horaire, sauf si le bateau est en mouvement
    '''
    day = df_donnees.iloc[24:55, 0]
    df_time = df_donnees.iloc[24:55, 7:8]
    colnames = ['Time']
    df_time.columns = colnames
    df_time['Time'] = df_time['Time'].apply(convert_to_time_or_text)
    # df_time['Time'] = pd.to_datetime(df_time['Time'], errors='ignore')

    df_time.reset_index(drop=True, inplace=True)

    VesselActivities = np.empty((len(day), 1), dtype=object)
    for ligne in range(len(day)):
        VesselActivity = get_VesselActivity_topiaID(
            df_time.iloc[ligne]['Time'], data_ll)
        VesselActivities[ligne, 0] = VesselActivity[0]
    np_time = np.column_stack((day, df_time, VesselActivities))
    df_time = pd.DataFrame(np_time, columns=['Day', 'Time', 'VesselActivity'])

    return df_time


def extract_temperature(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les horaires des coups de pêche 
    Elle retourne un champ type horaire, sauf si le bateau est en mouvement
    '''
    df_temp = df_donnees.iloc[24:55, 8:9]
    colnames = ['Température']
    df_temp.columns = colnames

    df_temp.reset_index(drop=True, inplace=True)
    return df_temp


def extract_fishingEffort(df_donnees):
    '''
    Fonction qui extrait et présente dans un dataframe les efforts de peche
    '''
    day = df_donnees.iloc[24:55, 0]
    df_fishingEffort = df_donnees.iloc[24:55, 9:12]

    np_fishingEffort = np.column_stack((day, df_fishingEffort))

    df_fishingEffort = pd.DataFrame(np_fishingEffort, columns=[
                                    'Day', 'Hooks per basket', 'Total hooks', 'Total lightsticks'])

    df_fishingEffort['Total hooks / Hooks per basket'] = df_fishingEffort['Total hooks'] / \
        df_fishingEffort['Hooks per basket']

    df_fishingEffort.reset_index(drop=True, inplace=True)

    return df_fishingEffort


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
    # print(df_tunas)
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
    colnames = ['No RET SPN', 'Kg RET SPN',
                'No ESC SPN', 'No DIS SPN']
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
    vessel_topiaid = json_construction.get_vessel_topiaID(
        df_donnees_p1, data_common)
    # Pour le webservice, il faut remplacer les # par des - dans les topiaid
    vessel_topiaid_WS = vessel_topiaid.replace("#", "-")
    programme_topiaid = request.session.get('dico_config')['programme']
    programme_topiaid_WS = programme_topiaid.replace("#", "-")

    print("="*20, vessel_topiaid_WS, "="*20)
    print("="*20, programme_topiaid_WS, "="*20)

    previous_trip = api.latest_trip(
        token, url_base, vessel_topiaid_WS, programme_topiaid_WS)
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


DIR = "./media/logbooks"


def presenting_previous_trip(request):

    # activate(request.LANGUAGE_CODE)

    selected_file = request.GET.get('selected_file')
    apply_conf = request.session.get('dico_config')

    print("="*20, "presenting_previous_trip", "="*20)
    print("apply conf : ", apply_conf)

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

        # On récupères le dictionnnaire de données jugées intéressantes de la précédente marée
        if get_previous_trip_infos(request, df_donnees_p1, data_common) is not None :
            context.update(get_previous_trip_infos(request, df_donnees_p1, data_common))
            


        # Si y a pas de previous trip associé
        else :
            context.update({'startDate': None,
                            'depPort': None,
                            'depPort_topiaid': None,
                            'endDate': None,
                            })
    
    request.session['context'] = context
    return render(request, 'LL_previoustrippage.html', context)

    # on garde les valeurs de context dans une variable de session
    # request.session['context'] = context
    # print(context)


def checking_logbook(request):

    # selected_file = request.GET.get('selected_file')

    print("="*20, "checking_logbook", "="*20)

    with open('./data_common.json', 'r', encoding='utf-8') as f:
        data_common = json.load(f)

    if request.method == 'POST':

        # continuetrip = request.POST.get('continuetrip')
        # newtrip = request.POST.get('newtrip')
        continuetrip = request.POST.get('continuetrip')
                
        file_path = request.session.get('file_path')
        context = request.session.get('context')
        
        context.update({"continuetrip": continuetrip})
        request.session['context'] = context
        print(context)

        print("="*20, "checking_logbook selected_file", "="*20)
        print(file_path)

        with open('./data_ll.json', 'r', encoding='utf-8') as f:
            data_ll = json.load(f)
        df_donnees_p1 = read_excel(file_path, 1)

        df_vessel = extract_vesselInfo_LL(df_donnees_p1)
        df_cruise = extract_cruiseInfo_LL(df_donnees_p1)
        df_report = extract_reportInfo_LL(df_donnees_p1)
        df_gear = extract_gearInfo_LL(df_donnees_p1)
        df_line = extract_lineMaterial_LL(df_donnees_p1)
        df_target = extract_target_LL(df_donnees_p1)
        df_date = extract_logbookDate_LL(df_donnees_p1)
        df_bait = extract_bait_LL(df_donnees_p1)
        df_fishingEffort = extract_fishingEffort(df_donnees_p1)

        df_position = extract_positions(df_donnees_p1)
        df_time = extract_time(df_donnees_p1, data_ll)
        df_temperature = extract_temperature(df_donnees_p1)
        df_tunas = extract_tunas(df_donnees_p1)
        df_billfishes = extract_billfishes(df_donnees_p1)
        df_otherfish = extract_otherfish(df_donnees_p1)

        df_donnees_p2 = read_excel(file_path, 2)
        df_sharksFAL = extract_sharksFAL(df_donnees_p2)
        df_sharksBSH = extract_sharksBSH(df_donnees_p2)
        df_sharksMAK = extract_sharksMAK(df_donnees_p2)
        df_sharksSPN = extract_sharksSPN(df_donnees_p2)
        df_sharksTIG = extract_sharksTIG(df_donnees_p2)
        df_sharksPSK = extract_sharksPSK(df_donnees_p2)
        df_sharksTHR = extract_sharksTHR(df_donnees_p2)
        df_sharksOCS = extract_sharksOCS(df_donnees_p2)
        df_mammals = extract_mammals(df_donnees_p2)
        df_seabirds = extract_seabird(df_donnees_p2)
        df_turtles = extract_turtles(df_donnees_p2)

        df_activity = pd.concat([df_position, df_time.loc[:, 'Time'], df_temperature,
                                df_fishingEffort, df_tunas, df_billfishes, df_otherfish,
                                df_sharksFAL, df_sharksBSH, df_sharksMAK,
                                df_sharksSPN, df_sharksTIG, df_sharksPSK,
                                df_sharksTHR, df_sharksOCS,
                                df_mammals, df_seabirds, df_turtles],
                                axis=1)

        previous_trip = get_previous_trip_infos(request, df_donnees_p1, data_common)
        list_ports = get_list_harbours(data_common)
        
        data_to_homepage = {
            'previous_trip': previous_trip,
            'continuetrip': continuetrip,
            # 'newtrip': newtrip,
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
            'df_activity': df_activity,

            'programme': context['program'],
            'ocean': context['ocean'],
        }
        
        return render(request, 'LL_homepage.html', data_to_homepage)

    else:
        # Gérer le cas où la méthode HTTP n'est pas POST
        pass
    return render(request, 'LL_homepage.html')


def send_logbook2Observe(request):
    warnings.simplefilter(action='ignore', category=FutureWarning)

    if request.method == 'POST':
        print("°"*20, "POST", "°"*20)

        file_path = request.session.get('file_path')
        # apply_conf = request.session.get('dico_config')
        context = request.session.get('context')
        
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        depPort = request.POST.get('depPort')
        endPort = request.POST.get('endPort')
        
        print("="*20, "data collected", "="*20)
        print("startDate ", startDate)
        print("endDate ", endDate)
        print("depPort ", depPort)
        print("endPort ", endPort)
                
        resultat = None
        
        #############################
        # messages d'erreurs
        
        if startDate is not None and depPort is None:
            print("Vous commencez une nouvelle marée, un port de départ est demandé")
            messages.warning(request, _("Vous commencez une nouvelle marée, un port de départ est demandé"))
        
        if endDate is None:
            messages.error(request, _("La date de fin de marée est nécessaire. Si votre marée est toujours en cours, saisissez la fin du mois du logbook"))
        #############################

        
        if context['continuetrip'] is None:
            context.update({'startDate': json_construction.create_starttimestamp_from_fieldDate(startDate), 
                            'depPort': depPort if depPort != '' else None})

        context.update({'endDate' : json_construction.create_starttimestamp_from_fieldDate(endDate),
                        'endPort': endPort if endPort != '' else None})
        
        print("°"*40, context)
        
        
        
        # apply_conf.update({'startDate': startDate if startDate is not None else context['startDate'],
        #                    'endDate': endDate,
        #                    'depPort': depPort if depPort != '' else None,
        #                    'endPort': endPort if endPort != '' else None})

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
        logbook_month = str(extract_logbookDate_LL(df_donnees_p1).loc[extract_logbookDate_LL(df_donnees_p1)['Logbook_name'] == 'Month', 'Value'].values[0])
        logbook_year = str(extract_logbookDate_LL(df_donnees_p1).loc[extract_logbookDate_LL(df_donnees_p1)['Logbook_name'] == 'Year', 'Value'].values[0])
        if len(logbook_month) == 1:
            logbook_month = '0' + logbook_month
            print(logbook_month, type(logbook_month))
        else:
            logbook_month = str(logbook_month)
        
        if context['startDate'][5:7] == logbook_month:
            start_extraction = int(context['startDate'][8:10]) - 1

            if context['endDate'][5:7] == logbook_month:
                end_extraction = int(context['endDate'][8:10]) - 1
                print("startDate & endDate in month logbook : ", start_extraction, end_extraction)
            
            else:
                end_extraction = len(extract_positions(df_donnees_p1))
                print("startDate in month logbook : ", start_extraction, end_extraction)
        
        else:
            start_extraction = 0
            if context['endDate'][5:7] == logbook_month:
                end_extraction = int(context['endDate'][8:10]) - 1
                print("endDate in month logbook : ", start_extraction, end_extraction)
            
            else:
                end_extraction = len(extract_positions(df_donnees_p1))
                print("nothing in month logbook : ", start_extraction, end_extraction)
        
        
        
        #############################
        # messages d'erreurs
        if (int(context['endDate'][5:7]) + int(context['endDate'][:4])) != (int(logbook_month) + int(logbook_year)):
            messages.error(request, _("La date de fin de trip doit être dans le mois. Saisir le dernier jour du mois dans le cas où le trip n'est pas réellement fini."))
        #############################
              
                              
        if context['continuetrip'] is None:
            
            print("="*80)
            print("Create Activity and Set")
            
            MultipleActivity = json_construction.create_activity_and_set(
                df_donnees_p1, df_donnees_p2, 
                data_common, data_ll, 
                start_extraction, end_extraction)

            print("="*80)
            print("Create Trip")
            
            #########
            # Ajouter une recherche de si 'departure' est bien trouvée à la date de départ demandée 
            # si non : demander si il veut vrmt envoyer 
            #########
            
            
            trip = json_construction.create_trip(
                df_donnees_p1, MultipleActivity, data_common, context)

            print("Creation of a new trip")
            resultat = api.send_trip(token, trip, url_base)
            print("resultats : ", resultat)

        else:            
            with open('./previoustrip.json', 'r', encoding='utf-8') as f:
                json_previoustrip = json.load(f)

            # Recherche si la 1ere date de mon excel est dans
            if extract_time(df_donnees_p1, data_ll).loc[0, 'VesselActivity'] == "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1":
                # Si c'est une fishing operation
                date = json_construction.create_starttimestamp(
                 df_donnees_p1, data_ll, 0, True)
            else:
                date = json_construction.create_starttimestamp(
                    df_donnees_p1, data_ll, 0, False)

            #############################
            # messages d'erreurs
            if json_construction.search_date_into_json(json_previoustrip['content'], date) is True:
                print(
                    "ERROR THE TRIP YOU WANT TO ADD IS ALREDAY ENTERED IN THE PREVIOUS ONE")
                messages.warning(request, _("Le logbook soumis n'a pas pu être saisi dans la base de données car il a déjà été envoyé dans un précédent trip. Merci de vérifier sur l'application"))
                # return render(request, 'LL_send_data.html', {'info': message})


            elif (int(context['endDate'][5:7]) + int(context['endDate'][:4]) + 1) != (int(logbook_month) + int(logbook_year)):
                print(int(context['endDate'][5:7]) + int(context['endDate'][:4]) + 1, "!=", int(logbook_month) + int(logbook_year))
                print(
                    "ERROR THE TRIP YOU WANT TO ADD IS NOT CONSECUTIVE")
                messages.warning(request, _("Le logbook soumis n'a pas pu être saisi dans la base de données car il n'est pas consécutif à la marée précédente"))
                
                # return render(request, 'LL_send_data.html', {'info': message})    
            #############################
            
            else:
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
                                topiaid=context['triptopiaid'])
        
        if resultat is not None:
            if resultat == ("Logbook inséré avec success", 1) :
                messages.success(request, _("Le logbook a bien été envoyé dans la base"))
            
            else: 
                messages.error(request, _("Il doit y avoir une erreur dedans car le logbook n'a pas été envoyé"))

        return render(request, 'LL_send_data.html')

    else:
        # ajouter une page erreur d'envoi
        return render(request, 'LL_file_selection.html')
