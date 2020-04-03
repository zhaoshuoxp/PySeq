#!/usr/bin/env python3
#####################################

import os,subprocess
import argparse


hg19_chrom_lengths = {'chrX': 155270560, 'chr13': 115169878, 
                    'chr12': 133851895, 'chr11': 135006516, 'chr10': 135534747, 'chr17': 81195210, 
                    'chr16': 90354753, 'chr15': 102531392, 'chr14': 107349540, 'chr19': 59128983, 
                    'chr18': 78077248, 'chr22': 51304566, 'chr20': 63025520, 'chr21': 48129895, 
                    'chr7': 159138663, 'chr6': 171115067, 'chr5': 180915260, 'chr4': 191154276, 
                    'chr3': 198022430, 'chr2': 243199373, 'chr1': 249250621, 'chr9': 141213431, 
                    'chr8': 146364022}

def rasqual(i, o, v, y, k, x, n, w, c, l):
    line_un = 0
    os.system('echo > %s' % o)
    
    for line in open(i):
        a = line.split()
        line_un+=1
        tp_id = a[0]
        chrom_s = a[1].split(';')[0]
        if c == True:
            chrom = chrom_s
        elif c == False:
            chrom = chrom_s[3:]
        start = a[2].replace(';',',')
        end = a[3].replace(';',',')
        if int(start.split(',')[0]) > w:
            vcf_s = int(start.split(',')[0])-w
        else: 
            vcf_s = 0
        try:
            if int(end.split(',')[-1])+w > hg19_chrom_lengths[chrom_s]:
                vcf_e = hg19_chrom_lengths[chrom]
            else:
                vcf_e = int(end.split(',')[-1])+w
        except KeyError:
            continue
        cand_snp = 'tabix %s %s:%i-%i' % (v, chrom, vcf_s, vcf_e)
        snp_num = subprocess.check_output(cand_snp+'|wc -l', shell=True).decode('utf-8').split()[0]
        
        if int(snp_num) >10:
            #1/6 feature SNPs of tested SNPs
            feature = int(int(snp_num)/6)
        elif 1 <= int(snp_num) <=10:
            feature = 1
        else: continue
        
        if l == True:
            t = ''
        elif l == False:
            t = '-t '
            
        rasqual = '%s | rasqual -y %s -k %s -x %s -n %s -j %i -l %s -m %i -s %s -e %s %s-f %s -z >> %s' % (cand_snp, y, k, x, n, line_un, snp_num, feature, start, end, t, tp_id, o)
        os.system(rasqual)


def main():
    parser = argparse.ArgumentParser(description="Call QTLs for a list of genes and a VCF file using RASQUAL, report lead SNP only")
    parser.add_argument("-v", "--vcf", help="bgzip and tabix VCF file")
    parser.add_argument('-g', '--genes', help="A gene list with positions, first 6 columns of featureCounts output, 2nd column should have \"chr\"")
    parser.add_argument('output', help="Output file name")
    parser.add_argument('-n', '--number', help="Sample size (number of individuals)")
    parser.add_argument('-w', '--window', help="Window size (+/-) of the transcript in bp to search cis-acting QTLs, default:50kb", default = 50000)
    parser.add_argument('-x', help='X (ovariates) binary file for RASQUAL')
    parser.add_argument('-y', help='Y (phenotype) binary file for RASQUAL')
    parser.add_argument('-k', help='K (offset) binary file for RASQUAL')
    parser.add_argument('-c', '--chr', action='store_true', default=False, help='Indicate if VCF file starts with "chr"')
    parser.add_argument('-a', '--all', action='store_true', default=False, help='Output all SNPs instead of lead SNP only')
    args = parser.parse_args()
    # run
    print(args)
    rasqual(args.genes, args.output, args.vcf, args.y, args.k, args.x, args.number, args.window, args.chr, args.all)

if __name__ == '__main__':
    main()


        
################ END ################
#          Created by Aone          #
#     quanyi.zhao@stanford.edu      #
################ END ################