#!/usr/bin/env python
############################################
#Usage: TSS_all_split.py genes_TSS.txt output_file extend(ex:5000)
#get the all genes TSS+-range and split 100 union
############################################
import sys
file1 = sys.argv[1]
output_file = sys.argv[2]
range1 = int(sys.argv[3])
range2 = range1/50
split100 = file(output_file,'w')
for line in open(file1,'r'):
	a = line.split()
	if a[4] == '+':
		for i in range(-50,50):
			split100.writelines(a[0]+'\t'+str(int(a[1]) + i*range2)+'\t'+str(int(a[1]) + (i+1)*range2)+'\t'+a[2]+'\t'+a[3]+'\n')
	if a[4] == '-':
		for i in range(-50,50):
			split100.writelines(a[0]+'\t'+str(int(a[1]) - (i+1)*range2)+'\t'+str(int(a[1]) - i*range2)+'\t'+a[2]+'\t'+a[3]+'\n')
split100.close()
