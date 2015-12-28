#!/usr/bin/env pypy
################################
# annotation_my.py input_peak_file species(hg19/mm10)
# annotate peakfile(long domains) using DIY reference
################################

##### FILE PREPARE #####
import sys,os
input_file = sys.argv[1]

# Define the reference genome annotation

# mouse mm10
if sys.argv[2] == 'mm10':
	pro = '/Users/Aone/Documents/Bioinf/Annotation/mm10/promoter.bed'
	exon = '/Users/Aone/Documents/Bioinf/Annotation/mm10/exon.bed'
	down = '/Users/Aone/Documents/Bioinf/Annotation/mm10/downstream.bed'
	intron = '/Users/Aone/Documents/Bioinf/Annotation/mm10/intron.bed'

# human hg19
elif sys.argv[2] == 'hg19':
	pro = '/Users/Aone/Documents/Bioinf/Annotation/hg19/promoter.bed'
	exon = '/Users/Aone/Documents/Bioinf/Annotation/hg19/exon.bed'
	down = '/Users/Aone/Documents/Bioinf/Annotation/hg19/downstream.bed'
	intron = '/Users/Aone/Documents/Bioinf/Annotation/hg19/intron.bed'

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

# get non-overlapped region for next calculatio 
def subtract(i,r,i2):
	cmd2 = 'subtractBed -a %s -b %s > %s' % (i, r, i2)
	os.system(cmd2)

######### MAIN ########

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

######### END #########
# zhaoshuoxp@whu.edu.cn
######### END #########
