#!/usr/bin/env python
####################################################################
# Usage: annotation_files.py                                       #
# Manual: generate annotaion files from genes GTF or TXT by UCSC   #
####################################################################
fp = open('promoter.bed','w')
fe = open('exon.bed','w')
fi = open('intron.bed','w')
fd = open('downstream.bed','w')

for line in open('/Users/Aone/Desktop/genes_TSS.txt'):
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
			start = 0
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

################ END ################
#          Created by Aone          #
#       zhaoshuoxp@whu.edu.cn       #
################ END ################