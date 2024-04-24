#!/usr/bin/env python3
#####################################

import os
import argparse
import gtfparse as gp
import polars
from pathlib import Path
from typing import List, Union

COMMONS_COL = ['seqname', 'source', 'feature', 'start', 'end', 'score', 'strand', 'frame']

def write_gtf(df: polars.DataFrame, export_path: Union[str, Path], headers: List[str] = None):
	headers = headers or []
	with open(export_path, 'w') as f:
		for header in headers:
			f.write(f"{header}\n")
		for row in df.iter_rows(named=True):
			f.write(f"{commons_cols(row)}\t{custom_fields(row)}\n")
			
def commons_cols(row) -> str:
	return "\t".join([str(row[field] or '.') for field in COMMONS_COL])

def custom_fields(row) -> str:
	return "; ".join([f'{field} "{row[field]}"' for field in row.keys() if (field not in COMMONS_COL) and (row[field])])

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-g','--gtf', help = 'original GTF file', default='/home/quanyi/genome/hg38/gencode.v44.chr_patch_hapl_scaff.annotation.gtf', type = str)
	parser.add_argument('-l','--list',  help = "gene name list to be subset from GTF file, Note that the gene name has to be EXACT office gene name in NCBI or ENSEMBL database", type = str)
	parser.add_argument('-o','--out', help = "path to output file", type = str)
	args = parser.parse_args()
	input_file = args.gtf
	output_file = args.out
	list_file = args.list
	genes=[]
	if input_file and output_file and list_file:
		for line in open(list_file):
			a=line.split()
			genes.append(a[0])
		df = gp.read_gtf(input_file)
		filtered_df = df.filter(df['gene_name'].is_in(genes))
		write_gtf(filtered_df, output_file)
	else:
		print('Error: GTF file path, gene name list, and output file path are required.')
	
if __name__ == '__main__':
	main()
################ END ################
#          Created by Aone          #
#     quanyi.zhao@stanford.edu      #
################ END ################