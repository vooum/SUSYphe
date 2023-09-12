import re, sys, os, math, subprocess, shutil
import numpy as np
sys.path.append(os.path.dirname(__file__))
from mpi4py import MPI
import pandas as pd
import datetime
import time

pwd = os.path.abspath(os.path.dirname(__file__))
#cwd = os.getcwd()
#print(cwd)

def data_filter(MNdata):
    #if '.csv' in MNdata:
    data = pd.read_csv(MNdata)
    #data = data.sort_values(by = 'x2', ascending = True)
    data = data[:]
    #data = data.loc[[12678]]
    return data

def split(whole_data, share_num):
    npdata = whole_data.to_numpy()
    sharenp_list = np.array_split(npdata, share_num)
    cols = whole_data.columns.values
    sharepd_list = [pd.DataFrame(i, columns=cols) for i in sharenp_list]
    print(sharepd_list)
    #parts_length = [len(i) for i in sharepd_list]
    #print(parts_length)
    return sharepd_list

def prospino_in_SMUSMU(prospino_in, SMUSMU_in):
    modefile = open(SMUSMU_in,'r')
    contents = modefile.read()
    modefile.close()
    prospino_in = open(prospino_in,'w')
    prospino_in.write(contents)
    prospino_in.close()

def prospino_in_SESE(prospino_in, SESE_in):
    modefile = open(SESE_in,'r')
    contents = modefile.read()
    modefile.close()
    prospino_in = open(prospino_in,'w')
    prospino_in.write(contents)
    prospino_in.close()

def calc(rank_path, run_path):      
    main_routine = run_path+"/prospino_2.run"
    print(main_routine)
    command = " ".join([main_routine, "> a.txt"])
    print(command)
    run=subprocess.Popen(command, cwd=rank_path, shell=True, close_fds=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    while run.poll() is None:
        infout,inferr=run.communicate()
    
    print("ProspinoErro:",inferr)
    prospino_out = rank_path+"/prospino.dat"
    modefile = open(prospino_out,'r')	
    contents = modefile.readline()
    print(contents)
    result = float(contents.split()[-1])
    modefile.close()
    return result

def sumcs(Index, prospino_path, rank_path, slha_in):
    SMUSMU_in = "{}/EWK_SMUSMU/ProspinoIn_{}.txt".format(slha_in, str(Index))
    SESE_in = "{}/EWK_SESE/ProspinoIn_{}.txt".format(slha_in, str(Index))
    prospino_in = "{}/prospino.in.les_houches".format(rank_path)
    prospino_in_SMUSMU(prospino_in, SMUSMU_in)
    sumcs13 = 0.
    result = [str(Index)]
    for i in range(48):
        n = i + 1
        run_path = "{}/Prospino2_{}".format(prospino_path, str(n))
        if n < 36:
            cs13 = calc(rank_path, run_path)
        else:
            try:
                prospino_in_SESE(prospino_in, SESE_in)
                cs13 = calc(rank_path, run_path)
            except IOError as e:
                print("Unable to copy file. %s" % e)
            except:
                print("Unexpected error:", sys.exc_info())
        result.append(str(cs13))
        sumcs13 += cs13
    result.append(str(sumcs13))
    print(result)
    data = [result]
    df = pd.DataFrame(data,columns=['Index', 'c1barc2_pb', 'c1barn2_pb', 'c1barn3_pb', 'c1barn4_pb', 'c1barn5_pb', 
                                            'c1c1bar_pb', 'c1c2bar_pb', 'c1n2_pb', 'c1n3_pb', 'c1n4_pb', 'c1n5_pb', 
                                            'c2barn2_pb', 'c2barn3_pb', 'c2barn4_pb', 'c2barn5_pb', 'c2c2bar_pb', 
                                            'c2n2_pb', 'c2n3_pb', 'c2n4_pb', 'c2n5_pb', 
                                            'n2n2_pb', 'n2n3_pb', 'n2n4_pb', 'n2n5_pb', 
                                            'n3n3_pb', 'n3n4_pb', 'n3n5_pb', 'n4n4_pb', 'n4n5_pb', 'n5n5_pb', 
                                            'smulsmul_pb', 'smursmur_pb', 'snmulsnmul_pb', 'smulPsnmul_pb', 'smulNsnmul_pb', 
                                            'selsel_pb', 'serser_pb', 'snelsnel_pb', 'selPsnel_pb', 'selNsnel_pb', 
                                            'sta1sta1_pb', 'sta2sta2_pb', 'sta1psta2m_pb', 'sntalsntal_pb', 
                                            'sta1Psntal_pb', 'sta1Nsntal_pb', 'sta2Psntal_pb', 'sta2Nsntal_pb', 
                                            'sumcs13_pb'])
    df['sta1msta2p_pb'] = df['sta1psta2m_pb']
    df['sumcs13_pb'] = np.float64(df['sumcs13_pb']) + np.float64(df['sta1msta2p_pb'])
    if os.access("{}/cs13.csv".format(rank_path), os.F_OK):
        df.to_csv("{}/cs13.csv".format(rank_path), sep=',', mode='a', header=False, index=None)
    if not os.access("{}/cs13.csv".format(rank_path), os.F_OK):
        df.to_csv("{}/cs13.csv".format(rank_path), sep=',', mode='w', header=True, index=None)

def setSmodelsInputfile(smodels_in, spectr):
    modefile = open(spectr,'r')
    contents = modefile.read()
    modefile.close()
    smodels_in = open(smodels_in,'w')
    smodels_in.write(contents)
    smodels_in.close()

def cs_smodels_comm(data, smodels_in, cs_sl1sl1, cs_sl2sl2, cs_sl3sl3, cs_sl4sl4, cs_sl5sl5, cs_sl6sl6, cs_sta1psta2m, cs_sta1msta2p, stau1_stau2,
                            cs_sv1sv1, cs_sl1Psv1, cs_sl1Nsv1, cs_sl2Psv1, cs_sl2Nsv1, cs_sl3Psv1, cs_sl3Nsv1, cs_sl4Psv1, cs_sl4Nsv1, cs_sl5Psv1, cs_sl5Nsv1, cs_sl6Psv1, cs_sl6Nsv1,
                            cs_sv2sv2, cs_sl1Psv2, cs_sl1Nsv2, cs_sl2Psv2, cs_sl2Nsv2, cs_sl3Psv2, cs_sl3Nsv2, cs_sl4Psv2, cs_sl4Nsv2, cs_sl5Psv2, cs_sl5Nsv2, cs_sl6Psv2, cs_sl6Nsv2, 
                            cs_sv3sv3, cs_sl1Psv3, cs_sl1Nsv3, cs_sl2Psv3, cs_sl2Nsv3, cs_sl3Psv3, cs_sl3Nsv3, cs_sl4Psv3, cs_sl4Nsv3, cs_sl5Psv3, cs_sl5Nsv3, cs_sl6Psv3, cs_sl6Nsv3):
    smodels_in =  open(smodels_in, 'a+')
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000024 -1000037")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1barc2_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000024 1000024")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1c1bar_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000024 1000037")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1c2bar_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000037 1000037")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1c2bar_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000011 1000011")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl1sl1) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000013 1000013")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl2sl2) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000015 1000015")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl3sl3) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -2000011 2000011")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl4sl4) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -2000013 2000013")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl5sl5) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -2000015 2000015")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl6sl6) + " SModelS 2.1.1")

    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 %s %s" %('-' + stau1_stau2[0], stau1_stau2[1]))
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sta1psta2m) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 %s %s" %(stau1_stau2[0], '-' + stau1_stau2[1]))
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sta1msta2p) + " SModelS 2.1.1")
    
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000012 1000012")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sv1sv1) + " SModelS 2.1.1")
    if cs_sl1Psv1 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000011 1000012")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl1Psv1) + " SModelS 2.1.1")
    if cs_sl1Nsv1 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000011 -1000012")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl1Nsv1) + " SModelS 2.1.1")
    if cs_sl2Psv1 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000013 1000012")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl2Psv1) + " SModelS 2.1.1")
    if cs_sl2Nsv1 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000013 -1000012")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl2Nsv1) + " SModelS 2.1.1")
    if cs_sl3Psv1 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000015 1000012")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl3Psv1) + " SModelS 2.1.1")
    if cs_sl3Nsv1 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000015 -1000012")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl3Nsv1) + " SModelS 2.1.1")
    if cs_sl4Psv1 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -2000011 1000012")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl4Psv1) + " SModelS 2.1.1")
    if cs_sl4Nsv1 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 2000011 -1000012")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl4Nsv1) + " SModelS 2.1.1")
    if cs_sl5Psv1 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -2000013 1000012")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl5Psv1) + " SModelS 2.1.1")
    if cs_sl5Nsv1 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 2000013 -1000012")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl5Nsv1) + " SModelS 2.1.1")
    if cs_sl6Psv1 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -2000015 1000012")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl6Psv1) + " SModelS 2.1.1")
    if cs_sl6Nsv1 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 2000015 -1000012")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl6Nsv1) + " SModelS 2.1.1")    

    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000014 1000014")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sv2sv2) + " SModelS 2.1.1")
    if cs_sl1Psv2 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000011 1000014")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl1Psv2) + " SModelS 2.1.1")
    if cs_sl1Nsv2 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000011 -1000014")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl1Nsv2) + " SModelS 2.1.1")
    if cs_sl2Psv2 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000013 1000014")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl2Psv2) + " SModelS 2.1.1")
    if cs_sl2Nsv2 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000013 -1000014")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl2Nsv2) + " SModelS 2.1.1")
    if cs_sl3Psv2 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000015 1000014")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl3Psv2) + " SModelS 2.1.1")
    if cs_sl3Nsv2 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000015 -1000014")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl3Nsv2) + " SModelS 2.1.1")
    if cs_sl4Psv2 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -2000011 1000014")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl4Psv2) + " SModelS 2.1.1")
    if cs_sl4Nsv2 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 2000011 -1000014")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl4Nsv2) + " SModelS 2.1.1")
    if cs_sl5Psv2 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -2000013 1000014")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl5Psv2) + " SModelS 2.1.1")
    if cs_sl5Nsv2 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 2000013 -1000014")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl5Nsv2) + " SModelS 2.1.1")
    if cs_sl6Psv2 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -2000015 1000014")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl6Psv2) + " SModelS 2.1.1")
    if cs_sl6Nsv2 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 2000015 -1000014")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl6Nsv2) + " SModelS 2.1.1")
    
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000016 1000016")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sv3sv3) + " SModelS 2.1.1")
    if cs_sl1Psv3 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000011 1000016")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl1Psv3) + " SModelS 2.1.1")
    if cs_sl1Nsv3 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000011 -1000016")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl1Nsv3) + " SModelS 2.1.1")
    if cs_sl2Psv3 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000013 1000016")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl2Psv3) + " SModelS 2.1.1")
    if cs_sl2Nsv3 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000013 -1000016")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl2Nsv3) + " SModelS 2.1.1")
    if cs_sl3Psv3 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000015 1000016")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl3Psv3) + " SModelS 2.1.1")
    if cs_sl3Nsv3 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000015 -1000016")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl3Nsv3) + " SModelS 2.1.1")
    if cs_sl4Psv3 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -2000011 1000016")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl4Psv3) + " SModelS 2.1.1")
    if cs_sl4Nsv3 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 2000011 -1000016")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl4Nsv3) + " SModelS 2.1.1")
    if cs_sl5Psv3 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -2000013 1000016")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl5Psv3) + " SModelS 2.1.1")
    if cs_sl5Nsv3 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 2000013 -1000016")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl5Nsv3) + " SModelS 2.1.1")
    if cs_sl6Psv3 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -2000015 1000016")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl6Psv3) + " SModelS 2.1.1")
    if cs_sl6Nsv3 != -1:
        smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 2000015 -1000016")
        smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(cs_sl6Nsv3) + " SModelS 2.1.1")


def cs_smodels_n1(data, smodels_in):
    smodels_in =  open(smodels_in, 'a+')
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000024 1000023")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1barn2_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000024 1000023")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1n2_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000037 1000023")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2barn2_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000037 1000023")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2n2_pb']) + " SModelS 2.1.1") 
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000023 1000023")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n2n2_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000023 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n2n3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000023 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n2n4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000023 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n2n5_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000024 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1barn3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000024 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1n3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000037 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2barn3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000037 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2n3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000025 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n3n3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000025 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n3n4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000025 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n3n5_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000024 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1barn4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000024 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1n4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000037 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2barn4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000037 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2n4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000035 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n4n4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000035 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n4n5_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000024 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1barn5_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000024 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1n5_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000037 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2barn5_pb']) + " SModelS 2.1.1") 
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000037 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2n5_pb']) + " SModelS 2.1.1")   
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000045 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n5n5_pb']) + " SModelS 2.1.1")  

def cs_smodels_n2(data, smodels_in):
    smodels_in =  open(smodels_in, 'a+')
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000024 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1barn3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000024 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1n3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000037 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2barn3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000037 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2n3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000025 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n3n3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000025 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n3n4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000025 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n3n5_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000024 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1barn4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000024 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1n4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000037 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2barn4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000037 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2n4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000035 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n4n4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000035 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n4n5_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000024 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1barn5_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000024 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1n5_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000037 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2barn5_pb']) + " SModelS 2.1.1") 
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000037 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2n5_pb']) + " SModelS 2.1.1")   
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000045 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n5n5_pb']) + " SModelS 2.1.1")  

def cs_smodels_n3(data, smodels_in):
    smodels_in =  open(smodels_in, 'a+')
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000024 1000023")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1barn2_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000024 1000023")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1n2_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000037 1000023")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2barn2_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000037 1000023")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2n2_pb']) + " SModelS 2.1.1") 
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000023 1000023")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n2n2_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000023 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n2n4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000023 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n2n5_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000024 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1barn4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000024 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1n4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000037 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2barn4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000037 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2n4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000035 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n4n4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000035 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n4n5_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000024 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1barn5_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000024 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1n5_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000037 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2barn5_pb']) + " SModelS 2.1.1") 
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000037 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2n5_pb']) + " SModelS 2.1.1")   
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000045 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n5n5_pb']) + " SModelS 2.1.1")

def cs_smodels_n4(data, smodels_in):
    smodels_in =  open(smodels_in, 'a+')
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000024 1000023")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1barn2_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000024 1000023")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1n2_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000037 1000023")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2barn2_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000037 1000023")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2n2_pb']) + " SModelS 2.1.1") 
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000023 1000023")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n2n2_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000023 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n2n3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000023 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n2n5_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000024 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1barn3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000024 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1n3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000037 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2barn3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000037 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2n3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000025 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n3n3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000025 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n3n5_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000024 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1barn5_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000024 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1n5_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000037 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2barn5_pb']) + " SModelS 2.1.1") 
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000037 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2n5_pb']) + " SModelS 2.1.1")   
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000045 1000045")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n5n5_pb']) + " SModelS 2.1.1")
  
def cs_smodels_n5(data, smodels_in):
    smodels_in =  open(smodels_in, 'a+')
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000024 1000023")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1barn2_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000024 1000023")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1n2_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000037 1000023")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2barn2_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000037 1000023")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2n2_pb']) + " SModelS 2.1.1") 
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000023 1000023")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n2n2_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000023 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n2n3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000023 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n2n4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000024 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1barn3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000024 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1n3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000037 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2barn3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000037 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2n3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000025 1000025")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n3n3_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000025 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n3n4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000024 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1barn4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000024 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c1n4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000037 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2barn4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 -1000037 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['c2n4_pb']) + " SModelS 2.1.1")
    smodels_in.write("\n" + "XSECTION  1.30E+04  2212 2212 2 1000035 1000035")
    smodels_in.write("\n" + "  0  2  0  0  0  0    " + str(data['n4n4_pb']) + " SModelS 2.1.1")

def runSmodelS(rank_path, packagedir):
	main_routine = packagedir+'runSModelS.py'
	command = ' '.join([main_routine, '-p', 'parameters.ini', '-f', 'gnmssm.slha', '-o', '.'])
	run=subprocess.Popen(command, cwd=rank_path, shell=True, close_fds=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
	while run.poll() is None:
		infout,inferr=run.communicate()
	print("SmodelS Error:", inferr)

def after_smodels(Index, rank_path):
	smodels_in = os.path.join(rank_path, 'gnmssm.slha')
	smodels_outputfile = os.path.join(rank_path, 'gnmssm.slha.smodels')
	modefile = open(smodels_outputfile,'r')	
	contents = modefile.readlines()
	modefile.close()
	string = "#Analysis  Sqrts  Cond_Violation  Theory_Value(fb)  Exp_limit(fb)  r  r_expected"
	words= "The highest r value is ="
	n_string = 0
	for line in contents:
		n_string += 1
		if string in line:
			experiment = contents[n_string+1].split()[0]
			Ecm = contents[n_string+1].split()[1]
			SR = contents[n_string+2].split()[-1]
			txnames = re.sub('[:,\n\t]', '', contents[n_string+3])
			txnames = "".join((txnames.strip()).split()[1:])
			break
		else:
			experiment = "no"
			Ecm = "no"
			SR = "no"
			txnames = "no"
	for line in contents:
		if words in line:
			r = line.split()[6]
			break
		else:
			r = "-1.0"
	r_smodels=[[int(Index), r, experiment, Ecm, SR, txnames]]
	print(r_smodels)
	r_smodels = pd.DataFrame(r_smodels,columns=['Index', 'r_smodels', 'experiment', 'Ecm', 'SR', 'txnames'])
	if os.access("{}/r_smodels.csv".format(rank_path), os.F_OK):
		r_smodels.to_csv("{}/r_smodels.csv".format(rank_path), sep=',', mode='a', header=False, index=None)
	if not os.access("{}/r_smodels.csv".format(rank_path), os.F_OK):
		r_smodels.to_csv("{}/r_smodels.csv".format(rank_path), sep=',', mode='w', header=True, index=None)
	
	smodels_inputfile_end=os.path.join(SmodelS_input, 'SPhenoSPC_'+str(Index)+'.slha')
	smodels_outputfile_end = os.path.join(SmodelS_output, 'SPhenoSPC_'+str(Index)+'.smodels')
	try:
		shutil.move(smodels_in, smodels_inputfile_end)
	except:
		pass
	try:
		shutil.move(smodels_outputfile, smodels_outputfile_end)
		
	except:
		pass

def reCal(data, rank, spectr_path, prospino_path, slha_in, SmodelS_package):
	rank_path = pwd+'/work/'+str(rank)+'/'
	print(rank_path)
	smodels_in = os.path.join(rank_path, 'gnmssm.slha')
	ResultsProspino = rank_path+'cs13.csv'
	n = 0
	data.index=data['Index'].astype(int)
	for index, row in data.iterrows():
		n += 1
		print(n)
		Index = int(round(float(index)))
		print('Index:', Index)
		spectr = os.path.join(spectr_path, 'SPhenoSPC_'+str(Index)+'.txt')
		sumcs(Index, prospino_path, rank_path, slha_in)
		cs_data=pd.read_csv(ResultsProspino, index_col="Index")
		cs_data=cs_data.loc[int(Index)]
		setSmodelsInputfile(smodels_in, spectr)

		cs_sv1sv1, cs_sl1Psv1, cs_sl1Nsv1, cs_sl2Psv1, cs_sl2Nsv1, cs_sl3Psv1, cs_sl3Nsv1, cs_sl4Psv1, cs_sl4Nsv1, cs_sl5Psv1, cs_sl5Nsv1, cs_sl6Psv1, cs_sl6Nsv1 = -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
		cs_sv2sv2, cs_sl1Psv2, cs_sl1Nsv2, cs_sl2Psv2, cs_sl2Nsv2, cs_sl3Psv2, cs_sl3Nsv2, cs_sl4Psv2, cs_sl4Nsv2, cs_sl5Psv2, cs_sl5Nsv2, cs_sl6Psv2, cs_sl6Nsv2 = -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
		cs_sv3sv3, cs_sl1Psv3, cs_sl1Nsv3, cs_sl2Psv3, cs_sl2Nsv3, cs_sl3Psv3, cs_sl3Nsv3, cs_sl4Psv3, cs_sl4Nsv3, cs_sl5Psv3, cs_sl5Nsv3, cs_sl6Psv3, cs_sl6Nsv3 = -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1

		if max(pow(row['ZV11'], 2), pow(row['ZV12'], 2), pow(row['ZV13'], 2)) == pow(row['ZV12'], 2):
			cs_sv1sv1 = cs_data['snmulsnmul_pb']
			if max(pow(row['ZE11'], 2), pow(row['ZE12'], 2), pow(row['ZE13'], 2), pow(row['ZE14'], 2), pow(row['ZE15'], 2), pow(row['ZE16'], 2)) == pow(row['ZE12'], 2):
				cs_sl1Psv1 = cs_data['smulPsnmul_pb']
				cs_sl1Nsv1 = cs_data['smulNsnmul_pb']
			if max(pow(row['ZE21'], 2), pow(row['ZE22'], 2), pow(row['ZE23'], 2), pow(row['ZE24'], 2), pow(row['ZE25'], 2), pow(row['ZE26'], 2)) == pow(row['ZE22'], 2):
				cs_sl2Psv1 = cs_data['smulPsnmul_pb']
				cs_sl2Nsv1 = cs_data['smulNsnmul_pb']
			if max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) == pow(row['ZE32'], 2):
				cs_sl3Psv1 = cs_data['smulPsnmul_pb']
				cs_sl3Nsv1 = cs_data['smulNsnmul_pb']
			if max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) == pow(row['ZE42'], 2):
				cs_sl4Psv1 = cs_data['smulPsnmul_pb']
				cs_sl4Nsv1 = cs_data['smulNsnmul_pb']
			if max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) == pow(row['ZE52'], 2):
				cs_sl5Psv1 = cs_data['smulPsnmul_pb']
				cs_sl5Nsv1 = cs_data['smulNsnmul_pb']
			if max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) == pow(row['ZE62'], 2):
				cs_sl6Psv1 = cs_data['smulPsnmul_pb']
				cs_sl6Nsv1 = cs_data['smulNsnmul_pb']
		elif max(pow(row['ZV11'], 2), pow(row['ZV12'], 2), pow(row['ZV13'], 2)) == pow(row['ZV11'], 2):
			cs_sv1sv1 = cs_data['snelsnel_pb'] 
			if max(pow(row['ZE11'], 2), pow(row['ZE12'], 2), pow(row['ZE13'], 2), pow(row['ZE14'], 2), pow(row['ZE15'], 2), pow(row['ZE16'], 2)) == pow(row['ZE11'], 2):
				cs_sl1Psv1 = cs_data['selPsnel_pb']
				cs_sl1Nsv1 = cs_data['selNsnel_pb']
			if max(pow(row['ZE21'], 2), pow(row['ZE22'], 2), pow(row['ZE23'], 2), pow(row['ZE24'], 2), pow(row['ZE25'], 2), pow(row['ZE26'], 2)) == pow(row['ZE21'], 2):
				cs_sl2Psv1 = cs_data['selPsnel_pb']
				cs_sl2Nsv1 = cs_data['selNsnel_pb']
			if max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) == pow(row['ZE31'], 2):
				cs_sl3Psv1 = cs_data['selPsnel_pb']
				cs_sl3Nsv1 = cs_data['selNsnel_pb']
			if max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) == pow(row['ZE41'], 2):
				cs_sl4Psv1 = cs_data['selPsnel_pb']
				cs_sl4Nsv1 = cs_data['selNsnel_pb']
			if max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) == pow(row['ZE51'], 2):
				cs_sl5Psv1 = cs_data['selPsnel_pb']
				cs_sl5Nsv1 = cs_data['selNsnel_pb']
			if max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) == pow(row['ZE61'], 2):
				cs_sl6Psv1 = cs_data['selPsnel_pb']
				cs_sl6Nsv1 = cs_data['selNsnel_pb']
		elif max(pow(row['ZV11'], 2), pow(row['ZV12'], 2), pow(row['ZV13'], 2)) == pow(row['ZV13'], 2):
			cs_sv1sv1 = cs_data['sntalsntal_pb'] 
			if max(pow(row['ZE11'], 2), pow(row['ZE12'], 2), pow(row['ZE13'], 2), pow(row['ZE14'], 2), pow(row['ZE15'], 2), pow(row['ZE16'], 2)) in [pow(row['ZE13'], 2), pow(row['ZE16'], 2)]:
				cs_sl1Psv1 = cs_data['sta1Psntal_pb']
				cs_sl1Nsv1 = cs_data['sta1Nsntal_pb']
				if max(pow(row['ZE21'], 2), pow(row['ZE22'], 2), pow(row['ZE23'], 2), pow(row['ZE24'], 2), pow(row['ZE25'], 2), pow(row['ZE26'], 2)) in [pow(row['ZE23'], 2), pow(row['ZE26'], 2)]:
					cs_sl2Psv1 = cs_data['sta2Psntal_pb']
					cs_sl2Nsv1 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) in [pow(row['ZE33'], 2), pow(row['ZE36'], 2)]:
					cs_sl3Psv1 = cs_data['sta2Psntal_pb']
					cs_sl3Nsv1 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) in [pow(row['ZE43'], 2), pow(row['ZE46'], 2)]:
					cs_sl4Psv1 = cs_data['sta2Psntal_pb']
					cs_sl4Nsv1 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
					cs_sl5Psv1 = cs_data['sta2Psntal_pb']
					cs_sl5Nsv1 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
					cs_sl6Psv1 = cs_data['sta2Psntal_pb']
					cs_sl6Nsv1 = cs_data['sta2Nsntal_pb']
			elif max(pow(row['ZE21'], 2), pow(row['ZE22'], 2), pow(row['ZE23'], 2), pow(row['ZE24'], 2), pow(row['ZE25'], 2), pow(row['ZE26'], 2)) in [pow(row['ZE23'], 2), pow(row['ZE26'], 2)]:
				cs_sl2Psv1 = cs_data['sta1Psntal_pb']
				cs_sl2Nsv1 = cs_data['sta1Nsntal_pb']
				if max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) in [pow(row['ZE33'], 2), pow(row['ZE36'], 2)]:
					cs_sl3Psv1 = cs_data['sta2Psntal_pb']
					cs_sl3Nsv1 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) in [pow(row['ZE43'], 2), pow(row['ZE46'], 2)]:
					cs_sl4Psv1 = cs_data['sta2Psntal_pb']
					cs_sl4Nsv1 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
					cs_sl5Psv1 = cs_data['sta2Psntal_pb']
					cs_sl5Nsv1 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
					cs_sl6Psv1 = cs_data['sta2Psntal_pb']
					cs_sl6Nsv1 = cs_data['sta2Nsntal_pb']
			elif max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) in [pow(row['ZE33'], 2), pow(row['ZE36'], 2)]:
				cs_sl3Psv1 = cs_data['sta1Psntal_pb']
				cs_sl3Nsv1 = cs_data['sta1Nsntal_pb']
				if max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) in [pow(row['ZE43'], 2), pow(row['ZE46'], 2)]:
					cs_sl4Psv1 = cs_data['sta2Psntal_pb']
					cs_sl4Nsv1 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
					cs_sl5Psv1 = cs_data['sta2Psntal_pb']
					cs_sl5Nsv1 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
					cs_sl6Psv1 = cs_data['sta2Psntal_pb']
					cs_sl6Nsv1 = cs_data['sta2Nsntal_pb']
			elif max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) in [pow(row['ZE43'], 2), pow(row['ZE46'], 2)]:
				cs_sl4Psv1 = cs_data['sta1Psntal_pb']
				cs_sl4Nsv1 = cs_data['sta1Nsntal_pb']
				if max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
					cs_sl5Psv1 = cs_data['sta2Psntal_pb']
					cs_sl5Nsv1 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
					cs_sl6Psv1 = cs_data['sta2Psntal_pb']
					cs_sl6Nsv1 = cs_data['sta2Nsntal_pb']
			elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
				cs_sl5Psv1 = cs_data['sta1Psntal_pb']
				cs_sl5Nsv1 = cs_data['sta1Nsntal_pb']
				if max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
					cs_sl6Psv1 = cs_data['sta2Psntal_pb']
					cs_sl6Nsv1 = cs_data['sta2Nsntal_pb']
		
		if max(pow(row['ZV21'], 2), pow(row['ZV22'], 2), pow(row['ZV23'], 2)) == pow(row['ZV22'], 2):
			cs_sv2sv2 = cs_data['snmulsnmul_pb']
			if max(pow(row['ZE11'], 2), pow(row['ZE12'], 2), pow(row['ZE13'], 2), pow(row['ZE14'], 2), pow(row['ZE15'], 2), pow(row['ZE16'], 2)) == pow(row['ZE12'], 2):
				cs_sl1Psv2 = cs_data['smulPsnmul_pb']
				cs_sl1Nsv2 = cs_data['smulNsnmul_pb']
			if max(pow(row['ZE21'], 2), pow(row['ZE22'], 2), pow(row['ZE23'], 2), pow(row['ZE24'], 2), pow(row['ZE25'], 2), pow(row['ZE26'], 2)) == pow(row['ZE22'], 2):
				cs_sl2Psv2 = cs_data['smulPsnmul_pb']
				cs_sl2Nsv2 = cs_data['smulNsnmul_pb']
			if max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) == pow(row['ZE32'], 2):
				cs_sl3Psv2 = cs_data['smulPsnmul_pb']
				cs_sl3Nsv2 = cs_data['smulNsnmul_pb']
			if max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) == pow(row['ZE42'], 2):
				cs_sl4Psv2 = cs_data['smulPsnmul_pb']
				cs_sl4Nsv2 = cs_data['smulNsnmul_pb']
			if max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) == pow(row['ZE52'], 2):
				cs_sl5Psv2 = cs_data['smulPsnmul_pb']
				cs_sl5Nsv2 = cs_data['smulNsnmul_pb']
			if max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) == pow(row['ZE62'], 2):
				cs_sl6Psv2 = cs_data['smulPsnmul_pb']
				cs_sl6Nsv2 = cs_data['smulNsnmul_pb']
		elif max(pow(row['ZV21'], 2), pow(row['ZV22'], 2), pow(row['ZV23'], 2)) == pow(row['ZV21'], 2):
			cs_sv2sv2 = cs_data['snelsnel_pb']
			if max(pow(row['ZE11'], 2), pow(row['ZE12'], 2), pow(row['ZE13'], 2), pow(row['ZE14'], 2), pow(row['ZE15'], 2), pow(row['ZE16'], 2)) == pow(row['ZE11'], 2):
				cs_sl1Psv2 = cs_data['selPsnel_pb']
				cs_sl1Nsv2 = cs_data['selNsnel_pb']
			if max(pow(row['ZE21'], 2), pow(row['ZE22'], 2), pow(row['ZE23'], 2), pow(row['ZE24'], 2), pow(row['ZE25'], 2), pow(row['ZE26'], 2)) == pow(row['ZE21'], 2):
				cs_sl2Psv2 = cs_data['selPsnel_pb']
				cs_sl2Nsv2 = cs_data['selNsnel_pb']
			if max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) == pow(row['ZE31'], 2):
				cs_sl3Psv2 = cs_data['selPsnel_pb']
				cs_sl3Nsv2 = cs_data['selNsnel_pb']
			if max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) == pow(row['ZE41'], 2):
				cs_sl4Psv2 = cs_data['selPsnel_pb']
				cs_sl4Nsv2 = cs_data['selNsnel_pb']
			if max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) == pow(row['ZE51'], 2):
				cs_sl5Psv2 = cs_data['selPsnel_pb']
				cs_sl5Nsv2 = cs_data['selNsnel_pb']
			if max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) == pow(row['ZE61'], 2):
				cs_sl6Psv2 = cs_data['selPsnel_pb']
				cs_sl6Nsv2 = cs_data['selNsnel_pb']
		elif max(pow(row['ZV21'], 2), pow(row['ZV22'], 2), pow(row['ZV23'], 2)) == pow(row['ZV23'], 2):
			cs_sv2sv2 = cs_data['sntalsntal_pb'] 
			if max(pow(row['ZE11'], 2), pow(row['ZE12'], 2), pow(row['ZE13'], 2), pow(row['ZE14'], 2), pow(row['ZE15'], 2), pow(row['ZE16'], 2)) in [pow(row['ZE13'], 2), pow(row['ZE16'], 2)]:
				cs_sl1Psv2 = cs_data['sta1Psntal_pb']
				cs_sl1Nsv2 = cs_data['sta1Nsntal_pb']
				if max(pow(row['ZE21'], 2), pow(row['ZE22'], 2), pow(row['ZE23'], 2), pow(row['ZE24'], 2), pow(row['ZE25'], 2), pow(row['ZE26'], 2)) in [pow(row['ZE23'], 2), pow(row['ZE26'], 2)]:
					cs_sl2Psv2 = cs_data['sta2Psntal_pb']
					cs_sl2Nsv2 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) in [pow(row['ZE33'], 2), pow(row['ZE36'], 2)]:
					cs_sl3Psv2 = cs_data['sta2Psntal_pb']
					cs_sl3Nsv2 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) in [pow(row['ZE43'], 2), pow(row['ZE46'], 2)]:
					cs_sl4Psv2 = cs_data['sta2Psntal_pb']
					cs_sl4Nsv2 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
					cs_sl5Psv2 = cs_data['sta2Psntal_pb']
					cs_sl5Nsv2 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
					cs_sl6Psv2 = cs_data['sta2Psntal_pb']
					cs_sl6Nsv2 = cs_data['sta2Nsntal_pb']
			elif max(pow(row['ZE21'], 2), pow(row['ZE22'], 2), pow(row['ZE23'], 2), pow(row['ZE24'], 2), pow(row['ZE25'], 2), pow(row['ZE26'], 2)) in [pow(row['ZE23'], 2), pow(row['ZE26'], 2)]:
				cs_sl2Psv2 = cs_data['sta1Psntal_pb']
				cs_sl2Nsv2 = cs_data['sta1Nsntal_pb']
				if max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) in [pow(row['ZE33'], 2), pow(row['ZE36'], 2)]:
					cs_sl3Psv2 = cs_data['sta2Psntal_pb']
					cs_sl3Nsv2 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) in [pow(row['ZE43'], 2), pow(row['ZE46'], 2)]:
					cs_sl4Psv2 = cs_data['sta2Psntal_pb']
					cs_sl4Nsv2 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
					cs_sl5Psv2 = cs_data['sta2Psntal_pb']
					cs_sl5Nsv2 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
					cs_sl6Psv2 = cs_data['sta2Psntal_pb']
					cs_sl6Nsv2 = cs_data['sta2Nsntal_pb']
			elif max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) in [pow(row['ZE33'], 2), pow(row['ZE36'], 2)]:
				cs_sl3Psv2 = cs_data['sta1Psntal_pb']
				cs_sl3Nsv2 = cs_data['sta1Nsntal_pb']
				if max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) in [pow(row['ZE43'], 2), pow(row['ZE46'], 2)]:
					cs_sl4Psv2 = cs_data['sta2Psntal_pb']
					cs_sl4Nsv2 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
					cs_sl5Psv2 = cs_data['sta2Psntal_pb']
					cs_sl5Nsv2 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
					cs_sl6Psv2 = cs_data['sta2Psntal_pb']
					cs_sl6Nsv2 = cs_data['sta2Nsntal_pb']
			elif max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) in [pow(row['ZE43'], 2), pow(row['ZE46'], 2)]:
				cs_sl4Psv2 = cs_data['sta1Psntal_pb']
				cs_sl4Nsv2 = cs_data['sta1Nsntal_pb']
				if max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
					cs_sl5Psv2 = cs_data['sta2Psntal_pb']
					cs_sl5Nsv2 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
					cs_sl6Psv2 = cs_data['sta2Psntal_pb']
					cs_sl6Nsv2 = cs_data['sta2Nsntal_pb']
			elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
				cs_sl5Psv2 = cs_data['sta1Psntal_pb']
				cs_sl5Nsv2 = cs_data['sta1Nsntal_pb']
				if max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
					cs_sl6Psv2 = cs_data['sta2Psntal_pb']
					cs_sl6Nsv2 = cs_data['sta2Nsntal_pb']
        
		if max(pow(row['ZV31'], 2), pow(row['ZV32'], 2), pow(row['ZV33'], 2)) == pow(row['ZV32'], 2):
			cs_sv3sv3 = cs_data['snmulsnmul_pb']
			if max(pow(row['ZE11'], 2), pow(row['ZE12'], 2), pow(row['ZE13'], 2), pow(row['ZE14'], 2), pow(row['ZE15'], 2), pow(row['ZE16'], 2)) == pow(row['ZE12'], 2):
				cs_sl1Psv3 = cs_data['smulPsnmul_pb']
				cs_sl1Nsv3 = cs_data['smulNsnmul_pb']
			if max(pow(row['ZE21'], 2), pow(row['ZE22'], 2), pow(row['ZE23'], 2), pow(row['ZE24'], 2), pow(row['ZE25'], 2), pow(row['ZE26'], 2)) == pow(row['ZE22'], 2):
				cs_sl2Psv3 = cs_data['smulPsnmul_pb']
				cs_sl2Nsv3 = cs_data['smulNsnmul_pb']
			if max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) == pow(row['ZE32'], 2):
				cs_sl3Psv3 = cs_data['smulPsnmul_pb']
				cs_sl3Nsv3 = cs_data['smulNsnmul_pb']
			if max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) == pow(row['ZE42'], 2):
				cs_sl4Psv3 = cs_data['smulPsnmul_pb']
				cs_sl4Nsv3 = cs_data['smulNsnmul_pb']
			if max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) == pow(row['ZE52'], 2):
				cs_sl5Psv3 = cs_data['smulPsnmul_pb']
				cs_sl5Nsv3 = cs_data['smulNsnmul_pb']
			if max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) == pow(row['ZE62'], 2):
				cs_sl6Psv3 = cs_data['smulPsnmul_pb']
				cs_sl6Nsv3 = cs_data['smulNsnmul_pb']
		elif max(pow(row['ZV31'], 2), pow(row['ZV32'], 2), pow(row['ZV33'], 2)) == pow(row['ZV31'], 2):
			cs_sv3sv3 = cs_data['snelsnel_pb']
			if max(pow(row['ZE11'], 2), pow(row['ZE12'], 2), pow(row['ZE13'], 2), pow(row['ZE14'], 2), pow(row['ZE15'], 2), pow(row['ZE16'], 2)) == pow(row['ZE11'], 2):
				cs_sl1Psv3 = cs_data['selPsnel_pb']
				cs_sl1Nsv3 = cs_data['selNsnel_pb']
			if max(pow(row['ZE21'], 2), pow(row['ZE22'], 2), pow(row['ZE23'], 2), pow(row['ZE24'], 2), pow(row['ZE25'], 2), pow(row['ZE26'], 2)) == pow(row['ZE21'], 2):
				cs_sl2Psv3 = cs_data['selPsnel_pb']
				cs_sl2Nsv3 = cs_data['selNsnel_pb']
			if max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) == pow(row['ZE31'], 2):
				cs_sl3Psv3 = cs_data['selPsnel_pb']
				cs_sl3Nsv3 = cs_data['selNsnel_pb']
			if max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) == pow(row['ZE41'], 2):
				cs_sl4Psv3 = cs_data['selPsnel_pb']
				cs_sl4Nsv3 = cs_data['selNsnel_pb']
			if max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) == pow(row['ZE51'], 2):
				cs_sl5Psv3 = cs_data['selPsnel_pb']
				cs_sl5Nsv3 = cs_data['selNsnel_pb']
			if max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) == pow(row['ZE61'], 2):
				cs_sl6Psv3 = cs_data['selPsnel_pb']
				cs_sl6Nsv3 = cs_data['selNsnel_pb']
		elif max(pow(row['ZV31'], 2), pow(row['ZV32'], 2), pow(row['ZV33'], 2)) == pow(row['ZV33'], 2):
			cs_sv3sv3 = cs_data['sntalsntal_pb'] 
			if max(pow(row['ZE11'], 2), pow(row['ZE12'], 2), pow(row['ZE13'], 2), pow(row['ZE14'], 2), pow(row['ZE15'], 2), pow(row['ZE16'], 2)) in [pow(row['ZE13'], 2), pow(row['ZE16'], 2)]:
				cs_sl1Psv3 = cs_data['sta1Psntal_pb']
				cs_sl1Nsv3 = cs_data['sta1Nsntal_pb']
				if max(pow(row['ZE21'], 2), pow(row['ZE22'], 2), pow(row['ZE23'], 2), pow(row['ZE24'], 2), pow(row['ZE25'], 2), pow(row['ZE26'], 2)) in [pow(row['ZE23'], 2), pow(row['ZE26'], 2)]:
					cs_sl2Psv3 = cs_data['sta2Psntal_pb']
					cs_sl2Nsv3 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) in [pow(row['ZE33'], 2), pow(row['ZE36'], 2)]:
					cs_sl3Psv3 = cs_data['sta2Psntal_pb']
					cs_sl3Nsv3 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) in [pow(row['ZE43'], 2), pow(row['ZE46'], 2)]:
					cs_sl4Psv3 = cs_data['sta2Psntal_pb']
					cs_sl4Nsv3 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
					cs_sl5Psv3 = cs_data['sta2Psntal_pb']
					cs_sl5Nsv3 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
					cs_sl6Psv3 = cs_data['sta2Psntal_pb']
					cs_sl6Nsv3 = cs_data['sta2Nsntal_pb']
			elif max(pow(row['ZE21'], 2), pow(row['ZE22'], 2), pow(row['ZE23'], 2), pow(row['ZE24'], 2), pow(row['ZE25'], 2), pow(row['ZE26'], 2)) in [pow(row['ZE23'], 2), pow(row['ZE26'], 2)]:
				cs_sl2Psv3 = cs_data['sta1Psntal_pb']
				cs_sl2Nsv3 = cs_data['sta1Nsntal_pb']
				if max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) in [pow(row['ZE33'], 2), pow(row['ZE36'], 2)]:
					cs_sl3Psv3 = cs_data['sta2Psntal_pb']
					cs_sl3Nsv3 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) in [pow(row['ZE43'], 2), pow(row['ZE46'], 2)]:
					cs_sl4Psv3 = cs_data['sta2Psntal_pb']
					cs_sl4Nsv3 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
					cs_sl5Psv3 = cs_data['sta2Psntal_pb']
					cs_sl5Nsv3 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
					cs_sl6Psv3 = cs_data['sta2Psntal_pb']
					cs_sl6Nsv3 = cs_data['sta2Nsntal_pb']
			elif max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) in [pow(row['ZE33'], 2), pow(row['ZE36'], 2)]:
				cs_sl3Psv3 = cs_data['sta1Psntal_pb']
				cs_sl3Nsv3 = cs_data['sta1Nsntal_pb']
				if max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) in [pow(row['ZE43'], 2), pow(row['ZE46'], 2)]:
					cs_sl4Psv3 = cs_data['sta2Psntal_pb']
					cs_sl4Nsv3 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
					cs_sl5Psv3 = cs_data['sta2Psntal_pb']
					cs_sl5Nsv3 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
					cs_sl6Psv3 = cs_data['sta2Psntal_pb']
					cs_sl6Nsv3 = cs_data['sta2Nsntal_pb']
			elif max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) in [pow(row['ZE43'], 2), pow(row['ZE46'], 2)]:
				cs_sl4Psv3 = cs_data['sta1Psntal_pb']
				cs_sl4Nsv3 = cs_data['sta1Nsntal_pb']
				if max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
					cs_sl5Psv3 = cs_data['sta2Psntal_pb']
					cs_sl5Nsv3 = cs_data['sta2Nsntal_pb']
				elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
					cs_sl6Psv3 = cs_data['sta2Psntal_pb']
					cs_sl6Nsv3 = cs_data['sta2Nsntal_pb']
			elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
				cs_sl5Psv3 = cs_data['sta1Psntal_pb']
				cs_sl5Nsv3 = cs_data['sta1Nsntal_pb']
				if max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
					cs_sl6Psv3 = cs_data['sta2Psntal_pb']
					cs_sl6Nsv3 = cs_data['sta2Nsntal_pb']

		sl_stau1 = 0
		cs_sta1psta2m = cs_data['sta1psta2m_pb']
		cs_sta1msta2p = cs_data['sta1msta2p_pb']
		if max(pow(row['ZE11'], 2), pow(row['ZE12'], 2), pow(row['ZE13'], 2), pow(row['ZE14'], 2), pow(row['ZE15'], 2), pow(row['ZE16'], 2)) in [pow(row['ZE13'], 2), pow(row['ZE16'], 2)]:
			sl_stau1 = 1
			cs_sl1sl1 = cs_data['sta1sta1_pb']
			if max(pow(row['ZE21'], 2), pow(row['ZE22'], 2), pow(row['ZE23'], 2), pow(row['ZE24'], 2), pow(row['ZE25'], 2), pow(row['ZE26'], 2)) in [pow(row['ZE23'], 2), pow(row['ZE26'], 2)]:
				cs_sl2sl2 = cs_data['sta2sta2_pb']
				stau1_stau2 = ["1000011", "1000013"]	# (1, 2)
			elif max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) in [pow(row['ZE33'], 2), pow(row['ZE36'], 2)]:
				cs_sl3sl3 = cs_data['sta2sta2_pb']
				stau1_stau2 = ["1000011", "1000015"]	# (1, 3)
			elif max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) in [pow(row['ZE43'], 2), pow(row['ZE46'], 2)]:
				cs_sl4sl4 = cs_data['sta2sta2_pb']
				stau1_stau2 = ["1000011", "2000011"]	# (1, 4)
			elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
				cs_sl5sl5 = cs_data['sta2sta2_pb']
				stau1_stau2 = ["1000011", "2000013"]	# (1, 5)
			elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
				cs_sl6sl6 = cs_data['sta2sta2_pb']
				stau1_stau2 = ["1000011", "2000015"]	# (1, 6)
		# else:
		if max(pow(row['ZE11'], 2), pow(row['ZE12'], 2), pow(row['ZE13'], 2), pow(row['ZE14'], 2), pow(row['ZE15'], 2), pow(row['ZE16'], 2)) == pow(row['ZE12'], 2):
			cs_sl1sl1 = cs_data['smulsmul_pb']
		elif max(pow(row['ZE11'], 2), pow(row['ZE12'], 2), pow(row['ZE13'], 2), pow(row['ZE14'], 2), pow(row['ZE15'], 2), pow(row['ZE16'], 2)) == pow(row['ZE15'], 2):
			cs_sl1sl1 = cs_data['smursmur_pb']
		elif max(pow(row['ZE11'], 2), pow(row['ZE12'], 2), pow(row['ZE13'], 2), pow(row['ZE14'], 2), pow(row['ZE15'], 2), pow(row['ZE16'], 2)) == pow(row['ZE11'], 2):
			cs_sl1sl1 = cs_data['selsel_pb']
		elif max(pow(row['ZE11'], 2), pow(row['ZE12'], 2), pow(row['ZE13'], 2), pow(row['ZE14'], 2), pow(row['ZE15'], 2), pow(row['ZE16'], 2)) == pow(row['ZE14'], 2):
			cs_sl1sl1 = cs_data['serser_pb']
		
		if not sl_stau1:
			if max(pow(row['ZE21'], 2), pow(row['ZE22'], 2), pow(row['ZE23'], 2), pow(row['ZE24'], 2), pow(row['ZE25'], 2), pow(row['ZE26'], 2)) in [pow(row['ZE23'], 2), pow(row['ZE26'], 2)]:
				sl_stau1 = 1
				cs_sl2sl2 = cs_data['sta1sta1_pb']
				if max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) in [pow(row['ZE33'], 2), pow(row['ZE36'], 2)]:
					cs_sl3sl3 = cs_data['sta2sta2_pb']
					stau1_stau2 = ["1000013", "1000015"]   # (2, 3)
				elif max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) in [pow(row['ZE43'], 2), pow(row['ZE46'], 2)]:
					cs_sl4sl4 = cs_data['sta2sta2_pb']
					stau1_stau2 = ["1000013", "2000011"]   # (2, 4)
				elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
					cs_sl5sl5 = cs_data['sta2sta2_pb']
					stau1_stau2 = ["1000013", "2000013"]   # (2, 5)
				elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
					cs_sl6sl6 = cs_data['sta2sta2_pb']
					stau1_stau2 = ["1000013", "2000015"]   # (2, 6)
		# else:
		if max(pow(row['ZE21'], 2), pow(row['ZE22'], 2), pow(row['ZE23'], 2), pow(row['ZE24'], 2), pow(row['ZE25'], 2), pow(row['ZE26'], 2)) == pow(row['ZE22'], 2):
			cs_sl2sl2 = cs_data['smulsmul_pb']
		elif max(pow(row['ZE21'], 2), pow(row['ZE22'], 2), pow(row['ZE23'], 2), pow(row['ZE24'], 2), pow(row['ZE25'], 2), pow(row['ZE26'], 2)) == pow(row['ZE25'], 2):
			cs_sl2sl2 = cs_data['smursmur_pb']
		elif max(pow(row['ZE21'], 2), pow(row['ZE22'], 2), pow(row['ZE23'], 2), pow(row['ZE24'], 2), pow(row['ZE25'], 2), pow(row['ZE26'], 2)) == pow(row['ZE21'], 2):
			cs_sl2sl2 = cs_data['selsel_pb']
		elif max(pow(row['ZE21'], 2), pow(row['ZE22'], 2), pow(row['ZE23'], 2), pow(row['ZE24'], 2), pow(row['ZE25'], 2), pow(row['ZE26'], 2)) == pow(row['ZE24'], 2):
			cs_sl2sl2 = cs_data['serser_pb']

		if not sl_stau1:
			if max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) in [pow(row['ZE33'], 2), pow(row['ZE36'], 2)]:
				sl_stau1 = 1
				cs_sl3sl3 = cs_data['sta1sta1_pb']
				if max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) in [pow(row['ZE43'], 2), pow(row['ZE46'], 2)]:
					cs_sl4sl4 = cs_data['sta2sta2_pb']
					stau1_stau2 = ["1000015", "2000011"]	# (3, 4)
				elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
					cs_sl5sl5 = cs_data['sta2sta2_pb']
					stau1_stau2 = ["1000015", "2000013"]	# (3, 5)
				elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
					cs_sl6sl6 = cs_data['sta2sta2_pb']
					stau1_stau2 = ["1000015", "2000015"]	# (3, 6)
		# else:
		if max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) == pow(row['ZE32'], 2):
			cs_sl3sl3 = cs_data['smulsmul_pb']
		elif max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) == pow(row['ZE35'], 2):
			cs_sl3sl3 = cs_data['smursmur_pb']
		elif max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) == pow(row['ZE31'], 2):
			cs_sl3sl3 = cs_data['selsel_pb']
		elif max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) == pow(row['ZE34'], 2):
			cs_sl3sl3 = cs_data['serser_pb']

		if not sl_stau1:
			if max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) in [pow(row['ZE43'], 2), pow(row['ZE46'], 2)]:
				sl_stau1 = 1
				cs_sl4sl4 = cs_data['sta1sta1_pb']
				if max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
					cs_sl5sl5 = cs_data['sta2sta2_pb']
					stau1_stau2 = ["2000011", "2000013"]	# (4, 5)
				elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
					cs_sl6sl6 = cs_data['sta2sta2_pb']
					stau1_stau2 = ["2000011", "2000015"]	# (4, 6)
		# else:
		if max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) == pow(row['ZE42'], 2):
			cs_sl4sl4 = cs_data['smulsmul_pb']
		elif max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) == pow(row['ZE45'], 2):
			cs_sl4sl4 = cs_data['smursmur_pb']
		elif max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) == pow(row['ZE41'], 2):
			cs_sl4sl4 = cs_data['selsel_pb']
		elif max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) == pow(row['ZE44'], 2):
			cs_sl4sl4 = cs_data['serser_pb']
		
		if not sl_stau1:
			if max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
				sl_stau1 = 1
				cs_sl5sl5 = cs_data['sta1sta1_pb']
				cs_sl6sl6 = cs_data['sta2sta2_pb']
				stau1_stau2 = ["2000013", "2000015"]	(5, 6)
		# else:
		if max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) == pow(row['ZE52'], 2):
			cs_sl5sl5 = cs_data['smulsmul_pb']
		elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) == pow(row['ZE55'], 2):
			cs_sl5sl5 = cs_data['smursmur_pb']
		elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) == pow(row['ZE51'], 2):
			cs_sl5sl5 = cs_data['selsel_pb']
		elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) == pow(row['ZE54'], 2):
			cs_sl5sl5 = cs_data['serser_pb']

		if max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) == pow(row['ZE62'], 2):
			cs_sl6sl6 = cs_data['smulsmul_pb']
		elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) == pow(row['ZE65'], 2):
			cs_sl6sl6 = cs_data['smursmur_pb']
		elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) == pow(row['ZE61'], 2):
			cs_sl6sl6 = cs_data['selsel_pb']
		elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) == pow(row['ZE64'], 2):
			cs_sl6sl6 = cs_data['serser_pb']

		cs_smodels_comm(cs_data, smodels_in, cs_sl1sl1, cs_sl2sl2, cs_sl3sl3, cs_sl4sl4, cs_sl5sl5, cs_sl6sl6, cs_sta1psta2m, cs_sta1msta2p, stau1_stau2,
                            cs_sv1sv1, cs_sl1Psv1, cs_sl1Nsv1, cs_sl2Psv1, cs_sl2Nsv1, cs_sl3Psv1, cs_sl3Nsv1, cs_sl4Psv1, cs_sl4Nsv1, cs_sl5Psv1, cs_sl5Nsv1, cs_sl6Psv1, cs_sl6Nsv1,
                            cs_sv2sv2, cs_sl1Psv2, cs_sl1Nsv2, cs_sl2Psv2, cs_sl2Nsv2, cs_sl3Psv2, cs_sl3Nsv2, cs_sl4Psv2, cs_sl4Nsv2, cs_sl5Psv2, cs_sl5Nsv2, cs_sl6Psv2, cs_sl6Nsv2, 
                            cs_sv3sv3, cs_sl1Psv3, cs_sl1Nsv3, cs_sl2Psv3, cs_sl2Nsv3, cs_sl3Psv3, cs_sl3Nsv3, cs_sl4Psv3, cs_sl4Nsv3, cs_sl5Psv3, cs_sl5Nsv3, cs_sl6Psv3, cs_sl6Nsv3)

		if max(pow(row['N11'], 2), pow(row['N12'], 2), sum([pow(row['N13'], 2), pow(row['N14'], 2)]), pow(row['N15'], 2)) == pow(row['N15'], 2):
			cs_smodels_n1(cs_data, smodels_in)
		elif max(pow(row['N21'], 2), pow(row['N22'], 2), sum([pow(row['N23'], 2), pow(row['N24'], 2)]), pow(row['N25'], 2)) == pow(row['N25'], 2):
			cs_smodels_n2(cs_data, smodels_in)
		elif max(pow(row['N31'], 2), pow(row['N32'], 2), sum([pow(row['N33'], 2), pow(row['N34'], 2)]), pow(row['N35'], 2)) == pow(row['N35'], 2):
			cs_smodels_n3(cs_data, smodels_in)
		elif max(pow(row['N41'], 2), pow(row['N42'], 2), sum([pow(row['N43'], 2), pow(row['N44'], 2)]), pow(row['N45'], 2)) == pow(row['N45'], 2):
			cs_smodels_n4(cs_data, smodels_in)
		elif max(pow(row['N51'], 2), pow(row['N52'], 2), sum([pow(row['N53'], 2), pow(row['N54'], 2)]), pow(row['N55'], 2)) == pow(row['N55'], 2):
			cs_smodels_n5(cs_data, smodels_in)
		runSmodelS(rank_path, SmodelS_package)
		after_smodels(Index, rank_path)


		

if __name__ == '__main__':
	MNdata =  '/home/zhd/cs_smodels_test/slhaReaderOutPut.csv'
	slha_in = '/home/zhd/cs_smodels_test/InputsForProspino'
	spectr_path = '/home/zhd/cs_smodels_test/muonSPhenoSPC/'
	prospino_path = '/home/zhd/cs_smodels_test/cross_section/prospino'
	SmodelS_package = '/home/zhd/cs_smodels_test/smodels-2/'

	SmodelS_input = '/home/zhd/cs_smodels_test/Results/SmodelS_input'
	SmodelS_output = '/home/zhd/cs_smodels_test/Results/SmodelS_output'

	source_prospino = os.path.abspath("{}/Pro2_subroutines".format(prospino_path))
	source_smodelsdata = os.path.abspath("{}/smodels-database".format(SmodelS_package))
	source_smodelsmodel = os.path.abspath("{}/smodels".format(SmodelS_package))
	source_smodelsparam = os.path.abspath("{}/parameters.ini".format(SmodelS_package))
	
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	size = comm.Get_size()
	recv_data = None
	for i in range(size):
		if rank == i:
			if rank == 0:
				try:
					os.mkdir(SmodelS_input)
					os.mkdir(SmodelS_output)
				except FileExistsError:
				#except IOError:
					shutil.rmtree(SmodelS_input)
					os.mkdir(SmodelS_input)
					shutil.rmtree(SmodelS_output)
					os.mkdir(SmodelS_output)
				for j in range(size):
					try:
						os.mkdir("work/{}".format(str(j)))
						target = pwd+'/work/'+str(j)+'/'
						os.system("cp -r {} {}".format(source_prospino, target))
						os.system("cp -r {} {}".format(source_smodelsdata, target))
						os.system("cp -r {} {}".format(source_smodelsmodel, target))
						os.system("cp -r {} {}".format(source_smodelsparam, target))
					except FileExistsError:
					#except IOError:
						shutil.rmtree("work/{}".format(str(j)))
						os.mkdir("work/{}".format(str(j)))
						target = pwd+'/work/'+str(j)+'/'
						os.system("cp -r {} {}".format(source_prospino, target))
						os.system("cp -r {} {}".format(source_smodelsdata, target))
						os.system("cp -r {} {}".format(source_smodelsmodel, target))
						os.system("cp -r {} {}".format(source_smodelsparam, target))
				data_filted = data_filter(MNdata)
				send_data = split(data_filted, size)
				print("process {} scatter data {} to other processes".format(rank, send_data))
			else:
				send_data = None
				print("process {}".format(rank))
			recv_data = comm.scatter(send_data, root=0)
			reCal(recv_data, rank, spectr_path, prospino_path, slha_in, SmodelS_package)
	
	



