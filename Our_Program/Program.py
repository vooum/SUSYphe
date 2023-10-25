import pandas as pd
import subprocess
import pandas as pd
import argparse   
import numpy as np
from importlib.resources import contents
import re, sys, os, math, subprocess, shutil
from tarfile import data_filter
import csv
import stat
import importlib
import ast



ROOTPATH = os.path.abspath(os.path.dirname(__file__))
SLHAREADEROUTPUT = os.path.join(ROOTPATH, "slhaReaderOutPut.csv")
PROSPINO_PATH = [os.path.join(ROOTPATH, "Cross_Section", "Pro2_subroutines"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_1"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_2"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_3"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_4"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_5"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_6"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_7"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_8"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_9"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_10"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_11"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_12"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_13"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_14"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_15"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_16"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_17"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_18"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_19"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_20"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_21"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_22"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_23"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_24"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_25"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_26"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_27"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_28"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_29"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_30"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_31"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_32"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_33"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_34"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_35"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_36"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_37"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_38"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_39"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_40"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_41"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_42"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_43"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_44"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_45"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_46"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_47"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_48")]
PROSPINO_RUN_PATH = os.path.join(ROOTPATH, "Prospino_Run")
PROSPINO_INPUT_PATH_EWK = os.path.join(ROOTPATH, "Prospino_Input", "EWK")
PROSPINO_INPUT_PATH_Se = os.path.join(ROOTPATH, "Prospino_Input", "Se")
PROSPINO_INPUT_PATH_Smu = os.path.join(ROOTPATH, "Prospino_Input", "Smu")
PROSPINO_INPUT_PATH_Stau = os.path.join(ROOTPATH, "Prospino_Input", "Stau")

print(PROSPINO_RUN_PATH) 
PROSPINO_IN_LES_HOUCHES_PATH = os.path.join(PROSPINO_RUN_PATH, "prospino.in.les_houches")
CROSSSEXTION_RESULT_PATH = os.path.join(ROOTPATH, "Results", "CrossSection.csv")
CROSSSEXTION_RESULT_COLUMNS = ["Index", "Pb_N2N2", "Pb_N2N3", "Pb_N2N4", "Pb_N2N5", "Pb_N2C1", "Pb_N2C2",  "Pb_N2C1bar", "Pb_N2C2bar", "Pb_N3N3", "Pb_N3N4", "Pb_N3N5","Pb_N3C1", "Pb_N3C2", "Pb_N3C1bar", "Pb_N3C2bar", "Pb_N4N4", "Pb_N4N5", "Pb_N4C1", "Pb_N4C2", "Pb_N4C1bar", "Pb_N4C2bar", "Pb_N5N5", "Pb_N5C1", "Pb_N5C2", "Pb_N5C1bar", "Pb_N5C2bar", "Pb_C1C1bar", "Pb_C1C2bar", "Pb_C2C1bar", "Pb_C2C2bar", "Pb_selsel", "Pb_serser", "Pb_snelsnel", "Pb_selPsnel", "Pb_selMsnel", "Pb_smulsmul", "Pb_smursmur", "Pb_snmulsnmul", "Pb_smuPsnmul", "Pb_smuMsnmul", "Pb_stau1stau1", "Pb_stau2stau2", "Pb_stau1stau2", "Pb_sntausntau", "Pb_stau1Psntau", "Pb_stau1Msntau", "Pb_stau2Psntau", "Pb_stau1Msntau", "Sum_CrossSection_EWK", "Sum_CrossSection_Se", "Sum_CrossSection_Smu", "Sum_CrossSection_Stau"]
print(len(CROSSSEXTION_RESULT_COLUMNS))
CROSSSECTIONNUMBER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48]



MC_list1 = ["hh_1", "hh_2", "hh_3", "Ah_2", "Ah_3", 
            "Chi_1", "Chi_2", "Chi_3", "Chi_4", "Chi_5", "Cha_1", "Cha_2",
           "Se_1", "Se_2", "Se_3", "Se_4", "Se_5", "Se_6"]
MC_list12 = ["Sel", "Ser", "Smul", "Smur", "Staul", "Staur", "Stau1", "Stau2"]
MC_list2 = ["Sv_1", "Sv_2", "Sv_3"]
MC_list23 = ["Sve", "Svmu", "Svtau"]
MC_list3 = ["Su_1", "Su_2", "Su_3", "Su_4", "Su_5", "Su_6", "Sd_1", "Sd_2", "Sd_3", "Sd_4", "Sd_5", "Sd_6"]
MC_list34 = ["Type_Singlino"]
MC_list4 = ["N11", "N12", "N13", "N14", "N15", "N21", "N22", "N23", "N24", "N25", "N31", "N32", "N33", "N34", "N35","N41", "N42", "N43", "N44", "N45", "N51", "N52", "N53", "N54", "N55", 
            "U11", "U12", "U21", "U22", "V11", "V12", "V21", "V22",
            "ZE11", "ZE12", "ZE13", "ZE14", "ZE15", "ZE16", "ZE21", "ZE22", "ZE23", "ZE24", "ZE25", "ZE26", "ZE31", "ZE32", "ZE33", "ZE34", "ZE35", "ZE36", "ZE41", "ZE42", "ZE43", "ZE44", "ZE45", "ZE46", "ZE51", "ZE52", "ZE53", "ZE54", "ZE55", "ZE56", "ZE61", "ZE62", "ZE63", "ZE64", "ZE65", "ZE66", 
            "ZV11", "ZV12", "ZV13", "ZV21", "ZV22", "ZV23", "ZV31", "ZV32", "ZV33"]
MC_list = ["Index"] + MC_list1 + MC_list12 + MC_list2 + MC_list23 + MC_list3 + MC_list34 + MC_list4

SCAN_BLOCK = MC_list1 + MC_list2 + MC_list3 + MC_list4
SIGLINO_TYPE_NUMBER = {"N15": 1, "N25": 2, "N35": 3, "N45": 4, "N55": 5}
SLEPTON_TYPE_NUMBER = {"SEL":   {"ZE11": "Se_1", "ZE21": "Se_2", "ZE31": "Se_3", "ZE41": "Se_4", "ZE51": "Se_5", "ZE61": "Se_6"},
                       "SMUL":   {"ZE12": "Se_1", "ZE22": "Se_2", "ZE32": "Se_3", "ZE42": "Se_4", "ZE52": "Se_5", "ZE62": "Se_6"},
                       "STAUL":  {"ZE13": "Se_1", "ZE23": "Se_2", "ZE33": "Se_3", "ZE43": "Se_4", "ZE53": "Se_5", "ZE63": "Se_6"},
                       "SER":  {"ZE14": "Se_1", "ZE24": "Se_2", "ZE34": "Se_3", "ZE44": "Se_4", "ZE54": "Se_5", "ZE64": "Se_6"},
                       "SMUR": {"ZE15": "Se_1", "ZE25": "Se_2", "ZE35": "Se_3", "ZE45": "Se_4", "ZE55": "Se_5", "ZE65": "Se_6"},
                       "STAUR": {"ZE16": "Se_1", "ZE26": "Se_2", "ZE36": "Se_3", "ZE46": "Se_4", "ZE56": "Se_5", "ZE66": "Se_6"}}
SV_TYPE_NUMBER = {"SVE": {"ZV11": "Sv_1", "ZV21": "Sv_2", "ZV31": "Sv_3"},
                  "SVMU": {"ZV12": "Sv_1", "ZV22": "Sv_2", "ZV32": "Sv_3"},
                  "SVTAU": {"ZV13": "Sv_1", "ZV23": "Sv_2", "ZV33": "Sv_3"}}
SLEPTON_PDG = {"Se_1":"1000011", "Se_2":"1000013", "Se_3":"1000015", "Se_4":"2000011",  "Se_5":"2000013", "Se_6":"2000015", "Sv_1":"1000012", "Sv_2":"1000014", "Sv_3":"1000016"}

Dict = {31:["Sel_type","Sel_type"], 32:["Ser_type", "Ser_type"], 33:["Sve_type", "Sve_type"], 34:["Sve_type","Sel_type"], 35:["Sel_type", "Sve_type"],
        36:["Smul_type","Smul_type"], 37:["Smur_type", "Smur_type"], 38:["Svmu_type", "Svmu_type"], 39:["Svmu_type", "Smul_type"], 40:["Smul_type", "Svmu_type"],
        41:["Stau1_type", "Stau1_type"], 42:["Stau2_type", "Stau2_type"], 43:["Stau2_type", "Stau1_type"], 44:["Svtau_type", "Svtau_type"], 45:["Svtau_type", "Stau1_type"], 46:["Stau1_type", "Svtau_type"], 47:["Svtau_type", "Stau2_type"], 48:["Stau2_type", "Svtau_type"], 432:["Stau1_type", "Stau2_type"]}
    

ROOTPATH = sys.path[0]
PROSPINO_RESULT_FILE = os.path.join(ROOTPATH, "Results")
SMODELS_IN_PATH = os.path.join(ROOTPATH, "smodels/SModelS_Input")
SMODELS_RUN_PATH = os.path.join(ROOTPATH, "smodels/smodels-2.3.2")
SMODELS_OUTPUT_FILE = os.path.join(SMODELS_RUN_PATH, "output_dir")
SMODELS_INPUT_FILE = os.path.join(ROOTPATH, "smodels/smodels-2.3.2/multi_spectr/")

def Read_CSV() -> (pd.DataFrame, list):
    '''
    读取 slhaReaderOutPut.csv
    '''
    Data_DF = pd.read_csv(SLHAREADEROUTPUT)
    IndexList = Data_DF["Index"].astype(int)
    return(Data_DF, IndexList)

def Make_ProspinoIn_EWK(Index: int):
    '''
    准备 Prospino 输入文件
    '''
    ProspinoInDir_EWK = os.path.join(PROSPINO_INPUT_PATH_EWK, f"ProspinoIn_{Index}.txt")
    print("cp input file")
    return(ProspinoInDir_EWK)

def Make_ProspinoIn_Se(Index: int):
    '''
    准备 Prospino 输入文件
    '''
    ProspinoInDir_Se = os.path.join(PROSPINO_INPUT_PATH_Se, f"ProspinoIn_{Index}.txt")
    os.system(f"cp {ProspinoInDir_Se} {PROSPINO_IN_LES_HOUCHES_PATH}")
    return(ProspinoInDir_Se)

def Make_ProspinoIn_Smu(Index: int):
    '''
    准备 Prospino 输入文件
    '''
    ProspinoInDir_Smu = os.path.join(PROSPINO_INPUT_PATH_Smu, f"ProspinoIn_{Index}.txt")
    os.system(f"cp {ProspinoInDir_Smu} {PROSPINO_IN_LES_HOUCHES_PATH}")
    return(ProspinoInDir_Smu)

def Make_ProspinoIn_Stau(Index: int):
    '''
    准备 Prospino 输入文件
    '''
    ProspinoInDir_Stau = os.path.join(PROSPINO_INPUT_PATH_Stau, f"ProspinoIn_{Index}.txt")
    os.system(f"cp {ProspinoInDir_Stau} {PROSPINO_IN_LES_HOUCHES_PATH}")
    return(ProspinoInDir_Stau)


def Execute_Prospino(Prospino_Number: int) -> float:
    '''
    单次运行 Prospino_EWK 
    '''
    print(Prospino_Number)
    command = PROSPINO_PATH[Prospino_Number] + "/prospino_2.run > a.txt"
    run = subprocess.Popen(command, cwd=PROSPINO_RUN_PATH, close_fds=False, universal_newlines=True, shell=True)
    out, err = run.communicate(input=None, timeout=None)
    print("Prospino Error: ", err)
    with open(os.path.join(PROSPINO_RUN_PATH, "prospino.dat"), 'r') as ProspinoOut:
        ProspinoResult = float(ProspinoOut.readline().split()[-1])
        print(ProspinoResult)
    return(ProspinoResult)

def Calculate_CrossSection(Index: int, Data_DF: pd.DataFrame):
    '''
    计算一个参数点所需的所有截面
    '''
    ProspinoResults = [Index]
    SLHA_Information = Data_DF[Data_DF["Index"] == Index]
    if SLHA_Information["Siglino_Type"].item() == "N1":
        for Prospino_Number in CROSSSECTIONNUMBER:
            ProspinoResults.append(Execute_Prospino(Prospino_Number))
    elif SLHA_Information["Siglino_Type"].item() == "N2":
        for Prospino_Number in CROSSSECTIONNUMBER:
            if Prospino_Number in [1, 2, 3, 4, 5, 6, 7, 8]:
                ProspinoResults.append(0)
            else:
                ProspinoResults.append(Execute_Prospino(Prospino_Number))
    elif SLHA_Information["Siglino_Type"].item() == "N3":
        for Prospino_Number in CROSSSECTIONNUMBER:
            if Prospino_Number in [2, 9, 10, 11, 12, 13, 14, 15]:
                ProspinoResults.append(0)
            else:
                ProspinoResults.append(Execute_Prospino(Prospino_Number))
    elif SLHA_Information["Siglino_Type"].item() == "N4":
        for Prospino_Number in CROSSSECTIONNUMBER:
            if Prospino_Number in [3, 10, 16, 17, 18, 19, 20, 21]:
                ProspinoResults.append(0)
            else:
                ProspinoResults.append(Execute_Prospino(Prospino_Number))
    elif SLHA_Information["Siglino_Type"].item() == "N5":
        for Prospino_Number in CROSSSECTIONNUMBER:
            if Prospino_Number in [4, 11, 17, 22, 23, 24, 25, 26]:
                ProspinoResults.append(0)
            else:
                ProspinoResults.append(Execute_Prospino(Prospino_Number))
    ProspinoResults.append(sum(ProspinoResults[1:30]))
    ProspinoResults.append(sum(ProspinoResults[31:35]))
    ProspinoResults.append(sum(ProspinoResults[36:40]))
    ProspinoResults.append(sum(ProspinoResults[41:48]))
    print(CROSSSEXTION_RESULT_COLUMNS)
    print(ProspinoResults)
    return(ProspinoResults)

def Export_CSV(ProspinoResults: list):
    '''
   "Sum_CrossSection_EWK" 把计算结果导出为 csv 格式文件
    '''
    if os.path.isfile(CROSSSEXTION_RESULT_PATH):
        pd.DataFrame([ProspinoResults], columns=CROSSSEXTION_RESULT_COLUMNS).to_csv(CROSSSEXTION_RESULT_PATH, header=False, index=False, mode='a')
    else:
        pd.DataFrame([ProspinoResults], columns=CROSSSEXTION_RESULT_COLUMNS).to_csv(CROSSSEXTION_RESULT_PATH, header=True, index=False, mode='w')

def PrePare_Check():
    '''
    每次开启新项目之前所做的先期准备和检查
    '''
    try:
        os.system(f"cp -r {PROSPINO_PATH[0]} {PROSPINO_RUN_PATH}")
        print(f'{PROSPINO_PATH[0]} is successfully copied to {PROSPINO_RUN_PATH}.')
    except FileNotFoundError:
        print(f'{PROSPINO_PATH[0]} does not exist.')
    except FileExistsError:
        print(f'Pro2_subroutines has already exists in {PROSPINO_RUN_PATH}.')
    except Exception as e:
        print(f'An error occurred while copying the folder：{e}.')
    try:
        os.remove(CROSSSEXTION_RESULT_PATH)
        print("Old CrossSection.csv file has removed!")
    except OSError as e:
        print("No old CrossSection.csv file exist!")



def Parse_Args():
    '''
    接收命令行参数，读取数据文件
    '''
    parser = argparse.ArgumentParser(description="Make csv data file normalization.")         
    parser.add_argument("--csv_file", default="./slhaReaderOutPut.csv", help="The path of file that you need to normalization.")     
    args = parser.parse_args()
    csv_file_path = args.csv_file
    try:
        scan_data = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return(scan_data)               

def Process_Data(scan_data):       
    '''
    对数据进行标准化处理
    '''
    norm_data = scan_data.loc[:, ["Index"]]
    print(norm_data)
    for column in SCAN_BLOCK:
        if column in scan_data:
            norm_data[column] = scan_data[column]     
        else:
            norm_data[column] = pd.Series(dtype='float64')    
    print(norm_data)
    norm_data["Type_Singlino"] = norm_data.loc[:, ["N15", "N25", "N35", "N45", "N55"]].apply(lambda NX5: (NX5 ** 2).idxmax(), axis=1).map(SIGLINO_TYPE_NUMBER)

    norm_data["Sel_type"] = norm_data.loc[:, ["ZE11", "ZE21", "ZE31", "ZE41", "ZE51", "ZE61"]].apply(lambda ZEX1: (ZEX1 ** 2).idxmax(), axis=1).map(SLEPTON_TYPE_NUMBER["SEL"])
    norm_data["Sel"] = norm_data.apply(lambda row: row[row["Sel_type"]], axis=1)      
    norm_data["Sel_PDG"] = norm_data.apply(lambda row: row["Sel_type"], axis=1).map(SLEPTON_PDG) 
    print(norm_data)

    norm_data["Ser_type"] = norm_data.loc[:, ["ZE14", "ZE24", "ZE34", "ZE44", "ZE54", "ZE64"]].apply(lambda ZEX4: (ZEX4 ** 2).idxmax(), axis=1).map(SLEPTON_TYPE_NUMBER["SER"])
    norm_data["Ser"] = norm_data.apply(lambda row: row[row["Ser_type"]] if pd.notnull(row["Ser_type"]) else np.nan, axis=1)
    norm_data["Ser_PDG"] = norm_data.apply(lambda row: row["Ser_type"], axis=1).map(SLEPTON_PDG) 
    print(norm_data)


    norm_data["Smul_type"] = norm_data.loc[:, ["ZE12", "ZE22", "ZE32", "ZE42", "ZE52", "ZE62"]].apply(lambda ZEX2: (ZEX2 ** 2).idxmax(), axis=1).map(SLEPTON_TYPE_NUMBER["SMUL"])
    norm_data["Smul"] = norm_data.apply(lambda row: row[row["Smul_type"]] if pd.notnull(row["Smul_type"]) else np.nan, axis=1)
    norm_data["Smul_PDG"] = norm_data.apply(lambda row: row["Smul_type"], axis=1).map(SLEPTON_PDG) 

    norm_data["Smur_type"]  = norm_data.loc[:, ["ZE15", "ZE25", "ZE35", "ZE45", "ZE55", "ZE65"]].apply(lambda ZEX5: (ZEX5 ** 2).idxmax(), axis=1).map(SLEPTON_TYPE_NUMBER["SMUR"])
    norm_data["Smur"] = norm_data.apply(lambda row: row[row["Smur_type"]] if pd.notnull(row["Smur_type"]) else np.nan, axis=1)
    norm_data["Smur_PDG"] = norm_data.apply(lambda row: row["Smur_type"], axis=1).map(SLEPTON_PDG) 

    norm_data["Staul_type"] = norm_data.loc[:, ["ZE13", "ZE23", "ZE33", "ZE43", "ZE53", "ZE63"]].apply(lambda ZEX3: (ZEX3 ** 2).idxmax(), axis=1).map(SLEPTON_TYPE_NUMBER["STAUL"])
    norm_data["Staul"] = norm_data.apply(lambda row: row[row["Staul_type"]] if pd.notnull(row["Staul_type"]) else np.nan, axis=1)
    norm_data["Staul_PDG"] = norm_data.apply(lambda row: row["Staul_type"], axis=1).map(SLEPTON_PDG) 

    norm_data["Staur_type"] = norm_data.loc[:, ["ZE16", "ZE26", "ZE36", "ZE46", "ZE56", "ZE66"]].apply(lambda ZEX6: (ZEX6 ** 2).idxmax(), axis=1).map(SLEPTON_TYPE_NUMBER["STAUR"])
    norm_data["Staur"] = norm_data.apply(lambda row: row[row["Staur_type"]] if pd.notnull(row["Staur_type"]) else np.nan, axis=1)
    norm_data["Staur_PDG"] = norm_data.apply(lambda row: row["Staur_type"], axis=1).map(SLEPTON_PDG) 

    norm_data["Stau1_type"] = norm_data.apply(lambda row: row["Staul_type"] if min(row["Staul"], row["Staur"]) == row["Staul"] else row["Staul_type"], axis =1)
    norm_data["Stau1"] = norm_data.apply(lambda row: min(row["Staul"], row["Staur"]), axis=1)       
    norm_data["Stau1_PDG"] = norm_data.apply(lambda row: row["Stau1"], axis=1).map(SLEPTON_PDG) 
    norm_data["Stau2_type"] = norm_data.apply(lambda row: row["Staul_type"] if max(row["Staul"], row["Staur"]) == row["Staul"] else row["Staul_type"], axis =1)
    norm_data["Stau2"] = norm_data.apply(lambda row: max(row["Staul"], row["Staur"]), axis=1)
    norm_data["Stau2_PDG"] = norm_data.apply(lambda row: row["Stau2"], axis=1).map(SLEPTON_PDG) 

    norm_data["Sve_type"] = norm_data.loc[:, ["ZV11", "ZV21", "ZV31"]].apply(lambda ZVX1: (ZVX1 ** 2).idxmax(), axis=1).map(SV_TYPE_NUMBER["SVE"])
    norm_data["Sve"] = norm_data.apply(lambda row: row[row["Sve_type"]] if pd.notnull(row["Sve_type"]) else np.nan, axis=1)     
    norm_data["Sve_PDG"] = norm_data.apply(lambda row: row["Sve_type"], axis=1).map(SLEPTON_PDG) 

    norm_data["Svmu_type"] = norm_data.loc[:, ["ZV12", "ZV22", "ZV32"]].apply(lambda ZVX2: (ZVX2 ** 2).idxmax(), axis=1).map(SV_TYPE_NUMBER["SVMU"])
    norm_data["Svmu"] = norm_data.apply(lambda row: row[row["Svmu_type"]] if pd.notnull(row["Svmu_type"]) else np.nan, axis=1)
    norm_data["Svmu_PDG"] = norm_data.apply(lambda row: row["Svmu_type"], axis=1).map(SLEPTON_PDG) 

    norm_data["Svtau_type"] = norm_data.loc[:, ["ZV13", "ZV23", "ZV33"]].apply(lambda ZVX3: (ZVX3 ** 2).idxmax(), axis=1).map(SV_TYPE_NUMBER["SVTAU"])
    norm_data["Svtau"] = norm_data.apply(lambda row: row[row["Svtau_type"]] if pd.notnull(row["Svtau_type"]) else np.nan, axis=1)
    norm_data["Svtau_PDG"] = norm_data.apply(lambda row: row["Svtau_type"], axis=1).map(SLEPTON_PDG) 

    for i in list(range(31,49)) + [432]:
        j = str(i)            
        norm_data[j]= norm_data.apply(lambda row: row[Dict[i][0]], axis=1).map(SLEPTON_PDG) + "," + "-" + norm_data.apply(lambda row: row[Dict[i][1]], axis=1).map(SLEPTON_PDG)
        print(norm_data[j]) 
    # return(norm_data[MC_list])
    return(norm_data)


ROOTPATH = sys.path[0]
PROSPINO_RESULT_FILE = os.path.join(ROOTPATH, "Results")
SMODELS_IN_PATH = os.path.join(ROOTPATH, "smodels/SModelS_Input")
SMODELS_RUN_PATH = os.path.join(ROOTPATH, "smodels/smodels-2.3.2")
SMODELS_OUTPUT_FILE = os.path.join(SMODELS_RUN_PATH, "output_dir")
SMODELS_INPUT_FILE = os.path.join(ROOTPATH, "smodels/smodels-2.3.2/multi_spectr/")


def Read_CS_CSV() -> (pd.DataFrame, list):
    '''
    读取 CrossSection.csv
    '''
    PROSPINO_RESULT = os.path.join(PROSPINO_RESULT_FILE, "CrossSection.csv")
    Data_DF = pd.read_csv(PROSPINO_RESULT)
    IndexList = Data_DF["Index"].astype(int)
    return(Data_DF, IndexList)




def GetSmodels_Input(Data_DF: pd.DataFrame, IndexList: pd.Series):
    global SModelS_InDir
    IndexList = Data_DF["Index"]
    Index = IndexList[0]
    SModelS_InDir = os.path.join(ROOTPATH, "smodels/SmodelS_Input/SmodelS_{}.slha".format(Index))
    return(SModelS_InDir)


def Make_SModelSIn(SModelS_InDir: str):
    '''
    制备 Smodels 标准输入谱
    '''
    SModelS_Input_spectr = os.path.join(SMODELS_INPUT_FILE, "NMSSM_slha")
    shutil.copyfile(SModelS_InDir, SModelS_Input_spectr)
    return(SModelS_Input_spectr)



def CrossSection_Write(SModelS_Input_spectr: str, data: pd.DataFrame):
    num_dict = {"Pb_N2N2": [1000023, 1000023],
    "Pb_N2N3": [1000023, 1000025],
    "Pb_N2N4": [1000023, 1000035],
    "Pb_N2N5": [1000023, 1000045],
    "Pb_N2C1": [1000023, -1000024],
    "Pb_N2C2": [1000023, -1000037],
    "Pb_N2C1bar": [1000023, 1000024],
    "Pb_N2C2bar": [1000023, 1000037],
    "Pb_N3N3" : [1000025, 1000025],
    "Pb_N3N4" : [1000025, 1000035],
    "Pb_N3N5" : [1000025, 1000045],
    "Pb_N3C1" : [1000025, -1000024],
    "Pb_N3C2" : [1000025, -1000037],
    "Pb_N3C1bar" : [1000025, 1000024],
    "Pb_N3C2bar" : [1000025, 1000037],
    "Pb_N4N4" : [1000035, 1000035],
    "Pb_N4N5" : [1000035, 1000045],
    "Pb_N4C1" : [1000035, -1000024],
    "Pb_N4C2" : [1000035, -1000037],
    "Pb_N4C1bar" : [1000035, 1000024],
    "Pb_N4C2bar" : [1000035, 1000037],
    "Pb_N5N5" : [1000045, 1000045],
    "Pb_N5C1" : [1000045, -1000024],
    "Pb_N5C2" : [1000045, -1000037],
    "Pb_N5C1bar" : [1000045, 1000024],
    "Pb_N5C2bar" : [1000045, 1000037],
    "Pb_C1C1bar" : [-1000037, 1000037],
    "Pb_C1C2bar" : [-100037, 1000024],
    "Pb_C2C1bar" : [-1000024, 1000037],
    "Pb_C2C2bar" : [-1000037, 1000037],
    "Pb_selsel" : ["31"],
    "Pb_serser" : ["32"],
    "Pb_snelsnel" : ["33"],
    "Pb_selPsnel" : ["34"],
    "Pb_selMsnel" : ["35"],
    "Pb_smulsmul" : ["36"],
    "Pb_smursmur" : ["37"],
    "Pb_snmulsnmul" : ["38"],
    "Pb_smuPsnmul" : ["39"],
    "Pb_smuMsnmul" : ["40"],
    "Pb_stau1stau1" : ["41"],
    "Pb_stau2stau2" : ["42"],
    "Pb_stau1stau2" : ["43"],
    "Pb_sntausntau" : ["44"],
    "Pb_stau1Psntau" : ["45"],
    "Pb_stau1Msntau" : ["46"],
    "Pb_stau2Psntau" : ["47"],
    "Pb_stau2Msntau" : ["48"],
}


    df1 = pd.read_csv("slhaReaderOutPut1.csv")
    print(df1)
    replace_dict = df1[["31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48"]].fillna(0).to_dict("records")[0]
    print(replace_dict)
    for key, value in num_dict.items():  
        if isinstance(value, list) and len(value) == 1 and isinstance(value[0], str):
            new_value = replace_dict.get(value[0]) 
            if new_value: 
                num_dict[key] = new_value
    print(num_dict)
    for key, value in num_dict.items(): 
        if isinstance(value, str) and ',' in value: 
            num_dict[key] = [int(x) for x in value.split(',')]
    print(num_dict)


    SModelS_Input_spectr = os.path.join(SMODELS_INPUT_FILE, "NMSSM_slha")
    with open(PROSPINO_RESULT_FILE + "/CrossSection.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_reader = list(csv_reader)
        columns = csv_reader[0][1:-4]
        csv_reader = [row[1:-4] for row in csv_reader[1:]]
        for row in csv_reader: 
            for key, value in zip(columns, row):
                if value != "0":
                    data[key] = float(value)
    os.chmod(SModelS_Input_spectr, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)
    try:
        with open(SModelS_Input_spectr, "a") as smodels_in:
            for key, value in data.items():
                num1, num2 = num_dict[key]
                print(num_dict)
                print(num1)
                print(num2)
                try:
                    bytes1 = smodels_in.write("\n" + "XSECTION  " + f"1.30E+04" + f"  2212 2212 2 {num1} {num2}")
                    print(bytes1)
                    print(f"第一行写入了{bytes1}个字节")
                    bytes2 = smodels_in.write("\n" + "  0  0  0  0  0  0    " + str(value) + " SModelS 2.3.2")
                    print(bytes2)
                    print(f"第一行写入了{bytes2}个字节")
                except IOerror as e :
                     print(f"文件write失败: {e}")
    except IOError as e:
       print(f"文件操作失败: {e}")
    except ValueError as e:
       print(f"数据格式错误: {e}")
    return



def Exec_SModelS(SModelS_Input_spectr: str):
    SModelS_Input_spectr = os.path.join(SMODELS_INPUT_FILE, "NMSSM_slha")
    command = SMODELS_RUN_PATH + "/runSModelS.py > a.txt -p parameters.ini -f ./multi_spectr/NMSSM_slha -o output_dir"
    run = subprocess.Popen(command, cwd = SMODELS_RUN_PATH, close_fds=False, universal_newlines=True, shell=True )
    out, err = run.communicate(input=None, timeout=None)

def Read_Output():
    #os.chdir(SMODELS_OUTPUT_FILE)
    sys.path.append(os.getcwd())
    #print(os.getcwd())
    #print(sys.modules.keys())
    r_smodels = importlib.import_module("NMSSM_slha").smodelsOutput["ExptRes"][0]['r']
    TxNames = importlib.import_module("NMSSM_slha").smodelsOutput["ExptRes"][0]['TxNames']
    AnalysisID = importlib.import_module("NMSSM_slha").smodelsOutput["ExptRes"][0]['AnalysisID']
    DataSetID = importlib.import_module("NMSSM_slha").smodelsOutput["ExptRes"][0]['DataSetID']
    #method chain
    Results = [TxNames, r_smodels, AnalysisID, DataSetID]
    print(Results)
    return(Results)






def main():
    PrePare_Check()
    Data_DF, IndexList = Read_CSV()
    for Index in IndexList:
        for Prospino_Number in CROSSSECTIONNUMBER:
            if 1 <= Prospino_Number <= 30:
                Make_ProspinoIn_EWK(Index)
            elif 31 <= Prospino_Number <= 35:
                Make_ProspinoIn_Se(Index)
            elif 36 <= Prospino_Number <= 40:
                Make_ProspinoIn_Smu(Index)
            elif 41 <= Prospino_Number <= 48:
                Make_ProspinoIn_Stau(Index)
            else:
                raise ValueError("Prospino_Number must be between 1 and 48")
        ProspinoResults = Calculate_CrossSection(Index, Data_DF)
        Export_CSV(ProspinoResults)
    slha_data = Parse_Args()
    norm_data = Process_Data(slha_data)
    norm_data.to_csv("slhaReaderOutPut1.csv", index=False)
    global SModelS_InDir
    SModelS_Input_spectr = os.path.join(SMODELS_INPUT_FILE, "NMSSM_slha")
    data = {}
    Data_DF, IndexList = Read_CS_CSV()
    GetSmodels_Input(Data_DF, IndexList)
    Make_SModelSIn(SModelS_InDir)
    CrossSection_Write(SModelS_Input_spectr, data)
    Exec_SModelS(SModelS_Input_spectr)
    os.chdir(SMODELS_OUTPUT_FILE)
    Read_Output()




if __name__ == "__main__":
    main()



