#!/usr/bin/env python
##############################################################################
# Usage: cuffmerge_diff.py $refgtf $refgenome sample1.bam sample2.bam.....   #
# Manual: get DEG list form SAM file by cuffmerge and cuffdiff               #
##############################################################################
import sys,os
import getopt
optlist,args = getopt.getopt(sys.argv[1:],'ho:',["help"])

########## subroutine ##########
# help_message()    print help message for this pipeline
def help_message():
			print '''##########
Usage:  %s     [options*] <GTF> <genome> <bam>|[<sample1.bam>|<sample2.bam>....]
Options:
-h|--help           print this help message
##########''' % sys.argv[0]

# cuffmerge ()
def cuffmerge(g,x,t):
	genome = '-s %s' % x
	output = '-o %s' % 'merge'
	assemble_list = t
	gtf = '-g %s' % g
	thread = '-p 4'
	return "cuffmerge %s %s %s %s %s" % (output,thread,gtf,genome,assemble_list)

# cuffdiff ()
def cuffdiff(l,b):
	output = '-o %s' % 'diff'
	gtf = './merge/merged.gtf'
	thread = '-p 4'
	rescue = '-u'
	labels = '-L %s' % l
	bam = '%s' % b
	return "cuffdiff %s %s %s %s %s %s" % (output,thread,rescue,labels,gtf,bam)

########## main ##########
# help
###	
for opt,value in optlist:
	if opt in ('-h'):
		help_message()
		sys.exit(0)

# get sample names and PATH
###
# get bam PATH
arguments = sys.argv[3:]
bam = ' '.join(arguments)

# get sample labels
n = []
for i in arguments:
	n.append((i.rsplit('/',1)[-1]).rsplit('.',1)[0])
label = ','.join(n)

# get GTF PATH list
g = []
for i in arguments:
	g.append(i.rsplit('bam',1)[0])
for i in range(len(g)):
	if i == 0:
		os.system('echo %sgtf > ./list.txt' % g[0])
	else:
		os.system('echo %sgtf >> ./list.txt' % g[i])
		
# cuffmerge
txt = './list.txt'
cmd = cuffmerge(args[0], args[1], txt)
os.system(cmd)

# cuffdiff
cmd = cuffdiff(label, bam)
os.system(cmd)

################ END ################
#          Created by Aone          #
#       zhaoshuoxp@whu.edu.cn       #
################ END ################