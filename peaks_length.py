#!/usr/bin/env python
################################
# Usage peaks_length.py input_peak_file(bed)
# Manual
################################
import sys
input_file = sys.argv[1]
x = 0
for line in open(input_file):
	a = line.split()
	v1 = int(a[1])
	v2 = int(a[2])
	x+ = v2 - v1
print x


######### END #########
# zhaoshuoxp@whu.edu.cn
######### END #########