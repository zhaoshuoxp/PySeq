#!/usr/bin/env python
###############################################################################################
# Usage: bwa_aln_mapping.py -o Output_name --paired_end/--single_end BWAindex reads1|reads2   #
# Manual: mapping ChIPseq reads to reference genone bu BWA_aln mode                           #
###############################################################################################
import sys,os
import getopt
optlist,args = getopt.getopt(sys.argv[1:],'ho:',["help","single_end","paired_end"])

########## subroutine ##########
# help_message()    print help message for this pipeline
def help_message():
            print '''##########
Usage:  %s     [options*]  <index> <R1.fastq>|<R2.fastq>
Options:
-h|--help           print this help message
-o 		            output (label)
--single_end        single end sequence mapping
--paired_end        paired end sequence mapping
##########''' % sys.argv[0]

# aln mapping ()
# single end align and output
def single_end(x,read,o):
    index = x
    sai_output = '%s.sai' % o
    sam_output = '%s.sam' % o
    reads = read
    seed_diff = '-k 2'
    seed_length = '-l 25'
    mapping_thread = '-t 4'
    # mapping to SAI
    os.system("bwa aln %s %s %s %s %s > %s" % (mapping_thread,seed_diff,seed_length,index,reads,sai_output)) 
    # output to SAM   
    os.system("bwa samse %s %s %s > %s" % (index,sai_output,reads,sam_output))

# paired end align and output
def paired_end(x,left,right,o):
    index = x
    sai_output1 = '%s_R1.sai' % o
    sai_output2 = '%s_R2.sai' % o
    reads1 = left
    reads2 = right
    seed_diff = '-k 2'
    seed_length = '-l 50'
    mapping_thread = '-t 4'
    sam_output = '%s.sam' % o
    # mapping Left reads
    os.system("bwa aln %s %s %s %s %s > %s" % (mapping_thread,seed_diff,seed_length,index,reads1,sai_output1))
    # mapping Right reads
    os.system("bwa aln %s %s %s %s %s > %s" % (mapping_thread,seed_diff,seed_length,index,reads2,sai_output2))
    # output to SAM
    os.system("bwa sampe %s %s %s %s %s > %s" % (index,sai_output1,sai_output2,reads1,reads2,sam_output))

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
        sam = output+'.sam'

    if opt in ('--single_end'):
        rmdup = '-s'
        single_end(args[0],args[1],output)
        
    if opt in ('--paired_end'):
        rmdup = '' #samtools 0.1.18
        paired_end(args[0],args[1],args[2],output)

###
# SAM to BAM
cmd = 'samtools view -S -b %s > %s.bam' % (sam,output)
os.system(cmd)

# BAM sort
cmd = 'samtools sort %s %s' % (output+'.bam',output+'.srt')
os.system(cmd)

# remove duplicated reads
cmd = 'samtools rmdup %s %s %s' % (rmdup,output+".srt.bam",output+".srt.rmdup.bam")
os.system(cmd)

# BAM to BED
cmd = 'bamToBed -i %s > %s' % (output+".srt.rmdup.bam",output+".bed")
os.system(cmd)

# remove temp file
os.system('rm %s*.sai' % output )
os.system('rm %s.sam' % output ) 
os.system('rm %s.srt.bam' % output ) 
os.system('rm %s.srt.rmdup.bam' % output ) 

################ END ################
#          Created by Aone          #
#       zhaoshuoxp@whu.edu.cn       #
################ END ################