#!/usr/bin/env python3
#####################################
# Usage:  split.py -i|--bed <inputfile(BED)> -d|--domian <bp> -t|--tss <bp> -p|--peak <bp> -g|--gene <up bp> <down bp>
# Manual: Split domains/tss/peaks/genes to 100 segments                         
#####################################

import os
import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('bed', help = 'peak/genes bed file')
	parser.add_argument('-f','--fasta', help = 'genome fasta file', default='/home/quanyi/genome/hg19/GRCh37.p13.genome.fa')
	parser.add_argument('-m','--mode',  help = "spliting mode: peak -- extend +/-(bp) from the center of the peaks <peaks.bed>; domain -- extend +/-(bp) from the border of the domains (large peaks, e.g. H3K27me3/H3K9me2) <peaks.bed>; tss --extend +/-(bp) from the TSS of the genes <genes_TSS.txt>; gene -- extend <up bp> and <down bp> from the TSS and TES of the genes <genes.bed>", choices = ['tss', 'peak', 'domain', 'gene'], type = str)
	parser.add_argument('-u','--up', help = "extend <up bp> from the TSS (only in gene mode!)", default = 5000, type = int)
	parser.add_argument('-d','--down', help = "extend <up bp> from the TES (only in gene mode!)", default = 3000, type = int)
	parser.add_argument('-e','--extend', help = "extend +/-(bp) (only in domian/tss/peaks mode!)", default = 0, type = int)
	args = parser.parse_args()
	input_file = args.bed
	name = input_file.rsplit('/',1)[-1].rsplit('.',1)[0]
	split_file = name + '.split100'
	extend = args.extend
	core = split(input_file, split_file, extend)
	
	if args.mode == 'domain':
		core.domian()
	elif args.mode == 'tss':
		core.tss()
	elif args.mode == 'peak':
		core.peaks()
	elif args.mode == 'gene':
		up = args.up
		down = args.down
		core.gene(up,down)
	else:
		print('-m|--mode is required')

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

		
if __name__ == '__main__':
	main()
################ END ################
#          Created by Aone          #
#     quanyi.zhao@stanford.edu      #
################ END ################