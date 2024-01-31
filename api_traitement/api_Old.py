import datetime
import os
import pandas as pd
import openpyxl as op
import numpy as np

import requests
import json

from api_traitement.json_fonctions import *


def date_convert(time_to_convert):
    return datetime.datetime.strptime(time_to_convert, '%H:%M:%S').time()


def open(username, password, rf_lo):


    url = "https://observe.ob7.ird.fr/observeweb-9-alternative"
    data = {
        "url": "/api/public/init/open",
        "method": "GET",
        "parameters": {
            "config.modelVersion": "9.0",
            "config.login": username,
            "config.password": password,
            "config.databaseName": "9a",
            "referentialLocale": rf_lo,
        }
    }

    # Recuperation du token
    url = url + data['url']
    rep = requests.get(url, params=data["parameters"])

    # orga = rep.url
    orga = json.loads(rep.text)
    message = ""
    token = None

    try:
        if orga["authenticationToken"]:
            token = orga["authenticationToken"]
        else:
            message = orga["message"]
    except KeyError as e:
        pass

    return token, message





def getOcean_Program(token, search="Ocean"):
    if search == "Program":
        ac = requests.get(
            "https://observe.ob7.ird.fr/observeweb-9-alternative/api/public/referential/ps/common/Program/all?authenticationToken=" + token
            + "&filters.gearType=seine&filters.logbook=true")
        prog_dic = {}
        for val in json.loads(ac.text)["content"]:
            prog_dic[val["topiaId"]] = val["label2"]
        return prog_dic
    else:
        ac = requests.get(
            "https://observe.ob7.ird.fr/observeweb-9-alternative/api/public/referential/common/Ocean/all?authenticationToken=" + token)
        prog_dic = {}
        for val in json.loads(ac.text)["content"]:
            prog_dic[val["topiaId"]] = val["label2"]
        return prog_dic


def get_lat_long(token, harbour):
    ac_cap = requests.get("https://observe.ob7.ird.fr/observeweb-9-alternative/api/public/referential/common/Harbour?authenticationToken="+ token + "&filters.label2=" + harbour)
    if ac_cap.status_code == 200:
        return float(json.loads(ac_cap.text)["content"][0]["latitude"]), float(json.loads(ac_cap.text)["content"][0]["longitude"])
    else:
        return None, None


def lat_long(lat1, lat2, lat3, long1, long2, long3):
    if lat1 is None or lat2 is None or lat3 is None or long1 is None or long2 is None or long3 is None:
        return None, None
    else:
        try:
            lat_1 = int(float(str(lat1).replace("°", "")))
            lat_2 = int(float(str(lat2).replace("'", "")))
            long_1 = int(float(str(long1).replace("°", "")))
            long_2 = int(float(str(long2).replace("'", "")))

            # print(lat_1, lat_2, lat3, long_1, long_2, )

            res_lat = str(lat_1) + "." + str(int((lat_2 / 60) * 100))
            res_long = str(long_1) + "." + str(int((long_2 / 60) * 100))

            if lat3.lower() == "s":
                res_lat = float(res_lat) * (-1)
            else:
                res_lat = float(res_lat)

            if long3.lower() == "w":
                res_long = float(res_long) * (-1)
            else:
                res_long = float(res_long)

            return res_lat, res_long

        except ValueError:
            return None, None


def getIdByRefCommonMod(token, moduleName ="Ocean", label1 ="atlantic", argment = None, route = None):

    headers = {
        "Content-Type":"application/json",
        'authenticationToken': token
    }

    if argment != None and route == None:
        url = "https://observe.ob7.ird.fr/observeweb-9-alternative/api/public/referential/common/"+ moduleName +"?filters." + argment
    elif route != None:
        url = "https://observe.ob7.ird.fr/observeweb-9-alternative/"+ route + moduleName +"?filters." + argment
    else:
        url = "https://observe.ob7.ird.fr/observeweb-9-alternative/api/public/referential/common/"+ moduleName +"?filters.label1=" + label1

    rep = requests.get(url, headers=headers)
    if rep.status_code == 200:
        return json.loads(rep.text)["content"][0]["topiaId"]
    else:
        return json.loads(rep.text)["message"]


# Traitement du logbook
def traiLogbook(logB, token):
    # Chargement du fichier
    # wb = Workbook()

    try:
        wb = op.load_workbook(logB)
    except Exception as e:
        print("Error :", e)

    if logB.name.split('.')[1] == "xlsm":
        # Recuperer le non du bateau et autres information utils
        #   st.text(wb.get_sheet_names())
        maree_log = wb["1.Marée"]

        # Recuperer la feuille active
        act_sheet = wb["2.Logbook"]
    else:
        # Recuperer le non du bateau et autres information utils
        maree_log = wb["Marée"]
        # st.text(wb.get_sheet_names())

        # Recuperer la feuille active
        act_sheet = wb["Logbook"]

    info_bat = {
        "Navire": maree_log["F"][1].value,
        "Depart_Port": maree_log["F"][12].value,
        "Depart_Date": str(maree_log["F"][13].value).split(" ")[0],
        "Arrivee_Port": maree_log["F"][17].value,
        "Arrivee_Date": str(maree_log["F"][18].value).split(" ")[0],
        "Arrivee_Loch": maree_log["F"][20].value,
    }

    observ = {
        "captain": maree_log["D"][9].value,
        "mar_homeId": maree_log["D"][10].value,
    }

    # Variable pour recuperer les donnée dans le logbook
    data = []
    obj = []

    # Recuperation des lignes qui nous interesses à partir de la ligne 33 dans le fichier

    i = 1
    for row in act_sheet.rows:
        if i >= 33:
            for index in range(len(row)):
                obj.append(row[index].value)
            data.append(obj)
            obj = []
        i = i + 1

    # Transformer le tableau "data" en dataFrame pour faciliter la manipulation des données
    data = pd.DataFrame(np.array(data))

    # Titrer le tableau
    data = data.rename(
        columns={0: "date", 1: "heure", 2: "lat1", 3: "lat2", 4: "lat3", 5: "long1", 6: "long2", 7: "long3", 8: "zee",
                 9: "temp_mer", 10: "vent_dir", 11: "vent_vit", 12: "calee_porta", 13: "calee_nul", 14: "calee_type",
                 15: "cap_alb_yft_p10_tail", 16: "cap_alb_yft_p10_cap", 17: "cap_alb_yft_m10_tail",
                 18: "cap_alb_yft_m10_cap", 19: "cap_lst_skj_tail", 20: "cap_lst_skj_cap", 21: "cap_pat_bet_p10_tail",
                 22: "cap_pat_bet_p10_cap", 23: "cap_pat_bet_m10_tail", 24: "cap_pat_bet_m10_cap",
                 25: "cap_ger_alb_tail", 26: "cap_ger_alb_cap", 27: "cap_aut_esp_oth_esp", 28: "cap_aut_esp_oth_tail",
                 29: "cap_aut_esp_oth_cap", 30: "cap_rej_dsc_esp", 31: "cap_rej_dsc_tail", 32: "cap_rej_dsc_cap",
                 33: "asso_bc_libre", 34: "asso_objet", 35: "asso_balise", 36: "asso_baliseur", 37: "asso_requin",
                 38: "asso_baleine", 39: "asso_oiseaux", 40: "obj_flot_act_sur_obj", 41: "obj_flot_typ_obj",
                 42: "obj_flot_typ_dcp_deriv", 43: "obj_flot_risq_mail_en_surf", 44: "obj_flot_risq_mail_sou_surf",
                 45: "bouee_inst_act_bou", 46: "bouee_inst_bou_prst_typ", 47: "bouee_inst_bou_prst_id",
                 48: "bouee_inst_bou_deplo_typ", 49: "bouee_inst_bou_deplo_id", 50: "comment"})

    #####  Traitement pour supprimer les lignes qui n'ont pas de donnée dans le datFrame 'data'

    # Suppression des lignes identiques c.a.d les doublons
    df_data = data.drop_duplicates(keep=False)
    df_data.loc[:, "date"] = df_data.loc[:, "date"].fillna(method="ffill").values
    df_data = df_data.loc[:, :"comment"]

    print("ErRRRRRRRRReeeeuuuuu  1121")
    # Constitution de la selections du Program et Ocean
    Ocean = getOcean_Program(token)
    Program = getOcean_Program(token, search="Program")

    print("ErRRRRRRRRReeeeuuuuu  2222222")


    return info_bat, df_data, observ, Ocean, Program


def cap_obs_sea(token, ob):
    ac = requests.get("https://observe.ob7.ird.fr/observeweb-9-alternative/api/public/referential/common/Person/all?authenticationToken="+ token)
    cap = logbookDataEntryOperator = []

    for val in json.loads(ac.text)["content"]:
        if val["captain"] == True :
            cap.append((val["topiaId"], val["firstName"].lower(), val["lastName"].lower()))
        elif val["dataEntryOperator"] == True :
            logbookDataEntryOperator.append((val["topiaId"], val["firstName"].lower(), val["lastName"].lower()))

    def sou_fonc(arra):
        no, pre = ob['captain'].split(" ")
        for val in arra:
            #print(val[0])
            if no.lower() in str(val) and pre.lower() in str(val):
                return val[0]
            elif "[inconnu]" == val[1] and "[inconnu]" == val[2]:
                return val[0]

    if cap == logbookDataEntryOperator:
        id_cap = sou_fonc(cap)
        return id_cap, id_cap
    else:
        id_cap = sou_fonc(cap)
        id_op = sou_fonc(logbookDataEntryOperator)
        return id_cap, id_op


# Constitution de contents
def build_trip(token, a, b, oce, prg, ob):
    tab3_floatingObject = []
    activite = []
    routes = []
    # js_catches = js_activitys = js_routeLogbooks = {}
    homeId = nb = nb_r = Som_thon = 0
    # js_contents = {}

    group = b.groupby(['date'])

    yft_id = getIdByRefCommonMod(token, "Species", argment="faoCode=YFT")
    skj_id = getIdByRefCommonMod(token, "Species", argment="faoCode=SKJ")
    bet_id = getIdByRefCommonMod(token, "Species", argment="faoCode=BET")
    germon_alb_id = getIdByRefCommonMod(token, "Species", argment="faoCode=ALB")

    WeightMeasureMet = getIdByRefCommonMod(token, "WeightMeasureMethod", argment="label2=Estimation visuelle")

    code_conser = getIdByRefCommonMod(token, "SpeciesFate", route="api/public/referential/ps/common/", argment="code=6")
    code_reje = getIdByRefCommonMod(token, "SpeciesFate", route="api/public/referential/ps/common/", argment="code=11")

    vers_code_6 = getIdByRefCommonMod(token, "VesselActivity", route="api/public/referential/ps/common/",
                                      argment="code=6")
    vers_code_13 = getIdByRefCommonMod(token, "VesselActivity", route="api/public/referential/ps/common/",
                                       argment="code=13")
    vers_code_99 = getIdByRefCommonMod(token, "VesselActivity", route="api/public/referential/ps/common/",
                                       argment="code=99")

    date = ""
    for val in group:
        for index, data in val[1].iterrows():
            date = data["date"]
            nb += 1

            # print(str(date).replace(" ","T").replace("00:00:00","")+str(data["heure"])+".000Z")
            tab4_catches = []

            # Permet d'incrementer le homeId sans perdre le file s'il n'y a pas d'activités
            if (data['cap_alb_yft_p10_tail'] != None or data['cap_alb_yft_p10_cap'] != None or \
                    data['cap_alb_yft_m10_tail'] != None or data['cap_alb_yft_m10_cap'] != None or \
                    data['cap_lst_skj_tail'] != None or data['cap_lst_skj_cap'] != None or \
                    data['cap_pat_bet_p10_tail'] != None or data['cap_pat_bet_p10_cap'] != None or \
                    data['cap_pat_bet_m10_tail'] != None or data['cap_pat_bet_m10_cap'] != None or \
                    data['cap_ger_alb_tail'] != None or data['cap_ger_alb_cap'] != None or \
                    data['cap_aut_esp_oth_esp'] != None or data['cap_aut_esp_oth_cap'] != None or \
                    data['cap_rej_dsc_esp'] != None or data['cap_rej_dsc_cap'] != None):

                # Recuperation des caputure et chercher les infor a partir de l'api pour concevoir le content pour catches
                js_catches = js_catche()  # intialisatiion des parametres defau
                if (data['cap_alb_yft_p10_tail'] != None and data['cap_alb_yft_p10_cap'] != None):
                    homeId += 1
                    # js_catches["homeId"] = homeId
                    js_catches["species"] = yft_id
                    js_catches["weight"] = data['cap_alb_yft_p10_cap']
                    Som_thon += float(data['cap_alb_yft_p10_cap'])
                    js_catches["weightMeasureMethod"] = WeightMeasureMet
                    js_catches["speciesFate"] = code_conser

                    tab4_catches.append(js_catches)

                js_catches = js_catche()  # intialisatiion des parametres defau
                if (data['cap_alb_yft_m10_tail'] != None and data['cap_alb_yft_m10_cap'] != None):
                    homeId += 1
                    # js_catches["homeId"] = homeId
                    js_catches["species"] = yft_id
                    js_catches["weight"] = data['cap_alb_yft_m10_cap']
                    Som_thon += float(data['cap_alb_yft_m10_cap'])
                    js_catches["weightMeasureMethod"] = WeightMeasureMet
                    js_catches["speciesFate"] = code_conser

                    tab4_catches.append(js_catches)

                js_catches = js_catche()  # intialisatiion des parametres defau
                if (data['cap_lst_skj_tail'] != None and data['cap_lst_skj_cap'] != None):
                    homeId += 1
                    # js_catches["homeId"] = homeId
                    js_catches["species"] = skj_id
                    js_catches["weight"] = data['cap_lst_skj_cap']
                    Som_thon += float(data['cap_lst_skj_cap'])
                    js_catches["weightMeasureMethod"] = WeightMeasureMet
                    js_catches["speciesFate"] = code_conser

                    tab4_catches.append(js_catches)

                js_catches = js_catche()  # intialisatiion des parametres defau
                if (data['cap_pat_bet_p10_tail'] != None and data['cap_pat_bet_p10_cap'] != None):
                    homeId += 1
                    # js_catches["homeId"] = homeId
                    js_catches["species"] = bet_id
                    js_catches["weight"] = data['cap_pat_bet_p10_cap']
                    Som_thon += float(data['cap_pat_bet_p10_cap'])
                    js_catches["weightMeasureMethod"] = WeightMeasureMet
                    js_catches["speciesFate"] = code_conser

                    tab4_catches.append(js_catches)

                js_catches = js_catche()  # intialisatiion des parametres defau
                if (data['cap_pat_bet_m10_tail'] != None and data['cap_pat_bet_m10_cap'] != None):
                    # homeId += 1
                    # js_catches["homeId"] = homeId
                    js_catches["species"] = bet_id
                    js_catches["weight"] = data['cap_pat_bet_m10_cap']
                    Som_thon += float(data['cap_pat_bet_m10_cap'])
                    js_catches["weightMeasureMethod"] = WeightMeasureMet
                    js_catches["speciesFate"] = code_conser

                    tab4_catches.append(js_catches)

                js_catches = js_catche()  # intialisatiion des parametres defau
                if (data['cap_ger_alb_tail'] != None and data['cap_ger_alb_cap'] != None):
                    homeId += 1
                    # js_catches["homeId"] = homeId
                    js_catches["species"] = germon_alb_id
                    js_catches["weight"] = data['cap_ger_alb_cap']
                    Som_thon += float(data['cap_ger_alb_cap'])
                    js_catches["weightMeasureMethod"] = WeightMeasureMet
                    js_catches["speciesFate"] = code_conser

                    tab4_catches.append(js_catches)
            """
                js_catches = js_catche() # intialisatiion des parametres defau
                if (data['cap_aut_esp_oth_esp'] != None and data['cap_aut_esp_oth_cap'] != None) :
                    homeId += 1
                    if data['cap_aut_esp_oth_tail'] == None:
                        #js_catches["homeId"] = homeId
                        js_catches["species"] = data['cap_aut_esp_oth_esp'] ###### PAscal  verifier si 3 lettres => recherce faoCode si trouve pas code recherche facode XXX* sinon XXX*
                        js_catches["weight"] = data['cap_aut_esp_oth_cap']
                        Som_thon += float(data['cap_aut_esp_oth_cap'])      ####### Revenir sur la capture Pascal ####
                        js_catches["weightMeasureMethod"] = WeightMeasureMet
                        js_catches["speciesFate"] = code_conser
                    else:
                        #js_catches["homeId"] = homeId
                        js_catches["species"] = data['cap_aut_esp_oth_esp'] ###### PAscal  verifier si 3 lettres => recherce faoCode si trouve pas code recherche facode XXX* sinon XXX*
    
                        js_catches["weight"] = data['cap_aut_esp_oth_cap']
                        Som_thon += float(data['cap_aut_esp_oth_cap'])
                        js_catches["weightMeasureMethod"] = WeightMeasureMet
                        js_catches["speciesFate"] = code_conser
                        
                        cap = data['cap_aut_esp_oth_tail']
    
                                
                    tab4_catches.append(js_catches)
    
                js_catches = js_catche() # intialisatiion des parametres defau
                if (data['cap_rej_dsc_esp'] != None and data['cap_rej_dsc_cap'] != None) :
                    homeId += 1
                    if data['cap_rej_dsc_tail'] == None:
                        #js_catches["homeId"] = homeId
                        js_catches["species"] = data['cap_rej_dsc_esp']  ###### PAscal idem ke oth
                        js_catches["weight"] = data['cap_rej_dsc_cap']
                        Som_thon += float(data['cap_rej_dsc_cap']) 
                        js_catches["weightMeasureMethod"] = WeightMeasureMet
                        js_catches["speciesFate"] = code_reje
                    else:
                        #js_catches["homeId"] = homeId
                        js_catches["species"] = data['cap_rej_dsc_esp']   ###### PAscal
                        js_catches["weight"] = data['cap_rej_dsc_cap']
                        Som_thon += float(data['cap_rej_dsc_cap'])
                        js_catches["weightMeasureMethod"] = WeightMeasureMet
                        js_catches["speciesFate"] = code_reje
    
                        cap = data['cap_rej_dsc_tail']
            
    
    
                    tab4_catches.append(js_catches)
            
                """

            ########### Activite ############

            js_activitys = js_activity(tab4_catches, tab3_floatingObject)

            if tab4_catches is not []:
                if data["comment"] is not None:
                    js_activitys["comment"] = data["comment"]
                else:
                    js_activitys["comment"] = "Aucun commentaire"
            else:
                js_activitys["comment"] = "Le programme de lecture du livre de bord n’a pas pu \
                                            déterminer le code bateau. Le nom du bateau était " + a['Navire']

            js_activitys["time"] = str(date).replace(" ", "T").replace("00:00:00", "") + str(data["heure"]) + ".000Z"
            js_activitys["number"] = int(nb)
            js_activitys["seaSurfaceTemperature"] = data["temp_mer"]
            js_activitys["windDirection"] = data["vent_dir"]

            if Som_thon != 0:
                js_activitys["totalWeight"] = Som_thon

            last = len(b) - 1
            if index == 0:
                if data["lat1"] != None and data["lat2"] != None and \
                        data["lat3"] != None and data["long1"] != None and \
                        data["long2"] != None and data["long3"] != None:
                    js_activitys["latitude"], js_activitys["longitude"] = lat_long(data["lat1"], data["lat2"],
                                                                                   data["lat3"], data["long1"],
                                                                                   data["long2"], data["long3"])

                else:
                    print("harbour :::::: ", a['Depart_Port'])
                    js_activitys["latitude"], js_activitys["longitude"] = get_lat_long(token, a['Depart_Port'])

            elif index == last:
                if data["lat1"] != None and data["lat2"] != None and \
                        data["lat3"] != None and data["long1"] != None and \
                        data["long2"] != None and data["long3"] != None:
                    js_activitys["latitude"], js_activitys["longitude"] = lat_long(data["lat1"], data["lat2"],
                                                                                   data["lat3"], data["long1"],
                                                                                   data["long2"], data["long3"])

                else:
                    js_activitys["latitude"], js_activitys["longitude"] = get_lat_long(token, a['Arrivee_Port'])
            else:
                js_activitys["latitude"], js_activitys["longitude"] = lat_long(data["lat1"], data["lat2"], data["lat3"],
                                                                               data["long1"], data["long2"],
                                                                               data["long3"])

            if (data['calee_porta'] is not None) and (data['calee_nul'] is not None):
                # Code 6
                js_activitys["setCount"] = 1

                ###########
                js_activitys["setSuccessStatus"] = "fr.ird.referential.ps.logbook.SetSuccessStatus#1464000000000#01"

                js_activitys["vesselActivity"] = vers_code_6

            elif data['obj_flot_act_sur_obj']:
                # Code 13
                js_activitys["setCount"] = 0

                ###########
                js_activitys["setSuccessStatus"] = "fr.ird.referential.ps.logbook.SetSuccessStatus#1464000000000#00"

                js_activitys["vesselActivity"] = vers_code_13

            else:
                # Code 99
                js_activitys["setCount"] = 0

                ###########
                js_activitys["setSuccessStatus"] = "fr.ird.referential.ps.logbook.SetSuccessStatus#1464000000000#02"

                js_activitys["vesselActivity"] = vers_code_99

            activite.append(js_activitys)
            Som_thon = 0

        js_routeLogbooks = js_routeLogbook(activite)
        js_routeLogbooks["date"] = str(date).replace(" ", "T") + ".000Z"

        routes.append(js_routeLogbooks)
        # print("num ",nb_r," activ nb: ",len(activite)," ",routes,"\n\n")
        # routes = []

        activite = []

        # print(activite)
        # print("Fini")
        nb = 0
        nb_r += 1
        # print("AAAAAAA")

    js_contents = js_content(routes, oce, prg)

    # noinspection PyBroadException
    try:
        # si plusieurs Rechercher celui qui a le code le plus elévé avec toujours son status == 1
        js_contents["vessel"] = getIdByRefCommonMod(token, "Vessel", argment="label2=" + a['Navire']+ "&filters.status=enabled")
    except:
        pass

    if a['Depart_Port'] == None:
        js_contents["departureHarbour"] = getIdByRefCommonMod(token, "Harbour", argment="code=999")
    else:
        # noinspection PyBroadException
        try:
            js_contents["departureHarbour"] = getIdByRefCommonMod(token, "Harbour",
                                                              argment="label2=" + (a['Depart_Port']).upper())
        except:
            pass

    if a['Arrivee_Port'] == None:
        js_contents["landingHarbour"] = getIdByRefCommonMod(token, "Harbour", argment="code=999")
    else:
        # noinspection PyBroadException
        try:
            js_contents["landingHarbour"] = getIdByRefCommonMod(token, "Harbour", argment="label2=" + (a['Arrivee_Port']).upper())
        except:
            pass

    if a['Depart_Date'] == None:
        js_contents["startDate"] = None
    else:
        js_contents["startDate"] = a['Depart_Date'] + "T00:00:00.000Z"  # "2021-03-02T00:00:00.000Z" #

    if a['Arrivee_Date'] == None:
        js_contents["endDate"] = None
    else:
        js_contents["endDate"] = a['Arrivee_Date'] + "T00:00:00.000Z"

    js_contents["captain"], js_contents["logbookDataEntryOperator"] = cap_obs_sea(token, ob)

    js_contents["loch"] = a['Arrivee_Loch']
    js_contents["homeId"] = str(ob["mar_homeId"])
    js_contents["observationsProgram"] = None
    js_contents["observationsAcquisitionStatus"] = "fr.ird.referential.ps.common.AcquisitionStatus#1464000000000#099"

    return js_contents


def check_trip(token, content):
    start = content["startDate"].replace("T00:00:00.000Z", "")
    end   = content["endDate"].replace("T00:00:00.000Z", "")

    id_ = ""
    ms_ = True
    # noinspection PyBroadException
    try:
        id_ = getIdByRefCommonMod(token, "Trip", route="api/public/data/ps/common/", argment="startDate="+ start +"&filters.endDate="+ end)
    except:
        ms_ = False

    return id_, ms_


def errorFilter(response):
    error = json.loads(response)
    tab_eur = []
    for val in error['exception']['result']['data']:
        for i in range(len(val['messages'])):
            tab_eur.append(val['messages'][i]['fieldName'] + ": " + val['messages'][i]['message'])
    return tab_eur


def add_trip(token, content):
    dict = content
    dicts = json.dumps(dict)

    headers = {
        "Content-Type": "application/json",
        'authenticationToken': token
    }

    id_, ms_ = check_trip(token, content)

    if ms_ != True:

        url = 'https://observe.ob7.ird.fr/observeweb-9-alternative/api/public/data/ps/common/Trip'

        print("La")

        res = requests.post(url, data=dicts, headers=headers)

        print(res.status_code, "\n")

        if res.status_code == 200:
            return True, json.loads(res.text)
        else:
            try:
                return False, errorFilter(res.text)
            except KeyError:
                return False, json.loads(res.text)['message']
    else:

        id_ = id_.replace("#", "-")

        url = 'https://observe.ob7.ird.fr/observeweb-9-alternative/api/public/data/ps/common/Trip/' + id_

        print(id_)

        print("iCI")

        res = requests.put(url, data=dicts, headers=headers)

        print(res.status_code, "\n")

        if res.status_code == 200:
            return True, json.loads(res.text)
        else:
            try:
                return False, errorFilter(res.text)
            except KeyError:
                return False, json.loads(res.text)['message']
#########################################################################################



