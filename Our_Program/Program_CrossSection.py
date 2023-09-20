import pandas as pd
import sys, os
import subprocess

#sys.path是一个列表，它存储了Python搜索模块的路径集。sys.path[0]是这个列表的第一项, 就是调用python解释器的脚本所在的目录，即就是存放需要运行的代码的路径
ROOTPATH = sys.path[0]

def Read_CSV(slha_dir: str):
    '''
    读取 slhaReaderOutPut.csv
    '''
    data = pd.read_csv(slha_dir)
    return(data)

def Get_ProspinoInput(data: pd.DataFrame, IndexList: pd.Series):
    IndexList = data["Index"]
    Index = IndexList[0]
    ProspinoInDir = os.path.join(ROOTPATH, "Prospino_Input/ProspinoIn_{}.txt".format(Index))
#{}是用来表示字符串格式化的占位符，它可以用format()方法来替换为指定的值。
    return(IndexList, ProspinoInDir)
    


def Make_ProspinoIn(ProspinoInDir: str):
    '''
    制备 prospino 标准输入谱
    '''
    os.system("cp {} ./Prospino2/prospino.in.les_houches".format(ProspinoInDir))


    '''
    运行 prospino
    '''
def Exec_Prospino():
    os.chdir("./Prospino2")
    command = "./prospino_2.run"
    run = subprocess.Popen(command)

def Find_CS(path):
    prospino_out = path+"/prospino.dat"
    modefile = open(prospino_out, 'r')
    contents = modefile.readline()
    print(contents)
    last_number = float(contents.split()[-1])
    print("last_number", last_number)
    modefile.close()
    return last_number

def Write_CS():
    path = os.path.join(ROOTPATH, "Prospino2")
    cs1 = [Find_CS(path)]
    df = pd.DataFrame(cs1)
    df.to_csv('CrossSection.csv', header=False, index=False)#将数据框写入




def main():
    slha_dir = './slhaReaderOutPut.csv'
   # path = os.path.join(ROOTPATH, "Prospino2")
    data = Read_CSV(slha_dir)
    IndexList = data["Index"]
    print(IndexList)
    ProspinoInDir = Get_ProspinoInput(data, IndexList)
    Make_ProspinoIn(ProspinoInDir)
    Exec_Prospino()
    Write_CS()


if __name__ == '__main__':
    main()
    
