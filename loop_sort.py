#!/usr/bin/env python
#####################################
# Usage:  loop_sort.py FitHiC_output SNP_BED GENE.txt(2nd col for TSS)             #
# Manual: Generate P(promoter)-P, P-D(Distal) and G(GWAS variants)-P interactions  #
#####################################

import os,sys
gwas = sys.argv[2]
loops = sys.argv[1]
loops_bed = loops.split('.')[0]+'.bed'
loops_gwas = loops.split('.')[0]+'.gwas'
loops_genes = loops.split('.')[0]+'.genes'
genes = sys.argv[3]
genes_bed = genes.split('.')[0]+'.bed'

G = 'G.txt'
G_bed = 'G.bed'
G_side2 = 'G_side2.bed'
P = 'P.txt'
P_bed = 'P.bed'
P_side2 = 'P_side2.bed'
G_D = 'G-D.txt'
G_P = 'G-P.txt'
P_D = 'P-D.txt'
P_P = 'P-P.txt'
P_G = 'P-G.txt'


def get_genebed(i,o):
	cmd = 'awk -v OFS="\\t" \'{print $1,$2,$2+1,$5}\' %s > %s ' % (i,o)
	os.system(cmd)
	
def get_loopbed(i,o):
	cmd = 'cut -f 1-4,7 %s | awk -v OFS="\\t" \'{print $1,$2-2500,$2+2500,$0"\\n"$3,$4-2500,$4+2500,$0}\' > %s ' % (i,o)
	os.system(cmd)
	
def intersect(i,j,o):
	cmd = "intersectBed -a %s -b %s -wao > %s" % (i,j,o)
	os.system(cmd)

def get_assc(i,o):
	cmd = 'awk -v OFS="\\t" \'{if($9!="."){print $4,$5,$6,$7,$8,$10,$12}}\' %s |sort -u > %s' % (i,o)
	os.system(cmd)

def exclude(i,o):
	cmd = 'awk -v OFS="\\t" \'{if ($6>=$2-2500 && $6<=$2+2500){print $1,$4-2500,$4+2500,$0}else if($6>=$4-2500 && $6<=$4+2500){print $1,$2-2500,$2+2500,$0}}\' %s > %s' % (i,o)
	os.system(cmd)
	
def get_assc_2(i,o1,o2):
	cmd1 = 'awk -v OFS="\\t" \'{if($11!="."){print $4,$5,$6,$7,$8,$9,$10,$12,$14}}\' %s |sort -u > %s' % (i,o1)
	os.system(cmd1)
	cmd2 = 'awk -v OFS="\\t" \'{if($11=="."){print $4,$5,$6,$7,$8,$9,$10}}\' %s |sort -u > %s' % (i,o2)
	os.system(cmd2)

def re_dup(i,o):
	nr = 1
	p1 = {}
	for line in open(i):
		a = line.split()
		p1[nr] = a
		nr+=1
		
	p2 = {}
	for i in p1:
		l1 = p1[i][-4:]
		l1.sort()
		p2.setdefault(''.join(l1), []).append(i)
		
	f = open(o,'w')
	for i in p2:
		if p2[i][0] in p1:
			f.writelines('\t'.join(p1[p2[i][0]])+'\n')
	
## loop to gwas	G
get_loopbed(loops,loops_bed)
intersect(loops_bed, gwas, loops_gwas)
get_assc(loops_gwas, G)

## loop to genes P
get_genebed(genes, genes_bed)
intersect(loops_bed, genes_bed, loops_genes)
get_assc(loops_genes, P)

## gwas to genes G-P
exclude(G, G_bed)
intersect(G_bed, genes_bed, G_side2)
get_assc_2(G_side2, G_P, G_D)

## genes to genes P-P
exclude(P, P_bed)
intersect(P_bed, genes_bed, P_side2)

# remove P-P duplicates
P_P_tmp = 'P_P.tmp'
P_D_tmp = 'P_D.tmp'
get_assc_2(P_side2, P_P_tmp, P_D_tmp)
re_dup(P_P_tmp, P_P)

# remove P-G to get P-D
P_D_tmp_bed = 'P_D.tmp.bed'
P_D_tmp_gwas = 'P_D.tmp.gwas'
exclude(P_D_tmp, P_D_tmp_bed)
intersect(P_D_tmp_bed, gwas, P_D_tmp_gwas)
get_assc_2(P_D_tmp_gwas, P_G, P_D)
	
os.system('rm %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (G,G_bed,G_side2,P,P_bed,P_side2,genes_bed,loops_bed,loops_gwas,loops_genes,P_P_tmp,P_G,P_D_tmp,P_D_tmp_bed,P_D_tmp_gwas) ) 

################ END ################
#          Created by Aone          #
#     quanyi.zhao@stanford.edu      #
################ END ################