import pandas as pd
import argparse   
import numpy as np

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
                       "SER":   {"ZE12": "Se_1", "ZE22": "Se_2", "ZE32": "Se_3", "ZE42": "Se_4", "ZE52": "Se_5", "ZE62": "Se_6"},
                       "SMUL":  {"ZE13": "Se_1", "ZE23": "Se_2", "ZE33": "Se_3", "ZE43": "Se_4", "ZE53": "Se_5", "ZE63": "Se_6"},
                       "SMUR":  {"ZE14": "Se_1", "ZE24": "Se_2", "ZE34": "Se_3", "ZE44": "Se_4", "ZE54": "Se_5", "ZE64": "Se_6"},
                       "STAUL": {"ZE15": "Se_1", "ZE25": "Se_2", "ZE35": "Se_3", "ZE45": "Se_4", "ZE55": "Se_5", "ZE65": "Se_6"},
                       "STAUR": {"ZE16": "Se_1", "ZE26": "Se_2", "ZE36": "Se_3", "ZE46": "Se_4", "ZE56": "Se_5", "ZE66": "Se_6"}}
SV_TYPE_NUMBER = {"SVE": {"ZV11": "Sv_1", "ZV21": "Sv_2", "ZV31": "Sv_3"},
                  "SVMU": {"ZV12": "Sv_1", "ZV22": "Sv_2", "ZV32": "Sv_3"},
                  "SVTAU": {"ZV13": "Sv_1", "ZV23": "Sv_2", "ZV33": "Sv_3"}}
SLEPTON_PDG = {"Se_1":"1000011", "Se_2":"1000013", "Se_3":"1000015", "Se_4":"2000011",  "Se_5":"2000013", "Se_6":"2000015", "Sv_1":"1000012", "Sv_2":"1000014", "Sv_3":"1000016"}

# 暂取 {43:["Stau2_type", "Stau1_type"]}, 另一个取为 {432:["Stau1_type", "Stau2_type"]}
Dict = {31:["Sel_type","Sel_type"], 32:["Ser_type", "Ser_type"], 33:["Sve_type", "Sve_type"], 34:["Sve_type","Sel_type"], 35:["Sel_type", "Sve_type"],
        36:["Smul_type","Smul_type"], 37:["Smur_type", "Smur_type"], 38:["Svmu_type", "Svmu_type"], 39:["Svmu_type", "Smul_type"], 40:["Smul_type", "Svmu_type"],
        41:["Stau1_type", "Stau1_type"], 42:["Stau2_type", "Stau2_type"], 43:["Stau2_type", "Stau1_type"], 44:["Svtau_type", "Svtau_type"], 45:["Svtau_type", "Stau1_type"], 46:["Stau1_type", "Svtau_type"], 47:["Svtau_type", "Stau2_type"], 48:["Stau2_type", "Svtau_type"], 432:["Stau1_type", "Stau2_type"]}
    

def Parse_Args():
    '''
    接收命令行参数，读取数据文件
    '''
    parser = argparse.ArgumentParser(description="Make csv data file normalization.")         
    parser.add_argument("--csv_file", default="./AllInfo.csv", help="The path of file that you need to normalization.")     
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
    for column in SCAN_BLOCK:
        if column in scan_data:
            norm_data[column] = scan_data[column]     
        else:
            norm_data[column] = pd.Series(dtype='float64')     
    norm_data["Type_Singlino"] = norm_data.loc[:, ["N15", "N25", "N35", "N45", "N55"]].apply(lambda NX5: (NX5 ** 2).idxmax(), axis=1).map(SIGLINO_TYPE_NUMBER)

    norm_data["Sel_type"] = norm_data.loc[:, ["ZE11", "ZE21", "ZE31", "ZE41", "ZE51", "ZE61"]].apply(lambda ZEX1: (ZEX1 ** 2).idxmax(), axis=1).map(SLEPTON_TYPE_NUMBER["SEL"])
    norm_data["Sel"] = norm_data.apply(lambda row: row[row["Sel_type"]], axis=1)      
    norm_data["Sel_PDG"] = norm_data.apply(lambda row: row["Sel_type"], axis=1).map(SLEPTON_PDG) 

    norm_data["Ser_type"] = norm_data.loc[:, ["ZE14", "ZE24", "ZE34", "ZE44", "ZE54", "ZE64"]].apply(lambda ZEX4: (ZEX4 ** 2).idxmax(), axis=1).map(SLEPTON_TYPE_NUMBER["SER"])
    norm_data["Ser"] = norm_data.apply(lambda row: row[row["Ser_type"]] if pd.notnull(row["Ser_type"]) else np.nan, axis=1)
    norm_data["Ser_PDG"] = norm_data.apply(lambda row: row["Ser_type"], axis=1).map(SLEPTON_PDG) 

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
        norm_data[j]= norm_data.apply(lambda row: row[Dict[i][0]], axis=1).map(SLEPTON_PDG) + "  " + "-" + norm_data.apply(lambda row: row[Dict[i][1]], axis=1).map(SLEPTON_PDG)
   
    # return(norm_data[MC_list])
    return(norm_data)


if __name__ == "__main__":
    slha_data = Parse_Args()
    norm_data = Process_Data(slha_data)
    norm_data.to_csv("slhaReaderOutPut.csv", index=False)
    