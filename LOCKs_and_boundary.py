#!/usr/bin/env python
###############################################################################
# Usage: LOCKs_and_boundary.py peak_file.bed LOCKs_file boudary_file          #
# Manual: get the LOCKs(>100kb) and boundary region(+_10kb) from a peak file  #
###############################################################################
import sys
file1 = sys.argv[1]
file2 = sys.argv[2]
file3 = sys.argv[3]
LOCKs = open(file2,'w')
boundary = open(file3,'w')

for line in open(file1,'r'):
	a = line.split()
	if ( int(a[2]) - int(a[1]) ) >= 100000:
		LOCKs.writelines(a[0]+'\t'+a[1]+'\t'+a[2]+'\t'+a[3]+'\n')
		boundary.writelines(a[0]+'\t'+str(int(a[1]) - 10000)+'\t'+str(int(a[1]) + 10000)+'\t'+a[3]+'\n')
		boundary.writelines(a[0]+'\t'+str(int(a[2]) - 10000)+'\t'+str(int(a[2]) + 10000)+'\t'+a[3]+'\n')

LOCKs.close()
boundary.close()
################ END ################
#          Created by Aone          #
#       zhaoshuoxp@whu.edu.cn       #
################ END ################