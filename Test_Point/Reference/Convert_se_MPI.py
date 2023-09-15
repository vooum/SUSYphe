#!/usr/bin/env python3
import os,sys,re,shutil
import pandas as pd
import numpy as np

#pwd = os.path.abspath(os.path.dirname(__file__))

def ConvertToInputfile(data, InputDir):
	i = 0
	for index, row in data.iterrows():
		#print('Index:', i, index)
		i+=1
		#print(row.index.values)
		point_data = row
		Template = "les_houches/prospino.in.les_houches"
		#if max(pow(point_data['N11'], 2), pow(point_data['N12'], 2), pow(point_data['N13'], 2), pow(point_data['N14'], 2), pow(point_data['N15'], 2)) == pow(point_data['N15'], 2):
		#   Template = "les_houches/prospino_n1.in.les_houches"
		#if max(pow(point_data['N21'], 2), pow(point_data['N22'], 2), pow(point_data['N23'], 2), pow(point_data['N24'], 2), pow(point_data['N25'], 2)) == pow(point_data['N25'], 2):
		#   Template = "les_houches/prospino_n2.in.les_houches"
		#if max(pow(point_data['N31'], 2), pow(point_data['N32'], 2), pow(point_data['N33'], 2), pow(point_data['N34'], 2), pow(point_data['N35'], 2)) == pow(point_data['N35'], 2):
		#   Template = "les_houches/prospino_n3.in.les_houches"
		#if max(pow(point_data['N41'], 2), pow(point_data['N42'], 2), pow(point_data['N43'], 2), pow(point_data['N44'], 2), pow(point_data['N45'], 2)) == pow(point_data['N45'], 2):
		#   Template = "les_houches/prospino_n4.in.les_houches"
		#if max(pow(point_data['N51'], 2), pow(point_data['N52'], 2), pow(point_data['N53'], 2), pow(point_data['N54'], 2), pow(point_data['N55'], 2)) == pow(point_data['N55'], 2):
		#   Template = "les_houches/prospino_n5.in.les_houches"
		modefile = open(Template,'r')
		contents = modefile.read()
		modefile.close()
		par_names = re.findall('Lian_\w+',contents)
		for name in par_names:
			#print(name)
			par_name = name.lstrip('Lian_')

			point_data['Se1'] = point_data['Se_1']
			point_data['Se2'] = point_data['Se_4']
			point_data['Se3'] = point_data['Se_2']
			point_data['Se4'] = point_data['Se_5']
			point_data['Se5'] = point_data['Se_3']
			point_data['Se6'] = point_data['Se_6']

			# if max(pow(point_data['ZE11'], 2), pow(point_data['ZE12'], 2), pow(point_data['ZE13'], 2), pow(point_data['ZE14'], 2), pow(point_data['ZE15'], 2), pow(point_data['ZE16'], 2)) == pow(point_data['ZE11'], 2):
			# 	point_data['Se1'] = point_data['Se_1']
			# elif max(pow(point_data['ZE21'], 2), pow(point_data['ZE22'], 2), pow(point_data['ZE23'], 2), pow(point_data['ZE24'], 2), pow(point_data['ZE25'], 2), pow(point_data['ZE26'], 2)) == pow(point_data['ZE21'], 2):
			# 	point_data['Se1'] = point_data['Se_2']
			# elif max(pow(point_data['ZE31'], 2), pow(point_data['ZE32'], 2), pow(point_data['ZE33'], 2), pow(point_data['ZE34'], 2), pow(point_data['ZE35'], 2), pow(point_data['ZE36'], 2)) == pow(point_data['ZE31'], 2):
			# 	point_data['Se1'] = point_data['Se_3']
			# elif max(pow(point_data['ZE41'], 2), pow(point_data['ZE42'], 2), pow(point_data['ZE43'], 2), pow(point_data['ZE44'], 2), pow(point_data['ZE45'], 2), pow(point_data['ZE46'], 2)) == pow(point_data['ZE41'], 2):
			# 	point_data['Se1'] = point_data['Se_4']
			# elif max(pow(point_data['ZE51'], 2), pow(point_data['ZE52'], 2), pow(point_data['ZE53'], 2), pow(point_data['ZE54'], 2), pow(point_data['ZE55'], 2), pow(point_data['ZE56'], 2)) == pow(point_data['ZE51'], 2):
			# 	point_data['Se1'] = point_data['Se_5']
			# elif max(pow(point_data['ZE61'], 2), pow(point_data['ZE62'], 2), pow(point_data['ZE63'], 2), pow(point_data['ZE64'], 2), pow(point_data['ZE65'], 2), pow(point_data['ZE66'], 2)) == pow(point_data['ZE61'], 2):
			# 	point_data['Se1'] = point_data['Se_6']

			# if max(pow(point_data['ZE11'], 2), pow(point_data['ZE12'], 2), pow(point_data['ZE13'], 2), pow(point_data['ZE14'], 2), pow(point_data['ZE15'], 2), pow(point_data['ZE16'], 2)) == pow(point_data['ZE12'], 2):
			# 	point_data['Se3'] = point_data['Se_1']
			# elif max(pow(point_data['ZE21'], 2), pow(point_data['ZE22'], 2), pow(point_data['ZE23'], 2), pow(point_data['ZE24'], 2), pow(point_data['ZE25'], 2), pow(point_data['ZE26'], 2)) == pow(point_data['ZE22'], 2):
			# 	point_data['Se3'] = point_data['Se_2']
			# elif max(pow(point_data['ZE31'], 2), pow(point_data['ZE32'], 2), pow(point_data['ZE33'], 2), pow(point_data['ZE34'], 2), pow(point_data['ZE35'], 2), pow(point_data['ZE36'], 2)) == pow(point_data['ZE32'], 2):
			# 	point_data['Se3'] = point_data['Se_3']
			# elif max(pow(point_data['ZE41'], 2), pow(point_data['ZE42'], 2), pow(point_data['ZE43'], 2), pow(point_data['ZE44'], 2), pow(point_data['ZE45'], 2), pow(point_data['ZE46'], 2)) == pow(point_data['ZE42'], 2):
			# 	point_data['Se3'] = point_data['Se_4']
			# elif max(pow(point_data['ZE51'], 2), pow(point_data['ZE52'], 2), pow(point_data['ZE53'], 2), pow(point_data['ZE54'], 2), pow(point_data['ZE55'], 2), pow(point_data['ZE56'], 2)) == pow(point_data['ZE52'], 2):
			# 	point_data['Se3'] = point_data['Se_5']
			# elif max(pow(point_data['ZE61'], 2), pow(point_data['ZE62'], 2), pow(point_data['ZE63'], 2), pow(point_data['ZE64'], 2), pow(point_data['ZE65'], 2), pow(point_data['ZE66'], 2)) == pow(point_data['ZE62'], 2):
			# 	point_data['Se3'] = point_data['Se_6']
			
			# if max(pow(point_data['ZE11'], 2), pow(point_data['ZE12'], 2), pow(point_data['ZE13'], 2), pow(point_data['ZE14'], 2), pow(point_data['ZE15'], 2), pow(point_data['ZE16'], 2)) == pow(point_data['ZE14'], 2):
			# 	point_data['Se2'] = point_data['Se_1']
			# elif max(pow(point_data['ZE21'], 2), pow(point_data['ZE22'], 2), pow(point_data['ZE23'], 2), pow(point_data['ZE24'], 2), pow(point_data['ZE25'], 2), pow(point_data['ZE26'], 2)) == pow(point_data['ZE24'], 2):
			# 	point_data['Se2'] = point_data['Se_2']
			# elif max(pow(point_data['ZE31'], 2), pow(point_data['ZE32'], 2), pow(point_data['ZE33'], 2), pow(point_data['ZE34'], 2), pow(point_data['ZE35'], 2), pow(point_data['ZE36'], 2)) == pow(point_data['ZE34'], 2):
			# 	point_data['Se2'] = point_data['Se_3']
			# elif max(pow(point_data['ZE41'], 2), pow(point_data['ZE42'], 2), pow(point_data['ZE43'], 2), pow(point_data['ZE44'], 2), pow(point_data['ZE45'], 2), pow(point_data['ZE46'], 2)) == pow(point_data['ZE44'], 2):
			# 	point_data['Se2'] = point_data['Se_4']
			# elif max(pow(point_data['ZE51'], 2), pow(point_data['ZE52'], 2), pow(point_data['ZE53'], 2), pow(point_data['ZE54'], 2), pow(point_data['ZE55'], 2), pow(point_data['ZE56'], 2)) == pow(point_data['ZE54'], 2):
			# 	point_data['Se2'] = point_data['Se_5']
			# elif max(pow(point_data['ZE61'], 2), pow(point_data['ZE62'], 2), pow(point_data['ZE63'], 2), pow(point_data['ZE64'], 2), pow(point_data['ZE65'], 2), pow(point_data['ZE66'], 2)) == pow(point_data['ZE64'], 2):
			# 	point_data['Se2'] = point_data['Se_6']

			# if max(pow(point_data['ZE11'], 2), pow(point_data['ZE12'], 2), pow(point_data['ZE13'], 2), pow(point_data['ZE14'], 2), pow(point_data['ZE15'], 2), pow(point_data['ZE16'], 2)) == pow(point_data['ZE15'], 2):
			# 	point_data['Se4'] = point_data['Se_1']
			# elif max(pow(point_data['ZE21'], 2), pow(point_data['ZE22'], 2), pow(point_data['ZE23'], 2), pow(point_data['ZE24'], 2), pow(point_data['ZE25'], 2), pow(point_data['ZE26'], 2)) == pow(point_data['ZE25'], 2):
			# 	point_data['Se4'] = point_data['Se_2']
			# elif max(pow(point_data['ZE31'], 2), pow(point_data['ZE32'], 2), pow(point_data['ZE33'], 2), pow(point_data['ZE34'], 2), pow(point_data['ZE35'], 2), pow(point_data['ZE36'], 2)) == pow(point_data['ZE35'], 2):
			# 	point_data['Se4'] = point_data['Se_3']
			# elif max(pow(point_data['ZE41'], 2), pow(point_data['ZE42'], 2), pow(point_data['ZE43'], 2), pow(point_data['ZE44'], 2), pow(point_data['ZE45'], 2), pow(point_data['ZE46'], 2)) == pow(point_data['ZE45'], 2):
			# 	point_data['Se4'] = point_data['Se_4']
			# elif max(pow(point_data['ZE51'], 2), pow(point_data['ZE52'], 2), pow(point_data['ZE53'], 2), pow(point_data['ZE54'], 2), pow(point_data['ZE55'], 2), pow(point_data['ZE56'], 2)) == pow(point_data['ZE55'], 2):
			# 	point_data['Se4'] = point_data['Se_5']
			# elif max(pow(point_data['ZE61'], 2), pow(point_data['ZE62'], 2), pow(point_data['ZE63'], 2), pow(point_data['ZE64'], 2), pow(point_data['ZE65'], 2), pow(point_data['ZE66'], 2)) == pow(point_data['ZE65'], 2):
			# 	point_data['Se4'] = point_data['Se_6']

			# if max(pow(point_data['ZE11'], 2), pow(point_data['ZE12'], 2), pow(point_data['ZE13'], 2), pow(point_data['ZE14'], 2), pow(point_data['ZE15'], 2), pow(point_data['ZE16'], 2)) in [pow(point_data['ZE13'], 2), pow(point_data['ZE16'], 2)]:
			# 	point_data['Se5'] = point_data['Se_1']
			# 	point_data['STAU11'] = point_data['ZE13']
			# 	point_data['STAU12'] = point_data['ZE16']
			# 	if max(pow(row['ZE21'], 2), pow(row['ZE22'], 2), pow(row['ZE23'], 2), pow(row['ZE24'], 2), pow(row['ZE25'], 2), pow(row['ZE26'], 2)) in [pow(row['ZE23'], 2), pow(row['ZE26'], 2)]:
			# 		point_data['Se6'] = point_data['Se_2']
			# 		point_data['STAU21'] = point_data['ZE23']
			# 		point_data['STAU22'] = point_data['ZE26']
			# 	elif max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) in [pow(row['ZE33'], 2), pow(row['ZE36'], 2)]:
			# 		point_data['Se6'] = point_data['Se_3']
			# 		point_data['STAU21'] = point_data['ZE33']
			# 		point_data['STAU22'] = point_data['ZE36']
			# 	elif max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) in [pow(row['ZE43'], 2), pow(row['ZE46'], 2)]:
			# 		point_data['Se6'] = point_data['Se_4']
			# 		point_data['STAU21'] = point_data['ZE43']
			# 		point_data['STAU22'] = point_data['ZE46']
			# 	elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
			# 		point_data['Se6'] = point_data['Se_5']
			# 		point_data['STAU21'] = point_data['ZE53']
			# 		point_data['STAU22'] = point_data['ZE56']
			# 	elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
			# 		point_data['Se6'] = point_data['Se_6']
			# 		point_data['STAU21'] = point_data['ZE63']
			# 		point_data['STAU22'] = point_data['ZE66']
			# elif max(pow(point_data['ZE21'], 2), pow(point_data['ZE22'], 2), pow(point_data['ZE23'], 2), pow(point_data['ZE24'], 2), pow(point_data['ZE25'], 2), pow(point_data['ZE26'], 2)) in [pow(point_data['ZE23'], 2), pow(point_data['ZE26'], 2)]:
			# 	point_data['Se5'] = point_data['Se_2']
			# 	point_data['STAU11'] = point_data['ZE23']
			# 	point_data['STAU12'] = point_data['ZE26']
			# 	if max(pow(row['ZE31'], 2), pow(row['ZE32'], 2), pow(row['ZE33'], 2), pow(row['ZE34'], 2), pow(row['ZE35'], 2), pow(row['ZE36'], 2)) in [pow(row['ZE33'], 2), pow(row['ZE36'], 2)]:
			# 		point_data['Se6'] = point_data['Se_3']
			# 		point_data['STAU21'] = point_data['ZE33']
			# 		point_data['STAU22'] = point_data['ZE36']
			# 	elif max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) in [pow(row['ZE43'], 2), pow(row['ZE46'], 2)]:
			# 		point_data['Se6'] = point_data['Se_4']
			# 		point_data['STAU21'] = point_data['ZE43']
			# 		point_data['STAU22'] = point_data['ZE46']
			# 	elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
			# 		point_data['Se6'] = point_data['Se_5']
			# 		point_data['STAU21'] = point_data['ZE53']
			# 		point_data['STAU22'] = point_data['ZE56']
			# 	elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
			# 		point_data['Se6'] = point_data['Se_6']
			# 		point_data['STAU21'] = point_data['ZE63']
			# 		point_data['STAU22'] = point_data['ZE66']
			# elif max(pow(point_data['ZE31'], 2), pow(point_data['ZE32'], 2), pow(point_data['ZE33'], 2), pow(point_data['ZE34'], 2), pow(point_data['ZE35'], 2), pow(point_data['ZE36'], 2)) in [pow(point_data['ZE33'], 2), pow(point_data['ZE36'], 2)]:
			# 	point_data['Se5'] = point_data['Se_3']
			# 	point_data['STAU11'] = point_data['ZE33']
			# 	point_data['STAU12'] = point_data['ZE36']
			# 	if max(pow(row['ZE41'], 2), pow(row['ZE42'], 2), pow(row['ZE43'], 2), pow(row['ZE44'], 2), pow(row['ZE45'], 2), pow(row['ZE46'], 2)) in [pow(row['ZE43'], 2), pow(row['ZE46'], 2)]:
			# 		point_data['Se6'] = point_data['Se_4']
			# 		point_data['STAU21'] = point_data['ZE43']
			# 		point_data['STAU22'] = point_data['ZE46']
			# 	elif max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
			# 		point_data['Se6'] = point_data['Se_5']
			# 		point_data['STAU21'] = point_data['ZE53']
			# 		point_data['STAU22'] = point_data['ZE56']
			# 	elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
			# 		point_data['Se6'] = point_data['Se_6']
			# 		point_data['STAU21'] = point_data['ZE63']
			# 		point_data['STAU22'] = point_data['ZE66']
			# elif max(pow(point_data['ZE41'], 2), pow(point_data['ZE42'], 2), pow(point_data['ZE43'], 2), pow(point_data['ZE44'], 2), pow(point_data['ZE45'], 2), pow(point_data['ZE46'], 2)) in [pow(point_data['ZE43'], 2), pow(point_data['ZE46'], 2)]:
			# 	point_data['Se5'] = point_data['Se_4']
			# 	point_data['STAU11'] = point_data['ZE43']
			# 	point_data['STAU12'] = point_data['ZE46']
			# 	if max(pow(row['ZE51'], 2), pow(row['ZE52'], 2), pow(row['ZE53'], 2), pow(row['ZE54'], 2), pow(row['ZE55'], 2), pow(row['ZE56'], 2)) in [pow(row['ZE53'], 2), pow(row['ZE56'], 2)]:
			# 		point_data['Se6'] = point_data['Se_5']
			# 		point_data['STAU21'] = point_data['ZE53']
			# 		point_data['STAU22'] = point_data['ZE56']
			# 	elif max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
			# 		point_data['Se6'] = point_data['Se_6']
			# 		point_data['STAU21'] = point_data['ZE63']
			# 		point_data['STAU22'] = point_data['ZE66']
			# elif max(pow(point_data['ZE51'], 2), pow(point_data['ZE52'], 2), pow(point_data['ZE53'], 2), pow(point_data['ZE54'], 2), pow(point_data['ZE55'], 2), pow(point_data['ZE56'], 2)) in [pow(point_data['ZE53'], 2), pow(point_data['ZE56'], 2)]:
			# 	point_data['Se5'] = point_data['Se_5']
			# 	point_data['STAU11'] = point_data['ZE53']
			# 	point_data['STAU12'] = point_data['ZE56']
			# 	if max(pow(row['ZE61'], 2), pow(row['ZE62'], 2), pow(row['ZE63'], 2), pow(row['ZE64'], 2), pow(row['ZE65'], 2), pow(row['ZE66'], 2)) in [pow(row['ZE63'], 2), pow(row['ZE66'], 2)]:
			# 		point_data['Se6'] = point_data['Se_6']
			# 		point_data['STAU21'] = point_data['ZE63']
			# 		point_data['STAU22'] = point_data['ZE66']
			
			point_data['STAU11'] = point_data['Rsl11']
			point_data['STAU12'] = point_data['Rsl12']
			point_data['STAU21'] = point_data['Rsl21']
			point_data['STAU22'] = point_data['Rsl22']

			point_data['Sv1'] = point_data['Sv_1']
			point_data['Sv2'] = point_data['Sv_2']
			point_data['Sv3'] = point_data['Sv_3']

			# if max(pow(point_data['ZV11'], 2), pow(point_data['ZV12'], 2), pow(point_data['ZV13'], 2)) == pow(point_data['ZV11'], 2):
			# 	point_data['Sv1'] = point_data['Sv_1']
			# 	if max(pow(point_data['ZV21'], 2), pow(point_data['ZV22'], 2), pow(point_data['ZV23'], 2)) == pow(point_data['ZV22'], 2):	
			# 		point_data['Sv2'] = point_data['Sv_2']
			# 		point_data['Sv3'] = point_data['Sv_3']
			# 	else:
			# 		point_data['Sv2'] = point_data['Sv_3']
			# 		point_data['Sv3'] = point_data['Sv_2']
			# elif max(pow(point_data['ZV21'], 2), pow(point_data['ZV22'], 2), pow(point_data['ZV23'], 2)) == pow(point_data['ZV21'], 2):
			# 	point_data['Sv1'] = point_data['Sv_2']
			# 	if max(pow(point_data['ZV11'], 2), pow(point_data['ZV12'], 2), pow(point_data['ZV13'], 2)) == pow(point_data['ZV12'], 2):	
			# 		point_data['Sv2'] = point_data['Sv_1']
			# 		point_data['Sv3'] = point_data['Sv_3']
			# 	else:
			# 		point_data['Sv2'] = point_data['Sv_3']
			# 		point_data['Sv3'] = point_data['Sv_1']
			# elif max(pow(point_data['ZV31'], 2), pow(point_data['ZV32'], 2), pow(point_data['ZV33'], 2)) == pow(point_data['ZV31'], 2):
			# 	point_data['Sv1'] = point_data['Sv_3']
			# 	if max(pow(point_data['ZV11'], 2), pow(point_data['ZV12'], 2), pow(point_data['ZV13'], 2)) == pow(point_data['ZV12'], 2):
			# 		point_data['Sv2'] = point_data['Sv_1']
			# 		point_data['Sv3'] = point_data['Sv_3']
			# 	else:
			# 		point_data['Sv2'] = point_data['Sv_3']
			# 		point_data['Sv3'] = point_data['Sv_1']
				
			subvalue = format(float(point_data[par_name]),'e')
			#print(subvalue)
			contents = re.sub(name, str(subvalue), contents)
		#print(contents)
		written_path = os.path.join(InputDir, 'ProspinoIn_'+str(index)+'.txt')
		input_write = open(written_path,'w')
		input_write.write(contents)
		input_write.close()

if __name__ == '__main__':
	datafile = 'AllInfo.csv'
	path_for_writing = 'InputsForProspino/EWK_SESE'
	#Template = 'prospino.in.les_houches'

	if len(sys.argv) == 2:
		datafile = sys.argv[1]
	elif len(sys.argv) >= 3:
		datafile = sys.argv[1]
		Template = sys.argv[2]

	try:
		os.mkdir(path_for_writing)
	except FileExistsError:
		shutil.rmtree(path_for_writing)
		os.mkdir(path_for_writing)
	#pd.set_option('display.float_format', lambda x: '%.3e' % x)
	data = pd.read_csv(datafile)
	data.index = data.iloc[:,0]
	print(data.loc[:,'Index'].values)
	data = data.loc[data.loc[:,'Index'].values]
	ConvertToInputfile(data, path_for_writing)





