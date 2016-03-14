#!/usr/bin/env python
###########################################################
# Usage: adapt_trim.py --single/paried_end Reads1|Reads2  #
# Manual: trim RAW reads by CUTADAPT                      #
###########################################################
import sys,os
import getopt
optlist,args = getopt.getopt(sys.argv[1:],'ho:',["single_end","paired_end"])

########## subroutine ##########
# help_message()    print help message for this pipeline
def help_message():
		print '''##########
Usage:  %s     [options*] <Rq.fastq>|<.R2.fastq>
Options:
-h|--help           print this help message
--single_end        single end sequence mapping
--paired_end        paired end sequence mapping
##########''' % sys.argv[0]

#def single end algorithm
def single_end(x):
	read = '%s' % x
	nx = x.rsplit('/',1)[-1].rsplit('.',1)[0]
	out = '-o %s_trimed.gz' % nx
	read_type = '-f fastq'
	adapt = '-a AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC'
	return 'cutadapt %s %s %s %s' % (read_type, adapt, out, read)

#def paired end algorithm
def paired_end(x,y):
	left = '%s' % x
	right = '%s' % y
	nx = x.rsplit('/',1)[-1].rsplit('.',1)[0]
	ny = y.rsplit('/',1)[-1].rsplit('.',1)[0]
	out_l = '-o %s_trimed.gz' % nx
	out_r = '-p %s_trimed.gz' % ny
	read_type = '-f fastq'
	adapt_l = '-a AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC'
	adapt_r = '-A AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT'
	return 'cutadapt %s %s %s %s %s %s %s' % (read_type, adapt_l, adapt_r, out_l, out_r, left, right)

######MAIN#########
for opt,value in optlist:
	if opt in ('-h'):
		help_message()
		sys.exit(0)

	if opt in ('--single_end'):
		cmd = single_end(args[0])
		os.system(cmd)

	if opt in ('--paired_end'):
		cmd = paired_end(args[0],args[1])
		os.system(cmd)
		
################ END ################
#          Created by Aone          #
#       zhaoshuoxp@whu.edu.cn       #
################ END ################