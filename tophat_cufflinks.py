#!/usr/bin/python
########################
#
#tophat_mapping.py -o output_dir --paired_end/--single_end $refgtf $bowtie2index reads1 (reads2) 
#
########################
import sys,os
import getopt
optlist,args = getopt.getopt(sys.argv[1:],'ho:',["help","single_end","paired_end"])

########## subroutine ##########
# help_message()    print help message for this pipeline
def help_message():
			print '''##########
Usage:  %s     [options*] <GTF> <index> <.fastq>|[<.R1.fastq>|<.R2.fastq>]
Options:
-h|--help           print this help message
-o                  output dir
--single_end        single end sequence mapping
--paired_end        paired end sequence mapping
##########''' % sys.argv[0]

# single_end ()
def single_end(o,g,x,r):
	index = x
	output = '-o %s' % o
	reads = r
	gtf = '-G %s' % g
	thread = '-p 4'
	return "tophat2 %s %s %s %s %s" % (thread,gtf,output,index,reads)

# paired_end ()
def paired_end(o,g,x,left,right):
	index = x
	left = '%s' % left
	right = '%s' % right
	output = '-o %s' % o
	inner_dist = '-r 100'
	thread = '-p 4'
	gtf = '-G %s' % g
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
# mapping
###
output = ''
for opt,value in optlist:
	if opt in ('-h'):
		help_message()
		sys.exit(0)

	if opt in ('-o'):
		output = value

	if opt in ('--single_end'):
		cmd = single_end(output,args[0],args[1],args[2])
		os.system(cmd)

	if opt in ('--paired_end'):
		cmd = paired_end(output,args[0],args[1],args[2],args[3])
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
cmd = cufflinks(output, args[0])
os.system(cmd)

# rename the GTF file (optional)
os.system('mv ./%s/transcripts.gtf ./%s/%s.gtf' % (output,output,output))
