#!/usr/bin/env python
#########################################################################
# Usage: sam_bed_rmdup.py input_file p/s                                #
# Manual: paired_end(p) or single_end(s), sam->bam->sort->rmdup->bed    #
#########################################################################	
import sys
import os
input_file = sys.argv[1]
file_name = input_file.split('.')[0]
ex = input_file.split('.')[1]
out_file = file_name+'.bed'

if sys.argv[2] == 'p': 
	rmdup = '' #samtools 0.1.18
if sys.argv[2] == 's': 
	rmdup = '-s'
	
if ex == 'sam':
	os.system('%s %s %s %s %s %s' % ('samtools', 'view', '-Sb', input_file, '>', file_name+'.bam'))
	os.system('%s %s %s %s' % ('samtools', 'sort', file_name+'.bam', file_name+'.srt'))
	os.system('%s %s %s %s %s' % ('samtools', 'rmdup', rmdup, file_name+'.srt.bam',file_name+'.rm.bam'))
	os.system('%s %s %s %s %s' % ('bamToBed', '-i', file_name+'.rm.bam', '>', out_file))
	os.system('rm %s.srt.bam' % file_name)
	os.system('rm %s.rm.bam' % file_name)
	os.system('rm %s.bam' % file_name)
	
elif ex == '.bam':
	os.system('%s %s %s %s' % ('samtools', 'sort', input_file, file_name+'.srt'))
	os.system('%s %s %s %s %s' % ('samtools', 'rmdup', rmdup, file_name+'.srt.bam',file_name+'.rm.bam'))
	os.system('%s %s %s %s %s' % ('bamToBed', '-i', file_name+'.rm.bam', '>', out_file))
	os.system('rm %s.srt.bam' % file_name)
	os.system('rm %s.rm.bam' % file_name)

################ END ################
#          Created by Aone          #
#       zhaoshuoxp@whu.edu.cn       #
################ END ################