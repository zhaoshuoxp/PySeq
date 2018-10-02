#!/usr/bin/env python
#####################################
# Usage:  reads_density.py --scale|point -i input.bed -e|<-u -d> <SIZE bp> reads1.bed reads2.bed...    
# Manual: Count RPM matrix, use aligned reads in bed format, with -e extension for point mode(peaks) or -d -u for scale mode(genes) 
#####################################

import sys,os
import getopt
optlist,args = getopt.getopt(sys.argv[1:],'hi:e:u:d:',["help","bed=","extend=","scale","point","upstream=","downstream="])

########## subroutine ##########

def help_message():
		print '''##########
Usage:  %s -i <peakfile> [--scale -u|--upsteam <bp> -d|--downstream <bp>]|[--point -e|--extend <bp>] reads1 reads2 reads3...
Options:
-h|--help           print this help message
--scale			scale mode, for genes TSS-TES
--point			point mode, for peaks center
-i|--bed           peak/genes bed file
-e|--extend			extend (bp) from the center of peaks (point mode only)
-u|--upstream			extend (bp) from the TSS of genes (scale mode only)
-d|--downstream			extend (bp) from the TES of genes (scale mode only)
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

# split genes, scale genes from TSS-TES in 60 seg, up/down stream 20+20 seg
def gene_split(i,o,u,d):
	file1 = i
	output_file = o
	upstream = u
	downstream = d
	split100 = open(output_file,'w')

	for line in open(i,'r'):
		a = line.split()
		cen = (int(a[1]) + int(a[2]))/2.0
		interval = (int(a[2]) - int(a[1]))/60
		
		if a[3]=='+':
			start = int(a[1])-upstream
			end = int(a[2])+downstream
			ext_int_up = upstream/20
			ext_int_down = downstream/20
			for i in range(20):
				split100.writelines(a[0]+'\t'+str(int(start + i*ext_int_up))+'\t'+str(int(start + (i+1)*ext_int_up))+'\t'+str(cen)+'\n')
			for i in range(-30,30):
				split100.writelines(a[0]+'\t'+str(int(cen + i*interval))+'\t'+str(int(cen + (i+1)*interval))+'\t'+str(cen)+'\n')
			for i in range(20):
				split100.writelines(a[0]+'\t'+str(int(end + i*ext_int_down))+'\t'+str(int(end + (i+1)*ext_int_down))+'\t'+str(cen)+'\n')
				
		elif a[3]=='-':
			start = int(a[2])+upstream
			end = int(a[1])-downstream
			ext_int_up = upstream/20
			ext_int_down = downstream/20
			for i in range(20):
				split100.writelines(a[0]+'\t'+str(int(start -(i+1)*ext_int_up))+'\t'+str(int(start - i*ext_int_up))+'\t'+str(cen)+'\n')
			for i in range(-30,30):
				split100.writelines(a[0]+'\t'+str(int(cen - (i+1)*interval))+'\t'+str(int(cen - i*interval))+'\t'+str(cen)+'\n')
			for i in range(20):
				split100.writelines(a[0]+'\t'+str(int(end - (i+1)*ext_int_down))+'\t'+str(int(end - i*ext_int_down))+'\t'+str(cen)+'\n')
				
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
	
		if opt in ('-i','--bed'):
			input_file = value
			name = input_file.rsplit('/',1)[-1].rsplit('.',1)[0]
			split_file = name + '.split100'
			
		if opt in ('-e','--extend'):
			extend = int(value)
			
		if opt in ('-u','--upstream'):
			up = int(value)
		
		if opt in ('-d','--downstream'):
			down = int(value)
		
		if opt in ('--scale'):
			mod = "scale"
		
		if opt in ('--point'):
			mod = "point"
			
	if mod=='point':
		peaks_split(input_file, split_file, extend)
		
	elif mod =='scale':
		gene_split(input_file, split_file, up, down)
	
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
#       quanyiz@stanford.edu        #
################ END ################