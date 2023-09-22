import pandas as pd
import sys, os
import subprocess
import shutil

ROOTPATH = os.path.abspath(os.path.dirname(__file__))
SLHAREADEROUTPUT = os.path.join(ROOTPATH, "slhaReaderOutPut.csv")
PROSPINO_PATH = [os.path.join(ROOTPATH, "Cross_Section", "Pro2_subroutines"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_1"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_2"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_3"),
                 os.path.join(ROOTPATH, "Cross_Section", "Prospino2_4")]
PROSPINO_RUN_PATH = os.path.join(ROOTPATH, "Prospino_Run")
PROSPINO_IN_LES_HOUCHES_PATH = os.path.join(PROSPINO_RUN_PATH, "prospino.in.les_houches")
CROSSSEXTION_RESULT_PATH = os.path.join(ROOTPATH, "Results", "CrossSection.csv")
CROSSSEXTION_RESULT_COLUMNS = ["Index", "Pb_C1C1bar", "Pb_C1C2bar", "Pb_C2C1bar", "Pb_C2C2bar", "Sum_CrossSection"]
N1CROSSSECTIONNUMBER = [1, 2, 3, 4]   # there is an example, EW should be list(range(1,31))

def Read_CSV() -> (pd.DataFrame, list):
    '''
    读取 slhaReaderOutPut.csv
    '''
    Data_DF = pd.read_csv(SLHAREADEROUTPUT)
    IndexList = Data_DF["Index"].astype(int)
    return(Data_DF, IndexList)

def Make_ProspinoIn(Index: int):
    '''
    准备 Prospino 输入文件
    '''
    ProspinoInDir = os.path.join(ROOTPATH, f"Prospino_Input/ProspinoIn_{Index}.txt")
    os.system(f"cp {ProspinoInDir} {PROSPINO_IN_LES_HOUCHES_PATH}")

def Execute_Prospino(Prospino_Number: int) -> float:
    '''
    单次运行 Prospino 
    '''
    command = PROSPINO_PATH[Prospino_Number] + "/prospino_2.run > a.txt"
    run = subprocess.Popen(command, cwd=PROSPINO_RUN_PATH, close_fds=False, univerfal_newlines=True)
    out, err = run.communicate()
    print("Prospino Error: ", err)
    with open(os.path.join(PROSPINO_RUN_PATH, "prospino.dat"), 'r') as ProspinoOut:
        ProspinoResult = float(ProspinoOut.readline().split()[-1])
    return(ProspinoResult)

def Calculate_CrossSection(Index: int, Data_DF: pd.DataFrame):
    '''
    计算一个参数点所需的所有截面
    '''
    ProspinoResults = [Index]
    SLHA_Information = Data_DF[Data_DF["Index"] == Index]
    if SLHA_Information["Siglino_Type"] == "N1":
        for Prospino_Number in N1CROSSSECTIONNUMBER:
            ProspinoResults.append(Execute_Prospino(Prospino_Number))
    ProspinoResults.append(sum(ProspinoResults[1:]))
    return(ProspinoResults)

def Export_CSV(ProspinoResults: list):
    '''
    把计算结果导出为 csv 格式文件
    '''
    if os.path.isfile(CROSSSEXTION_RESULT_PATH):
        pd.DataFrame(ProspinoResults, columns=CROSSSEXTION_RESULT_COLUMNS).to_csv(CROSSSEXTION_RESULT_PATH, header=False, index=False, mode='a')
    else:
        pd.DataFrame(ProspinoResults, columns=CROSSSEXTION_RESULT_COLUMNS).to_csv(CROSSSEXTION_RESULT_PATH, header=True, index=False, mode='w')

def PrePare_Check():
    '''
    每次开启新项目之前所做的先期准备和检查
    '''
    try:
        shutil.copytree(PROSPINO_PATH[0], PROSPINO_RUN_PATH)
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

def main():
    PrePare_Check()
    Data_DF, IndexList = Read_CSV()
    for Index in IndexList:
        Make_ProspinoIn(Index)
        ProspinoResults = Calculate_CrossSection(Index, Data_DF)
        Export_CSV(ProspinoResults)

if __name__ == "__main__":
    main()