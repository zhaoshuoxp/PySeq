#!/usr/bin/env python3
###############################################################################
# Usage: adapt_trim.py --single_end/paired_end --truseq/nextra Reads1|Reads2  #
# Manual: trim RAW reads by CUTADAPT                					      #
###############################################################################
import sys,os
import getopt
optlist,args = getopt.getopt(sys.argv[1:],'htn',["help","single_end","paired_end","truseq","nextera"])

########## subroutine ##########
# help_message()    print help message for this pipeline
def help_message():
		print(('''##########
Usage:  %s [options*] <Rq.fastq>|<.R2.fastq>
Options:
-h|--help           print this help message
--single_end        single end sequence 
--paired_end        paired end sequence 
--truseq|-t			Truseq adapters, full sequence
--nextera|-n			Nextra adapters, transposase sequence 
##########''' % sys.argv[0]))

#def single end algorithm
class trim_adapt:
	def __init__(self,x,m):
		self.left = '%s' % x
		self.nx = x.rsplit('/',1)[-1].rsplit('.',1)[0]
		self.out_l = '-o %s_trimed.gz' % self.nx
		self.read_type = '-f fastq'
		self.kept_len = '-m 30'
		self.core = '-j 16'
		
		### TruSeq Index:
		if m == 'truseq':
			self.adapt_l = '-a AGATCGGAAGAGC'
			self.adapt_r = '-A AGATCGGAAGAGC'
			self.adapt5_l = '-g GCTCTTCCGATCT'
			self.adapt5_r = '-G GCTCTTCCGATCT'
			
			#CAGTCAACAATCTCGTATGCCGTCTTCTGCTTG 
		### Nextera Index:
		elif m == 'nextera':
			self.adapt_l = '-a CTGTCTCTTATACACATCT'
			self.adapt_r = '-A CTGTCTCTTATACACATCT'
			self.adapt5_l = '-g AGATGTGTATAAGAGACAG'
			self.adapt5_r = '-G AGATGTGTATAAGAGACAG'
		
	def single_end(self):
		return 'cutadapt %s %s %s %s %s %s %s > %s_cutadapt.log' % (self.read_type, self.kept_len, self.core, self.adapt_l, self.adapt5_l, self.out_l, self.left, self.nx)

	def paired_end(self,y):
		self.right = '%s' % y
		self.ny = y.rsplit('/',1)[-1].rsplit('.',1)[0]
		self.out_r = '-p %s_trimed.gz' % self.ny
		return 'cutadapt %s %s %s %s %s %s %s %s %s %s %s > %s_cutadapt.log' % (self.read_type, self.kept_len, self.core, self.adapt_l, self.adapt_r, self.adapt5_l, self.adapt5_r, self.out_l, self.out_r, self.left, self.right, self.nx)

######MAIN#########
if __name__ == '__main__':
	for opt,value in optlist:

		if opt in ('-h','--help'):
			help_message()
			sys.exit(0)
		
		if opt in ('--truseq'):
			seq_mod = 'truseq'
			core = trim_adapt(args[0], seq_mod)
			
		if opt in ('--nextera'):
			seq_mod = 'nextera'
			core = trim_adapt(args[0], seq_mod)
			
	for opt,value in optlist:		
		if opt in ('--single_end'):
			cmd = core.single_end()
			print(("cutadapt is running with SE, %s mode!" % seq_mod.capitalize()))
			os.system(cmd)

		if opt in ('--paired_end'):
			cmd = core.paired_end(args[1])
			print(("cutadapt is running with PE, %s mode!" % seq_mod.capitalize()))
			os.system(cmd)
		
################ END ################
#          Created by Aone          #
#       quanyiz@stanford.edu        #
################ END ################