#!/usr/bin/env pypy
############################################
#Usage: peak_split.py peaks.bed output_file +range(ex:10000)
#get the all peaks+-range and split 100 pieces
############################################
import sys
file1 = sys.argv[1]
output_file = sys.argv[2]
extend = int(sys.argv[3])
split100 = file(output_file,'w')

for line in open(file1,'r'):
	a = line.split()
	cen = (int(a[1]) + int(a[2]))/2.0
	start = int(a[1])
	end = int(a[2])
	range1 = (end - start)/80.0
	ex0 = start - extend
	ex2 = end + extend
	range0 = extend/10.0
	for i in range(10):
		split100.writelines(a[0]+'\t'+str(int(ex0 + i*range0))+'\t'+str(int(ex0 + (i+1)*range0))+'\t'+str(cen)+'\n')
	for i in range(-40,40):
		split100.writelines(a[0]+'\t'+str(int(cen + i*range1))+'\t'+str(int(cen + (i+1)*range1))+'\t'+str(cen)+'\n')
	for i in range(10):
		split100.writelines(a[0]+'\t'+str(int(end + i*range0))+'\t'+str(int(end + (i+1)*range0))+'\t'+str(cen)+'\n')