#!/usr/bin/env python
#####################################
# Usage:  peaks_split.py	 input.bed output.bed extend_size                          #
# Manual: split peaks to 100 segments, -extend size, center of peaks, +extend size #
#####################################

import sys
file1 = sys.argv[1]
output_file = sys.argv[2]
extend = int(sys.argv[3])
split100 = open(output_file,'w')

for line in open(file1,'r'):
	a = line.split()
	cen = (int(a[1]) + int(a[2]))/2.0
	interval = extend/50
	for i in range(-50,50):
		split100.writelines(a[0]+'\t'+str(int(cen + i*interval))+'\t'+str(int(cen + (i+1)*interval))+'\t'+str(cen)+'\n')

split100.close()

################ END ################
#          Created by Aone          #
#     quanyi.zhao@stanford.edu      #
################ END ################