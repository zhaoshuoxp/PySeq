#!/usr/bin/env python3
import argparse,sys

def main():
	parser = argparse.ArgumentParser(description = "This script extracts promoter region (-500bp to TSS by default) of each gene, for multiple transcripts the most 5' TSS will be used")
	parser.add_argument('genelist', help = 'input file of the gene list, one gene per row')
	parser.add_argument('-o','--out', help = 'output file path, in BED format')
	parser.add_argument('-u','--up', help = "extend (bp) from upstream of TSS (default 500)", default = 500, type = int)
	parser.add_argument('-d','--down', help = "extend (bp) from downstream of TSS (default 500)", default = 0, type = int)
	parser.add_argument('-g','--genome', choices=['hg38', 'hg19', 'mm10'], help = "select genome build to lookup")
	parser.add_argument('-b','--bed', help = "custom BED file to lookup, 3rd: strand + or -, 4th:official gene name")
	args = parser.parse_args()
	input_file = args.genelist
	if args.out:
		outfile = args.out
	else:
		name = input_file.rsplit('/',1)[-1].rsplit('.',1)[0]
		outfile = name+'.bed'
	up = args.up
	down = args.down
	if args.bed:
		bed = args.bed
	elif args.genome == 'hg38':
		bed = '/nfs/baldar/quanyiz/genome/hg38/genes.bed'
	elif args.genome == 'hg19':
		bed = '/nfs/baldar/quanyiz/genome/hg19/genes.bed'
	elif  args.genome == 'mm10':
		bed = '/nfs/baldar/quanyiz/genome/mm10/genes.bed'
	else:
		sys.exit("chose genome build or provide the reference bed file")
	lookup_bed(input_file,bed,outfile,up,down)

def lookup_bed(i,b,o,u,d):
	genelist=[]

	for line in open(i):
		a=line.split()
		genelist.append(a[0])
		
	f=open(o,'w')
	for line in open(b):
		a=line.split()
		if a[4] in genelist:
			if a[3]=='+':
				f.writelines(a[0]+'\t'+str(int(a[1])-u)+'\t'+str(int(a[1])+d)+'\t'+a[3]+'\t'+a[4]+'\n')
			elif a[3]=='-':
				f.writelines(a[0]+'\t'+str(int(a[2])-d)+'\t'+str(int(a[2])+u)+'\t'+a[3]+'\t'+a[4]+'\n')
	f.close()

if __name__ == '__main__':
	main()
	