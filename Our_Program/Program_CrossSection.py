
#!/usr/bin/env python3

# 作者: 李霏

# 假设 prospino 程序配置完毕
# 假设 ProspinoIn_{}.txt 已制备好({}是一个表示索引的整型),位于目录 /home/zhd/cs_smodels_test/InputsForProspino/A/ 下, 其中 A 是项目相关的目录名称
import os
import re
import shutil
import pandas as pd

def cross_section(_1st, _2nd, _3rd, _4th, _5th, _6th, _7th, _8th):
    # 选择输出文件 cs13.csv 的部分列索引, 此四列表是否与截面编号一致有待检验
    if _1st != _2nd:
        EWkino = ['c1barc2_pb', 'c1barn2_pb', 'c1barn3_pb', 'c1barn4_pb', 'c1barn5_pb', 
                                            'c1c1bar_pb', 'c1c2bar_pb', 'c1n2_pb', 'c1n3_pb', 'c1n4_pb', 'c1n5_pb', 
                                            'c2barn2_pb', 'c2barn3_pb', 'c2barn4_pb', 'c2barn5_pb', 'c2c2bar_pb', 
                                            'c2n2_pb', 'c2n3_pb', 'c2n4_pb', 'c2n5_pb', 
                                            'n2n2_pb', 'n2n3_pb', 'n2n4_pb', 'n2n5_pb', 
                                            'n3n3_pb', 'n3n4_pb', 'n3n5_pb', 'n4n4_pb', 'n4n5_pb', 'n5n5_pb']
    else:    
        EWkino = []
        
    if _3rd != _4th:
        Smu = ['smulsmul_pb', 'smursmur_pb', 'snmulsnmul_pb', 'smulPsnmul_pb', 'smulNsnmul_pb']
    else:
        Smu = []
        
    if _5th != _6th:
        Se = ['selsel_pb', 'serser_pb', 'snelsnel_pb', 'selPsnel_pb', 'selNsnel_pb']
    else:
        Se = []
    
    if _7th != _8th:
        Stau = ['sta1sta1_pb', 'sta2sta2_pb', 'sta1psta2m_pb', 'sntalsntal_pb', 
                                            'sta1Psntal_pb', 'sta1Nsntal_pb', 'sta2Psntal_pb', 'sta2Nsntal_pb']
    else:
        Stau = []

    Process_list = list(range(_1st, _2nd))+list(range(_3rd, _4th))+list(range(_5th, _6th))+list(range(_7th, _8th))
    for filename in os.listdir(slha_dir):    # 获取文件名, 将一个点的所有过程一次性计算完毕,算完直接求总截面
        if re.match("ProspinoIn_[1-9][0-9]{3,3}.txt", filename):
            Index = int(re.findall("[1-9]", filename)[0])  # 提取索引

        # Process_list = list(range(_1st, _2nd))+list(range(_3rd, _4th))+list(range(_5th, _6th))+list(range(_7th, _8th))
        for process in Process_list:
            run_dir = root_dir + "/cs_smodels_test/cross_section/prospino" + "/Prospino2_{}".format(str(process))        
            shutil.copy(filename, run_dir + '/prospino.in.les_houches')
            command = " ".join([run_dir + "/prospino_2.run", "> a.txt"])      # prospino 运行命令, Key is here!
            
            # 读写结果
            with open(run_dir + '/prospino.dat', 'r') as f:            
                if os.access("{}/prospino_out.csv".format(run_dir), os.F_OK):     
                    lines = f.readlines()     # 读取数据行                    
                    data = [line.split() for line in lines]   
                    data[0].insert(0, '{}'.format(Index))
                    data=[data[0]]
   
                    # 保存为 .csv
                    df = pd.DataFrame(data)              
                    df.to_csv("{}/prospino_out.csv".format(run_dir), mode='a',index=False, header=False)

                if not os.access("{}/prospino_out.csv".format(run_dir), os.F_OK):
                    lines = f.readlines()

                    # 将每行内容分割成列表, 并删除空行
                    data = [line.split() for line in lines]                
                    data = [x for x in data if x !=[]]                
                    
                    # 两行互换, 添加空格                
                    if len(data[0]) > len(data[1]):     # 此判断多余                    
                        data[0], data[1] = data[1], data[0]                
                    data[0].insert(0, 'Index')                
                    data[0].insert(1, 'FSI')   # FSI = final_state_in
                    data[1].insert(0, '{}'.format(Index))
                    
                    # 保存为.csv
                    df = pd.DataFrame(data)                
                    df.to_csv("{}/prospino_out.csv".format(run_dir), mode='w',index=False, header=False)        
        
        
        NLO_list = []
        XS = 0.
        for process in Process_list:            
            run_dir = root_dir + "/cs_smodels_test/cross_section/prospino" + "/Prospino2_{}".format(str(process))
            df = pd.read_csv("{}/prospino_out.csv".format(run_dir))

            # 根据index索引提取截面并将其添加到一个列表中
            df.set_index('Index',inplace=True)
            NLO = df.loc[Index].iloc[-1]
            NLO_list.append(NLO)
        
        # 计算总截面
        for xs in NLO_list:
            XS += xs
        NLO_list.append(XS)
        
        
        data = [[str(Index)] + NLO_list]
        columns=['Index'] + EWkino + Smu + Se + Stau +['XS_pb']
        df = pd.DataFrame(data,columns=columns)
        
        # 生成最终的 cs13.csv 表格
        if os.access("{}/cs13.csv".format(program_dir), os.F_OK):
            df.to_csv("{}/cs13.csv".format(program_dir), sep=',', mode='a', header=False, index=False)
        if not os.access("{}/cs13.csv".format(program_dir), os.F_OK):  
            df.to_csv("{}/cs13.csv".format(program_dir), sep=',', mode='w', header=True, index=False)     


# 将一个点的所有过程一次性计算完毕,算完直接求总截面
if __name__ == '__main__':
    root_dir = "/home/zhd"
    program_dir = root_dir + '/cs_smodels_test'
    slha_dir = root_dir + '/cs_smodels_test/InputsForProspino/A' 
    cross_section(1, 31, 31, 36, 36, 41, 41, 49)  