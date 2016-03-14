#!/usr/bin/env python
##############################################################################################
# Usage: ANOVA.py input_file                                                                 #
# Manual: caculate P value (F-test, ANOVA) of two number groups (inputfile column 1 and 2)   #
##############################################################################################
import sys
import numpy as np
from scipy import stats
input_file = sys.argv[1]
list_1 = []
list_2 = []

def main(i):
	for line in open(i):
		a = line.split()
		list_1.append(a[0])
		list_2.append(a[1])
	array_1 = np.array(map(float, list_1))
	array_2 = np.array(map(float, list_2))
	f, p = stats.f_oneway(array_1, array_2) # F test oneway
	return p
	
print main(input_file)

################ END ################
#          Created by Aone          #
#       zhaoshuoxp@whu.edu.cn       #
################ END ################