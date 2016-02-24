#!/usr/bin/env python
##########################################
#small_medium_LOCKs.py input_peak.bed output_small output_medium
#get the small and medium LOCKs from bed file(ex:H3K9me3)
##########################################
import sys
file1 = sys.argv[1]
ofile1 = sys.argv[2]
ofile2 = sys.argv[3]
small = open(ofile1,'w')
medium = open(ofile2,'w')
for line in open(file1,'r'):
	a = line.split()
	if 50000 <= ( int(a[2]) - int(a[1]) ) <= 100000:
		medium.writelines(line)
	if 50000 >= ( int(a[2]) - int(a[1]) ):
		small.writelines(line)
small.close()
medium.close()