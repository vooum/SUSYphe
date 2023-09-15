#!/usr/bin/env python

import os.path
import re
import sys
import pandas as pd
import csv
from mpi4py import MPI


pwd = os.path.abspath(os.path.dirname(__file__))
path = sys.path[0]

def correct(no):
   data = pd.read_csv("{}/AllInfo.csv".format(path))
   ret = list(data.columns)
   ret[0]='Index'
   data.columns = ret
   Index = data['Index'].loc[no-1]
   name = "SPhenoSPC_" + str(Index)
   def find(Index, words):
      with open("{}/recSPhenoOmgSPC/BP{}.spectr".format(path, str(Index)), 'r') as f2:
          n = 0
          lines = f2.readlines()
          for line in lines:
             n += 1
             if words in line:
               break 
      return n
   ini_words = "Block MODSEL"
   #final_words = "DECAY   2000006"
   ini_n = find(Index, ini_words)
   #final_n = find(Index, final_words)
   with open("{}/recSPhenoOmgSPC/BP{}.spectr".format(path, str(Index)), 'r') as f3:
       lines = f3.readlines()
       with open("{}/correct/SPhenoSPC_{}.txt".format(path, str(Index)), 'w') as f4:
           #for line1 in lines[0:ini_n-1]:
           for line1 in lines[0:ini_n]:
              f4.write(line1)
           f4.write("     3  1   #  NMSSM particle content\n")
           #for line2 in lines[final_n-1:]:
           for line2 in lines[ini_n:]:
              f4.write(line2)


if __name__ == "__main__":
      comm=MPI.COMM_WORLD
      rank=comm.Get_rank()
      ranks=comm.Get_size()
      df = pd.read_csv("{}/AllInfo.csv".format(path),encoding= 'utf-8')
      #index_num = df.index
      #print(index_num)
      # total = a * b
      a = 1
      b = 4
      for i in range(a):
         if rank == i:
           print(rank)
           n = b*(i) + 1
           m = b*(i + 1) + 1
           for no in range(n, m):
              print(no)
              correct(no)
