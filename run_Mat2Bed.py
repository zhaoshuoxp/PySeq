#! /home/mumbach/Software/anaconda/bin/python
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Process HiC-Pro matrix to bedPE format')
parser.add_argument('-c','--chr', help='Input chr number',required=True)
parser.add_argument('-k','--key', help='Input bed region to ID key',required=True)
parser.add_argument('-m','--mat', help='Input HiCPro matrix',required=True)

args = parser.parse_args()
chrom=str(args.chr)
key=str(args.key)
mat=str(args.mat)

key_lines = [line.strip().split() for line in open(key)]
mat_lines = [line.strip().split() for line in open(mat)]

key_dict = {}
for region in key_lines:
	key_dict[region[3]] = region[0:3]

out_file = mat + ".bed"
out = open(out_file,"w")
for bin_pair in mat_lines:
	bed1 = key_dict[bin_pair[0]]
	bed2 = key_dict[bin_pair[1]]
	out.write(bed1[0] + "\t" + bed1[1] + "\t" + bed1[2] + "\t" + bed2[0] + "\t" + bed2[1] + "\t" + bed2[2] + "\t" + bin_pair[2] + "\n")

out.close()

