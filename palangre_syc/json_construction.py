import json
import pandas as pd
import palangre_syc.api
import palangre_syc.views

def get_captain_topiaid(df_donnees_p1, allData):
    """
    Fonction qui propose le topiaID associé au capitaine du logbook 
    (ou inconnu is non présent dans les données de référence)

    Args:
        df_donnees_p1 (dataframe): page 1 du doc excel
        allData (json): Données de références

    Returns:
        _type_: topiaID du capitaine présenté dans le logbook
    """
    for captain in allData['Person']:

        captain_logbook = palangre_syc.views.extract_cruise_info(df_donnees_p1).loc[palangre_syc.views.extract_cruise_info(df_donnees_p1)['Logbook_name'] == 'Captain', 'Value'].values[0]
        captain_json = captain['firstName'] + ' ' + captain['lastName']
        if captain_logbook == captain_json:
            return captain['topiaId']
        else:
            captain_logbook = '[inconnu] [inconnu]'
            if captain_logbook == captain_json:
                return captain['topiaId']
    return None

def get_operator_topiaid(df_donnees_p1, allData):
    """
    Fonction qui propose le topiaID de la personne qui a saisi les données du logbook (ou inconnu is non présent dans les données de référence)

    Args:
        df_donnees_p1 (dataframe): page 1 du doc excel
        allData (json): Données de références

    Returns:
        _type_: topiaID de l'opérateur 
    """
    for person in allData['Person']:

        reported_logbook = palangre_syc.views.extract_report_info(df_donnees_p1).loc[palangre_syc.views.extract_report_info(
            df_donnees_p1)['Logbook_name'] == 'Person reported', 'Value'].values[0]
        reported_json = person['firstName'] + ' ' + person['lastName']
        if reported_logbook == reported_json:
            return person['topiaId']
        else:
            reported_logbook = '[inconnu] [inconnu]'
            if reported_logbook == reported_json:
                return person['topiaId']
    return None

def get_vessel_topiaid(df_donnees_p1, allData):
    """
    Fonction qui propose le topiaId du navire cité dans le logbook à partir de son 'nationlId' s'il existe 

    Args:
        df_donnees_p1 (dataframe): page 1 du doc excel
        allData (json): Données de références
        
    Returns:
        _type_: topiaID du navire (vessel)
    """
    vessel_logbook = palangre_syc.views.extract_vessel_info(df_donnees_p1).loc[palangre_syc.views.extract_vessel_info(df_donnees_p1)['Logbook_name'] == 'Official Number', 'Value'].values[0]
    for vessel in allData["Vessel"]:
        if 'nationalId' in vessel:
            vessel_json = vessel['nationalId']
            if vessel_logbook == vessel_json:
                return vessel['topiaId']

    # il faudrait faire un message qui dit de vérifier si le bateau est bien existant et présent dans la base
    # si 'nationalId' n'est pas dans vessel
    return None


def get_baittype_topiaid(row, allData):
    """
    Fonction qui propose le topiaId de l'appat coché dans le logbook 

    Args:
        row (dataframe): nom de l'appât 
        allData (json):  Données de références

    Returns:
        str: topiaID de l'appât utilisé
    """
    baittypes = allData["BaitType"]
    bait_logbook = row['Logbook_name']
    for baittype in baittypes:
        if baittype.get("label1")[:len(bait_logbook)] == bait_logbook:
            return baittype["topiaId"]


def get_species_topiaid(fao_code_logbook, allData):
    """
    Fonction qui propose le topiaId pour une espèce à partir de son code FAO (saisi manuellement dans la trascription du excel)

    Args:
        FAO_code_logbook (_type_): Code FAO (3 caractères) extrait du datatable de prises créé depuis la page 1 et 2
        allData (json): Données de références
        
    Returns:
        str: topiaID de l'espèce demandée
    """
    species = allData["Species"]

    for specie in species:
        if fao_code_logbook == specie.get("faoCode"):
            return specie["topiaId"]
        # On part du principe que si le code fao n'est pas exactement trouvé, c'est qu'il s'agit d'une espèce non identifié
        
    return "fr.ird.referential.common.Species#1433499266610#0.696541526820511"


def get_catchfate_topiaid(catchfate_logbook, allData):
    """
    Fonction qui propose le topiaId du devenir de l'espèce (associé manuellement à l'espèce dans la trascription du excel)

    Args:
        catchFate_logbook (str): Code catchFate (3 caractères) extrait du datatable de prises créé depuis la page 1 et 2
        allData (json): Données de références

    Returns:
        str: topiaID du devenir de l'espèce demandée
    """

    fates = allData["CatchFate"]
    for catchfate in fates:
        if 'code' in catchfate:
            if catchfate.get("code") == catchfate_logbook:
                return catchfate["topiaId"]
        else :
            return None


# Opimisation éventuelle : ajouter unparamètre qui permettrait de distinguer les fish des bycatch
# notamment si les by catch son relachées A alive ou D dead


def get_processing_topiaid(fao_code, allData):
    """
    Fonction qui associe un process on board à une espèce de poisson

    Args:
        fao_code (str): espèce de poisson
        allData (json):  Données de références

    Returns:
        topiaid: OnBoardProcess
    """
    ''' on associe pour chaque espèce un processing et on lui ajoute en onBoardProcessing '''
    if fao_code == 'SBF' or fao_code == 'BET' or fao_code == 'YFT':
        processing_code = "GG"
    elif fao_code == 'SWO' or fao_code == 'MLS' or fao_code == 'BUM' or fao_code == 'BLM' or fao_code == 'SFA' or fao_code == 'SSP':
        processing_code = "HG"
    elif fao_code == 'ALB' or  fao_code == 'OIL' or fao_code == 'XXX':
        processing_code = "WL"
    else : 
        processing_code = "UNK"
    
    processings = allData["OnBoardProcessing"]
    for processing in processings:
        if 'code' in processing:
            if processing.get("code") == processing_code:
                
                return processing["topiaId"]
        else :
            return None

def get_target_species_topiaid(df_donnees_p1, allData):
    """
    Fonction qui va récupérer les topiaid de chacune des espèces visées dans une liste

    Args:
        df_donnees_p1 (dataframe): page 1 du doc excel
        allData (json):  Données de références

    Returns:
        list de topiaid
    """
    data = palangre_syc.views.extract_target_species(df_donnees_p1)
    list_target_topiaid = []
    for target in data['Logbook_name']:
        if 'Tropical Tuna' in target: 
            # list_target_topiaid.loc[len(list_target_topiaid)] = get_species_topiaid("YFT", data_common)
            list_target_topiaid.append(get_species_topiaid("YFT", allData))
            list_target_topiaid.append(get_species_topiaid("BET", allData))
        elif 'Albacore Tuna' in target:
            list_target_topiaid.append(get_species_topiaid("ALB", allData))
        elif 'Swordfish' in target: 
            list_target_topiaid.append(get_species_topiaid("SWO", allData))
        else: 
            list_target_topiaid.append(get_species_topiaid("XXX*", allData))
        
    return list_target_topiaid

def construction_catch_table(fish_file):
    """

    Args:
        fish_file (dataframe): Issu des fonction d'extraction propre à chaque espèce ou groupe d'espèce

    Returns:
        dataframe: Construction d'un df avec chaque code FAO et le catchfate associée en lignes
    """
    df_catches = pd.DataFrame(columns=['fao_code', 'catch_fate', 'count', 'totalWeight'])

    # On récupère les données des colonnes de FAO et catchFate
    for col in fish_file.columns:
        fao_code = col[-3:]
        catchfate = col[-7:-4]
        df_catches.loc[len(df_catches)] = {'fao_code': fao_code, 'catch_fate': catchfate}

    # On supprime les doublons
    df_catches = df_catches.drop_duplicates()
    df_catches.reset_index(drop=True, inplace=True)

    return df_catches

# a voir si c'est pertinent en terme de gain de temps de découper la fonction ici en 2
# on pourrait avoir une fonctionn qui gère les lignes issues des noms de colonnes
# et une seconde fonction qui remplirait les lignes count et totalWeight en allant chercher les infos dans le excel


def create_catch_table_fish_perday(fish_file, row_number):
    """
    Args:
        fish_file (datatable): issu des extraction, donc un datatable par groupe d'espèce
        row_number (int): ligne (ou un jour de pêche) à extraire

    Returns:
        dataframe: par type de poisson pêché et par jour de pêche de 4 colonnes 
    Ce dataframe contient les champs obligatoires à remplir dans la table 'catch' de Observe
    """

    df_catches = construction_catch_table(fish_file)

    # On rempli la suite du dataframe pour count et totalWeight (pour une ligne donnée)
    for index, row in df_catches.iterrows():
        col_end_name = row['catch_fate'] + ' ' + row['fao_code']
        for col in fish_file.columns:
            if col[-7:] == col_end_name:
                if col[:2] == 'No':
                    fish_file_colname = 'No' + ' ' + col_end_name
                    count = fish_file.loc[row_number, fish_file_colname]
                    df_catches.loc[index, 'count'] = count
                    # df_catches.loc[index, 'count'] = int(df_catches.loc[index, 'count'])

                if col[:2] == 'Kg':
                    fish_file_colname = 'Kg' + ' ' + col_end_name
                    total_weight = fish_file.loc[row_number, fish_file_colname]
                    df_catches.loc[index, 'totalWeight'] = total_weight
                    # df_catches.loc[index, 'totalWeight'] = int(df_catches.loc[index, 'totalWeight'])

                # a voir si on veut des Nan car il n'y a pas de donnée ou des 0
                else:
                    df_catches.loc[index, 'totalWeight'] = int(0)

    return df_catches


def create_catch_table_fishes(df_donnees_p1, df_donnees_p2, row_number):
    """

    Args:
        df_donnees_p1 (dataframe): page 1 du doc excel
        df_donnees_p2 (dataframe): page 2 du doc excel
        row_number (int): ligne ou jour du set

    Returns:
        dataframe: avec les prises réalisées pour une journée de pêche (code FAO, catchFate, nombre de prise et Poids tot)
    """
    liste_fct_extraction = [palangre_syc.views.extract_tunas(df_donnees_p1),
                            palangre_syc.views.extract_billfishes(
                                df_donnees_p1),
                            palangre_syc.views.extract_otherfish(
                                df_donnees_p1),
                            palangre_syc.views.extract_sharksFAL(
                                df_donnees_p2),
                            palangre_syc.views.extract_sharksBSH(
                                df_donnees_p2),
                            palangre_syc.views.extract_sharksMAK(
                                df_donnees_p2),
                            palangre_syc.views.extract_sharksSPN(
                                df_donnees_p2),
                            palangre_syc.views.extract_sharksTIG(
                                df_donnees_p2),
                            palangre_syc.views.extract_sharksPSK(
                                df_donnees_p2),
                            palangre_syc.views.extract_sharksTHR(
                                df_donnees_p2),
                            palangre_syc.views.extract_sharksOCS(
                                df_donnees_p2),
                            palangre_syc.views.extract_mammals(df_donnees_p2),
                            palangre_syc.views.extract_seabird(df_donnees_p2),
                            palangre_syc.views.extract_turtles(df_donnees_p2)]

    df_catches = pd.DataFrame(
        columns=['fao_code', 'catch_fate', 'count', 'totalWeight'])

    for fish_file in liste_fct_extraction:
        df_per_extraction = create_catch_table_fish_perday(
            fish_file, row_number)
        df_catches = pd.concat(
            [df_catches, df_per_extraction], ignore_index=True)

    # Tester si les colonnes 'count' et 'totalWeight' contiennent des zéros
    not_catch = df_catches[(df_catches['count'] == 0) &
                           (df_catches['totalWeight'] == 0)]
    # Supprimer les lignes qui contiennent des zéros dans ces colonnes
    df_catches = df_catches.drop(not_catch.index)
    df_catches.reset_index(drop=True, inplace=True)

    return df_catches

# TopType et tracelineType sont unknown


def create_branchelines_composition(df_donnees_p1):
    """
    Fonction de construction du json pour les branchlineComposition

    Args:
        df_donnees_p1 (dataframe): page 1 du doc excel

    Returns:
        _type_: le json rempli à partir des infos de mon logbook
    """
    branchlines_composition = [{
        'homeId': None,
        'length': palangre_syc.views.extract_gear_info(df_donnees_p1).loc[palangre_syc.views.extract_gear_info(df_donnees_p1)['Logbook_name'] == 'Set Line length m', 'Value'].values[0],
        'proportion': None,
        'tracelineLength': None,
        'topType': "fr.ird.referential.ll.common.LineType#1239832686157#0.9",
        'tracelineType': "fr.ird.referential.ll.common.LineType#1239832686157#0.9",
    }]
    return branchlines_composition


def create_bait_composition(bait_datatable, allData):
    """
    Fonction de construction du json pour les BaitComposition

    Args:
        bait_datatable (datatable): datatable non vide 'Baits' construite in views.py
        allData (json):  Données de références

    Returns:
        _type_: le json rempli à partir des infos de mon logbook
    """
    total_baits = len(bait_datatable)
    MultipleBaits = []

    for index, row in bait_datatable.iterrows():
        BaitsComposition = {
            "homeId": None,
            "proportion": 100/total_baits,
            "individualSize": None,
            "individualWeight": None,
            "baitSettingStatus": None,
            "baitType": get_baittype_topiaid(row, allData),
        }
        MultipleBaits.append(BaitsComposition)

    return MultipleBaits


def create_floatline_composition(df_gear):
    """
    Fonction de construction du json pour les FloatlineComposition

    Args:
        df_donnees_p1 (dataframe): page 1 du doc excel

    Returns:
        _type_: le json rempli à partir des infos de mon logbook
    """
    floatlines_composition = [{
        "homeId": None,
        # "length": palangre_syc.views.extract_gear_info(df_donnees_p1).loc[palangre_syc.views.extract_gear_info(df_donnees_p1)['Logbook_name'] == 'Floatline length m', 'Value'].values[0],
        "length": df_gear.loc[df_gear['Logbook_name'] == 'Floatline length m', 'Value'].values[0],
        "proportion": 100,
        "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
    }]
    return floatlines_composition

# peut etre ajouter le healthStatus

def create_catches(datatable, allData):
    """
    Fonction de construction du json pour les catches

    Args:
        datatable (datatable): datatable créé pour une journée / un set
        allData (json):  Données de références

    Returns:
        _type_: le json rempli à partir des infos de mon logbook
    """
    MultipleCatches = []
    for n_ligne_datatable in range(len(datatable)):
        catches = {"homeId": None, }
        if get_species_topiaid(datatable.loc[n_ligne_datatable, 'fao_code'], allData) == 'fr.ird.referential.common.Species#1433499266610#0.696541526820511' or get_species_topiaid(datatable.loc[n_ligne_datatable, 'fao_code'], allData) == 'fr.ird.referential.common.Species#1239832685020#0.7691470969492022':
            catches.update({"comment": "Other fish non specified", })
        else:
            catches.update({"comment": None, })
        catches.update({"count": datatable.loc[n_ligne_datatable, 'count'],
                        "totalWeight": datatable.loc[n_ligne_datatable, 'totalWeight'],
                        "hookWhenDiscarded": None,
                        "depredated": None,
                        "beatDiameter": None,
                        "photoReferences": None,
                        "number": None,
                        "acquisitionMode": None,
                        "countDepredated": None,
                        "depredatedProportion": None,
                        "tagNumber": None,
                        "catchFate": get_catchfate_topiaid(datatable.loc[n_ligne_datatable, 'catch_fate'], allData),
                        "discardHealthStatus": None,
                        "species": get_species_topiaid(datatable.loc[n_ligne_datatable, 'fao_code'], allData),
                        "predator": [],
                        "catchHealthStatus": None,
                        "onBoardProcessing": get_processing_topiaid(datatable.loc[n_ligne_datatable, 'fao_code'], allData),
                        "weightMeasureMethod": None
                        })
        MultipleCatches.append(catches)
    return MultipleCatches


def create_starttimestamp(df_donnees_p1, allData, index_day, need_hour=bool):
    """ Fonction qui permet d'avoir le bon format de date-time pour envoyer le json

    Args:
        df_donnees_p1 (_type_): ma page excel 1
        allData (json):  Données de références
        index_day (int): le numero de la ligne de mon datatable
        need_hour (bool) : si true - on va chercher l'heure correspondante dans le datatable, 
        si false - on ajoute '00:00:00' cad que le bateau n'est pas en train de pêcher donc il nous faut une horaire juste pour convenir au format demandé

    Returns:
        _type_: la datetime au format qui permet l'insersion dans la bdd
    """
    if need_hour is True:
        time_ = palangre_syc.views.extract_time(df_donnees_p1, allData).loc[index_day, 'Time']
    else:
        time_ = '00:00:00'

    date_formated = '{}-{:02}-{:02}T{}.000Z'.format(
        palangre_syc.views.extract_logbook_date(df_donnees_p1).loc[palangre_syc.views.extract_logbook_date(
            df_donnees_p1)['Logbook_name'] == 'Year', 'Value'].values[0],
        palangre_syc.views.extract_logbook_date(df_donnees_p1).loc[palangre_syc.views.extract_logbook_date(
            df_donnees_p1)['Logbook_name'] == 'Month', 'Value'].values[0],
        palangre_syc.views.extract_time(df_donnees_p1, allData).loc[index_day, 'Day'], time_)
    return date_formated

def create_starttimestamp_from_field_date(date):
    """ 
    Fonction qui permet d'avoir le bon format de date-time pour envoyer le json

    Args: 
        date: issue du input 
        
    Returns:
        datetime: pour stratDate et endDAte
    """
    date_formated = '{}-{:02}-{:02}T{}.000Z'.format(
        date[:4],
        date[5:7],
        date[-2:],
        '00:00:00')
    return date_formated

def search_date_into_json(json_previoustrip, date_to_look_for):
    """
    Fonction qui cherche une date est présente dans un précédent trip (json file)

    Args:
        json_previoustrip (json): du précédent trip qu'on veut continuer
        date_to_look_for (date): aaaa-mm-jj 

    Returns:
        bool: True si la date est dans le json, False sinon
    """
 
    for content in json_previoustrip:
        for activity in content['activityLogbook'] :
            start_time = activity.get('startTimeStamp')
            if start_time and start_time.startswith(date_to_look_for) :
                return True
    return False
            
def create_activity_and_set(df_donnees_p1, df_donnees_p2, allData, start_extraction, end_extraction):
    
    #############################
    # messages d'erreurs
    if isinstance(palangre_syc.views.extract_gear_info(df_donnees_p1), tuple):
        df_gear, _ = palangre_syc.views.extract_gear_info(df_donnees_p1)
    else:
        df_gear = palangre_syc.views.extract_gear_info(df_donnees_p1)
        
    # mais pour l'instant on ne traite pas cette info anyways 
    if isinstance(palangre_syc.views.extract_line_material(df_donnees_p1), tuple):
        df_line, _ = palangre_syc.views.extract_line_material(df_donnees_p1)
    else:
        df_line = palangre_syc.views.extract_line_material(df_donnees_p1)  
    #############################

    
    MultipleActivity = []
    for i in range(start_extraction, end_extraction):
        set = {
            'homeId': None,
            'comment': None,
            'number': None,
            'basketsPerSectionCount': None,
            'branchlinesPerBasketCount': None,
            'totalSectionsCount': None,
            'totalBasketsCount': palangre_syc.views.extract_fishing_effort(df_donnees_p1).loc[i, 'Total hooks / Hooks per basket'],
            'totalHooksCount': palangre_syc.views.extract_fishing_effort(df_donnees_p1).loc[i, 'Total hooks'],
            'totalLightsticksCount': palangre_syc.views.extract_fishing_effort(df_donnees_p1).loc[i, 'Total lightsticks'],
            'weightedSnap': False,
            'snapWeight': None,
            'weightedSwivel': False,
            'swivelWeight': None,
            'timeBetweenHooks': None,
            'shooterUsed': False,
            'shooterSpeed': None,
            'maxDepthTargeted': None, }

        set.update({'settingStartTimeStamp': create_starttimestamp(df_donnees_p1, allData, index_day=i, need_hour=True)})

        set.update({'settingStartLatitude': palangre_syc.views.extract_positions(df_donnees_p1).loc[i, 'Latitude'],
                    'settingStartLongitude': palangre_syc.views.extract_positions(df_donnees_p1).loc[i, 'Longitude'],
                    'settingEndTimeStamp': None,
                    'settingEndLatitude': None,
                    'settingEndLongitude': None,
                    'settingVesselSpeed': None,
                    'haulingDirectionSameAsSetting': None,
                    'haulingStartTimeStamp': None,
                    'haulingStartLatitude': None,
                    'haulingStartLongitude': None,
                    'haulingEndTimeStamp': None,
                    'haulingEndLatitude': None,
                    'haulingEndLongitude': None,
                    'haulingBreaks': None,
                    'monitored': False,
                    # En fait "totalLineLength" serait de plusierus km, ce qui ne correspond pas avec le champ "Set Line length m"
                    # 'totalLineLength' : extract_gear_info(df_donnees_p1).loc[extract_gear_info(df_donnees_p1)['Logbook_name'] == 'Set Line length m', 'Value'].values[0],
                    'totalLineLength': None,
                    'basketLineLength': None,
                    'lengthBetweenBranchlines': df_gear.loc[df_gear['Logbook_name'] == 'Length between branches m', 'Value'].values[0]
                    })

        bait_datatable = palangre_syc.views.extract_bait(df_donnees_p1)
        set.update({'baitsComposition': create_bait_composition(bait_datatable, allData),})

        set.update({'floatlinesComposition': create_floatline_composition(df_gear),
                    'hooksComposition': [], 
                    'settingShape': None, })

        datatable = create_catch_table_fishes(
            df_donnees_p1, df_donnees_p2, row_number=i)
        set.update({
            'catches': create_catches(datatable, allData),
            'lineType': None,
            'lightsticksUsed': False,
            'lightsticksType': None,
            'lightsticksColor': None,
            'mitigationType': [],
            'branchlinesComposition': []
        })

        activity = {
            'homeId': None,
            'comment': None, }
        if palangre_syc.views.extract_time(df_donnees_p1, allData).loc[i, 'VesselActivity'] == 'fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1':
            activity.update({'startTimeStamp': create_starttimestamp(
                df_donnees_p1, allData, index_day=i, need_hour=True)})
        else:
            activity.update({'startTimeStamp': create_starttimestamp(df_donnees_p1, allData, index_day=i, need_hour=False)                             # 'startTimeStamp' : '2022-07-26T00:00:00.000Z'
                            , })

        activity.update({'endTimeStamp': None,
                        'latitude': palangre_syc.views.extract_positions(df_donnees_p1).loc[i, 'Latitude'],
                        'longitude': palangre_syc.views.extract_positions(df_donnees_p1).loc[i, 'Longitude'],
                        'seaSurfaceTemperature': palangre_syc.views.extract_temperature(df_donnees_p1).loc[i, 'Température'],
                        'wind': None,
                        'windDirection': None,
                        'currentSpeed': None,
                        'currentDirection': None,
                        'vesselActivity': palangre_syc.views.extract_time(df_donnees_p1, allData).loc[i, 'VesselActivity'],
                        'dataQuality': None,
                        'fpaZone': None,
                        'relatedObservedActivity': None,
                        })

        if activity.get('vesselActivity') == 'fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1':
            activity.update({'set': set, })
        else:
            activity.update({
                'set': None,
                'sample': None
            })

        MultipleActivity.append(activity)

    return MultipleActivity


def create_trip(df_donnees_p1, MultipleActivity, allData, context):
    # Dans le trip on a fixé :
    # tripType = Marée de pêche commerciale
    # observer = unknown car non présent
    # startDate et endDate sont entrées en dur aussi

    # species semble être TargetSpecies - a voir si on développe

    trip = {
        'homeId': None,
        'startDate': context['startDate'],
        'endDate': context['endDate'],
        'noOfCrewMembers': palangre_syc.views.extract_cruise_info(df_donnees_p1).loc[palangre_syc.views.extract_cruise_info(df_donnees_p1)['Logbook_name'] == 'No Of Crew', 'Value'].values[0],
        'ersId': None,
        'gearUseFeatures': None,
        'activityObs': None,
        'activityLogbook': MultipleActivity,
        'landing': None,
        'sample': None,
        'tripType': 'fr.ird.referential.ll.common.TripType#1464000000000#02',
        'observationMethod': None,
        'observer': 'fr.ird.referential.common.Person#1254317601353#0.6617065204572095',
        'vessel': get_vessel_topiaid(df_donnees_p1, allData),
        'observationsProgram': None,
        'logbookProgram': context['programtopiaid'],
        'captain': get_captain_topiaid(df_donnees_p1, allData),
        'observationsDataEntryOperator': None,
        'logbookDataEntryOperator': get_operator_topiaid(df_donnees_p1, allData),
        'sampleDataEntryOperator': None,
        'landingDataEntryOperator': None,
        'ocean': context['oceantopiaid'],
        'departureHarbour': context['depPort'],
        'landingHarbour': context['endPort'],
        'observationsDataQuality': None,
        'logbookDataQuality': None,
        'generalComment': None,
        'observationsComment': None,
        'logbookComment': None,
        'species': get_target_species_topiaid(df_donnees_p1, allData),
        'observationsAvailability': False,
        'logbookAvailability': True,
    }
    
    return trip


def remove_keys(obj, keys_to_remove):
    if isinstance(obj, dict):
        for key in keys_to_remove:
            obj.pop(key, None)
        for value in obj.values():
            remove_keys(value, keys_to_remove)
    elif isinstance(obj, list):
        for item in obj:
            remove_keys(item, keys_to_remove)
    return obj

def replace_null_false_true(obj):
    if isinstance(obj, dict):
        return {key: replace_null_false_true(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [replace_null_false_true(item) for item in obj]
    elif obj == "null":
        return None
    elif obj == "true":
        return True
    elif obj == "false":
        return False
    else:
        return obj


def pretty_print(json_data, file="sample.json", mode="a"):
    """ Fonction qui affiche avec les bonnes indentations un fichier json

    Args:
        json_data (json): Données json en entrée
        file (str, optional): Nom de fichier json de sortie "sample.json".
        mode (str, optional): Defaults to "a" pour "append" - "w" pour "write"
    """
    
    json_formatted_str = json.dumps(
        json_data, indent=2, default=palangre_syc.api.serialize)
    # print("¤"*20, "pretty print function" ,"¤"*20)
    # print("pretty print type ::::", type(json_formatted_str), 'and before it was :::', type(json_data))
    with open(file, mode) as outfile:
        outfile.write(json_formatted_str)


DIR = "./palangre_syc/media"




# if __name__ == "__main__":
#     start_time = time.time()
#     main()
#     print("--- %s seconds ---" % (time.time() - start_time))
