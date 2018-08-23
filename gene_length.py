#!/usr/bin/env python
#####################################
# Usage: gene_length.py UCSC_refGenes_table.txt output.txt #
# Manual:Get genes average length in KB                    #
#####################################
import sys
import numpy
f_output = open(sys.argv[2],'w')
genes={}
gen_len = {}

for line in open(sys.argv[1]):
	i = line.split()
	name = i[12]
	cdsS = i[9].split(',')[:-1]
	cdsE = i[10].split(',')[:-1]
	length = 0
	for j in range(len(cdsS)):
		length+=int(cdsE[j])-int(cdsS[j])
	genes.setdefault(name,[]).append(length)
	
for i in genes:
	gen_len.setdefault(i,[]).append(str(numpy.mean(genes[i])/1000))
	
for i in genes_k:
	f_output.writelines(i+'\t'+''.join(gen_len[i])+'\n')
	
f_output.close()
################ END ################
#          Created by Aone          #
#     quanyi.zhao@stanford.edu      #
################ END ################