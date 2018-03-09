#!/usr/bin/env python
#####################################
# Usage:                            #
# Manual:                           #
#####################################

import sys
file1 = sys.argv[1]
output_file = sys.argv[2]
upstream = int(sys.argv[3])
downstream = int(sys.argv[4])
split100 = open(output_file,'w')

for line in open(file1,'r'):
	a = line.split()
	cen = (int(a[1]) + int(a[2]))/2.0
	interval = (int(a[2]) - int(a[1]))/60.0
	if a[3]=='+':
		start = int(a[1])-upstream
		end = int(a[2])+downstream
		ext_int_up = upstream/20.0
		ext_int_down = downstream/20.0
		for i in range(20):
			split100.writelines(a[0]+'\t'+str(int(start + i*ext_int_up))+'\t'+str(int(start + (i+1)*ext_int_up))+'\t'+str(cen)+'\n')
		for i in range(-30,30):
			split100.writelines(a[0]+'\t'+str(int(cen + i*interval))+'\t'+str(int(cen + (i+1)*interval))+'\t'+str(cen)+'\n')
		for i in range(20):
			split100.writelines(a[0]+'\t'+str(int(end + i*ext_int_down))+'\t'+str(int(end + (i+1)*ext_int_down))+'\t'+str(cen)+'\n')
	elif a[3]=='-':
		start = int(a[2])+upstream
		end = int(a[1])-downstream
		ext_int_up = upstream/20.0
		ext_int_down = downstream/20.0
		for i in range(20):
			split100.writelines(a[0]+'\t'+str(int(start -(i+1)*ext_int_up))+'\t'+str(int(start - i*ext_int_up))+'\t'+str(cen)+'\n')
		for i in range(-30,30):
			split100.writelines(a[0]+'\t'+str(int(cen - (i+1)*interval))+'\t'+str(int(cen - i*interval))+'\t'+str(cen)+'\n')
		for i in range(20):
			split100.writelines(a[0]+'\t'+str(int(end - (i+1)*ext_int_down))+'\t'+str(int(end - i*ext_int_down))+'\t'+str(cen)+'\n')
			
split100.close()


################ END ################
#          Created by Aone          #
#     quanyi.zhao@stanford.edu      #
################ END ################