#!/usr/bin/env python
################################################
# Usage: translation.py inputfile outputfile   #
# Manual: translate DNA seq to PROTEIN seq     #
################################################
#def Code:AA
code = {
	'TTT':'F','TTC':'F','TTA':'L','TTG':'L','TCT':'S','TCC':'S','TCA':'S','TCG':'S','TAT':'Y','TAC':'Y','TAA':'*','TAG':'*','TGT':'C','TGC':'C','TGA':'*','TGG':'W','CTT':'L','CTC':'L','CTA':'L','CTG':'L','CCT':'P','CCC':'P','CCA':'P','CCG':'P','CAT':'H','CAC':'H','CAA':'Q','CAG':'Q','CGT':'R','CGC':'R','CGA':'R','CGG':'R','ATT':'I','ATC':'I','ATA':'I','ATG':'M','ACT':'T','ACC':'T','ACA':'T','ACG':'T','AAT':'N','AAC':'N','AAA':'K','AAG':'K','AGT':'S','AGC':'S','AGA':'R','AGG':'R','GTT':'V','GTC':'V','GTA':'V','GTG':'V','GCT':'A','GCC':'A','GCA':'A','GCG':'A','GAT':'D','GAC':'D','GAA':'E','GAG':'E','GGT':'G','GGC':'G','GGA':'G','GGG':'G','UUU':'F','UUC':'F','UUA':'L','UUG':'L','UCU':'S','UCC':'S','UCA':'S','UCG':'S','UAU':'Y','UAC':'Y','UAA':'*','UAG':'*','UGU':'C','UGC':'C','UGA':'*','UGG':'W','CUU':'L','CUC':'L','CUA':'L','CUG':'L','CCU':'P','CAU':'H','CGU':'R','AUU':'I','AUC':'I','AUA':'I','AUG':'M','ACU':'T','AAU':'N','AGU':'S','GUU':'V','GUC':'V','GUA':'V','GUG':'V','GCU':'A','GAU':'D','GGU':'G'
	}
	
#def AA:Code
edoc = {
	'PHE': ['TTT', 'TTC'], 'LEU': ['TTA', 'TTG', 'CTT', 'CTC', 'CTA', 'CTG'], 'SER': ['TCT', 'TCC', 'TCA', 'TCG', 'AGT', 'AGC'], 'TYR': ['TAT', 'TAC'], 'CYS': ['TGT', 'TGC'], 'TRP': ['TGG'], 'PRO': ['CCT', 'CCC', 'CCA', 'CCG'], 'HIS': ['CAT', 'CAC'], 'GLN': ['CAA', 'CAG'], 'ARG': ['CGT', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG'], 'ILE': ['ATT', 'ATC', 'ATA'], 'MET': ['ATG'], 'THR': ['ACT', 'ACC', 'ACA', 'ACG'], 'ASN': ['AAT', 'AAC'], 'LYS': ['AAA', 'AAG'], 'VAL': ['GTT', 'GTC', 'GTA', 'GTG'], 'ALA': ['GCT', 'GCC', 'GCA', 'GCG'], 'ASP': ['GAT', 'GAC'], 'GLU': ['GAA', 'GAG'], 'GLY': ['GGT', 'GGC', 'GGA', 'GGG'],'*': ['TAA', 'TAG', 'TGA']
	}

#def AA:short name
AA = {
	'H':'HIS','D':'ASP','R':'ARG','F':'PHE','A':'ALA','C':'CYS','G':'GLY','Q':'GLN','E':'GLU','K':'LYS','L':'LEU','M':'MET','N':'ASN','S':'SER','Y':'TYR','T':'THR','I':'ILE','W':'TRP','P':'PRO','V':'VAL'
	}
	
#def base
base = ['A','a','T','t','G','g','C','c','U','u']	
	
#def translation
def triple(x):
	seq = {}
	result = {}
	n = len(x)
	#get sequence 3 codon list
	for i in range(0,n,3):
		seq.setdefault(0, []).append(x[i:i+3])
		seq.setdefault(1, []).append(x[i+1:i+4])
		seq.setdefault(2, []).append(x[i+2:i+5])
	#get AA sequence list
	for i in range(3):
		for i2 in seq[i]:
			if i2 in code:
				result.setdefault(i, []).append(code[i2])
	return result
	
#def get DNA sequence from input or file
def add(x):
	ins = []
	n = len(x)
	for i in range(n):
		if x[i] in base:
			ins.append(x[i].upper())
	return ''.join(ins)
	
####MAIN####
#from file (arguments)
try:
	import sys
	in_file = sys.argv[1]
	inf = open(in_file,'r')
	out_file = sys.argv[2]
	outf = open(out_file,'w')
	a = inf.read()
	x = add(a)
	y = triple(x)
	try:
		outf.writelines(''.join(y[0])+'\n'+''.join(y[1])+'\n'+''.join(y[2])+'\n')
	except:pass

#from raw input
except IndexError:
	while True:
		a = raw_input('Enter the input sequence:')
		if not a:break
		#search for AA codon
		if a.upper() in edoc:
			print a.capitalize()+':\t'+'\t'.join(edoc[a.upper()]) 
		elif a.upper() in AA:
			print AA[a.upper()].capitalize()+':\t'+'\t'.join(edoc[AA[a.upper()]])
		else:
			x = add(a)
			y = triple(x)
			try:
				print ''.join(y[0])
				print ''.join(y[1])
				print ''.join(y[2])
			except:pass	

################ END ################
#          Created by Aone          #
#       zhaoshuoxp@whu.edu.cn       #
################ END ################