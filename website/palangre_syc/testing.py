from views import * 
import os

DIR = "./website/palangre_syc/media"

for file in os.listdir(DIR) :
    if '~$' not in file : 
        file_path = DIR + '/' + file
        file_open = read_excel(file_path, 1)
        #vessel = extract_vesselInfo_LL(file_path)
        #cruise = extract_cruiseInfo_LL(file_path)
        #report = extract_reportInfo_LL(file_path)
        #gear = extract_gearInfo_LL(file_path)
        # line = extract_lineMaterial_LL(file_path)
        # target = extract_target_LL(file_path)
        # date = extract_logbookDate_LL(file_path)
        # bait = extract_bait_LL(file_path)
        positions = extract_positions(file_path)
        print(file, positions)
        # time = extract_time(file_path)
        # temperature = extract_temperature(file_path)
        # fish = extract_fishingEffort(file_path)
        # tunas = extract_tunas(file_path)
        # extract_billfishes(file_path)
        # extract_otherfish(file_path)

       
        
        
        
