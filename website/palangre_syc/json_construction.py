from views import * 
import json


file_path = './website/palangre_syc/media/july2022-FV GOLDEN FULL NO.168.xlsx'
with open('./website/data_common.json', 'r', encoding = 'utf-8') as f:
    data_common = json.load(f)


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







print(Trip)