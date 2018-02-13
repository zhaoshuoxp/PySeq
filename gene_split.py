#!/usr/bin/env python
##########################################################################
# Usage: gene_split.py genelistwithTSS/TES output_file +range(ex:10000)  #
# Manual: get gene bodies +-range and split to 100 segments              #
##########################################################################
import sys
file1 = sys.argv[1]
output_file = sys.argv[2]
extend = int(sys.argv[3])
split100 = open(output_file,'w')

for line in open(file1,'r'):
	a = line.split()
	cen = (int(a[1])+int(a[2]))/2.0
	if a[3] == '+':
		start = int(a[1])
		end = int(a[2])
		range1 = (end-start)/70.0
		ex0 = start-extend
		ex2 = end+extend
		range0 = extend/15.0
		for i in range(15):
			split100.writelines(a[0]+'\t'+str(int(ex0 + i*range0))+'\t'+str(int(ex0 + (i+1)*range0))+'\t'+str(cen)+'\n')
		for i in range(-35,35):
			split100.writelines(a[0]+'\t'+str(int(cen + i*range1))+'\t'+str(int(cen + (i+1)*range1))+'\t'+str(cen)+'\n')
		for i in range(15):
			split100.writelines(a[0]+'\t'+str(int(end + i*range0))+'\t'+str(int(end + (i+1)*range0))+'\t'+str(cen)+'\n')
			
	if a[3] == '-':
		end = int(a[1])
		start = int(a[2])
		range1 = (start-end)/70.0
		ex0 = end-extend
		ex2 = start+extend
		range0 = extend/15.0
		for i in range(15):
			split100.writelines(a[0]+'\t'+str(int(ex2 - (i+1)*range0))+'\t'+str(int(ex2 - i*range0))+'\t'+str(cen)+'\n')
		for i in range(-35,35):
			split100.writelines(a[0]+'\t'+str(int(cen - (i+1)*range1))+'\t'+str(int(cen - i*range1))+'\t'+str(cen)+'\n')
		for i in range(15):
			split100.writelines(a[0]+'\t'+str(int(end - (i+1)*range0))+'\t'+str(int(end - i*range0))+'\t'+str(cen)+'\n')

split100.close()

################ END ################
#          Created by Aone          #
#       zhaoshuoxp@whu.edu.cn       #
################ END ################