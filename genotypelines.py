#!/usr/bin/env python3
#####################################
import os
import argparse

def get_geno(r,v,o):
	if v.endswith('.gz'):
		cmd1 = 'gunzip -c %s |head -n 1000|grep ^# > %s\n' % (v, o)
		cmd2 = 'awk \'NR==FNR{a[$0]}NR>FNR{if($3 in a){print $0}}\' %s <(pigz -dc %s) >> %s' % (r, v, o)
	elif v.endswith('.vcf'):		
		cmd1 = 'head -n 100 %s|grep ^# > %s\n' % (v, o)
		cmd2 = 'awk \'NR==FNR{a[$0]}NR>FNR{if($3 in a){print $0}}\' %s %s >> %s' % (r, v, o)
	shell = open('./shell.sh','w')
	shell.write(cmd1)
	shell.write(cmd2)
	shell.close()
	os.system('bash shell.sh')

def get_lines(f,m):
	for line in open(f):
		a = line.split()
		if line[0:2] != '##':
			if a[0] == '#CHROM':
				cells = {}
				for i in range(9,len(a)):
					cells[a[i]] = i
			else:
				rsid = a[2]
				cell = []
				res = []
				for i in range(9,len(a)):
					if a[i].split(":")[0] == m:
						cell.append(i)
				for i in cells:
					if cells[i] in cell:
						res.append(i)
				print(rsid+'\t'+' '.join(res))
						
		
def main():
	parser = argparse.ArgumentParser(description="Search rsID and get heterozygous/homozygous  lines in the VCF file")
	parser.add_argument("-v", "--vcf", help="(gzipped) genotypes VCF file", default='/home/quanyi/data/genotypes/72vcf_snp_only/snps_only.vcf.gz')
	parser.add_argument("-m", "--mode", help="heterozygous/homozygous", choices=['1|1','1|0','0|1','0|0'], default='1|1')
	parser.add_argument('rs', help="input SNP, a rsID per line")
	args = parser.parse_args()
	get_geno(args.rs, args.vcf, './tmp')
	get_lines('./tmp', args.mode)
	os.system('rm ./tmp ./shell.sh')

if __name__ == '__main__':
	main()


################ END ################
#          Created by Aone          #
#     quanyi.zhao@stanford.edu      #
################ END ################
