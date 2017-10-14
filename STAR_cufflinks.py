#!/usr/bin/env python
#####################################
# STAR_cufflinks.py -o output_file(label) --paired_end/--single_end species reads1|reads2 #
# Manual: mapping RNAseq reads to reference genome by STAR     
#####################################

import sys,os
import getopt
optlist,args = getopt.getopt(sys.argv[1:],'ho:',["help","single_end","paired_end"])

########## subroutine ##########
# help_message()    print help message for this pipeline
def help_message():
			print '''##########
Usage:  %s [options*]  <index> <Rq.fastq>|<.R2.fastq>
Options:
-h|--help           print this help message
-o                  output file prefix
--single_end        single end sequence mapping
--paired_end        paired end sequence mapping
##########''' % sys.argv[0]
class STAR:
	def __init__(self,i,o):
		self.genome = '--genomeDir %s' % i
		self.output = '--outSAMtype BAM SortedByCoordinate --outFileNamePrefix ./%s/' % o
		self.thread = '--runThreadN 16'
		self.cufflinks = '--outSAMstrandField intronMotif --outFilterIntronMotifs RemoveNoncanonical'
		self.gunzip = '--readFilesCommand gunzip -c'
	# single_end ()
	def single_end(self,r):
		self.fastq = '--readFilesIn %s' % r
		return "STAR %s %s %s %s %s %s" % (self.cufflinks, self.gunzip, self.thread, self.genome, self.fastq, self.output)

	# paired_end ()
	def paired_end(self,left,right):
		self.fastq = '--readFilesIn %s %s' % (left, right)
		return "STAR %s %s %s %s %s %s" % (self.cufflinks, self.gunzip, self.thread, self.genome, self.fastq, self.output)

def cufflinks(o,g):
	output = '-o %s' % o
	thread = '-p 16'
	gtf = '-g %s' % g
	labels = '-L %s' % o
	resuce = '-u'
	norm = '--total-hits-norm'
	input_bam = bam
	return "cufflinks %s %s %s %s %s %s %s" % (output,thread,gtf,labels,resuce,norm,input_bam)
	
########## main ##########
# mapping
###
if __name__ == '__main__':
	
	species = ['hg19','mm10','dm6']
	if args[0] in species:
		#pre-built transcriptome index (system env)
		star_index = '$starindex_%s' % args[0]
		#pre-built genome index (system env)
		bowtie_index = '$bowtie2index_%s' % args[0]
		#pre-built GTF fle (system env)
		gtf = '$gtf_%s' % args[0]
	else: 
		print "species must be hg19/mm10/dm6!!!"
		sys.exit(0)
		
	for opt,value in optlist:
		if opt in ('-h'):
			help_message()
			sys.exit(0)
		
		if opt in ('-o'):
			output = value
			bam = './%s/%s.bam' % (output, output)
			os.system('mkdir %s' % output)
			core = STAR(star_index, output)
			
		if opt in ('--single_end'):
			cmd = core.single_end(args[1])
			os.system(cmd)

		if opt in ('--paired_end'):
			cmd = core.paired_end(args[1],args[2])
			os.system(cmd)
	
	
	os.system('mv ./%s/Aligned.sortedByCoord.out.bam %s' % (output, bam))
	cmd = cufflinks(output, gtf)
	os.system(cmd)

################ END ################
#          Created by Aone          #
#     quanyi.zhao@stanford.edu      #
################ END ################