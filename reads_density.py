#!/usr/bin/env python

import sys,os
import getopt
optlist,args = getopt.getopt(sys.argv[1:],'hi:e:',["help","peak=","extend="])

########## subroutine ##########

def help_message():
		print '''##########
Usage:  %s -i <peakfile> -e <bps> reads1 reads2 reads3...
Options:
-h|--help           print this help message
-i|--peak           peak file
-e|--extend			extend (bps) from the center of peaks
##########''' % sys.argv[0]

# split peaks into 100 segments +/- extend size from center of peaks 
def peaks_split(i,o,e):
	file1 = i
	output_file = o
	extend = e
	split100 = open(output_file,'w')

	for line in open(file1,'r'):
		a = line.split()
		cen = (int(a[1]) + int(a[2]))/2.0
		interval = extend/50
		# make sure no <0 positions in BED file, may discard some peaks!!!
		if cen - extend >= 0:	
			for i in range(-50,50):
				split100.writelines(a[0]+'\t'+str(int(cen + i*interval))+'\t'+str(int(cen + (i+1)*interval))+'\t'+str(cen)+'\n')

	split100.close()

# intersectBed/bedtools required, count reads density
def intersect(p,r,o):
	cmd = 'intersectBed -a %s -b %s -c > %s' % (p,r,o)
	os.system(cmd)

# get reads for every splited peak (collect reads every 100 rows) and normalize by FPM
def split_turn(i,o,r):
	result = []
	out_file = open(o,'w')
	# get total number of reads for normalization
	cmd = 'wc -l %s' % r
	count = float(os.popen(cmd).read().split()[0])/1000000

	for line in open(i):
		a = line.split()
		result.append(float(a[-1])/count)
	for i in range(0, len(result), 100):
		b = result[i:i+100]
		for i2 in b:
			out_file.writelines(str(i2)+'\t')
		out_file.writelines('\n')
		
	out_file.close()

########## main ##########

###
try:
	for opt,value in optlist:
		if opt in ('-h','--help'):
			help_message()
			sys.exit(0)
	
		if opt in ('-i','--peak'):
			input_file = value
			name = input_file.rsplit('/',1)[-1].rsplit('.',1)[0]
			split_file = name + '.split100'
			
		if opt in ('-e','--extend'):
			extend = int(value)
		
	peaks_split(input_file, split_file, extend)
	
	intersected_list = []		
	for i in args:
		postfix = i.rsplit('/',1)[-1].rsplit('.',1)[0]
		intersected = split_file + '_' + postfix
		intersect(split_file, i, intersected)
		intersected_list.append(intersected)
		output_file = name + '.' + postfix
		split_turn(intersected, output_file, i)
	
	# clean temp files
	os.system('rm %s %s' % (split_file, ' '.join(intersected_list)))
	
except getopt.GetoptError:  
	print("getopt error!")
	help_message()  
	sys.exit(1)		
		


################ END ################
#          Created by Aone          #
#       zhaoshuoxp@whu.edu.cn       #
################ END ################