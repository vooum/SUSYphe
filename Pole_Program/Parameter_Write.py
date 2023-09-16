####################################################################
#    PROGRAM 2: write several groups of input parameters           #
#    BY: Pole                                                      #
#    2023/09/15                                                    #
####################################################################

import pandas as pd
data = pd.read_csv('/home/bzy/test2.csv')
#读取.txt文件，将其内容存储在contents变量中
with open('/home/bzy/Prospino_Input/prospinoIn_1.txt', 'r', encoding='ascii') as f: 
    contents = f.read()
    poles = ['Pole_tanb', 'Pole_m_1', 'Pole_m_2', 'Pole_N23', 'Pole_N22', 'Pole_N21', 'Pole_N24', 'Pole_snuel', 'Pole_N31', 'Pole_N32', 'Pole_N33', 'Pole_N34', 'Pole_sel', 'Pole_ser', 'Pole_lino3', 'Pole_lino1', 'Pole_lino2', 'Pole_N12', 'Pole_N13', 'Pole_N11', 'Pole_N14', 'Pole_gino2', 'Pole_gino1', 'Pole_N41', 'Pole_N43', 'Pole_N42', 'Pole_N44']
    columns = ['tanbeta', 'M1', 'M2', 'N23', 'N22', 'N21', 'N24', 'Sv_1', 'N31', 'N32', 'N33', 'N34', 'Se_1', 'Se_2', 'Chi_4', 'Chi_2', 'Chi_3',  'N12', 'N13', 'N11', 'N14', 'Cha_2', 'Cha_1', 'N41', 'N43', 'N42', 'N44']
   # columns = [‘X’, ‘Y’, ‘Z’]#定义一个列表，存储要选择的三个列的名称
folder = '/home/bzy/Prospino_Input'
#遍历数据框中从第一行开始的每一行，用变量row表示
for index, row in data.iloc[0:].iterrows():
    #print(index, row)
    for pole, column in zip(poles, columns):
        subvalue = str(row[column]) 
        new_contents = contents.replace(pole, subvalue)
        contents = new_contents   
    print("Input:", new_contents)
    new_file = folder + '/prospino_' + str(index) + '.in.les_houches'
    print("new_file", new_file)
    with open(new_file, 'w') as f: 
        f.write(new_contents)
    with open('/home/bzy/Prospino_Input/prospinoIn_1.txt', 'r', encoding='ascii') as f:
        contents = f.read()


