
from views import * 
import json, os
import numpy as np

file_path = './palangre_syc/media/july2022-FV GOLDEN FULL NO.168.xlsx'
with open('./data_common.json', 'r', encoding = 'utf-8') as f:
    data_common = json.load(f)
with open('./data_ll.json', 'r', encoding = 'utf-8') as f:
    data_ll = json.load(f)    
    
    
    
    
if os.path.exists("samplebis.json") : 
    os.remove("samplebis.json")

def pretty_print(json_data):
    # Convert int64 values to native Python types
    def convert_to_serializable(obj):
        if isinstance(obj, np.int64):
            return int(obj)
        raise TypeError("Type not serializable")

    # Serialize with custom conversion function
    json_formatted_str = json.dumps(json_data, indent=2, default=convert_to_serializable)

    # Append to the file
    with open("samplebis.json", "a") as outfile:
        outfile.write(json_formatted_str)
        
    
def get_tunasSpecies_topiaID(FAO_code_logbook):
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
    # else : 
    #     return None


print(get_tunasSpecies_topiaID(file_path))

def create_catches(FAO_code_logbook):
    catches = {
        "homeId": index + 1,
        "comment": '',
        "count": extract_tunas(file_path).loc[index, column],
        "totalWeight": '',
        "hookWhenDiscarded": '',
        "depredated": '',
        "beatDiameter": '',
        "photoReferences": '',
        "number": '',
        "acquisitionMode": '',
        "countDepredated": '',
        "depredatedProportion": '',
        "tagNumber": '',
        "catchFate": "",
        "discardHealthStatus": '',
        "species": get_tunasSpecies_topiaID(FAO_code_logbook),
        "predator": '',
        "catchHealthStatus": '',
        "onBoardProcessing": '',
        "weightMeasureMethod": ''
        }
    return catches



   
        
days_in_a_month = len(extract_time(file_path))
for index in range(days_in_a_month):
    # if extract_time(file_path).loc[extract_time(file_path)['Time']][index] != str:
    
    Set = {'homeId' : index + 1, }
        
        
    MultipleCatches = []
    Numberof = extract_tunas(file_path).columns[::2]
    Weightof = extract_tunas(file_path).columns[1::2]
    for column in Numberof:
        FAO_code_logbook = column[-3:]           
        MultipleCatches.append(create_catches(FAO_code_logbook))
        Set.update({'catches' : MultipleCatches,})
        
    
    pretty_print(Set)
print(type(Set))