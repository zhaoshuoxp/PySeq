#!/usr/bin/env python3
#####################################
# Usage:  split.py -i|--bed <inputfile(BED)> -d|--domian <bp> -t|--tss <bp> -p|--peak <bp> -g|--gene <up bp> <down bp>
# Manual: Split domains/tss/peaks/genes to 100 segments                         
#####################################

import sys,os
import getopt
optlist,args = getopt.getopt(sys.argv[1:],'hi:e:dtpg',["help","bed=","extend=""domian","tss","peak","gene"])

def help_message():
		print('''
Usage:  %s -i|--bed <BEDfile>  [--domian|-d]|[--tss|-t]|[--peak|-p] -e <EXT bp>|[--gene|-g <up bp> <down bp>]

Options:
  -h|--help		print this help message
  -i|--bed		peak/genes bed file
  -e|--extend		extend +/-(bp) (only in domian/tss/peaks mode!)
  -d|--domian		extend +/-(bp) from the border of the domains (large peaks, ex.H3K27me3/H3K9me2) <peaks.bed>
  -t|--tss		extend +/-(bp) from the TSS of the genes <genes_TSS.txt>
  -p|--peaks		extend +/-(bp) from the center of the peaks <peaks.bed>
  -g|--gene		extend <up bp> and <down bp> from the TSS and TES of the genes <genes.bed>
''' % sys.argv[0])
class split:
	def __init__(self,i,o,e):
		self.input = open(i)
		self.split100 = open(o,'w')
		self.interval = int(e)/50
		
	def peaks(self):
		for line in self.input:
			a = line.split()
			cen = (int(a[1]) + int(a[2]))/2.0
			for i in range(-50,50):
				self.split100.writelines(a[0]+'\t'+str(int(cen + i*self.interval))+'\t'+str(int(cen + (i+1)*self.interval))+'\t'+str(cen)+'\n')
		self.split100.close()

	def tss(self):
		for line in self.input:
			a = line.split()
			if a[2] == '+':
				for i in range(-50,50):
					self.split100.writelines(a[0]+'\t'+str(int(a[1]) + i*self.interval)+'\t'+str(int(a[1]) + (i+1)*self.interval)+'\t'+a[2]+'\t'+a[3]+'\n')
			if a[2] == '-':
				for i in range(-50,50):
					self.split100.writelines(a[0]+'\t'+str(int(a[1]) - (i+1)*self.interval)+'\t'+str(int(a[1]) - i*self.interval)+'\t'+a[2]+'\t'+a[3]+'\n')			
		self.split100.close()
	
	def domian(self):
		for line in self.input:
			a = line.split()
			cen = (int(a[1]) + int(a[2]))/2.0
			start = int(a[1])
			end = int(a[2])
			range1 = (end - start)/80
			ex0 = start - self.interval*50
			ex2 = end + self.interval*50
			range0 = self.interval*5
			for i in range(10):
				self.split100.writelines(a[0]+'\t'+str(int(ex0 + i*range0))+'\t'+str(int(ex0 + (i+1)*range0))+'\t'+str(cen)+'\n')
			for i in range(-40,40):
				self.split100.writelines(a[0]+'\t'+str(int(cen + i*range1))+'\t'+str(int(cen + (i+1)*range1))+'\t'+str(cen)+'\n')
			for i in range(10):
				self.split100.writelines(a[0]+'\t'+str(int(end + i*range0))+'\t'+str(int(end + (i+1)*range0))+'\t'+str(cen)+'\n')
		self.split100.close()

	def gene(self,u,d):
		for line in self.input:
			a = line.split()
			cen = (int(a[1]) + int(a[2]))/2.0
			interval = (int(a[2]) - int(a[1]))/60
			if a[3]=='+':
				start = int(a[1])-int(u)
				end = int(a[2])+int(d)
				ext_int_up = int(u)/20
				ext_int_down = int(d)/20
				for i in range(20):
					self.split100.writelines(a[0]+'\t'+str(int(start + i*ext_int_up))+'\t'+str(int(start + (i+1)*ext_int_up))+'\t'+str(cen)+'\n')
				for i in range(-30,30):
					self.split100.writelines(a[0]+'\t'+str(int(cen + i*interval))+'\t'+str(int(cen + (i+1)*interval))+'\t'+str(cen)+'\n')
				for i in range(20):
					self.split100.writelines(a[0]+'\t'+str(int(end + i*ext_int_down))+'\t'+str(int(end + (i+1)*ext_int_down))+'\t'+str(cen)+'\n')
			elif a[3]=='-':
				start = int(a[2])+int(u)
				end = int(a[1])-int(d)
				ext_int_up = int(u)/20
				ext_int_down = int(d)/20
				for i in range(20):
					self.split100.writelines(a[0]+'\t'+str(int(start -(i+1)*ext_int_up))+'\t'+str(int(start - i*ext_int_up))+'\t'+str(cen)+'\n')
				for i in range(-30,30):
					self.split100.writelines(a[0]+'\t'+str(int(cen - (i+1)*interval))+'\t'+str(int(cen - i*interval))+'\t'+str(cen)+'\n')
				for i in range(20):
					self.split100.writelines(a[0]+'\t'+str(int(end - (i+1)*ext_int_down))+'\t'+str(int(end - i*ext_int_down))+'\t'+str(cen)+'\n')
		self.split100.close()

try:
	extend = 0
	
	for opt,value in optlist:
		if opt in ('-h','--help'):
			help_message()
			os._exit(0)
	
		if opt in ('-i','--bed'):
			input_file = value
			name = input_file.rsplit('/',1)[-1].rsplit('.',1)[0]
			split_file = name + '.split100'
		
		if opt in ('-e','--extend'):
			extend = value
			
	main = split(input_file, split_file, extend)
	
	for opt,value in optlist:
		if opt in ('-d','--domian'):
			main.domian()
			
		if opt in ('-t','--tss'):
			main.tss()
			
		if opt in ('-p','--peak'):
			main.peaks()
						
		if opt in ('-g','--gene'):
			up = args[0]
			down = args[1]
			main.gene(up,down)
		
except:  
	print("getopt error!")
	help_message()  
	sys.exit(1)		
		

################ END ################
#          Created by Aone          #
#     quanyi.zhao@stanford.edu      #
################ END ################