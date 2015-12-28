#!/usr/bin/env python
##################################
#Usage genelist_overlap_exp.py exp_file genelist output_file
#Overlap TWO genelist,one is expression, the other is genelist
##################################
import sys
file1=sys.argv[1]
file2-sys.argv[2]
item=[]
pool=[]
for line in open(file1,'r'):
        temp=line.split()
        str1=float(temp[1])
        str2=float(temp[2])
        if str1>0.0 or str2>0.0:
            item.append([temp[0],temp[1],temp[2]])
for line2 in open(file2,'r'):
        temp2=line2.split()
        pool.append(temp2[0])
f=open(output_file,'w')
for i in item:
    if i[0] in pool:
        f.writelines(i[0]+'\t'+i[1]+'\t'+i[2]+'\n')