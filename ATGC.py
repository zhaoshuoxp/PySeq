#!/usr/bin/env python3
##################################################################
# Usage: ATGC.py input_file output_file r/c/rc                   #
# Manual: r/R:reverse c/C:complement rc/RC: reverse complement   #
##################################################################

#translation table:
RC_TABLE = {
	ord('A'):ord('T'),
	ord('T'):ord('A'),
	ord('C'):ord('G'),
	ord('G'):ord('C'),
	ord('a'):ord('t'),
	ord('t'):ord('a'),
	ord('c'):ord('g'),
	ord('g'):ord('c')
}

RC_TABLE_RNA = {
	ord('A'):ord('U'),
	ord('U'):ord('A'),
	ord('C'):ord('G'),
	ord('G'):ord('C'),
	ord('a'):ord('u'),
	ord('u'):ord('a'),
	ord('c'):ord('g'),
	ord('g'):ord('c')
}

def seq(x,y,t):
	if y.upper() == 'C':
		return x.translate(t)
	elif y.upper() == 'R':
		return x[::-1]
	elif y.upper() == 'RC':
		return x.translate(t)[::-1]
	else:
		return x
	
#select only nucleatides sequences
#def base
base=['A','a','T','t','G','g','C','c','U','u']	

def add(x):
	s = ''
	#get list
	for i in range(len(x)):
		if x[i] in base:
			s += x[i]
	return s
			
####MAIN####
#from file (arguments)
try:
	import sys
	in_file = open(sys.argv[1])
	out_file = open(sys.argv[2], 'w')
	mode = sys.argv[3]
	for line in in_file:
		sequence = add(line)
		if 'U' in sequence or 'u' in sequence:
			warn = '!!!The sequence contains "U" or "u", Using A:U pair!!!'
			out_file.writelines(seq(sequence, mode, RC_TABLE_RNA)+'\n')	
		else:
			out_file.writelines(seq(sequence, mode, RC_TABLE)+'\n')	
	print(warn)
	out_file.close()

#from raw input
except IndexError:
	while True:
		content = input('Enter the input sequence:')
		if not content: break
		mode = input('Reverse(r) or Complement(c) or Reverse Complement(rc):')
		sequence = add(content)
		#RNA sequence "U" warning
		if 'U' in sequence or 'u' in sequence:
			print('!!!The sequence contains "U" or "u", Using A:U pair!!!')
			print((seq(sequence, mode, RC_TABLE_RNA)))	
		else:
			print((seq(sequence, mode, RC_TABLE)))	

################ END ################
#          Created by Aone          #
#       zhaoshuoxp@whu.edu.cn       #
################ END ################
