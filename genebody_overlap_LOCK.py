#!/usr/bin/env pypy
#####################################
#Usage: gene_overlap_peak.py gene_TSS_TES.bed peak_file(bed) output_file overlap_ratio(eg:0.5)
#Ratio: gene overlap with peak/gene TES-TSS %
#####################################
import sys
gene_file = sys.argv[1]
peak_file = sys.argv[2]
output_file = sys.argv[3]
ratio = float(sys.argv[4])

genes = []
for line in open(gene_file,'r'):
	gene = line.split()
	genes.append([gene[0], gene[1], gene[2], gene[4]])

peaks = []
for line2 in open(peak_file,'r'):
	peak = line2.split()
	peaks.append([peak[0], peak[1], peak[2]])

result=[]
for i in genes:
	v3 = int(i[1])
	v4 = int(i[2])
	for i2 in peaks:
		v1 = int(i2[1])
		v2 = int(i2[2])
		if i[0] == i2[0]:
			if v3 <= v1 <= v4 <= v2:	
				if float(v4 - v1)/(v4 - v3) >= ratio:	
					result.append(i[3])
			elif v1 <= v3 <= v4 <= v2:		
				result.append(i[3])			
			elif v3 <= v1 <= v2 <= v4:
				if float(v2 - v1)/(v4 - v3) >= ratio:		
					result.append(i[3])
			elif v1 <= v3 <= v2 <= v4:
				if float(v2 - v3)/(v4 - v3) >= ratio:
					result.append(i[3])

overlap = open(output_file,'w')
for i3 in result:
	overlap.writelines(i3+'\n')
overlap.close()