#!/usr/bin/env python3
#####################################

import os
import argparse

def main():
	parser = argparse.ArgumentParser(description = "This script uses cisVar output to generate two fasta files containing OPEN or CLOSED alleles for motif analysis. {prefix}_open.fa and {prefix}_closed.fa will be stored in current(./) directoy. ###BEDtools and AWK are required###")
	parser.add_argument('cisVar', help = 'cisVar output file {prefix}.{depth}.final.txt')
	parser.add_argument('-f','--fasta', help = 'genome fasta file (default /genome/hg19/GRCh37.p13.genome.fa)', default='/genome/hg19/GRCh37.p13.genome.fa')
	parser.add_argument('-e','--extend', help = "extend (bp) from SNP (default 50)", default = 50, type = int)
	parser.add_argument('-p','--pvalue',  help = "p value cutoff (default 0.001)", default = 0.001, type = float)
	args = parser.parse_args()
	input_file = args.cisVar
	name = input_file.rsplit('/',1)[-1].rsplit('.',1)[0]
	extend = args.extend
	fasta = args.fasta
	pvalue = args.pvalue
	
	open_file = open(('%s_open.fa' % name), 'w')
	closed_file = open(('%s_closed.fa' % name), 'w')

	tmp = get_tmp(input_file, pvalue, extend, fasta, name)
	out_files(tmp, open_file, closed_file, extend)

	# clean temp files
	os.system('rm %s' % tmp)

# prepare files
def get_tmp(i,p,e,f,n):
	p_filtered = '%s.pass' % n
	# filter with P vaule cutoff and genereate BED file with SNP alleles for BEDtools getfasta
	cmd1 = 'awk \'$12<%s\' %s |awk -v OFS="\\t" \'{print $2, $3-%s, $3+%s, $5, $6, $1}\' > %s' % (p, i, e, e, p_filtered)
	os.system(cmd1)
	fa = '%s.fa' % n
	# get fasta sequences in table format by bedtools
	cmd2 = 'bedtools getfasta -fi %s -bed %s -fo %s -tab' % (f, p_filtered, fa)
	os.system(cmd2)
	tmp = '%s.tmp' % n
	# combine fasta sequences and SNP alleles 
	cmd3 = 'paste %s %s>%s' % (fa, p_filtered, tmp)
	os.system(cmd3)
	# remove tmps
	os.system('rm %s %s' % (p_filtered, fa))
	return tmp

# flip SNP alleles
def sub(string,p,c):
		new = []
		for s in string:
			new.append(s)
		new[p] = c
		return ''.join(new)

# wirte files
def out_files(i,o1,o2,e):
	for line in open(i):
		a = line.split()
		seq = a[1]
		open_a = a[5]
		close_a = a[6]
		idx = a[7]
		pos = e-1
		# write open alleles
		seq_open = sub(seq, pos, open_a)
		o1.writelines(">"+a[0]+'_'+idx+'\n'+seq_open+'\n')
		# write closed alleles
		seq_close = sub(seq, pos, close_a)
		o2.writelines(">"+a[0]+'_'+idx+'\n'+seq_close+'\n')
	o1.close()
	o2.close()
	
#MIAN
if __name__ == '__main__':
	main()
	
################ END ################
#          Created by Aone          #
#     quanyi.zhao@stanford.edu      #
################ END ################