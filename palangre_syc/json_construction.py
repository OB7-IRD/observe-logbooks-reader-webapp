import pytz
from views import * 
import json, os
import numpy as np
import warnings
import api



def get_captain_topiaID(df_donnees_p1, data_common):
    for captain in data_common['content']['fr.ird.observe.entities.referential.common.Person']:
        
        captain_Logbook = extract_cruiseInfo_LL(df_donnees_p1).loc[extract_cruiseInfo_LL(df_donnees_p1)['Logbook_name'] == 'Captain', 'Value'].values[0]
        captain_json = captain['firstName'] + ' ' + captain['lastName']
        if captain_Logbook == captain_json :
            return captain['topiaId']
        else : 
            captain_Logbook = '[inconnu] [inconnu]'
            if captain_Logbook == captain_json :
                return captain['topiaId']
    return None

def get_lb_operator_topiaID(df_donnees_p1, data_common):
    for person in data_common['content']['fr.ird.observe.entities.referential.common.Person']:
        
        reported_Logbook = extract_reportInfo_LL(df_donnees_p1).loc[extract_reportInfo_LL(df_donnees_p1)['Logbook_name'] == 'Person reported', 'Value'].values[0]
        reported_json = person['firstName'] + ' ' + person['lastName']
        if reported_Logbook == reported_json :
            return person['topiaId']
        else : 
            reported_Logbook = '[inconnu] [inconnu]'
            if reported_Logbook == reported_json :
                return person['topiaId']
    return None


def get_vessel_topiaID(df_donnees_p1, data_common):
    ''' Fonction qui propose le topiaId du navire cité dans le logbook à partir de son 'nationlId' s'il existe 
    '''
    vessel_Logbook = extract_vesselInfo_LL(df_donnees_p1).loc[extract_vesselInfo_LL(df_donnees_p1)['Logbook_name'] == 'Official Number', 'Value'].values[0]
    for vessel in data_common["content"]["fr.ird.observe.entities.referential.common.Vessel"]:
        if 'nationalId' in vessel:
            vessel_json = vessel['nationalId']
            if vessel_Logbook == vessel_json :
                return vessel['topiaId']
    return None
                
def get_BaitType_topiaId(row, data_ll):
    BaitTypes = data_ll["content"]["fr.ird.observe.entities.referential.ll.common.BaitType"]
    if row['Value'] == 'V' : 
        Bait_logbook = row['Logbook_name']
        for BaitType in BaitTypes:
            if BaitType.get("label1")[:len(Bait_logbook)] == Bait_logbook :
                return BaitType["topiaId"]
    else : 
        return None

def get_Species_topiaID(FAO_code_logbook, data_common):
    '''
    Fonction 
    '''
    Species = data_common["content"]["fr.ird.observe.entities.referential.common.Species"]
    for Specie in Species:
        if 'faoCode' in Specie:
            # faoCode_json = Specie['faoCode']
            # if FAO_code_logbook == faoCode_json :
            #     return Specie['topiaId']
            if FAO_code_logbook in Specie.get("faoCode") :
                print(Specie['topiaId'])
                return Specie["topiaId"]
    else : 
        return None
    
def get_catchFate_topiaID(catchFate_logbook, data_ll):
    '''
    Fonction 
    '''
    Fates = data_ll["content"]["fr.ird.observe.entities.referential.ll.common.CatchFate"]
    for catchFate in Fates:
        if 'code' in catchFate:
            if catchFate.get("code") == catchFate_logbook:
                return catchFate["topiaId"]
    else : 
        return None


# Opimisation éventuelle : ajouter unparamètre qui permettrait de distinguer les fish des bycatch 
# notamment si les by catch son relachées A alive ou D dead

def construction_catch_table(fish_file):
    df_catches = pd.DataFrame(columns=['FAO_code', 'catchFate', 'count', 'totalWeight'])

    # On récupère les données des colonnes de FAO et catchFate
    for col in fish_file.columns:
        FAO_code = col[-3:]
        catchFate = col[-7:-4] 
        df_catches.loc[len(df_catches)] = {'FAO_code': FAO_code, 'catchFate': catchFate}
    
    # On supprime les doublons
    df_catches = df_catches.drop_duplicates()
    df_catches.reset_index(drop=True, inplace=True)
    
    return df_catches

# a voir si c'est pertinent en terme de gain de temps de découper la fonction ici en 2 
# on pourrait avoir une fonctionn qui gère les lignes issues des noms de colonnes
# et une seconde fonction qui remplirait les lignes count et totalWeight en allant chercher les infos dans le excel

def create_catch_table_fish_perday(fish_file, row_number):
    '''
    Fonction qui prend en argument (1) une fonction d'extraction de données de poisson gardés à bord 
    et (2) une ligne (ou un jour de pêche) à extraire
    Elle ressort un dataframe (par type de poisson pêché et par jour de pêche) de 4 colonnes 
    Ce dataframe continet les champs obligatoires à remplir dans la table 'catch' de Observe
    '''
    df_catches = construction_catch_table(fish_file)
    
    # On rempli la suite du dataframe pour count et totalWeight (pour une ligne donnée)
    for index, row in df_catches.iterrows():
        col_end_name = row['catchFate'] + ' ' + row['FAO_code']
        for col in fish_file.columns:
            if col[-7:] == col_end_name : 
                if col[:2] == 'No':
                    fish_file_colname = 'No' + ' ' + col_end_name
                    count = fish_file.loc[row_number, fish_file_colname]
                    df_catches.loc[index, 'count'] = count
                    # df_catches.loc[index, 'count'] = int(df_catches.loc[index, 'count'])

                if col[:2] == 'Kg':
                    fish_file_colname = 'Kg' + ' ' + col_end_name
                    totalWeight = fish_file.loc[row_number, fish_file_colname]
                    df_catches.loc[index, 'totalWeight'] = totalWeight
                    # df_catches.loc[index, 'totalWeight'] = int(df_catches.loc[index, 'totalWeight'])
                
                # a voir si on veut des Nan car il n'y a pas de donnée ou des 0
                else : 
                    df_catches.loc[index, 'totalWeight'] = int(0)
    
    return df_catches


def create_catch_table_fishes(df_donnees_p1, df_donnees_p2, row_number):
    # print("create_catch_table_fishes")
    liste_fct_extraction = [extract_tunas(df_donnees_p1), 
                            extract_billfishes(df_donnees_p1), 
                            extract_otherfish(df_donnees_p1), 
                            extract_sharksFAL(df_donnees_p2), 
                            extract_sharksBSH(df_donnees_p2), 
                            extract_sharksMAK(df_donnees_p2), 
                            extract_sharksSPN(df_donnees_p2),
                            extract_sharksTIG(df_donnees_p2),
                            extract_sharksPSK(df_donnees_p2),
                            extract_sharksTHR(df_donnees_p2),
                            extract_sharksOCS(df_donnees_p2),
                            extract_mammals(df_donnees_p2),
                            extract_seabird(df_donnees_p2),
                            extract_turtles(df_donnees_p2)]
    
    df_catches = pd.DataFrame(columns=['FAO_code', 'catchFate', 'count', 'totalWeight'])
    
    for fish_file in liste_fct_extraction :
        df_per_extraction = create_catch_table_fish_perday(fish_file, row_number)
        df_catches = pd.concat([df_catches, df_per_extraction], ignore_index=True)
    
    # Tester si les colonnes 'count' et 'totalWeight' contiennent des zéros
    not_catch = df_catches[(df_catches['count'] == 0) & (df_catches['totalWeight'] == 0)]
    # Supprimer les lignes qui contiennent des zéros dans ces colonnes
    df_catches = df_catches.drop(not_catch.index)
    df_catches.reset_index(drop=True, inplace=True)

    return df_catches

# TopType et tracelineType sont unknown
def create_branchelinesComposition(df_donnees_p1):
    branchlinesComposition = [{
        'homeId'  : None,
        'length' : extract_gearInfo_LL(df_donnees_p1).loc[extract_gearInfo_LL(df_donnees_p1)['Logbook_name'] == 'Set Line length m', 'Value'].values[0], 
        'proportion' : None, 
        'tracelineLength' : None, 
        'topType' : "fr.ird.referential.ll.common.LineType#1239832686157#0.9", 
        'tracelineType'  : "fr.ird.referential.ll.common.LineType#1239832686157#0.9",
        }]
    return branchlinesComposition

    
def create_BaitComposition(bait_datatable, data_ll):
    '''
    Fonction qui prend en arguemnt la table extraite de Baits, filtre pour conserver uniquement les données non vides
    et ressort le BaitsComposition
    '''
    baits_used = bait_datatable.loc[bait_datatable['Value'] != "None"]
    total_baits = len(baits_used)
    MultipleBaits = []
            
    for index, row in baits_used.iterrows() : 
        BaitsComposition = {
            "homeId": None,
            "proportion": 100/total_baits,
            "individualSize": None,
            "individualWeight": None,
            "baitSettingStatus": None,
            "baitType": get_BaitType_topiaId(row, data_ll), 
        }
        MultipleBaits.append(BaitsComposition)

    return MultipleBaits


def create_FloatlineComposition(df_donnees_p1):
    FloatlinesComposition = [{
        "homeId": None,
        "length": extract_gearInfo_LL(df_donnees_p1).loc[extract_gearInfo_LL(df_donnees_p1)['Logbook_name'] == 'Floatline length m', 'Value'].values[0],
        "proportion": 100,
        "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
    }]
    return FloatlinesComposition

# peut etre ajouter le healthStatus
def create_catches(datatable, data_common, data_ll):
    MultipleCatches = []
    for n_ligne_datatable in range(len(datatable)):
        catches = {
        "homeId" : None,
        "comment": None,
        "count" : datatable.loc[n_ligne_datatable, 'count'], 
        # "count" : 7,
        "totalWeight": datatable.loc[n_ligne_datatable, 'totalWeight'],
        # "totalWeight": 35,
        "hookWhenDiscarded": None,
        "depredated": None,
        "beatDiameter": None,
        "photoReferences": None,
        "number": None,
        "acquisitionMode": None,
        "countDepredated": None,
        "depredatedProportion": None,
        "tagNumber": None,
        "catchFate": get_catchFate_topiaID(datatable.loc[n_ligne_datatable, 'catchFate'], data_ll),
        # "catchFate": 'fr.ird.referential.ll.common.CatchFate#1239832686125#0.2', 
        "discardHealthStatus": None,
        "species": get_Species_topiaID(datatable.loc[n_ligne_datatable, 'FAO_code'], data_common),
        # "species": 'fr.ird.referential.common.Species#1239832683725#0.39445809291491807', 
        "predator": [],
        "catchHealthStatus": None,
        "onBoardProcessing": None,
        "weightMeasureMethod": None 
        }
        MultipleCatches.append(catches)
    return MultipleCatches

def create_starttimestamp(df_donnees_p1, data_ll, index_day, need_hour = bool):
    """ Fonction qui permet d'avoir le bon format de date-time pour envoyer le json

    Args:
        df_donnees_p1 (_type_): ma page excel 1
        data_ll (_type_): Données de ref pour ll
        index_day (_type_): le numero de la ligne de mon datatable
        need_hour (bool) : si true - on va chercher l'heure correspondante dans le datatable, 
        si false - on ajoute '00:00:00' cad que le bateau n'est pas en train de p9^cher donc il nous faut une horaire juste pour convenir au format demandé

    Returns:
        _type_: la datetime au format qui permet l'insersion dans la bdd
    """
    if need_hour == True : 
        time_ = extract_time(df_donnees_p1, data_ll).loc[index_day, 'Time']
    else : 
        time_ = '00:00:00'
        
    date_formated = '{}-{:02}-{:02}T{}.000Z'.format(
        extract_logbookDate_LL(df_donnees_p1).loc[extract_logbookDate_LL(df_donnees_p1)['Logbook_name'] == 'Year', 'Value'].values[0],
        extract_logbookDate_LL(df_donnees_p1).loc[extract_logbookDate_LL(df_donnees_p1)['Logbook_name'] == 'Month', 'Value'].values[0],
        extract_time(df_donnees_p1, data_ll).loc[index_day, 'Day'],
        time_) 
    return date_formated

def pretty_print(json_data, file = "sample.json", mode ="a"):
    print(json_data)
    json_formatted_str = json.dumps(json_data, indent=2, default=api.serialize)
    with open(file, mode) as outfile:
        outfile.write(json_formatted_str)


def main():
      
    warnings.simplefilter(action='ignore', category=FutureWarning)

    if os.path.exists("sample.json") : 
        print("="*80)
        os.remove("sample.json")

    print("="*80)
    print("Load JSON data file")
    
    file_path = './palangre_syc/media/july2022-FV GOLDEN FULL NO.168.xlsx'
    with open('./data_common.json', 'r', encoding = 'utf-8') as f:
        data_common = json.load(f)
    with open('./data_ll.json', 'r', encoding = 'utf-8') as f:
        data_ll = json.load(f) 

    print("="*80)
    print("Read excel file")
    
    df_donnees_p1 = read_excel(file_path, 1)
    df_donnees_p2 = read_excel(file_path, 2)
    
    print("="*80)
    print("Create Activity and Set")
        
    days_in_a_month = len(extract_positions(df_donnees_p1))
    # MultipleSet = []
    MultipleActivity = []
    for i in range(0, days_in_a_month):
        set = {
            'homeId' : None, 
            'comment' : None,
            'number' : None,
            'basketsPerSectionCount' : None,
            'branchlinesPerBasketCount': extract_gearInfo_LL(df_donnees_p1).loc[extract_gearInfo_LL(df_donnees_p1)['Logbook_name'] == 'Branchline length m', 'Value'].values[0], 
            'totalSectionsCount' : None, 
            # 'totalBasketsCount' : extract_fishingEffort(file_path).loc[extract_fishingEffort(file_path)['Day'] == index + 1, 'Hooks'].values[0], 
            # Lui je sais pas si la valeur correspond bien enft
            'totalBasketsCount' : extract_fishingEffort(df_donnees_p1).loc[i, 'Hooks'], 
            'totalHooksCount' : extract_fishingEffort(df_donnees_p1).loc[i, 'Total hooks'],             
            'totalLightsticksCount' : extract_fishingEffort(df_donnees_p1).loc[i, 'Total lightsticks'], 
            'totalLightsticksCount' : None, 
            'weightedSnap' : False, 
            'snapWeight' : None, 
            'weightedSwivel' : False, 
            'swivelWeight' : None, 
            'timeBetweenHooks' : None, 
            'shooterUsed' : False, 
            'shooterSpeed' : None, 
            'maxDepthTargeted' : None,}
            
        set.update({'settingStartTimeStamp' : create_starttimestamp(df_donnees_p1, data_ll, index_day= i, need_hour=True)
                # '2023-04-30T06:00:00.000Z',
            })
   
        set.update({'settingStartLatitude' : extract_positions(df_donnees_p1).loc[i, 'Latitute'],
            'settingStartLongitude' : extract_positions(df_donnees_p1).loc[i, 'Longitude'],
            'settingEndTimeStamp' : None, 
            'settingEndLatitude' : None, 
            'settingEndLongitude' : None, 
            'settingVesselSpeed'  : None, 
            'haulingDirectionSameAsSetting' : None, 
            'haulingStartTimeStamp' : None, 
            'haulingStartLatitude' : None, 
            'haulingStartLongitude' : None, 
            'haulingEndTimeStamp' : None, 
            'haulingEndLatitude' : None, 
            'haulingEndLongitude'  : None,
            'haulingBreaks' : None, 
            'monitored' : False, 
            'totalLineLength' : extract_gearInfo_LL(df_donnees_p1).loc[extract_gearInfo_LL(df_donnees_p1)['Logbook_name'] == 'Set Line length m', 'Value'].values[0], 
            'basketLineLength' : None, 
            'lengthBetweenBranchlines' : extract_gearInfo_LL(df_donnees_p1).loc[extract_gearInfo_LL(df_donnees_p1)['Logbook_name'] == 'Length between branches m', 'Value'].values[0]
            })
            
        bait_datatable = extract_bait_LL(df_donnees_p1)
        set.update({'baitsComposition' : create_BaitComposition(bait_datatable, data_ll),})
        
        set.update({'floatlinesComposition' : create_FloatlineComposition(df_donnees_p1),   
            'hooksComposition' : [], 
            'settingShape' : None, })
        
        datatable = create_catch_table_fishes(df_donnees_p1, df_donnees_p2, row_number = i)
        print(datatable)
        set.update({'catches' : create_catches(datatable, data_common, data_ll),})
        # set.update({'catches' : [], })
        # set.update({"catches": [
        #     {
        #         "homeId": None,
        #         "comment": None,
        #         "count": 1.0,
        #         "totalWeight": 18.0,
        #         "hookWhenDiscarded": None,
        #         "depredated": None,
        #         "beatDiameter": None,
        #         "photoReferences": None,
        #         "number": None,
        #         "acquisitionMode": None,
        #         "countDepredated": None,
        #         "depredatedProportion": None,
        #         "tagNumber": None,
        #         "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
        #         "discardHealthStatus": None,
        #         "species": "fr.ird.referential.common.Species#1239832685474#0.8943253454598569",
        #         "predator": None,
        #         # "catchHealthStatus": "fr.ird.referential.ll.common.HealthStatus#1239832686128#0.4",
        #         "catchHealthStatus": None,
        #         "onBoardProcessing": None,
        #         # "onBoardProcessing": "fr.ird.referential.ll.common.OnBoardProcessing#1464000000000#0.3",
        #         "weightMeasureMethod": None,
        #         # "weightMeasureMethod": "fr.ird.referential.common.WeightMeasureMethod#666#03"
        #     },
        #     {
        #         "homeId": None,
        #         "comment": None,
        #         "count": 1.0,
        #         "totalWeight": 6.0,
        #         "hookWhenDiscarded": None,
        #         "depredated": None,
        #         "beatDiameter": None,
        #         "photoReferences": None,
        #         "number": None,
        #         "acquisitionMode": None,
        #         "countDepredated": None,
        #         "depredatedProportion": None,
        #         "tagNumber": None,
        #         "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
        #         "discardHealthStatus": None,
        #         "species": "fr.ird.referential.common.Species#1239832683725#0.39445809291491807",
        #         "predator": [],
        #         "catchHealthStatus": None,
        #         # "catchHealthStatus": "fr.ird.referential.ll.common.HealthStatus#1239832686128#0.4",
        #         "onBoardProcessing": None,
        #         # "onBoardProcessing": "fr.ird.referential.ll.common.OnBoardProcessing#1464000000000#0.3",
        #         "weightMeasureMethod": None,
        #         # "weightMeasureMethod": "fr.ird.referential.common.WeightMeasureMethod#666#03"
        #         }
        #      ],})
        
            
        set.update({'lineType' : None, 
            'lightsticksUsed' : False, 
            'lightsticksType' : None, 
            'lightsticksColor' : None, 
            'mitigationType' : [],
            # 'branchlinesComposition': create_branchelinesComposition(df_donnees_p1)
            'branchlinesComposition': []
        })
        
        # MultipleSet.append(set)
        
        
        
        
        ######
        # on va copier coller un code de la documentation, voir si c'est ok ! 
        set2 = {
            "homeId": "FINSS-1093484",
            "comment": None,
            "number": None,
            "basketsPerSectionCount": None,
            "branchlinesPerBasketCount": None,
            "totalSectionsCount": None,
            "totalBasketsCount": None,
            "totalHooksCount": None,
            "lightsticksPerBasketCount": None,
            "totalLightsticksCount": None,
            "weightedSnap": False,
            "snapWeight": None,
            "weightedSwivel": False,
            "swivelWeight": None,
            "timeBetweenHooks": None,
            "shooterUsed": False,
            "shooterSpeed": None,
            "maxDepthTargeted": None,
            "settingStartTimeStamp": create_starttimestamp(df_donnees_p1, data_ll, index_day= 1, need_hour=True),
            "settingStartLatitude": -2.116667,
            "settingStartLongitude": 55.05,
            "settingEndTimeStamp": None,
            "settingEndLatitude": None,
            "settingEndLongitude": None,
            "settingVesselSpeed": None,
            "haulingDirectionSameAsSetting": None,
            "haulingStartTimeStamp": None,
            "haulingStartLatitude": None,
            "haulingStartLongitude": None,
            "haulingEndTimeStamp": None,
            "haulingEndLatitude": -1.65,
            "haulingEndLongitude": 54.816666,
            "haulingBreaks": None,
            "monitored": False,
            "totalLineLength": None,
            "basketLineLength": None,
            "lengthBetweenBranchlines": None,
            "baitsComposition": [
        # {
        #     "homeId": None,
        #     "proportion": 34.0,
        #     "individualSize": 1.0,
        #     "individualWeight": 0.49,
        #     "baitSettingStatus": "fr.ird.referential.ll.common.BaitSettingStatus#1239832686123#0.1",
        #     "baitType": "fr.ird.referential.ll.common.BaitType#1239832686124#0.1"
        #     },
        #     {
        #     "homeId": None,
        #     "proportion": 66.0,
        #     "individualSize": 2.0,
        #     "individualWeight": 1.0,
        #     "baitSettingStatus": "fr.ird.referential.ll.common.BaitSettingStatus#1239832686123#0.3",
        #     "baitType": "fr.ird.referential.ll.common.BaitType#1239832686124#1.0"
        #     }
        ],
            "floatlinesComposition": [
            # {
            # "homeId": None,
            # "length": 12.0,
            # "proportion": 90.0,
            # "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
            # },
            # {
            # "homeId": None,
            # "length": 1.0,
            # "proportion": 10.0,
            # "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
            # }
        ],
            "hooksComposition": [
            # {
            #     "homeId": None,
            #     "proportion": 23.0,
            #     "hookOffset": 12.0,
            #     "hookType": "fr.ird.referential.ll.common.HookType#1433499457247#0.796845980919898",
            #     "hookSize": "fr.ird.referential.ll.common.HookSize#1239832686151#0.2"
            #     },
            # {
            #     "homeId": None,
            #     "proportion": 77.0,
            #     "hookOffset": 1.0,
            #     "hookType": "fr.ird.referential.ll.common.HookType#1239832686152#0.5",
            #     "hookSize": "fr.ird.referential.ll.common.HookSize#1239832686151#0.3"
            # }
            ],
            "settingShape": None,
            "catches": [
            {
                "homeId": None,
                "comment": None,
                "count": 1.0,
                "totalWeight": 18.0,
                "hookWhenDiscarded": None,
                "depredated": None,
                "beatDiameter": None,
                "photoReferences": None,
                "number": None,
                "acquisitionMode": None,
                "countDepredated": None,
                "depredatedProportion": None,
                "tagNumber": None,
                "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
                "discardHealthStatus": None,
                "species": "fr.ird.referential.common.Species#1239832685474#0.8943253454598569",
                "predator": None,
                # "catchHealthStatus": "fr.ird.referential.ll.common.HealthStatus#1239832686128#0.4",
                "catchHealthStatus": None,
                "onBoardProcessing": None,
                # "onBoardProcessing": "fr.ird.referential.ll.common.OnBoardProcessing#1464000000000#0.3",
                "weightMeasureMethod": None,
                # "weightMeasureMethod": "fr.ird.referential.common.WeightMeasureMethod#666#03"
            },
            {
                "homeId": None,
                "comment": None,
                "count": 1.0,
                "totalWeight": 6.0,
                "hookWhenDiscarded": None,
                "depredated": None,
                "beatDiameter": None,
                "photoReferences": None,
                "number": None,
                "acquisitionMode": None,
                "countDepredated": None,
                "depredatedProportion": None,
                "tagNumber": None,
                "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
                "discardHealthStatus": None,
                "species": "fr.ird.referential.common.Species#1239832683725#0.39445809291491807",
                "predator": [],
                "catchHealthStatus": None,
                # "catchHealthStatus": "fr.ird.referential.ll.common.HealthStatus#1239832686128#0.4",
                "onBoardProcessing": None,
                # "onBoardProcessing": "fr.ird.referential.ll.common.OnBoardProcessing#1464000000000#0.3",
                "weightMeasureMethod": None,
                # "weightMeasureMethod": "fr.ird.referential.common.WeightMeasureMethod#666#03"
                }
             ],
            "lineType": None,
            "lightsticksUsed": False,
            "lightsticksType": None,
            "lightsticksColor": None,
            "mitigationType": [
            #     "fr.ird.referential.ll.common.MitigationType#1239832686140#0.12",
            #     "fr.ird.referential.ll.common.MitigationType#1239832686140#0.14"
            ],
            "branchlinesComposition": [
                # {
                # "homeId": None,
                # "length": 12.0,
                # "proportion": 97.0,
                # "tracelineLength": None,
                # "topType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9",
                # "tracelineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
                # },
                # {
                # "homeId": None,
                # "length": 1.0,
                # "proportion": 3.0,
                # "tracelineLength": None,
                # "topType": "fr.ird.referential.ll.common.LineType#1239832686157#0.5",
                # "tracelineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.6"
                # }
        ]
        }
            
            
            
            ######
            
            
        activity = {
            'homeId' : None, 
            'comment' : None,}
        if extract_time(df_donnees_p1, data_ll).loc[i, 'VesselActivity'] == 'fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1' :
            # activity.update({'startTimeStamp' : extract_time(df_donnees_p1, data_ll).loc[days, 'Time'],})
            activity.update({'startTimeStamp' : create_starttimestamp(df_donnees_p1, data_ll, index_day= i, need_hour=True)
                # '2023-04-26T06:00:00.000Z',
                })
        else : 
            activity.update({'startTimeStamp' : create_starttimestamp(df_donnees_p1, data_ll, index_day= i, need_hour=False)
                # 'startTimeStamp' : '2022-07-26T00:00:00.000Z'
                ,})
            
        activity.update({'endTimeStamp' : None,
            'latitude' : extract_positions(df_donnees_p1).loc[i, 'Latitute'],
            'longitude' : extract_positions(df_donnees_p1).loc[i, 'Longitude'], 
            'seaSurfaceTemperature' : extract_temperature(df_donnees_p1).loc[i, 'Température'], 
            'wind' : None, 
            'windDirection' : None, 
            'currentSpeed' : None, 
            'currentDirection' : None, 
            'vesselActivity' : extract_time(df_donnees_p1, data_ll).loc[i, 'VesselActivity'], 
            # 'vesselActivity' : 'fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1',
            'dataQuality' : None, 
            'fpaZone' : None, 
            'relatedObservedActivity' : None, 
            # 'set' : MultipleSet, 
            })
        
        if activity.get('vesselActivity') == 'fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1' :
            activity.update({'set' : set,})
        else :
            activity.update({
            'set' : None,
            'sample' : None
            })
        
        MultipleActivity.append(activity)
         
    print("="*80)
    print("Create Trip")
    
    # Dans le trip on a fixé :
    # ocean = Océan indien
    # tripType = Marée de pêche commerciale 
    # observer = unknown car non présent
    # logbookProgram = Sandbox
    # startDate et endDate sont entrées en dur aussi
    
    # species semble être TargetSpecies - a voir si on développe
    trip = {
        'homeId' : None, 
        # 'startDate' : extract_cruiseInfo_LL(df_donnees_p1).loc[extract_cruiseInfo_LL(df_donnees_p1)['Logbook_name'] == 'Departure Date', 'Value'].values[0],
        # 'endDate' : extract_cruiseInfo_LL(df_donnees_p1).loc[extract_cruiseInfo_LL(df_donnees_p1)['Logbook_name'] == 'Arrival Date', 'Value'].values[0],
        # 'startDate' : datetime.datetime(2023,4,26,2,0, tzinfo=pytz.utc),
        # 'endDate' :  datetime.datetime(2023,5,26,5,9, tzinfo=pytz.utc),
        "startDate": "2022-07-01T00:00:00.000Z",
        "endDate": "2022-07-31T00:00:00.000Z",
        'noOfCrewMembers' : extract_cruiseInfo_LL(df_donnees_p1).loc[extract_cruiseInfo_LL(df_donnees_p1)['Logbook_name'] == 'No Of Crew', 'Value'].values[0],
        'ersId' : None, 
        'gearUseFeatures' : None, 
        'activityObs' : None, 
        'activityLogbook' : MultipleActivity, 
        # 'activityLogbook' : None,
        'landing' : None, 
        'sample' : None, 
        'tripType' : 'fr.ird.referential.ll.common.TripType#1464000000000#02', 
        'observationMethod' : None, 
        'observer' : 'fr.ird.referential.common.Person#1254317601353#0.6617065204572095', 
        'vessel' : get_vessel_topiaID(df_donnees_p1, data_common), 
        'observationsProgram' : None, 
        'logbookProgram' : 'fr.ird.referential.ll.common.Program#1707391938404#0.8314199988069012', 
        'captain' : get_captain_topiaID(df_donnees_p1, data_common),
        'observationsDataEntryOperator' : None,
        'logbookDataEntryOperator' : get_lb_operator_topiaID(df_donnees_p1, data_common),
        'sampleDataEntryOperator' : None,
        'landingDataEntryOperator' : None,
        'ocean' : 'fr.ird.referential.common.Ocean#1239832686152#0.8325731048817705', 
        # departureHarbour et landingHarbour à remplir
        'departureHarbour' : None, 
        'landingHarbour' : None, 
        'observationsDataQuality'  : None, 
        'logbookDataQuality' : None, 
        'generalComment' : None, 
        'observationsComment' : None, 
        'logbookComment' : None, 
        'species' : None, 
        'observationsAvailability' : False, 
        'logbookAvailability'  : True,
    }

    # pretty_print(trip)
    
    token = get_token()
    url_base = 'https://observe.ob7.ird.fr/observeweb/api/public'

    api.send_trip(token, trip, url_base)
    api.close(token)
       
    

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
    