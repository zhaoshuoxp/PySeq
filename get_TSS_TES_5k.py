#!/usr/bin/env python
#########################################################
# Usage: get_TSS_TES_5k.py input_genes.txt(from UCSC)   #
# Manual: input file downloade from UCSC                #
#########################################################
import sys
genes = sys.argv[1]
f1 = open('genes_TSS_5k.bed','w')
f2 = open('genes_TSS_TES.bed','w')
f3 = open('genes_TSS.txt','w')

for line in open(genes):
	a = line.split('\t')
	f2.writelines(a[2]+'\t'+a[4]+'\t'+a[5]+'\t'+a[3]+'\t'+a[1]+'\t'+a[12]+'\n')
	if a[3] == '+':
		v1 = int(a[4])-5000
		v2 = int(a[4])+5000
		f1.writelines(a[2]+'\t'+str(v1)+'\t'+str(v2)+'\t'+a[3]+'\t'+a[1]+'\t'+a[12]+'\n')
		f3.writelines(a[2]+'\t'+a[4]+'\t'+a[3]+'\t'+a[1]+'\t'+a[12]+'\n')
	if a[3] == '-':
		v1 = int(a[5])-5000
		v2 = int(a[5])+5000
		f1.writelines(a[2]+'\t'+str(v1)+'\t'+str(v2)+'\t'+a[3]+'\t'+a[1]+'\t'+a[12]+'\n')
		f3.writelines(a[2]+'\t'+a[5]+'\t'+a[3]+'\t'+a[1]+'\t'+a[12]+'\n')

f1.close()
f2.close()
f3.close()
################ END ################
#          Created by Aone          #
#       zhaoshuoxp@whu.edu.cn       #
################ END ################
