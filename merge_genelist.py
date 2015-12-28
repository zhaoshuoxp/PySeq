#!/usr/bin/env python
#####################################
#Usage: merge_genelist.py input_file1 input_file2 output_file
#Merge the gene list of TWO sample
#ex:		sample1 sample2
#	gene1	value1	0
#	gene2	0	value2
#####################################
import sys
file1=sys.argv[1]
file2=sys.argv[2]
output_file=sys.argv[3]
result={}
s1={}
s2={}
for line in open(file1,'r'):
	a=line.split()
	result.setdefault(a[0], [])
	s1[a[0]]=a[1]
for line in open(file2,'r'):
	b=line.split()
	result.setdefault(b[0], [])
	s2[b[0]]=b[1]
result_file=open(output_file,'w')
for i in result:
	if i in s1 and i in s2:
		result_file.writelines(i+'\t'+s1[i]+'\t'+s2[i]+'\n')
	if i in s1 and i not in s2:
		result_file.writelines(i+'\t'+s1[i]+'\t'+'0'+'\n')
	if i not in s1 and i in s2:
		result_file.writelines(i+'\t'+'0'+'\t'+s2[i]+'\n')
