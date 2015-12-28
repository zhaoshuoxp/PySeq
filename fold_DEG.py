#!/usr/bin/env python
#############################
#Usage: fold_DEG.py input_file output_file fold backgroud
#############################
import sys
input_file=sys.argv[1]
output_file=sys.argv[2]
f=open(output_file,'w')
fold=float(sys.argv[3])
backgroud=sys.argv[4]
value=float(backgroud)
for line in open(input_file,'r'):
    temp=line.split('\t')
    v1=float(temp[1])+value
    v2=float(temp[2])+value
    if v1/v2>=fold or v1/v2<=(1/fold):
        f.writelines(line)
