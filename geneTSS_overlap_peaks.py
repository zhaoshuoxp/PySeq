#!/usr/bin/env pypy
##################################################################################################
# Usage: geneTSS_overlap_peaks.py gene_TSS.txt peak_file(bed) output_file extend(ex:5000(5kb))   #
# Manual: get genelist TSS+-5kb overlapped (at least 1bp) with peaks                             #
##################################################################################################
import sys
gene_file = sys.argv[1]
peak_file = sys.argv[2]
output_file = sys.argv[3]
extend = int(sys.argv[4])

genes = []
for line in open(gene_file,'r'):
	gene = line.split()
	genes.append([gene[0], gene[1], gene[3]])

peaks = []
for line2 in open(peak_file,'r'):
	peak = line2.split()
	peaks.append([peak[0], peak[1], peak[2]])

result=[]
for i in genes:
	for i2 in peaks:
		if i[0] == i2[0]:
			TSS = int(i[1])
			start = TSS-extend
			end = TSS+extend
			v1 = int(i2[1])
			v2 = int(i2[2])
			if v1 <= start <= v2 or v1 <= end <=v2:
				result.append(i[2])
result = set(result)

overlap = open(output_file,'w')
for i3 in result:
	overlap.writelines(i3+'\n')
overlap.close()

################ END ################
#          Created by Aone          #
#       zhaoshuoxp@whu.edu.cn       #
################ END ################