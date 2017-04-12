#!/usr/bin/env python
#############################################################################################################
# Usage: tophat_cufflinks.py -o output_dir --paired_end/--single_end species(hg19/mm10/dm6) reads1|reads2   #
# Manual: mapping RNAseq reads to ref genome and transcriptome by tophat2 and cufflinks                     #
#############################################################################################################
import sys,os
import getopt
optlist,args = getopt.getopt(sys.argv[1:],'ho:',["help","single_end","paired_end"])

########## subroutine ##########
# help_message()    print help message for this pipeline
def help_message():
			print '''##########
Usage:  %s     [options*] <species> <.fastq>|[<.R1.fastq>|<.R2.fastq>]
Options:
-h|--help           print this help message
-o                  output dir
--single_end        single end sequence mapping
--paired_end        paired end sequence mapping
##########''' % sys.argv[0]

# single_end ()
def single_end(o,t,g,r):
	index = g
	output = '-o %s' % o
	reads = r
	gtf = '--transcriptome-index=%s' % t
	thread = '-p 4'
	return "tophat2 %s %s %s %s %s" % (thread,gtf,output,index,reads)

# paired_end ()
def paired_end(o,t,g,left,right):
	index = g
	left = '%s' % left
	right = '%s' % right
	output = '-o %s' % o
	inner_dist = '-r 100'
	thread = '-p 4'
	gtf = '--transcriptome-index=%s' % t
	return "tophat2 %s %s %s %s %s %s %s" % (inner_dist,thread,gtf,output,index,left,right)

# cufflinks ()
def cufflinks(o,g):
	output = '-o %s' % o
	thread = '-p 4'
	gtf = '-g %s' % g
	labels = '-L %s' % o
	resuce = '-u'
	norm = '--total-hits-norm'
	input_bam = './%s/%s.bam' % (o,o)
	return "cufflinks %s %s %s %s %s %s %s" % (output,thread,gtf,labels,resuce,norm,input_bam)

########## main ##########
###
species = ['hg19','mm10','dm6']
if args[0] in species:
	#pre-built transcriptome index (system env)
	tm_index = '$transcriptome_bowtie2_%s' % args[0]
	#pre-built genome index (system env)
	genome_index = '$bowtie2index_%s' % args[0]
	#pre-built GTF fle (system env)
	gtf = '$gtf_%s' % args[0]
else: 
	print "species must be hg19/mm10/dm6!!!"
output = ''

for opt,value in optlist:
	if opt in ('-h'):
		help_message()
		sys.exit(0)

	if opt in ('-o'):
		output = value

	if opt in ('--single_end'):
		cmd = single_end(output,tm_index,genome_index,args[1])
		os.system(cmd)

	if opt in ('--paired_end'):
		cmd = paired_end(output,tm_index,genome_index,args[1],args[2])
		os.system(cmd)

###
# BAM to SAM (optional)
#cmd = 'samtools view -h ./%s/accepted_hits.bam > ./%s/%s.sam' % (output,output,output)
#os.system(cmd)

###
# rename the BAM file (optional)
os.system('mv ./%s/accepted_hits.bam ./%s/%s.bam' % (output,output,output))

###
# Cufflinks
cmd = cufflinks(output, gtf)
os.system(cmd)

# rename the GTF file (optional)
os.system('mv ./%s/transcripts.gtf ./%s/%s.gtf' % (output,output,output))

################ END ################
#          Created by Aone          #
#       Quanyi.zhao@ucsf.edu        #
################ END ################