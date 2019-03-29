# Py-NGS

----

This repository has the following python scripts which can be used for High-throughput sequecning data analysis.

 * loop_sort.py: assign HiC loops in FitHiC format to genes and SNPs.
 * reads_density.py: count reads densities for ploting on given genomic regions or genes.
 * split.py: genomic regions spliting function seperated from reads_density.py.
 * split_turn_FPM.py: reads density matrix function seperated from reads_density.py.
 * snp_flip.py: generate two fasta files containing OPEN or CLOSED alleles from [cisVar output](https://github.com/TheFraserLab/cisVar) for motif analysis.
 * ATGC.py: nucleotide sequence convert and formating.
 * translation.py: nucleotide to amino acid sequence.
 * annotation_homer.py: re-format of homer peak annotation.
 * annotation_my.py: customized peak annotation.
 * find_nearest_peaks.py: find closest gene for each given genomic region in BED.

> Requirements:
> Python3, bedtools, awk



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

This script generates RPM matrix(s) of peaks|genes with extension for each condtion(reads in BED format). Defualt resolution is 100 segments for each peak or gene. 
> bedtools required

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
./reads_density.py --scale -i genes.bed -u 10000 -d 5000 ond1_reads.bed cond2_reads.bed...
```

####  Output

All matrix files will be store in current (./) directory:

* peaks.cond1_reads
* peaks.cond2_reads
   ...

The output can be ploted by [lineplot.R]()



-----

## split.py

This script is seperated from reads_density.py. It splits genomic regions from the center or gene from TSS to 100 segments for intersection and ploting.

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
        -d|--domian		extend +/-(bp) from the border of the domains (large peaks, ex.H3K27me3/H3K9me2) <peaks.bed>
        -t|--tss		extend +/-(bp) from the TSS of the genes <genes_TSS.txt>
        -p|--peaks		extend +/-(bp) from the center of the peaks <peaks.bed>
        -g|--gene		extend <up bp> and <down bp> from the TSS and TES of the genes <genes.bed>
```

#### Example run

```shell
wget https://raw.githubusercontent.com/zhaoshuoxp/Py-NGS/master/split.py
chmod 755 split.py
# for peaks, ex: TF-ChIPseq:
./split.py -i peaks.bed -t -e 1000
# for genes:
./split.py -i genes.bed -g 10000 5000
# for TSS:
./split.py -i genes.bed -t -e 5000
# for domians, ex: H3K9me2, H3K27ac-ChIPseq:
./split.py -i domains.bed -d -e 10000
```

####  Output

The splited file will be store in current (./) directory:

* peaks/genes/domians.split100: in BED format, 100 continus rows for a row in original input.

This output can be used for reads counting with bedtools, ex:

```shell
intersectBed -a peaks.split100 -b cond1_reads.bed -c > peaks.split.cond1
```



-----

## split_turn_FPM.py

This script is seperated from reads_density.py. It generates matrix from the output of split.py with reads counting data for ploting.

#### Input

BED file with the reads counting data in last column. ex: the bedtools interected output of split.py.

#### Usage

```shell
./split_turn_FPM.py peaks.split.cond1 peaks.cond1.matrix <total cond1 reads number in M>
```

#### Output

* peaks.cond1.matrix: the matrix file of the peaks, ech row stands for a peak, having 100 values.

-----









-----

------
Author [@zhaoshuoxp](https://github.com/zhaoshuoxp)  
Mar 28 2019  