from views import * 
import json


file_path = './website/palangre_syc/media/july2022-FV GOLDEN FULL NO.168.xlsx'
with open('./website/data_common.json', 'r', encoding = 'utf-8') as f:
    data_common = json.load(f)
with open('./website/data_ll.json', 'r', encoding = 'utf-8') as f:
    data_ll = json.load(f)    


def captain_topiaID():
    for captain in data_common['content']['fr.ird.observe.entities.referential.common.Person']:
        
        captain_Logbook = extract_cruiseInfo_LL(file_path).loc[extract_cruiseInfo_LL(file_path)['Logbook_name'] == 'Captain', 'Value'].values[0]
        captain_json = captain['firstName'] + ' ' + captain['lastName']
        if captain_Logbook == captain_json :
            return captain['topiaId']
    return None

if 'content' in data_common and 'fr.ird.observe.entities.referential.common.Vessel' in data_common['content']:
    # Accéder à la liste des personnes
    print('c oui')
    vessel_data = data_common['content']['fr.ird.observe.entities.referential.common.Vessel']



def vessel_topiaID():
    vessel_Logbook = extract_vesselInfo_LL(file_path).loc[extract_vesselInfo_LL(file_path)['Logbook_name'] == 'Vessel Name', 'Value'].values[0]
    print(vessel_Logbook)
    for vessel in vessel_data:
        vessel_json = vessel['label1']
        if vessel_Logbook == vessel_json :
            return vessel['topiaId']
    return None


    
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
    'vessel' : vessel_topiaID(), 
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

def get_VesselActivity_topiaId(startTimeStamp):
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
                
    
# filtered_df = extract_time(file_path)[pd.to_datetime(extract_time(file_path)['Time'], errors='coerce').notna()]
days_in_a_month = len(extract_time(file_path))
for index in range(days_in_a_month):
    # if extract_time(file_path).loc[extract_time(file_path)['Time']][index] != str:
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
        'vesselActivity' : get_VesselActivity_topiaId(extract_time(file_path).loc[index, 'Time']), 
        'dataQuality' : '', 
        'fpaZone' : '', 
        'relatedObservedActivity' : '', 
        'set' : '', 
        'sample' : ''
        }
        
        
    print(Activity)

