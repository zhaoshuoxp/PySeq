#!/usr/bin/env python3
##################################################################
# Usage: annotation_my.py genes_TSS.txt input_peak_file 		 #
# Manual: annotate peakfile(long domains) using DIY reference    #
##################################################################

##### FILE PREPARE #####
import sys,os
genes = sys.argv[1]
input_file = sys.argv[2]

# Define the reference genome annotation
fp = open('promoter.bed','w')
fe = open('exon.bed','w')
fi = open('intron.bed','w')
fd = open('downstream.bed','w')

for line in open(genes):
	a = line.split()
	if a[2] == '+':
		if (int(a[1])-2000) >= 0:
			start = str(int(a[1])-2000)
			end = str(int(a[1])+1000)
			fp.writelines(a[0]+'\t'+start+'\t'+end+'\t'+a[2]+'\n')
		else:
			start = '0'
			end = str(int(a[1])+1000)
			fp.writelines(a[0]+'\t'+start+'\t'+end+'\t'+a[2]+'\n')
	elif a[2]=='-':
		if (int(a[1])-1000) >= 0:
			start = str(int(a[1])-1000)
			end = str(int(a[1])+2000)
			fp.writelines(a[0]+'\t'+start+'\t'+end+'\t'+a[2]+'\n')
		else:
			start = '0'
			end = str(int(a[1])+2000)
			fp.writelines(a[0]+'\t'+start+'\t'+end+'\t'+a[2]+'\n')
			
for line in open('/Users/Aone/Desktop/genes.txt'):
	a = line.split('\t')
	exon_start = a[9].split(',')
	exon_end = a[10].split(',')
	num = int(a[8])
	for i in range(num):
		fe.writelines(a[2]+'\t'+exon_start[i]+'\t'+exon_end[i]+'\t'+a[3]+'\n')
	for i in range(num-1):
		fi.writelines(a[2]+'\t'+exon_end[i]+'\t'+exon_start[i+1]+'\t'+a[3]+'\n')
	if a[3] == '+':
		fd.writelines(a[2]+'\t'+str(int(a[5])-100)+'\t'+str(int(a[5])+1000)+'\t'+a[3]+'\n')
	if a[3] == '-':
		fd.writelines(a[2]+'\t'+str(int(a[4])-1000)+'\t'+str(int(a[4])+100)+'\t'+a[3]+'\n')

fp.close()
fe.close()
fi.close()
fd.close()

# Define temp file name
output_pro = '%s_pro.bed' % input_file.split('.')[0]
output_exon = '%s_exon.bed' % input_file.split('.')[0]
output_down = '%s_down.bed' % input_file.split('.')[0]
output_intron = '%s_intron.bed' % input_file.split('.')[0]

input_exon = '%s-pro.bed' % input_file.split('.')[0]
input_down = '%s-exon.bed' % input_file.split('.')[0]
input_intron = '%s-down.bed' % input_file.split('.')[0]

####### DEFINE ALGORITHM #######
# Define intersectBed command line

# -wb write the overlapped region only in fraction B
def intersect(i,r,o):
	# intersectBed get overlapped region
	cmd1 = 'intersectBed -a %s -b %s -wo > %s' % (i, r, o)
	os.system(cmd1)
	# append all overlapped region
	overlap = []
	for line in open(o):
		a = line.split()
		overlap.append(int(a[7]))
	# calculate the total length of overlapped region
	length = 0.0
	for i in overlap:
		length+ = i
	return length

# get non-overlapped region for next calculation
def subtract(i,r,i2):
	cmd2 = 'subtractBed -a %s -b %s > %s' % (i, r, i2)
	os.system(cmd2)

######### MAIN ########

pro = 'promoter.bed'
exon = 'exon.bed'
intron = 'intron.bed'
down = 'downstream.bed'

# calculate length of each element
pro_l = intersect(input_file, pro, output_pro)
subtract(input_file, pro, input_exon)

exon_l = intersect(input_exon, exon, output_exon)
subtract(input_exon, exon, input_down)

down_l = intersect(input_down, down, output_down)
subtract(input_down, down, input_intron)

intron_l = intersect(input_intron, intron, output_intron)

# caculate total length of PEAK file
total = 0.0
for line in open(input_file):
	a = line.split()
	total+ = int(a[2]) - int(a[1])
	
# caculate intergenic length
intergenic_l = total - pro_l - exon_l - down_l - intron_l

# caculate rates(percentage) of each element
pro_r = pro_l/total*100
exon_r = exon_l/total*100
down_r = down_l/total*100
intron_r = intron_l/total*100
intergenic_r = intergenic_l/total*100

######### OUTPUT RESULT ########
print "%s Annotation:" % input_file
print "Promoter	%.3f %s" % (pro_r,'%')
print "Exon	%.3f %s" % (exon_r,'%')
print "Downstream	%.3f %s" % (down_r,'%')
print "Intron	%.3f %s" % (intron_r,'%')
print "Intergenic	%.3f %s" % (intergenic_r,'%')

# remove temp file
os.system('rm %s %s %s %s' %(output_pro, output_exon, output_down, output_intron))
os.system('rm %s %s %s' %(input_exon, input_down, input_intron))
os.system('rm %s %s %s %s' %(exon, intron, down, pro))

################ END ################
#          Created by Aone          #
#       zhaoshuoxp@whu.edu.cn       #
################ END ################