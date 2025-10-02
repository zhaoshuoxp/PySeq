#!/usr/bin/env python3
#####################################
import os
import argparse

def get_genebed(i,o):
	cmd = 'awk -v OFS="\\t" \'{print $1,$2,$2+1,$5}\' %s > %s ' % (i,o)
	os.system(cmd)
	
def get_loopbed(i,o,r):
	cmd = 'cut -f 1-4,7 %s | awk -v OFS="\\t" \'{print $1,$2-%s,$2+%s,$0"\\n"$3,$4-%s,$4+%s,$0}\' > %s ' % (i,r,r,r,r,o)
	os.system(cmd)
	
def intersect(i,j,o):
	cmd = "intersectBed -a %s -b %s -wao > %s" % (i,j,o)
	os.system(cmd)

def get_assc(i,o):
	cmd = 'awk -v OFS="\\t" \'{if($9!="."){print $4,$5,$6,$7,$8,$10,$12}}\' %s |sort -u > %s' % (i,o)
	os.system(cmd)

def exclude(i,o,r):
	cmd = 'awk -v OFS="\\t" \'{if ($6>=$2-%s && $6<=$2+%s){print $1,$4-%s,$4+%s,$0}else if($6>=$4-%s && $6<=$4+%s){print $1,$2-%s,$2+%s,$0}}\' %s > %s' % (r,r,r,r,r,r,r,r,i,o)
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
	
#MAIN
def main():
	parser = argparse.ArgumentParser(description = "This script uses FitHiC output to sort HiC loops into four groups: P(promoter)-P, P-D(Distal), G(GWAS variants)-P and G-D interactions. All results will be stored in current(./) directoy. ###BEDtools and AWK are required###")
	parser.add_argument("fithic", help = "FitHiC output file")
	parser.add_argument('-s','--snps', help = "snps file in BED format(#chr	start	end	rsid	category)",default = '/home/quanyi/SNP_dataset/CAD_SNP.bed')
	parser.add_argument('-g','--genes', help = "genes file in text format(#chr	tss	strand	transcriptID		gene_symbol)", default = '/home/quanyi/genome/hg19/tables/genes_TSS.txt')
	parser.add_argument('-r','--res',  help = "resolution of FitHiC output (default 5000bp)", default = 5000)
	args = parser.parse_args()
	loops = args.input
	name = loops.rsplit('/',1)[-1].rsplit('.',1)[0]
	loops_bed = name+'.bed'
	loops_gwas = name+'.gwas'
	loops_genes = name+'.genes'
	genes = args.genes
	gwas = args.snps
	res = int(args.res)/2
	
	G = 'G.txt'
	P = 'P.txt'
	G_D = 'G-D.txt'
	G_P = 'G-P.txt'
	P_D = 'P-D.txt'
	P_P = 'P-P.txt'
	P_G = 'P-G.txt'
	name2 = genes.rsplit('/',1)[-1].rsplit('.',1)[0]
	genes_bed = name2+'.bed'

	## loop to gwas	G
	get_loopbed(loops,loops_bed, res)
	intersect(loops_bed, gwas, loops_gwas)
	get_assc(loops_gwas, G)

	## loop to genes P
	get_genebed(genes, genes_bed)
	intersect(loops_bed, genes_bed, loops_genes)
	get_assc(loops_genes, P)

	## gwas to genes G-P
	G_bed = 'G.bed'
	G_side2 = 'G_side2.bed'
	exclude(G, G_bed, res)
	intersect(G_bed, genes_bed, G_side2)
	get_assc_2(G_side2, G_P, G_D)

	## genes to genes P-P
	P_bed = 'P.bed'
	P_side2 = 'P_side2.bed'
	exclude(P, P_bed, res)
	intersect(P_bed, genes_bed, P_side2)

	# remove P-P duplicates
	P_P_tmp = 'P_P.tmp'
	P_D_tmp = 'P_D.tmp'
	get_assc_2(P_side2, P_P_tmp, P_D_tmp)
	re_dup(P_P_tmp, P_P)

	# remove P-G to get P-D
	P_D_tmp_bed = 'P_D.tmp.bed'
	P_D_tmp_gwas = 'P_D.tmp.gwas'
	exclude(P_D_tmp, P_D_tmp_bed, res)
	intersect(P_D_tmp_bed, gwas, P_D_tmp_gwas)
	get_assc_2(P_D_tmp_gwas, P_G, P_D)

	# clean temp files
	os.system('rm %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (G,G_bed,G_side2,P,P_bed,P_side2,genes_bed,loops_bed,loops_gwas,loops_genes,P_P_tmp,P_G,P_D_tmp,P_D_tmp_bed,P_D_tmp_gwas) )
	
if __name__ == '__main__':
	main()

################ END ################
#          Created by Aone          #
#     quanyi.zhao@stanford.edu      #
################ END ################