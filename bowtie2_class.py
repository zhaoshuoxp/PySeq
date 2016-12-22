#!/usr/bin/env python
#######################################################################################################
# Usage: bowtie2_class.py -o output_file(label) --paired_end/--single_end $bowtie2index reads1|reads2 #
# Manual: mapping ChIPseq reads to reference genome by BOWTIE2 CLASS                                  #
#######################################################################################################
import sys,os
import getopt
optlist,args = getopt.getopt(sys.argv[1:],'ho:',["help","single_end","paired_end"])

#define mapping Flags
###
class bowtie:
	def __init__(self,x,o):
		self.index = '-x ' + x
		self.output = '-S %s' % o
		self.mapping_input = '-q --phred33'
		self.mapping_alignment = '--end-to-end --sensitive'
		self.mapping_report = '-k 1 --no-unal'
		self.mapping_thread = '-p 4'
	
	# single end
	def single(self,reads):
		self.fastq = '-U ' + reads
		return "bowtie2 %s %s %s %s %s %s %s" % (self.mapping_input,self.mapping_alignment,self.mapping_report,self.mapping_thread,self.index,self.fastq,self.output)
	
	# paired end
	def paried(self,left,right):
		self.left = '-1 %s' % left
		self.right = '-2 %s' % right
		self.mapping_ruler = '--fr --no-mixed --no-discordant'
		self.mapping_insert = '-X 1000'
		return "bowtie2 %s %s %s %s %s %s %s %s %s %s" % (self.mapping_input,self.mapping_alignment,self.mapping_report,self.mapping_thread,self.mapping_ruler,self.mapping_insert,self.index,self.left,self.right,self.output)

# mapping
###
class mapping:
	def __init__(self):
		pass				
	# help_message()    print help message for this pipeline
	def help_message():
		print '''##########
Usage:  bowtie2_class.py [options*] <index> <Rq.fastq>|<.R2.fastq>
Options:
-h|--help           print this help message
-o                  output file prefix
--single_end        single end sequence mapping
--paired_end        paired end sequence mapping
##########'''
		sys.exit(0)		
		
	# generate Class bowtie
	def output(self):
		return bowtie(args[0], sam)
	
	# single end mapping	
	def single(self):
		cmd = core.single(args[1])
		os.system(cmd)
		return '-s'
		
	# paired end mapping	
	def paired(self):
		cmd = core.single(args[1],args[2])
		os.system(cmd)
		return '-S'
		
# SAM file process		
class samtools:
	def __init__(self):
		pass
	
	# sam to bam convert	
	def sam2bam(self,sam,output):
		cmd = 'samtools view -S -b %s > %s.bam' % (sam,output)
		os.system(cmd)
	
	# bam sort
	def bamsort(self,output):
		cmd = 'samtools sort %s -o %s' % (output+'.bam',output+'.srt.bam')
		os.system(cmd)
	
	# bam remove duplicates
	def rmdup(self,rmdup,output):
		cmd = 'samtools rmdup %s %s %s' % (rmdup,output+".srt.bam",output+".srt.rmdup.bam")
		os.system(cmd)	
	
	# bam to bed convert	
	def bam2bed(self,output):
		cmd = 'bamToBed -i %s > %s' % (output+".srt.rmdup.bam",output+".bed")
		os.system(cmd)
	
	# remove sam, sorted_bam and rmduped_bam 	
	def clean(self,output):
		os.system('rm %s.sam' % output ) 
		os.system('rm %s.srt.bam' % output ) 
		os.system('rm %s.srt.rmdup.bam' % output ) 

def sam_bed(s, o, r):
	# initiation
	sam2bed = samtools()
	# sam to bam
	sam2bed.sam2bam(s, o)
	# bam sort
	sam2bed.bamsort(o)
	# bam rmdup
	sam2bed.rmdup(r, o)
	# bam to bed
	sam2bed.bam2bed(o)
	# clean temp files
	sam2bed.clean(o)
	
########## main ##########
###
for opt,value in optlist:
	# main Class
	status = mapping()
	# help 
	if opt in ('-h'):
		status.help_message()
	
	# SAM outputfile & bowtie Class	
	if opt in ('-o'):
		output = value
		sam = output+'.sam'
		core = status.output()
	
	# core single COMMAND	
	if opt in ('--single_end'):
		rmdup = status.single()
		#samtools rmdup mode
		
	# core paired COMMAND
	if opt in ('--paired_end'):
		rmdup = status.paired()

# SAM file process MAIN
sam_bed(sam, output, rmdup)

################ END ################
#          Created by Aone          #
#       zhaoshuoxp@whu.edu.cn       #
################ END ################