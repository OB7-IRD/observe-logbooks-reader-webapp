from views import * 
import json, os
import numpy as np
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

if os.path.exists("sample.json") : 
    os.remove("sample.json")
def pretty_print(json_data):
    def convert_to_serializable(obj):
        if isinstance(obj, np.int64):
            return int(obj)
        raise TypeError("Type not serializable")
    json_formatted_str = json.dumps(json_data, indent=2, default=convert_to_serializable)
    with open("sample.json", "a") as outfile:
        outfile.write(json_formatted_str)

file_path = './palangre_syc/media/july2022-FV GOLDEN FULL NO.168.xlsx'
with open('./data_common.json', 'r', encoding = 'utf-8') as f:
    data_common = json.load(f)
with open('./data_ll.json', 'r', encoding = 'utf-8') as f:
    data_ll = json.load(f) 


def get_captain_topiaID(file_path):
    for captain in data_common['content']['fr.ird.observe.entities.referential.common.Person']:
        
        captain_Logbook = extract_cruiseInfo_LL(file_path).loc[extract_cruiseInfo_LL(file_path)['Logbook_name'] == 'Captain', 'Value'].values[0]
        captain_json = captain['firstName'] + ' ' + captain['lastName']
        if captain_Logbook == captain_json :
            return captain['topiaId']
    return None

if 'content' in data_common and 'fr.ird.observe.entities.referential.common.Vessel' in data_common['content']:
    vessel_data = data_common['content']['fr.ird.observe.entities.referential.common.Vessel']


def get_vessel_topiaID(file_path):
    ''' Fonction qui propose le topiaId du navire cité dans le logbook à partir de son 'nationlId' s'il existe 
    '''
    vessel_Logbook = extract_vesselInfo_LL(file_path).loc[extract_vesselInfo_LL(file_path)['Logbook_name'] == 'Official Number', 'Value'].values[0]
    for vessel in data_common["content"]["fr.ird.observe.entities.referential.common.Vessel"]:
        if 'nationalId' in vessel:
            vessel_json = vessel['nationalId']
            if vessel_Logbook == vessel_json :
                return vessel['topiaId']
    return None

def get_VesselActivity_topiaID(startTimeStamp):
    '''
    Fonction qui prend en argument une heure de depart et qui donne un topiaID de VesselActivity en fonction du type et du contenu de l'entrée
    cad si'il y a une heure - on est en activité de pêche,
    En revanche si c'est du texte qui contient "CRUIS" alors on est en cruise, 
    et s'il contient 'PORT' alors le bateau est au port 
    'FISHING
    '''
    if ":" in startTimeStamp:
        code = "FO"
    
    elif 'CRUIS' in startTimeStamp : 
        code = "CRUISE"
        
    elif 'PORT' in startTimeStamp : 
        code = "PORT"
    
    elif startTimeStamp == None:
        return None  
    
    else : 
        code = "OTH"
    
    VesselActivities = data_ll["content"]["fr.ird.observe.entities.referential.ll.common.VesselActivity"]
    for VesselActivity in VesselActivities:
        if VesselActivity.get("code") == code:
            return VesselActivity["topiaId"]
         
    return None
                
def get_BaitType_topiaId(row):
    BaitTypes = data_ll["content"]["fr.ird.observe.entities.referential.ll.common.BaitType"]
    if row['Value'] == 'V' : 
        Bait_logbook = row['Logbook_name']
        for BaitType in BaitTypes:
            if BaitType.get("label1")[:len(Bait_logbook)] == Bait_logbook :
                return BaitType["topiaId"]
    else : 
        return None

def get_Species_topiaID(FAO_code_logbook):
    '''
    Fonction 
    '''
    Species = data_common["content"]["fr.ird.observe.entities.referential.common.Species"]
    for Specie in Species:
        if 'faoCode' in Specie:
            # faoCode_json = Specie['faoCode']
            # if FAO_code_logbook == faoCode_json :
            #     return Specie['topiaId']
            if Specie.get("faoCode") == FAO_code_logbook:
                return Specie["topiaId"]
    else : 
        return None
    
def get_catchFate_topiaID(catchFate_logbook):
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
    df_catches = pd.DataFrame(columns=['FAO_code', 'catchFate', 'count', 'totalWeight'])

    # On récupère les données des colonnes de FAO et catchFate
    for col in fish_file.columns:
        FAO_code = col[-3:]
        catchFate = col[-7:-4] 
        df_catches.loc[len(df_catches)] = {'FAO_code': FAO_code, 'catchFate': catchFate}
            
    # Supprimer les doublons
    df_catches = df_catches.drop_duplicates()
    
    # On rempli la suite du dataframe pour count et totalWeight (pour une ligne donnée)
    for index, row in df_catches.iterrows():
        col_end_name = df_catches.loc[index, 'catchFate'] + " " + df_catches.loc[index, 'FAO_code']
        for col in fish_file.columns:
            if col[-7:] == col_end_name : 
                if col[:2] == 'No':
                    fish_file_colname = 'No' + ' ' + col_end_name
                    count = fish_file.loc[row_number, fish_file_colname]
                    df_catches.loc[index, 'count'] = count
                    df_catches.loc[index, 'count'] = int(df_catches.loc[index, 'count'])

                if col[:2] == 'Kg':
                    fish_file_colname = 'Kg' + ' ' + col_end_name
                    totalWeight = fish_file.loc[row_number, fish_file_colname]
                    df_catches.loc[index, 'totalWeight'] = totalWeight
                    df_catches.loc[index, 'totalWeight'] = int(df_catches.loc[index, 'totalWeight'])
                
                # a voir si on veut des Nan car il n'y a pas de donnée ou des 0
                else : 
                    df_catches.loc[index, 'totalWeight'] = int(0)
    return df_catches


def create_catch_table_fishes(file_path, row_number):
    liste_fct_extraction = [extract_tunas(file_path), 
                            extract_billfishes(file_path), 
                            extract_otherfish(file_path), 
                            extract_sharksFAL(file_path), 
                            extract_sharksBSH(file_path), 
                            extract_sharksMAK(file_path), 
                            extract_sharksSPN(file_path),
                            extract_sharksTIG(file_path),
                            extract_sharksPSK(file_path),
                            extract_sharksTHR(file_path),
                            extract_sharksOCS(file_path),
                            extract_mammals(file_path),
                            extract_seabird(file_path),
                            extract_turtles(file_path)
                            ]
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

print(create_catch_table_fishes(file_path, 0))

def create_branchelinesComposition(file_path):
    branchlinesComposition = {
        'homeId'  : '',
        'length' : extract_gearInfo_LL(file_path).loc[extract_gearInfo_LL(file_path)['Logbook_name'] == 'Set Line length m', 'Value'].values[0], 
        'proportion' : '', 
        'tracelineLength' : '', 
        'topType' : '', 
        'tracelineType'  : '',
        } 
    return branchlinesComposition

def create_BaitComposition(row):
    BaitsComposition = {
        "homeId": index,
        "proportion": '',
        "individualSize": '',
        "individualWeight": '',
        "baitSettingStatus": '',
        "baitType": get_BaitType_topiaId(row)
    }
    if BaitsComposition["baitType"] is not None:
        return BaitsComposition
    else :
        return BaitsComposition 





Trip = {
    'homeId' : 1, 
    'startDate' : extract_cruiseInfo_LL(file_path).loc[extract_cruiseInfo_LL(file_path)['Logbook_name'] == 'Departure Date', 'Value'].values[0],
    'endDate' : extract_cruiseInfo_LL(file_path).loc[extract_cruiseInfo_LL(file_path)['Logbook_name'] == 'Arrival Date', 'Value'].values[0],
    'noOfCrewMembers' : extract_cruiseInfo_LL(file_path).loc[extract_cruiseInfo_LL(file_path)['Logbook_name'] == 'No Of Crew', 'Value'].values[0],
    'ersId' : '', 
    'gearUseFeatures' : '', 
    'activityObs' : '', 
    'activityLogbook' : '', 
    'landing' : '', 
    'sample' : '', 
    'tripType' : '', 
    'observationMethod' : '', 
    'observer' : '', 
    'vessel' : get_vessel_topiaID(file_path), 
    'observationsProgram' : '', 
    'logbookProgram' : '', 
    'captain' : '', 
    'observationsDataEntryOperator' : '',
    'logbookDataEntryOperator' : '',
    'sampleDataEntryOperator' : '',
    'landingDataEntryOperator' :'',
    'ocean' : '', 
    'departureHarbour' : '', 
    'landingHarbour' : '', 
    'observationsDataQuality'  : '', 
    'logbookDataQuality' : '', 
    'generalComment' : '', 
    'observationsComment' : '', 
    'logbookComment' : '', 
    'species' : '', 
    'observationsAvailability' : '', 
    'logbookAvailability'  : '',
}

   
# def get_LineType_topiaId(file_path):
    
LineType = {
    "code": 'MON',
    "uri": '',
    "homeId": '',
    "needComment": '',
    "status": "enabled",
    "label1": "Monofilament nylon",
    "label2": "Nylon Monofilament",
    "label3": "Monofilament nylon",
    "label4": '',
    "label5": '',
    "label6": '',
    "label7": '',
    "label8": ''
}
    

# for index, row in extract_bait_LL(file_path).iterrows():
#     print(index)
#     print(row)
#     BaitsComposition = {
#         "homeId": index,
#         "proportion": '',
#         "individualSize": '',
#         "individualWeight": '',
#         "baitSettingStatus": '',
#         "baitType": get_BaitType_topiaId(row)
#     }

    # print(BaitsComposition)
    


def create_catches(file_path, ligne_catch_table_fishes):
    catches = {
        "homeId": ligne_catch_table_fishes + 1,
        "comment": '',
        "count": create_catch_table_fishes(file_path, ligne_catch_table_fishes).loc[ligne_catch_table_fishes, 'count'],
        "totalWeight": create_catch_table_fishes(file_path, ligne_catch_table_fishes).loc[ligne_catch_table_fishes, 'totalWeight'],
        "hookWhenDiscarded": '',
        "depredated": '',
        "beatDiameter": '',
        "photoReferences": '',
        "number": '',
        "acquisitionMode": '',
        "countDepredated": '',
        "depredatedProportion": '',
        "tagNumber": '',
        "catchFate": get_catchFate_topiaID(create_catch_table_fishes(file_path, ligne_catch_table_fishes).loc[ligne_catch_table_fishes, 'catchFate']),
        "discardHealthStatus": '',
        "species": get_Species_topiaID(create_catch_table_fishes(file_path, ligne_catch_table_fishes).loc[ligne_catch_table_fishes, 'FAO_code']),
        "predator": '',
        "catchHealthStatus": '',
        "onBoardProcessing": '',
        "weightMeasureMethod": ''
        }
    return catches

# filtered_df = extract_time(file_path)[pd.to_datetime(extract_time(file_path)['Time'], errors='coerce').notna()]
days_in_a_month = len(extract_time(file_path))
for days in range(days_in_a_month):
    # if extract_time(file_path).loc[extract_time(file_path)['Time']][index] != str:
    Set = {
        'homeId' : days + 1, 
        'comment' : '',
        'number' : '',
        'basketsPerSectionCount' : extract_fishingEffort(file_path).loc[days, 'Hooks'],
        'branchlinesPerBasketCount': extract_gearInfo_LL(file_path).loc[extract_gearInfo_LL(file_path)['Logbook_name'] == 'Branchline length m', 'Value'].values[0], 
        'totalSectionsCount' : '', 
        # 'totalBasketsCount' : extract_fishingEffort(file_path).loc[extract_fishingEffort(file_path)['Day'] == index + 1, 'Hooks'].values[0], 
        'totalBasketsCount' : '', 
        'totalHooksCount' : extract_fishingEffort(file_path).loc[days, 'Total hooks'], 
        'lightsticksPerBasketCount' : '', 
        'totalLightsticksCount' : extract_fishingEffort(file_path).loc[days, 'Total lightsticks'], 
        'weightedSnap' : '', 
        'snapWeight' : '', 
        'weightedSwivel' : '', 
        'swivelWeight' :'', 
        'timeBetweenHooks' : '', 
        'shooterUsed' : '', 
        'shooterSpeed' : '', 
        'maxDepthTargeted' : '',
        'settingStartTimeStamp' : extract_time(file_path).loc[days, 'Time'],
        'settingStartLatitude' : extract_positions(file_path).loc[days, 'Latitute'],
        'settingStartLongitude' : extract_positions(file_path).loc[days, 'Longitude'],
        'settingEndTimeStamp' : '', 
        'settingEndLatitude' : '', 
        'settingEndLongitude' : '', 
        'settingVesselSpeed'  : '', 
        'haulingDirectionSameAsSetting' : '', 
        'haulingStartTimeStamp' : '', 
        'haulingStartLatitude' : '', 
        'haulingStartLongitude' : '', 
        'haulingEndTimeStamp' : '', 
        'haulingEndLatitude' : '', 
        'haulingEndLongitud'  : '',
        'haulingBreaks' : '', 
        'monitored' : '', 
        'totalLineLength' : '', 
        'basketLineLength' : '', 
        'lengthBetweenBranchlines'  : ''}
    
    MultipleBaitComposition = []
    
    for index, row in extract_bait_LL(file_path).iterrows():
        if create_BaitComposition(row)["baitType"] is not None:
            MultipleBaitComposition.append(create_BaitComposition(row))
            Set.update({'baitsComposition' : MultipleBaitComposition})
         
    Set.update({'floatlinesComposition' : '', 
        'hooksComposition' : '', 
        'settingShape' : '', })
               
    MultipleCatches = []
    # Numberof = extract_tunas(file_path).columns[::2]
    # for column in Numberof:
    #     FAO_code_logbook = column[-3:]           
    #     MultipleCatches.append(create_catches(FAO_code_logbook))
    #     Set.update({'catches' : MultipleCatches,})
    
    datatable = create_catch_table_fishes(file_path, row_number = days)
    for ligne_catch_table_fishes in range(len(datatable)) :
        # FAO_code_logbook = column[-3:]     
        print(ligne_catch_table_fishes) 
        print(create_catch_table_fishes(file_path, ligne_catch_table_fishes).loc[ligne_catch_table_fishes, 'FAO_code'])
        # MultipleCatches.append(create_catches(file_path, days))
        # print(MultipleCatches)
        # Set.update({'catches' : MultipleCatches,})
        
    Set.update({'lineType' : '', 
        'lightsticksUsed' : '', 
        'lightsticksType' : '', 
        'lightsticksColor' : '', 
        'mitigationType' : '',
        'branchlinesComposition': create_branchelinesComposition(file_path)
    })
    
    Activity = {
        'homeId' : index + 1, 
        'comment' : '',
        'startTimeStamp' : extract_time(file_path).loc[index, 'Time'],
        'endTimeStamp' : '',
        'latitude' : extract_positions(file_path).loc[index, 'Latitute'],
        'longitude' : extract_positions(file_path).loc[index, 'Longitude'], 
        'seaSurfaceTemperature' : extract_temperature(file_path).loc[index, 'Température'], 
        'wind' : '', 
        'windDirection' : '', 
        'currentSpeed' : '', 
        'currentDirection' : '', 
        'vesselActivity' : get_VesselActivity_topiaID(extract_time(file_path).loc[index, 'Time']), 
        'dataQuality' : '', 
        'fpaZone' : '', 
        'relatedObservedActivity' : '', 
        'set' : Set, 
        'sample' : ''
        }
        
    pretty_print(Activity)
    
