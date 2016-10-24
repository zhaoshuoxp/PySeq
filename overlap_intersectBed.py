#!/usr/bin/env python
###########################################################################################
# Usage: overlap_intersectBed.py gene_file peakfile(bed) output(label) ratio(ex:0.5)      #
# Manual: get the ratio% of genes overlapped with peaks                                   #
###########################################################################################
import os,sys
genefile = sys.argv[1]
peakfile = sys.argv[2]
output = sys.argv[3]
ratio = sys.argv[4]

def intersect(g,p,o,r):
	genes = '-a %s' % g
	peaks = '-b %s' % p
	ratios = '-f %s' % r
	outputfile = '-u > %s.bed' % o
	os.system('intersectBed %s %s %s %s' % (genes, peaks, ratios, outputfile))
	
intersect(genefile, peakfile, output, ratio)

result_txt = '%s.txt' % output
f = open(result_txt,'w')
bed_result = '%s.bed' % output

for line in open(bed_result,'r'):
	a = line.split('\t')
	f.writelines(a[4]+'\t'+a[5])
f.close()
os.system('rm %s.bed' % output)

################ END ################
#          Created by Aone          #
#       zhaoshuoxp@whu.edu.cn       #
################ END ################