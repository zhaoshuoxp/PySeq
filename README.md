# Py-NGS

----

This repository has the following python scripts which can be used for High-throughput sequencing data analysis.

 * [loop_sort.py](https://github.com/zhaoshuoxp/Py-NGS#loo_sortpy): assign HiC loops in FitHiC format to genes and SNPs.
 * [reads_density.py](https://github.com/zhaoshuoxp/Py-NGS#reads_densitypy): count reads densities for ploting on given genomic regions or genes.
 * [split.py](https://github.com/zhaoshuoxp/Py-NGS#splitpy): genomic regions splitting function separated from reads_density.py.
 * [split_turn_FPM.py](https://github.com/zhaoshuoxp/Py-NGS#split_turn_FPMpy): reads density matrix function separated from reads_density.py.
 * [snp_flip.py](https://github.com/zhaoshuoxp/Py-NGS#snp_flippy): generates two fasta files containing OPEN or CLOSED alleles from [cisVar output](https://github.com/TheFraserLab/cisVar) for motif analysis.
 * [ATGC.py](https://github.com/zhaoshuoxp/Py-NGS#ATGCpy): nucleotide sequence convert and formating.
 * [translation.py](https://github.com/zhaoshuoxp/Py-NGS#translationpy): nucleotide to amino acid sequence.
 * [find_nearest_peaks.py](https://github.com/zhaoshuoxp/Py-NGS#find_nearest_peakspy): find closest gene/peak for each given genomic region in BED.
 * [genotypelines.py](https://github.com/zhaoshuoxp/Py-NGS#genotypelinespy): search VCF file for lines having homo/hetero alleles of given SNPs(rsID).

> Requirements:
> Python3, bedtools, awk, argparse,

[![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu) [![LICENSE](https://img.shields.io/badge/license-Anti%20996-blue.svg)](https://github.com/996icu/996.ICU/blob/master/LICENSE)

----

## loop_sort.py

This script uses FitHiC output to sort HiC loops into four groups:
P(promoter)-P, P-D(Distal), G(GWAS variants)-P and G-D interactions. 

#### Input

*P* value filtered [FitHiC output](https://github.com/ay-lab/fithic#output) 

#### Options

help message can be shown by `loop_sort.py -h`

```shell
Usage: loop_sort.py -i|--input <FitHiC output> -s|--snps <snps in BED> -g|--genes <genes in text> -r|--res <resolution of FitHiC output>
    Options:
        -h|--help		print this help message
        -i|--input		FitHiC output
        -s|--snps		snps file in BED format
            #chr	start	end	rsid	category
        -g|--genes		genes file in text 
            #chr	tss	strand	transcriptID	gene_symbol
        -r|--res		resolution of FitHiC output (default 5000bp)
```

#### Example run

```shell
wget https://raw.githubusercontent.com/zhaoshuoxp/Py-NGS/master/loop_sort.py
chmod 755 loop_sort.py
./loop_sort.py -i fithic_qe-2.txt -s gwas.bed -g genes_TSS.txt -r 5000
```
####  Output

All results will be store in current (./) directory.

* P-P.txt: promoter - promoter interactions.

    ```shell
    #anchor1_chr    anchor1_midpos  anchor2_chr anchor2_midpos  p_value TSS1    gene1   TSS2    gene2
    chr17   14142500        chr17   15667500        6.432004e-65    14140150        CDRT15  15668016        CDRT15P2
    ```

* P-D.txt: promoter - distal interactions.

    ```shell
    #anchor1_chr    anchor1_midpos  anchor2_chr anchor2_midpos  p_value TSS gene
    chr10   100012500       chr10   101192500       6.935044e-03    101190530       GOT1
    ```

* G-P.txt: SNPs(GWAS) - promoter interactions.

    ```shell
    #anchor1_chr    anchor1_midpos  anchor2_chr anchor2_midpos  p_value SNP_loc rsID    TSS gene
    chr1    109817500       chr1    109937500       3.842047e-09    109818530       rs646776        109935979       SORT1
    ```

* G-D.txt: SNPs(GWAS) - distal interactions.

    ```shell
    #anchor1_chr    anchor1_midpos  anchor2_chr anchor2_midpos  p_value SNP_loc rsID
    chr10   104717500       chr10   104777500       4.970126e-03    104719096       rs12413409
    ```



----

## reads_density.py

This script generates RPM matrix(s) of peaks|genes with extension for each condition (reads in BED format). Default resolution is 100 segments for each peak or gene. 
> bedtools is required

#### Input

Genomic regions or genes in BED format. For genes, the strand (+/-) should be in 6th column.

#### Options
help message can be shown by `reads_density.py -h`

```shell
Usage: reads_density.py -i <peakfile> [--scale -u|--upsteam <bp> -d|--downstream <bp>]|[--point -e|--extend <bp>] reads1 reads2 reads3...
    Options:
        -h|--help		    print this help message
        --scale			    scale mode, for genes TSS-TES
        --point			    point mode, for peaks center
        -i|--bed		    peak/genes bed file
        -e|--extend		    extend (bp) from the center of peaks (point mode only)
        -u|--upstream		extend (bp) from the TSS of genes (scale mode only)
        -d|--downstream		extend (bp) from the TES of genes (scale mode only)
```

#### Example run

```shell
wget https://raw.githubusercontent.com/zhaoshuoxp/Py-NGS/master/reads_density.py
chmod 755 reads_density.py
# for peaks in point mode:
./reads_density.py --point -i peaks.bed -e 1000 cond1_reads.bed cond2_reads.bed...
# for genes in scale mode:
./reads_density.py --scale -i genes.bed -u 10000 -d 5000 cond1_reads.bed cond2_reads.bed...
```

####  Output

All matrix files will be store in current (./) directory:

* peaks.cond1_reads
* peaks.cond2_reads
   ...

The output can be plotted by [lineplot.R](https://github.com/zhaoshuoxp/Rplots-NGS#lineplotr)



-----

## split.py

This script is separated from reads_density.py. It splits genomic regions from the center or gene from TSS to 100 segments for intersection and plotting.

#### Input
Genomic regions or genes in BED format. For genes, the strand (+/-) should be in 6th column.

#### Options
help message can be shown by `split.py -h`

```shell
Usage: split.py -i|--bed <BEDfile>  [--domian|-d]|[--tss|-t]|[--peak|-p] -e <EXT bp>|[--gene|-g <up bp> <down bp>]
    Options:
        -h|--help		print this help message
        -i|--bed		peak/genes bed file
        -e|--extend		extend +/-(bp) (only in domian/tss/peaks mode!)
        -d|--domian		extend +/-(bp) from the border of the domains (large peaks, i.e. H3K27me3/H3K9me2) <peaks.bed>
        -t|--tss		extend +/-(bp) from the TSS of the genes <genes_TSS.txt>
        -p|--peaks		extend +/-(bp) from the center of the peaks <peaks.bed>
        -g|--gene		extend <up bp> and <down bp> from the TSS and TES of the genes <genes.bed>
```

#### Example run 

```shell
wget https://raw.githubusercontent.com/zhaoshuoxp/Py-NGS/master/split.py
chmod 755 split.py
# for peaks, i.e.: TF-ChIPseq:
./split.py -i peaks.bed -t -e 1000
# for genes:
./split.py -i genes.bed -g 10000 5000
# for TSS:
./split.py -i genes.bed -t -e 5000
# for domians, i.e.: H3K9me2, H3K27ac-ChIPseq:
./split.py -i domains.bed -d -e 10000
```

####  Output

The splited file will be store in current (./) directory:

* peaks/genes/domians.split100: in BED format, 100 continus rows for a row in original input.

This output can be used for reads counting with bedtools, i.e.

```shell
intersectBed -a peaks.split100 -b cond1_reads.bed -c > peaks.split.cond1
```



-----

## split_turn_FPM.py

This script is seperated from reads_density.py. It generates matrix from the output of split.py with reads counting data for ploting.

#### Input

BED file with the reads counting data in last column. i.e. the bedtools interected output of split.py.

#### Example run

```shell
./split_turn_FPM.py peaks.split.cond1 peaks.cond1.matrix <total cond1 reads number in M>
```

#### Output

* peaks.cond1.matrix: the matrix file of the peaks, ech row stands for a peak, having 100 values.

  

-----

## snp_flip.py

 This script generates two fasta files containing OPEN or CLOSED alleles from [cisVar output](https://github.com/TheFraserLab/cisVar) for [HOMER](http://homer.ucsd.edu/homer/motif/fasta.html) motif analysis.

#### Input

The output of cisVar, i.e. {prefix}.{read_depth}.final.txt.

#### Options

help message can be shown by `./snp_flip.py -h`

```shell
Usage: snp_flip.py -i|--input <cisVar output> -p|--pvalue <pvalue cutoff> -e|extend <extension from SNP> -f|fasta <reference genome fasta file>
		Options:
      -h|--help			print this help message
      -i|--input		cisVar output <{prefix}.{depth}.final.txt>
      -p|--pvalue		p value cutoff (default 0.001)
      -e|--extend		extend (bp) from SNP (default 50bp)
      -f|--fasta		genome fasta file (default /home/quanyi/genome/hg19/GRCh37.p13.genome.fa)
```

#### Usage

```shell
wget https://raw.githubusercontent.com/zhaoshuoxp/Py-NGS/master/snp_flip.py
chmod 755 snp_flip.py
./snp_flip.py -i test.20.final.txt -p 0.001 -e 50 -f hg19.fa
```

#### Output

- test_open.fa:  the fasta file with OPEN alleles.
- test_closed.fa: the fasta file with CLOSED alleles.

The two fasta files can be used as target-vs-background each other for motifs scanning, i.e.

```shell
# find motifs which can open chromatin 
findMotifs.pl test_open.fa fasta open -fasta test_closed.fa
# find motifs which can close chromatin 
findMotifs.pl test_closed.fa fasta closed -fasta test_open.fa
```

See [more details](http://homer.ucsd.edu/homer/motif/fasta.html).



-----

## ATGC.py

This script converts nucleotide sequences between "reverse (r)", "complement (c)" and "reverse complement (rc)". 

#### Input

Both stdin and text file are accepted. 

> NOTE: In text-reading mode, all lines are consider as one sequence. Split every query to a single file if you have >1 sequences.

#### Usage

In stdin mode:

```shell
# i.e.
./ATGC.py
Enter the input sequence:AATTGGCC
Reverse(r) or Complement(c) or Reverse Complement(rc):rc
GGCCAATT
# jump back to input step
Enter the input sequence:AATTGGCC
# enter without mode to show original seq
Reverse(r) or Complement(c) or Reverse Complement(rc):
AATTGGCC
# use A:U pair if U detected
Enter the input sequence:AAUUGGCC
Reverse(r) or Complement(c) or Reverse Complement(rc):c
# warning message
!!!The sequence contains "U" or "u", Using A:U pair!!!
TTAACCGG
# script stops when no input detected
Enter the input sequence:
```

In text-reading mode:

```shell
./ATGC.py <input.txt> <output.txt> <mode>
```



-----

## translation.py

This scirpt translates nucleatide sequences to amino acid sequence by 3-frame translation.

#### Usage

As ATGC.py, translation.py can be run with stdin mode:

```shel
./translation.py
Enter the input sequence:GAGATGTTGGAATGTGACGGGTTGA
EMLECDGL
RCWNVTG*
DVGM*RV
```

text-reading mode:

```shell 
./translation.py <input file> <output file>
```

> NOTE: Split every query to a single file if you have >1 sequences.



----

## find_nearest_peaks.py

This is a python version of [closestBed](https://bedtools.readthedocs.io/en/latest/content/tools/closest.html). The script assigns a closest peak/genomic region to each query. The input can be peaks, regions or genes in BED format.

#### Usage

```shell
./find_nearest_peaks.py peaks1.bed peaks2.bed output.txt
# count the peaks without neighbors, usually be 0
0 peaks have no neighbors
```

#### Output

The output stores the 2 peaks/genes genomic coordinates and the distance of the two peaks center in text. 

```
#chr_1	start1	end1	id1	chr_2	start2	end2	id2	distance
chr1	100	200	peak1	chr2	400	500	gene1	300
```



----

## genotypelines.py

This script takes an input file of rsID to search VCF file for homozygous/heterozygous cell lines/samples.

#### Input

A text file having a rsID per line.

#### Options

help message can be shown by `./genotypelines.py -h`

```shell
usage: genotypelines.py [-h] [-v VCF] [-m {1|1,1|0,0|1,0|0}] rs

Search rsID and get heterozygous/homozygous lines in the VCF file

positional arguments:
  rs                    input SNP, a rsID per line

optional arguments:
  -h, --help            show this help message and exit
  -v VCF, --vcf VCF     (gzipped) genotypes VCF file
  -m {1|1,1|0,0|1,0|0}, --mode {1|1,1|0,0|1,0|0}
                        heterozygous/homozygous
```

#### Usage

```shell
wget https://raw.githubusercontent.com/zhaoshuoxp/Py-NGS/master/genotypelines.py
chmod 755 snp_flip.py
./snp_flip.py -v sample.vcf.gz -m 1|1 rsID.txt
```

#### Output

The output is <stdout>.

------
Author [@zhaoshuoxp](https://github.com/zhaoshuoxp)  
May 23 2019  