####################################################################
#    PROGRAM 1: extract useful data from scanning result table     #
#    BY: Pole                                                      #
#    2023/09/12                                                    #
####################################################################

import re
import pandas as pd
import csv
import shutil
import os

# 打开原始文件，只读取数据
with open('/home/bzy/recPoints.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    indices = [i for i, col in enumerate(header) if col in ['Index', 'N11', 'N12', 'N13', 'N14', 'tanbeta', 'N21', 'N22', 'N23', 'N24', 'N31', 'N32', 'N33', 'N34', 'N41', 'N42','N43', 'N44',  'M2', 'M1', 'U_11', 'U_12', 'U_21', 'U_22', 'V_11', 'V_12', 'V_21', 'V_22', 'Cha_1','Cha_2', 'Chi_1','Chi_2','Chi_3','Chi_4','Se_1','Se_2','Sv_1','V_21','M_1', 'M_2', 'mu']] # 41个
    # 获取第一行的标题，并找出你想要提取的列的索引。你可以使用next函数来读取第一行，并使用列表推导式来筛选出包含Index, CB2 , CB1, CJ2, mh1, tanbeta的列的索引

    # 提取扫描表格里在蒙卡中需要改参数的所有数据
    data = []
    for row in reader:
        data.append([row[i] for i in indices])

# 打开新文件，只写入数据，并指定编码格式为utf-8
with open('extracted.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # 写入标题行
    writer.writerow([header[i] for i in indices])
    # 写入提取的数据
    writer.writerows(data)

# 创建一个新的CSV文件，并写入提取的列的数据。可以使用open函数以写模式打开一个新文件，并创建一个csv.writer对象来写入数据。
# 可以使用writerow方法来写入一行数据，或者使用writerows方法来写入多行数据。
