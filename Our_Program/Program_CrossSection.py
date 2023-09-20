import pandas as pd
import sys, os
import subprocess

ROOTPATH = sys.path[0]

def Read_CSV(slha_dir: str):
    '''
    读取 slhaReaderOutPut.csv
    '''
    data = pd.read_csv(slha_dir)
    return(data)

def Get_Index(data: pd.DataFrame):
    '''
    获取索引
    '''
    IndexList = data["Index"]
    return(IndexList)

def Get_ProspinoInput(IndexList: pd.Series):
    '''
    获取 prospino 输入文件的路径
    '''
    Index = IndexList[0]
    ProspinoInDir = os.path.join(ROOTPATH, "Prospino_Input/ProspinoIn_{}.txt".format(Index))
    return(ProspinoInDir)

def Make_ProspinoIn(ProspinoInDir: str):
    '''
    制备 prospino 标准输入谱
    '''
    os.system("cp {} ./Prospino2/prospino.in.les_houches".format(ProspinoInDir))

def Exec_Prospino():
    '''
    运行 prospino
    '''
    os.chdir("./Prospino2")
    command = "./prospino_2.run"
    run = subprocess.Popen(command)



def main():
    slha_dir = './slhaReaderOutPut.csv'
    data = Read_CSV(slha_dir)
    IndexList = Get_Index(data)
    ProspinoInDir = Get_ProspinoInput(IndexList)
    Make_ProspinoIn(ProspinoInDir)
    Exec_Prospino()


if __name__ == '__main__':
    main()