#!/usr/bin/env pypy
#####################################
# Usage:                            #
# Manual:                           #
#####################################

import sys

cen1 = sys.argv[1]
cen2 = sys.argv[2]
out = open(sys.argv[3], 'w')
out.write('#chr_1	start1	end1	id1	chr_2	start2	end2	id2	distance\n')

def get_peaks(f):
	peaks = {}
	for line in open(f):
		a=line.split()
		for i in range(3):
			peaks.setdefault(a[3], []).append(a[i])
	return peaks
	
cen1_peaks = get_peaks(cen1)
cen2_peaks = get_peaks(cen2)

for i in cen1_peaks:
	dist = {}
	chro1 = cen1_peaks[i][0]
	cen1 = (int(cen1_peaks[i][1]) + int(cen1_peaks[i][2]))/2
	for j in cen2_peaks:
		chro2 = cen2_peaks[j][0]
		cen2 = (int(cen2_peaks[j][1]) + int(cen2_peaks[j][2]))/2
		if chro2 == chro1:
			dist[j]=abs(cen2-cen1)
	try:
		min_v = min(zip(dist.values(),dist.keys()))
		id_j = min_v[1]
		dis_v = min_v[0]
		out.writelines('\t'.join(cen1_peaks[i])+'\t'+i+'\t'+'\t'.join(cen2_peaks[id_j])+'\t'+id_j+'\t'+str(dis_v)+'\n')
	except: pass

out.close()

################ END ################
#          Created by Aone          #
#     quanyi.zhao@stanford.edu      #
################ END ################