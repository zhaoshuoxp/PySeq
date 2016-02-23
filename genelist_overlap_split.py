#!/usr/bin/env python
#############################
#Usage:genelist_overlap_split.py genelist splited_total_file output_file
#get the split content of special genelist from the total
#############################
import sys
file1=sys.argv[1]
splited=sys.argv[2]
output_filw=sys.argv[3]
candi=[]
for line in open(file1,'r'):
	a=line.split()
	candi.append(a[0])
result=file(output_file,'w')
for line2 in open(splited,'r'):
	b=line2.split()
	for i in candi:
		if i == b[3]:
			result.writelines(line2)