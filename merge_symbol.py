#!/usr/bin/env python
##############################################
#Usage merge_symbol.py input_file(gene_exp.diff) output_file
#merge multi values of the same gene symbol
##############################################
import sys
file1=sys.argv[1]
file2=sys.argv[2]
gene1={}
gene2={}
result={}
ff=open(file1,'r')
for line in ff.readlines()[2:]:
    a=line.split('\t')
    gene1.setdefault(a[2],[]).append(a[7])
    gene2.setdefault(a[2],[]).append(a[8])
for i in gene1:
    A=gene1[i]
    x=0.0
    for s in range(len(A)):
        x+=float(A[s])
    result.setdefault(i,[]).append(x)
for i2 in gene2:
     B=gene2[i2]
     y=0.0
     for s2 in range(len(B)):
         y+=float(B[s2])
     result.setdefault(i2,[]).append(y)
f=open(file2,'w')
for i in result:
    f.writelines(i+'\t'+str(result[i][0])+'\t'+str(result[i][1])+'\n')
