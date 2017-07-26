#!/usr/bin/env python
#######################################################################################################
# Usage: bowtie2_class.py -o output_file(label) --paired_end/--single_end $bowtie2index reads1|reads2 #
# Manual: mapping ChIPseq reads to reference genone bu BOWTIE2 DEF                                    #
#######################################################################################################
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

# single_end ()
def single_end(x,q,o):
    index = '-x' + x
    output = '-S %s' % o
    fastq = '-U ' + q
    mapping_input = '-q --phred33'
    mapping_alignment = '--end-to-end --sensitive'
    mapping_report = '-k 1 --no-unal'
    mapping_thread = '-p 4'
    return "bowtie2 %s %s %s %s %s %s %s" % (mapping_input,mapping_alignment,mapping_report,mapping_thread,index,fastq,output)

# paired_end ()
def paired_end(x,left,right,o):
    index = '-x' + x
    left = '-1 %s' % left
    right = '-2 %s' % right
    output = '-S %s' % o
    mapping_input = '-q --phred33'
    mapping_alignment = '--end-to-end --sensitive'
    mapping_report = '-k 1 --no-unal'
    mapping_thread = '-p 4'
    mapping_ruler = '--fr --no-mixed --no-discordant'
    mapping_insert = '-X 1000'
    return "bowtie2 %s %s %s %s %s %s %s %s %s %s" % (mapping_input,mapping_alignment,mapping_report,mapping_thread,mapping_ruler,mapping_insert,index,left,right,output)

########## main ##########
# mapping
###
if __name__ == '__main__':
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
            cmd = single_end(args[0],args[1],sam)
            os.system(cmd)

        if opt in ('--paired_end'):
            rmdup = '' 
            cmd = paired_end(args[0],args[1],args[2],sam)
            os.system(cmd)

    ###
    # SAM to BAM
    cmd = 'samtools view -S -b %s -o %s.bam' % (sam,output)
    os.system(cmd)

    # BAM sort
    cmd = 'samtools sort %s -o %s' % (output+'.bam',output+'.srt.bam')
    os.system(cmd)

    # remove duplicated reads
    cmd = 'samtools rmdup %s %s %s' % (rmdup,output+".srt.bam",output+".srt.rmdup.bam")
    os.system(cmd)

    # BAM to BED
    cmd = 'bamToBed -i %s > %s' % (output+".srt.rmdup.bam",output+".bed")
    os.system(cmd)

    # remove temp files
    os.system('rm %s.sam' % output ) 
    os.system('rm %s.srt.bam' % output ) 
    os.system('rm %s.srt.rmdup.bam' % output ) 

################ END ################
#          Created by Aone          #
#       zhaoshuoxp@whu.edu.cn       #
################ END ################