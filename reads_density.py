#!/usr/bin/env python3
#####################################

import os
import argparse

########## subroutine ##########
def main():
	parser = argparse.ArgumentParser(description = "This script generates RPM matrix(s) of peaks|genes with extension for each condtion(reads in BED format). Defualt resolution is 100 segments for each peak|gene. All output will be stored in current(./) directoy. ###BEDtools is required###")
	parser.add_argument('reads', nargs='+')
	parser.add_argument('-i','--bed', help = 'peak/genes bed file')
	parser.add_argument('-e','--extend', help = "extend (bp) from the center of peaks (point mode only)")
	parser.add_argument('-u','--up',  help = "extend (bp) from the TSS of genes (scale mode only)")
	parser.add_argument('-d','--down',  help = "extend (bp) from the TES of genes (scale mode only)")
	parser.add_argument('-s', '--scale', action = 'store_true', help = 'scale mode, for genes TSS-TES', default = False)
	parser.add_argument('-p','--point', action = 'store_true', help = 'point mode, for peaks center', default = False)
	args = parser.parse_args()
	input_file = args.bed
	name = input_file.rsplit('/',1)[-1].rsplit('.',1)[0]
	split_file = name + '.split100'
	
	if args.point == True:
		mod = 'point'
		extend = int(args.extend)
		up = 0
		down = 0
		peaks_split(input_file, split_file, extend)
	elif args.scale == True:
		mod = 'scale'
		up = int(args.up)
		down = int(args.down)
		gene_split(input_file, split_file, up, down)
	else:
		print("please chosse a mode: -p| -s")
	
	intersected_list = []		
	for i in args.reads:
			postfix = i.rsplit('/',1)[-1].rsplit('.',1)[0]
			intersected = split_file + '_' + postfix
			intersect(split_file, i, intersected)
			intersected_list.append(intersected)
			output_file = name + '.' + postfix
			split_turn(intersected, output_file, i, mod, input_file, up, down)
		
	# clean temp files
	os.system('rm %s %s' % (split_file, ' '.join(intersected_list)))

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
		
		if a[5]=='+':
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
				
		elif a[5]=='-':
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
def split_turn(i,o,r,m,p,up,down):
	result = []
	out_file = open(o,'w')
	# get total number of reads for normalization
	cmd = 'wc -l %s' % r
	count = float(os.popen(cmd).read().split()[0])/1000000
	
	for line in open(i):
		a = line.split()
		result.append(float(a[-1])/count)

	if m == 'scale':
		length = []
		for line in open(p):
			a = line.split()
			length.append(int(a[2])-int(a[1]))
		n = 0
		assert len(result)/100 == len(length)
		
	for i in range(0, len(result), 100):
		b = result[i:i+100]
		if m == 'point':
			for i2 in b:
				out_file.writelines(str(i2)+'\t')
			out_file.writelines('\n')
		elif m == 'scale':
			tp_l = float(length[n])/60
			ratio_u = tp_l/float(up/20)
			ratio_d = tp_l/float(down/20)
			for j in range(0,20):
				out_file.writelines(str(b[j]*ratio_u)+'\t')
			for j in range(20,80):
				out_file.writelines(str(b[j])+'\t')
			for j in range(80,100):
				out_file.writelines(str(b[j]*ratio_d)+'\t')
			out_file.writelines('\n')
			n+=1	
	out_file.close()

########## main ##########

if __name__ == "__main__":
	main()
################ END ################
#          Created by Aone          #
#       quanyiz@stanford.edu        #
################ END ################
