#!/usr/bin/env pypy
####################################
# annotation.py input_file
# caculate elment rates from homer annotatePeaks.pl output
####################################
import sys,os
species=sys.argv[2]
input_file=sys.argv[1]
output_file='%s.annoation.txt' % input_file
os.system("annotatePeaks.pl %s %s > %s" % (input_file,species,output_file))
promoter=0.00
intron=0.00
exon=0.00
intergenic=0.00
TTS=0.00
UTR5=0.00
UTR3=0.00
for line in open(output_file):
	a=line.split()
	annotation=a[7]
	if annotation=='promoter-TSS':promoter+=1
	elif annotation=='Intergenic':intergenic+=1
	elif annotation=='intron':intron+=1
	elif annotation=='TTS':TTS+=1
	elif annotation=='exon' or annotation=='non-coding':exon+=1
	elif annotation=="3'":UTR3+=1
	elif annotation=="5'":UTR5+=1
total=promoter+intron+exon+intergenic+TTS+UTR3+UTR5
print "Promoter-TSS:	%s" % str(promoter/total)
print "Intron:	%s" % str(intron/total)
print "Exon:	%s" % str(exon/total)
print "Intergenic:	%s" % str(intergenic/total)
print "TTS:	%s" % str(TTS/total)
print "5'UTR:	%s" % str(UTR5/total)
print "3'UTR:	%s" % str(UTR3/total)
