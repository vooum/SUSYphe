import pandas as pd
import sys, os
import subprocess
import shutil 

class package(object):
    def __init__(self
            ,package_name : str
            ,package_dir = None
            ,command = ''):
        self.package_dir = os.path.dirname(__file__)
        #self.package_dir = package_dir
        print(self.package_dir)
        self.run_dir = os.path.join(self.package_dir, "Prospino2")
        print(self.run_dir)

    def Read_CSV(self, slha_dir: str):
        data = pd.read_csv(slha_dir)
        return data

    def Get_ProspinoInput(self
            ,data: pd.DataFrame
            ,IndexList: pd.Series):
        #self.IndexList = self.data["Index"]
        Index = self.IndexList[0]
        self.ProspinoInDir = os.path.join(self.package_dir, "Prospino_Input/ProspinoIn_{}.txt".format(Index))
        print(isinstance(self.ProspinoInDir, str))
        #return(self.IndexList, self.ProspinoInDir)
        return self.ProspinoInDir

    def Exec_Prospino(self, ProspinoInDir: str):
       # print(isinstance(self.ProspinoInDir, str))
       # shutil.copy(ProspinoInDir, "/home/bzy/Our_Program/Prospino2/prospino.in.les_houches")
        shutil.copy(ProspinoInDir, os.path.join(self.run_dir, "prospino.in.les_houches"))
        self.command = os.path.join(self.run_dir, "prospino_2.run")
        run = subprocess.Popen(self.command, shell=True, cwd=self.run_dir, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        run.wait(timeout=None)
        stdout,error=run.communicate(input=None, timeout=None)

    def Find_CS(self):
        print(self.run_dir)
        prospino_out = os.path.join(self.run_dir, "prospino.dat")
        print(prospino_out)
        modefile = open(prospino_out, 'r')
        contents = modefile.readline()
        print(contents)
        last_number = float(contents.split()[-1])
        print("last_number", last_number)
        modefile.close()
        return last_number

    def Write_CS(self):
        cs1 = [self.Find_CS()]
        df = pd.DataFrame(cs1)
        df.to_csv('CrossSection.csv', header=False, index=False)

    def main(self):
        self.slha_dir = os.path.join(self.package_dir, "slhaReaderOutPut.csv")
        self.data = self.Read_CSV(self.slha_dir)
        self.IndexList = self.data["Index"]
        print(self.IndexList)
        self.ProspinoInDir = self.Get_ProspinoInput(self.data, self.IndexList)
        print(type(self.ProspinoInDir))
        #print(isinstance(self.ProspinoInDir, str))
        #self.Make_ProspinoIn(self.ProspinoInDir)
        self.Exec_Prospino(self.ProspinoInDir)
        self.Write_CS()


if __name__ == '__main__':
    package_instance = package(package_name="example_package")
    package_instance.main()
