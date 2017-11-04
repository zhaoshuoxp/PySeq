#!/usr/bin/env python
###############################################################################
# Usage: adapt_trim.py --single_end/paired_end --truseq/nextra Reads1|Reads2  #
# Manual: trim RAW reads by CUTADAPT                					      #
###############################################################################
import sys,os
import getopt
optlist,args = getopt.getopt(sys.argv[1:],'h',["single_end","paired_end","truseq","nextra"])

########## subroutine ##########
# help_message()    print help message for this pipeline
def help_message():
		print '''##########
Usage:  %s [options*] <Rq.fastq>|<.R2.fastq>
Options:
-h|--help           print this help message
--single_end        single end sequence 
--paired_end        paired end sequence 
--truseq			Truseq adapters (default), full sequence
--nextra			Nextra adapters, transposase sequence 
##########''' % sys.argv[0]

#def single end algorithm
class trim_adapt:
	def __init__(self,x,m):
		self.left = '%s' % x
		self.nx = x.rsplit('/',1)[-1].rsplit('.',1)[0]
		self.out_l = '-o %s_trimed.gz' % self.nx
		self.read_type = '-f fastq'
		self.kept_len = '-m 20'
		
		### TruSeq Index:
		if m = 'truseq':
			self.adapt_l = '-a AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC'
			self.adapt_r = '-A AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT'
		### Nextra Index:
		elif m = 'nextra':
			self.adapt_l = '-a CTGTCTCTTATACACATCT'
			self.adapt_r = '-A CTGTCTCTTATACACATCT'
		
	def single_end(self):
		return 'cutadapt %s %s %s %s %s > %s_cutadapt.log' % (self.read_type, self.kept_len, self.adapt_l, self.out_l, self.left, self.nx)

	def paired_end(self,y):
		self.right = '%s' % y
		self.ny = y.rsplit('/',1)[-1].rsplit('.',1)[0]
		self.out_r = '-p %s_trimed.gz' % self.ny
		return 'cutadapt %s %s %s %s %s %s %s %s > %s_cutadapt.log' % (self.read_type, self.kept_len, self.adapt_l, self.adapt_r, self.out_l, self.out_r, self.left, self.right, self.nx)

######MAIN#########
if __name__ == '__main__':
	for opt,value in optlist:
		if opt in ('-h'):
			help_message()
			sys.exit(0)
		
		seq_mod = 'truseq'
		if opt in ('--truseq'):
			core = trim_adapt(args[0], seq_mod)
			
		elif opt in ('--nextra'):
			seq_mod ='nextra'
			core = trim_adapt(args[0], seq_mod)
			
		if opt in ('--single_end'):
			cmd = core.single_end()
			print "cutadapt is running with SE, %s mode!" % seq_mod.capitalize()
			os.system(cmd)

		elif opt in ('--paired_end'):
			cmd = core.paired_end(args[1])
			print "cutadapt is running with PE, %s mode!" % seq_mod.capitalize()
			os.system(cmd)
		
################ END ################
#          Created by Aone          #
#       quanyiz@stanford.edu        #
################ END ################