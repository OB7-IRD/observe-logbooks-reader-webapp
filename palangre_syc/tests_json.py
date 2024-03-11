

# file_path = './palangre_syc/media/july2022-FV GOLDEN FULL NO.168.xlsx'
# with open('./data_common.json', 'r', encoding = 'utf-8') as f:
#     data_common = json.load(f)
# with open('./data_ll.json', 'r', encoding = 'utf-8') as f:
#     data_ll = json.load(f)    
    
    
    
    
# if os.path.exists("samplebis.json") : 
#     os.remove("samplebis.json")

# def pretty_print(json_data):
#     # Convert int64 values to native Python types
#     def convert_to_serializable(obj):
#         if isinstance(obj, np.int64):
#             return int(obj)
#         raise TypeError("Type not serializable")

#     # Serialize with custom conversion function
#     json_formatted_str = json.dumps(json_data, indent=2, default=convert_to_serializable)

#     # Append to the file
#     with open("samplebis.json", "a") as outfile:
#         outfile.write(json_formatted_str)
        
    
# def get_tunasSpecies_topiaID(FAO_code_logbook):
#     '''
#     Fonction 
#     '''
#     Species = data_common["content"]["fr.ird.observe.entities.referential.common.Species"]
#     for Specie in Species:
#         if 'faoCode' in Specie:
#             # faoCode_json = Specie['faoCode']
#             # if FAO_code_logbook == faoCode_json :
#             #     return Specie['topiaId']
#             if Specie.get("faoCode") == FAO_code_logbook:
#                 return Specie["topiaId"]
#     # else : 
#     #     return None


# print(get_tunasSpecies_topiaID(file_path))

# def create_catches(FAO_code_logbook):
#     catches = {
#         "homeId": checking_logbook + 1,
#         "comment": '',
#         "count": extract_tunas(file_path).loc[checking_logbook, column],
#         "totalWeight": '',
#         "hookWhenDiscarded": '',
#         "depredated": '',
#         "beatDiameter": '',
#         "photoReferences": '',
#         "number": '',
#         "acquisitionMode": '',
#         "countDepredated": '',
#         "depredatedProportion": '',
#         "tagNumber": '',
#         "catchFate": "",
#         "discardHealthStatus": '',
#         "species": get_tunasSpecies_topiaID(FAO_code_logbook),
#         "predator": '',
#         "catchHealthStatus": '',
#         "onBoardProcessing": '',
#         "weightMeasureMethod": ''
#         }
#     return catches



   
        
# days_in_a_month = len(extract_time(file_path))
# for checking_logbook in range(days_in_a_month):
#     # if extract_time(file_path).loc[extract_time(file_path)['Time']][index] != str:
    
#     Set = {'homeId' : checking_logbook + 1, }
        
        
#     MultipleCatches = []
#     Numberof = extract_tunas(file_path).columns[::2]
#     Weightof = extract_tunas(file_path).columns[1::2]
#     for column in Numberof:
#         FAO_code_logbook = column[-3:]           
#         MultipleCatches.append(create_catches(FAO_code_logbook))
#         Set.update({'catches' : MultipleCatches,})
        
    
#     pretty_print(Set)
# print(type(Set))

from api import get_token, update_trip

token = get_token()
url_base = 'https://observe.ob7.ird.fr/observeweb/api/public'

triptopiaid = "fr.ird.data.ll.common.Trip-1709712114406-1.34450647835127113"

trip = {
  "startDate": "2023-07-01T00:00:00.000Z",
  "endDate": "2023-08-31T00:00:00.000Z",
  "noOfCrewMembers": 27,
  "gearUseFeatures": [],
  "activityObs": [],
  "activityLogbook": [
    {
      "startTimeStamp": "2023-07-01T02:00:00.000Z",
      "latitude": 1.53,
      "longitude": 68.72,
      "seaSurfaceTemperature": 30.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 175,
        "totalHooksCount": 3500,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-01T02:00:00.000Z",
        "settingStartLatitude": 1.53,
        "settingStartLongitude": 68.72,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "count": 15,
            "totalWeight": 764.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832685475#0.13349466123905152",
            "predator": []
          },
          {
            "comment": "Other fish non specified",
            "count": 3,
            "totalWeight": 119.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1433499266610#0.696541526820511",
            "predator": []
          },
          {
            "count": 3,
            "totalWeight": 162.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683791#0.20975568563021063",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-02T02:00:00.000Z",
      "latitude": 1.55,
      "longitude": 68.72,
      "seaSurfaceTemperature": 30.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 175,
        "totalHooksCount": 3500,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-02T02:00:00.000Z",
        "settingStartLatitude": 1.55,
        "settingStartLongitude": 68.72,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "count": 8,
            "totalWeight": 452.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832685475#0.13349466123905152",
            "predator": []
          },
          {
            "comment": "Other fish non specified",
            "count": 2,
            "totalWeight": 74.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1433499266610#0.696541526820511",
            "predator": []
          },
          {
            "count": 2,
            "totalWeight": 87.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683791#0.20975568563021063",
            "predator": []
          },
          {
            "count": 4,
            "totalWeight": 193.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683731#0.3892121873590658",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-03T02:00:00.000Z",
      "latitude": 1.5,
      "longitude": 68.72,
      "seaSurfaceTemperature": 30.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 175,
        "totalHooksCount": 3500,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-03T02:00:00.000Z",
        "settingStartLatitude": 1.5,
        "settingStartLongitude": 68.72,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "count": 9,
            "totalWeight": 599.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832685475#0.13349466123905152",
            "predator": []
          },
          {
            "count": 1,
            "totalWeight": 52.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683791#0.20975568563021063",
            "predator": []
          },
          {
            "count": 1,
            "totalWeight": 46.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683731#0.3892121873590658",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-04T02:00:00.000Z",
      "latitude": 1.5,
      "longitude": 68.72,
      "seaSurfaceTemperature": 30.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 175,
        "totalHooksCount": 3500,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-04T02:00:00.000Z",
        "settingStartLatitude": 1.5,
        "settingStartLongitude": 68.72,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "count": 10,
            "totalWeight": 548.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832685475#0.13349466123905152",
            "predator": []
          },
          {
            "comment": "Other fish non specified",
            "count": 5,
            "totalWeight": 155.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1433499266610#0.696541526820511",
            "predator": []
          },
          {
            "count": 2,
            "totalWeight": 107.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683791#0.20975568563021063",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-05T02:00:00.000Z",
      "latitude": 1.55,
      "longitude": 68.72,
      "seaSurfaceTemperature": 30.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 175,
        "totalHooksCount": 3500,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-05T02:00:00.000Z",
        "settingStartLatitude": 1.55,
        "settingStartLongitude": 68.72,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "count": 3,
            "totalWeight": 134.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832685475#0.13349466123905152",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-06T02:00:00.000Z",
      "latitude": 1.48,
      "longitude": 68.72,
      "seaSurfaceTemperature": 30.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 175,
        "totalHooksCount": 3500,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-06T02:00:00.000Z",
        "settingStartLatitude": 1.48,
        "settingStartLongitude": 68.72,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "count": 1,
            "totalWeight": 19.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832685475#0.13349466123905152",
            "predator": []
          },
          {
            "comment": "Other fish non specified",
            "count": 1,
            "totalWeight": 38.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1433499266610#0.696541526820511",
            "predator": []
          },
          {
            "count": 1,
            "totalWeight": 26.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683791#0.20975568563021063",
            "predator": []
          },
          {
            "count": 1,
            "totalWeight": 62.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683731#0.3892121873590658",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-07T00:00:00.000Z",
      "latitude": -1.28,
      "longitude": 69.05,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01"
    },
    {
      "startTimeStamp": "2023-07-08T00:00:00.000Z",
      "latitude": -3.22,
      "longitude": 70.93,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01"
    },
    {
      "startTimeStamp": "2023-07-09T00:00:00.000Z",
      "latitude": -3.53,
      "longitude": 74.23,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01"
    },
    {
      "startTimeStamp": "2023-07-10T00:00:00.000Z",
      "latitude": -2.52,
      "longitude": 76.65,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01"
    },
    {
      "startTimeStamp": "2023-07-11T04:00:00.000Z",
      "latitude": -1.07,
      "longitude": 77.87,
      "seaSurfaceTemperature": 30.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 175,
        "totalHooksCount": 3500,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-11T04:00:00.000Z",
        "settingStartLatitude": -1.07,
        "settingStartLongitude": 77.87,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "count": 12,
            "totalWeight": 596.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832685475#0.13349466123905152",
            "predator": []
          },
          {
            "comment": "Other fish non specified",
            "count": 1,
            "totalWeight": 41.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1433499266610#0.696541526820511",
            "predator": []
          },
          {
            "count": 1,
            "totalWeight": 26.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683785#0.49501050869628815",
            "predator": []
          },
          {
            "count": 1,
            "totalWeight": 35.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683731#0.3892121873590658",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-12T05:00:00.000Z",
      "latitude": -0.95,
      "longitude": 77.88,
      "seaSurfaceTemperature": 30.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 175,
        "totalHooksCount": 3500,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-12T05:00:00.000Z",
        "settingStartLatitude": -0.95,
        "settingStartLongitude": 77.88,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "count": 6,
            "totalWeight": 338.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832685475#0.13349466123905152",
            "predator": []
          },
          {
            "comment": "Other fish non specified",
            "count": 3,
            "totalWeight": 84.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1433499266610#0.696541526820511",
            "predator": []
          },
          {
            "count": 3,
            "totalWeight": 116.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683731#0.3892121873590658",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-13T05:00:00.000Z",
      "latitude": -0.67,
      "longitude": 77.88,
      "seaSurfaceTemperature": 30.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 175,
        "totalHooksCount": 3500,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-13T05:00:00.000Z",
        "settingStartLatitude": -0.67,
        "settingStartLongitude": 77.88,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "count": 7,
            "totalWeight": 326.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832685475#0.13349466123905152",
            "predator": []
          },
          {
            "comment": "Other fish non specified",
            "count": 2,
            "totalWeight": 94.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1433499266610#0.696541526820511",
            "predator": []
          },
          {
            "count": 3,
            "totalWeight": 226.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683731#0.3892121873590658",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-14T05:00:00.000Z",
      "latitude": -0.42,
      "longitude": 77.87,
      "seaSurfaceTemperature": 30.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 175,
        "totalHooksCount": 3500,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-14T05:00:00.000Z",
        "settingStartLatitude": -0.42,
        "settingStartLongitude": 77.87,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "count": 1,
            "totalWeight": 60.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832685475#0.13349466123905152",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-15T06:00:00.000Z",
      "latitude": -0.6,
      "longitude": 77.88,
      "seaSurfaceTemperature": 30.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 160,
        "totalHooksCount": 3200,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-15T06:00:00.000Z",
        "settingStartLatitude": -0.6,
        "settingStartLongitude": 77.88,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "count": 1,
            "totalWeight": 37.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683731#0.3892121873590658",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-16T00:00:00.000Z",
      "latitude": 0.53,
      "longitude": 78.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01"
    },
    {
      "startTimeStamp": "2023-07-17T01:00:00.000Z",
      "latitude": 1.98,
      "longitude": 78.05,
      "seaSurfaceTemperature": 30.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 140,
        "totalHooksCount": 2800,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-17T01:00:00.000Z",
        "settingStartLatitude": 1.98,
        "settingStartLongitude": 78.05,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "count": 5,
            "totalWeight": 235.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832685475#0.13349466123905152",
            "predator": []
          },
          {
            "comment": "Other fish non specified",
            "count": 3,
            "totalWeight": 164.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1433499266610#0.696541526820511",
            "predator": []
          },
          {
            "count": 2,
            "totalWeight": 83.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683731#0.3892121873590658",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-18T00:00:00.000Z",
      "latitude": 1.5,
      "longitude": 78.22,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01"
    },
    {
      "startTimeStamp": "2023-07-19T00:00:00.000Z",
      "latitude": -1.28,
      "longitude": 78.03,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01"
    },
    {
      "startTimeStamp": "2023-07-20T05:00:00.000Z",
      "latitude": -3.65,
      "longitude": 78.25,
      "seaSurfaceTemperature": 30.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 160,
        "totalHooksCount": 3200,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-20T05:00:00.000Z",
        "settingStartLatitude": -3.65,
        "settingStartLongitude": 78.25,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "count": 14,
            "totalWeight": 714.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832685475#0.13349466123905152",
            "predator": []
          },
          {
            "comment": "Other fish non specified",
            "count": 7,
            "totalWeight": 269.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1433499266610#0.696541526820511",
            "predator": []
          },
          {
            "count": 2,
            "totalWeight": 78.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683731#0.3892121873590658",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-21T05:00:00.000Z",
      "latitude": -3.8,
      "longitude": 78.23,
      "seaSurfaceTemperature": 30.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 175,
        "totalHooksCount": 3500,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-21T05:00:00.000Z",
        "settingStartLatitude": -3.8,
        "settingStartLongitude": 78.23,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "count": 7,
            "totalWeight": 377.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832685475#0.13349466123905152",
            "predator": []
          },
          {
            "comment": "Other fish non specified",
            "count": 2,
            "totalWeight": 85.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1433499266610#0.696541526820511",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-22T06:00:00.000Z",
      "latitude": -4.0,
      "longitude": 77.95,
      "seaSurfaceTemperature": 30.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 165,
        "totalHooksCount": 3300,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-22T06:00:00.000Z",
        "settingStartLatitude": -4.0,
        "settingStartLongitude": 77.95,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "count": 1,
            "totalWeight": 108.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832685475#0.13349466123905152",
            "predator": []
          },
          {
            "comment": "Other fish non specified",
            "count": 3,
            "totalWeight": 100.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1433499266610#0.696541526820511",
            "predator": []
          },
          {
            "count": 2,
            "totalWeight": 98.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683731#0.3892121873590658",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-23T06:00:00.000Z",
      "latitude": -3.75,
      "longitude": 78.08,
      "seaSurfaceTemperature": 30.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 165,
        "totalHooksCount": 3300,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-23T06:00:00.000Z",
        "settingStartLatitude": -3.75,
        "settingStartLongitude": 78.08,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "comment": "Other fish non specified",
            "count": 2,
            "totalWeight": 70.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1433499266610#0.696541526820511",
            "predator": []
          },
          {
            "count": 2,
            "totalWeight": 73.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683731#0.3892121873590658",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-24T00:00:00.000Z",
      "latitude": -2.65,
      "longitude": 80.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01"
    },
    {
      "startTimeStamp": "2023-07-25T00:00:00.000Z",
      "latitude": -0.68,
      "longitude": 82.78,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01"
    },
    {
      "startTimeStamp": "2023-07-26T05:00:00.000Z",
      "latitude": 0.28,
      "longitude": 84.2,
      "seaSurfaceTemperature": 29.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 160,
        "totalHooksCount": 3200,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-26T05:00:00.000Z",
        "settingStartLatitude": 0.28,
        "settingStartLongitude": 84.2,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "count": 1,
            "totalWeight": 65.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832685475#0.13349466123905152",
            "predator": []
          },
          {
            "comment": "Other fish non specified",
            "count": 1,
            "totalWeight": 47.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1433499266610#0.696541526820511",
            "predator": []
          },
          {
            "count": 3,
            "totalWeight": 110.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683731#0.3892121873590658",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-27T14:00:00.000Z",
      "latitude": 0.43,
      "longitude": 85.75,
      "seaSurfaceTemperature": 30.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 125,
        "totalHooksCount": 2500,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-27T14:00:00.000Z",
        "settingStartLatitude": 0.43,
        "settingStartLongitude": 85.75,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "comment": "Other fish non specified",
            "count": 1,
            "totalWeight": 35.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1433499266610#0.696541526820511",
            "predator": []
          },
          {
            "count": 1,
            "totalWeight": 31.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683791#0.20975568563021063",
            "predator": []
          },
          {
            "count": 1,
            "totalWeight": 38.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683731#0.3892121873590658",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-28T06:00:00.000Z",
      "latitude": 0.43,
      "longitude": 86.27,
      "seaSurfaceTemperature": 30.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 150,
        "totalHooksCount": 3000,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-28T06:00:00.000Z",
        "settingStartLatitude": 0.43,
        "settingStartLongitude": 86.27,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "count": 6,
            "totalWeight": 386.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832685475#0.13349466123905152",
            "predator": []
          },
          {
            "comment": "Other fish non specified",
            "count": 1,
            "totalWeight": 23.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1433499266610#0.696541526820511",
            "predator": []
          },
          {
            "count": 3,
            "totalWeight": 67.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683791#0.20975568563021063",
            "predator": []
          },
          {
            "count": 2,
            "totalWeight": 52.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683731#0.3892121873590658",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-29T06:00:00.000Z",
      "latitude": 0.43,
      "longitude": 86.28,
      "seaSurfaceTemperature": 30.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 175,
        "totalHooksCount": 3500,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-29T06:00:00.000Z",
        "settingStartLatitude": 0.43,
        "settingStartLongitude": 86.28,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "count": 7,
            "totalWeight": 366.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832685475#0.13349466123905152",
            "predator": []
          },
          {
            "comment": "Other fish non specified",
            "count": 1,
            "totalWeight": 16.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1433499266610#0.696541526820511",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-30T15:00:00.000Z",
      "latitude": -1.32,
      "longitude": 89.33,
      "seaSurfaceTemperature": 30.0,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#1239832686138#0.1",
      "set": {
        "totalBasketsCount": 125,
        "totalHooksCount": 2500,
        "weightedSnap": False,
        "weightedSwivel": False,
        "shooterUsed": False,
        "settingStartTimeStamp": "2023-07-30T15:00:00.000Z",
        "settingStartLatitude": -1.32,
        "settingStartLongitude": 89.33,
        "monitored": False,
        "lengthBetweenBranchlines": 37.0,
        "baitsComposition": [
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1433499458077#0.820353789720684"
          },
          {
            "proportion": 50,
            "baitType": "fr.ird.referential.ll.common.BaitType#1652967633671#0.11966760938258336"
          }
        ],
        "floatlinesComposition": [
          {
            "length": 35.0,
            "proportion": 100,
            "lineType": "fr.ird.referential.ll.common.LineType#1239832686157#0.9"
          }
        ],
        "hooksComposition": [],
        "catches": [
          {
            "count": 8,
            "totalWeight": 512.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832685475#0.13349466123905152",
            "predator": []
          },
          {
            "count": 1,
            "totalWeight": 44.0,
            "acquisitionMode": 0,
            "catchFate": "fr.ird.referential.ll.common.CatchFate#1239832686125#0.2",
            "species": "fr.ird.referential.common.Species#1239832683785#0.49501050869628815",
            "predator": []
          }
        ],
        "lightsticksUsed": False,
        "mitigationType": [],
        "branchlinesComposition": []
      }
    },
    {
      "startTimeStamp": "2023-07-31T00:00:00.000Z",
      "latitude": -0.25,
      "longitude": 89.95,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01"
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-01T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 1.27,
      "longitude": 87.47,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-02T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 3.15,
      "longitude": 84.67,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-03T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 4.77,
      "longitude": 82.23,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-04T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 5.52,
      "longitude": 82.1,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-05T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 3.57,
      "longitude": 83.72,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-06T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 3.55,
      "longitude": 85.42,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-07T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 3.13,
      "longitude": 88.38,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-08T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 6.88,
      "longitude": 92.32,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-09T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 5.08,
      "longitude": 94.55,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-10T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 3.42,
      "longitude": 97.92,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-11T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 1.3,
      "longitude": 100.42,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-12T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 3.2,
      "longitude": 103.9,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-13T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 5.32,
      "longitude": 105.33,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-14T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 9.85,
      "longitude": 107.13,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-15T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 11.8,
      "longitude": 109.75,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-16T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 14.97,
      "longitude": 112.12,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-17T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 18.9,
      "longitude": 114.7,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-18T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 21.5,
      "longitude": 116.5,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-19T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 23.35,
      "longitude": 117.75,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-20T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 26.93,
      "longitude": 118.95,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-21T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 29.75,
      "longitude": 121.63,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-22T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 35.77,
      "longitude": 124.57,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#01",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-23T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 35.05,
      "longitude": 129.03,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#03",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-24T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 35.05,
      "longitude": 129.03,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#03",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-25T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 35.05,
      "longitude": 129.03,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#03",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-26T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 35.05,
      "longitude": 129.03,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#03",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-27T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 35.05,
      "longitude": 129.03,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#03",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-28T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 35.05,
      "longitude": 129.03,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#03",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-29T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 35.05,
      "longitude": 129.03,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#03",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-30T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 35.05,
      "longitude": 129.03,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#03",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    },
    {
      "homeId": None,
      "comment": None,
      "startTimeStamp": "2023-08-31T00:00:00.000Z",
      "endTimeStamp": None,
      "latitude": 35.05,
      "longitude": 129.03,
      "seaSurfaceTemperature": None,
      "wind": None,
      "windDirection": None,
      "currentSpeed": None,
      "currentDirection": None,
      "vesselActivity": "fr.ird.referential.ll.common.VesselActivity#666#03",
      "dataQuality": None,
      "fpaZone": None,
      "relatedObservedActivity": None,
      "set": None,
      "sample": None
    }
  ],
  "landing": [],
  "sample": [],
  "tripType": "fr.ird.referential.ll.common.TripType#1464000000000#02",
  "observer": "fr.ird.referential.common.Person#1254317601353#0.6617065204572095",
  "vessel": "fr.ird.referential.common.Vessel#1464000000000#0.00016731",
  "logbookProgram": "fr.ird.referential.ll.common.Program#1707391938404#0.8314199988069012",
  "captain": "fr.ird.referential.common.Person#1254317601353#0.6617065204572095",
  "logbookDataEntryOperator": "fr.ird.referential.common.Person#1254317601353#0.6617065204572095",
  "ocean": "fr.ird.referential.common.Ocean#1239832686152#0.8325731048817705",
  "departureHarbour": "fr.ird.referential.common.Harbour#11#0.11",
  "species": [],
  "observationsAvailability": False,
  "logbookAvailability": True
}



update_trip(token=token, 
                data=trip, 
                url_base=url_base, 
                topiaid=triptopiaid)
