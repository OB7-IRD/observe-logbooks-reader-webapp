from views import * 
import os

DIR = "./palangre_syc/media"

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
        # time = extract_time(file_path)
        # temperature = extract_temperature(file_path)
        # fish = extract_fishingEffort(file_path)
        # tunas = extract_tunas(file_path)
        # extract_billfishes(file_path)
        # extract_otherfish(file_path)
        fal =  extract_sharksFAL(file_path)
        bsh = extract_sharksBSH(file_path)
        mak = extract_sharksMAK(file_path)
        spn = extract_sharksSPN(file_path)
        tig = extract_sharksTIG(file_path)
        psk = extract_sharksPSK(file_path)
        thr = extract_sharksTHR(file_path)
        ocs = extract_sharksOCS(file_path)
        mammals = extract_mammals(file_path)
        seabird = extract_seabird(file_path)
        turtles = extract_turtles(file_path)
       
        
        
        
