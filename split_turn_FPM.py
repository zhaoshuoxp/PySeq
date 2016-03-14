#!/usr/bin/env python
#########################################################################
# Usage: split_turn_FPM.py splited_reads_file result_file reads_count   #
# Manual: splited(100) files turn to 100*n matrix                       #
#########################################################################
import sys
result = []
out_file = open(sys.argv[2],'w')
count = float(sys.argv[3])

for line in open(sys.argv[1]):
	a = line.split()
	result.append(float(a[3])/count)
for i in range(0, len(result), 100):
	b = result[i:i+100]
	for i2 in b:
		out_file.writelines(str(i2)+'\t')
	out_file.writelines('\n')
	
out_file.close()

################ END ################
#          Created by Aone          #
#       zhaoshuoxp@whu.edu.cn       #
################ END ################