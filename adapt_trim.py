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
class trim_adapt:
	def __init__(self,x):
		self.left = '%s' % x
		self.nx = x.rsplit('/',1)[-1].rsplit('.',1)[0]
		self.out_l = '-o %s_trimed.gz' % self.nx
		self.read_type = '-f fastq'
		self.kept_len = '-m 20'
		self.adapt_l = '-a AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC'
		self.adapt_r = '-A AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT'
	
	def single_end(self):
		return 'cutadapt %s %s %s %s %s' % (self.read_type, self.kept_len, self.adapt_l, self.out_l, self.left)

	def paired_end(self,y):
		self.right = '%s' % y
		self.ny = y.rsplit('/',1)[-1].rsplit('.',1)[0]
		self.out_r = '-p %s_trimed.gz' % self.ny
		return 'cutadapt %s %s %s %s %s %s %s %s' % (self.read_type, self.kept_len, self.adapt_l, self.adapt_r, self.out_l, self.out_r, self.left, self.right)

######MAIN#########
for opt,value in optlist:
	if opt in ('-h'):
		help_message()
		sys.exit(0)
		
	core = trim_adapt(args[0])
	
	if opt in ('--single_end'):
		cmd = core.single_end()
		os.system(cmd)

	if opt in ('--paired_end'):
		cmd = core.paired_end(args[1])
		os.system(cmd)
		
################ END ################
#          Created by Aone          #
#       Quanyi.Zhao@ucsf.edu        #
################ END ################