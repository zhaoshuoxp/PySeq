#!/usr/bin/env python
#####################################
# Usage:                            #
# Manual:                           #
#####################################

import sys
file1 = sys.argv[1]
output_file = sys.argv[2]
#extend = int(sys.argv[3])
split100 = open(output_file,'w')

for line in open(file1,'r'):
	a = line.split()
	cen = (int(a[1]) + int(a[2]))/2.0
	#start = int(a[1])-5000
	#end = int(a[2])+5000
	range1 = 100
	#ex0 = start - extend
	#ex2 = end + extend
	#range0 = extend/10.0
	#for i in range(10):
		#split100.writelines(a[0]+'\t'+str(int(ex0 + i*range0))+'\t'+str(int(ex0 + (i+1)*range0))+'\t'+str(cen)+'\n')
	for i in range(-50,50):
		split100.writelines(a[0]+'\t'+str(int(cen + i*range1))+'\t'+str(int(cen + (i+1)*range1))+'\t'+str(cen)+'\n')
	#for i in range(10):
		#split100.writelines(a[0]+'\t'+str(int(end + i*range0))+'\t'+str(int(end + (i+1)*range0))+'\t'+str(cen)+'\n')

split100.close()


################ END ################
#          Created by Aone          #
#     quanyi.zhao@stanford.edu      #
################ END ################