#!/usr/bin/env python3
#####################################

import sys,os
import getopt
optlist,args = getopt.getopt(sys.argv[1:],'hi:p:e:f:', ["help", "extend=", "input=", "pvalue=", "fasta="])

def help_message():
		print('''##########
Usage:  %s -i|--input <cisVar output> -p|--pvalue <pvalue cutoff> -e|extend <extension from SNP> -f|fasta <reference genome fasta file>
This script uses cisVar output to generate two fasta files containing OPEN or CLOSED alleles for motif analysis.
{prefix}_open.fa and {prefix}_closed.fa will be stored in current(./) directoy.
!!!BEDtools and AWK are required!!!
Options:
-h|--help           print this help message
-i|--input			cisVar output <{prefix}.{depth}.final.txt>
-p|--pvalue			p value cutoff (default 0.001)
-e|--extend			extend (bp) from SNP (defualt 50bp)
-f|--fasta			genome fasta file (defualt /home/quanyi/genome/hg19/GRCh37.p13.genome.fa)
##########''' % sys.argv[0])

## DEFAULT CONFIGURATION ##
extend = 50
fasta = '/home/quanyi/genome/hg19/GRCh37.p13.genome.fa'
pvalue = 0.001

################ MAIN #################
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
try:
	for opt,value in optlist:
		if opt in ('-h','--help'):
			help_message()
			os._exit(0)

		if opt in ('-i','--input'):
			input_file = value
			name = input_file.rsplit('/',1)[-1].rsplit('.',1)[0]
			
		if opt in ('-e','--extend'):
			extend = int(value)
			
		if opt in ('-f','--fasta'):
			fasta = value
		
		if opt in ('-p','--pvalue'):
			pvalue = value
	# 
	open_file = open(('%s_open.fa' % name), 'w')
	closed_file = open(('%s_closed.fa' % name), 'w')

	tmp = get_tmp(input_file, pvalue, extend, fasta, name)
	out_files(tmp, open_file, closed_file, extend)

	# clean temp files
	os.system('rm %s' % tmp)
		
except:  
	print("getopt error!")
	help_message()  
	sys.exit(1)	
	
################ END ################
#          Created by Aone          #
#     quanyi.zhao@stanford.edu      #
################ END ################