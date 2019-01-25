#!/usr/bin/env python3
##################################################################
# Usage: ATGC.py input_file output_file r/c/rc                   #
# Manual: r/R:reverse c/C:complement rc/RC: reverse complement   #
##################################################################

#def Complement/Reverse/Reverse_Complement algorithm
def seq(x,y):
	comp = []
	for i in x:
		if i == 'A': comp.append('T')
		elif i == 'a': comp.append('t')
		elif i == 'T': comp.append('A')
		elif i == 't': comp.append('a')
		elif i == 'G': comp.append('C')
		elif i == 'g': comp.append('c')
		elif i == 'C': comp.append('G')
		elif i == 'c': comp.append('g')
		elif i == 'U': comp.append('A')
		elif i == 'u': comp.append('a')
	if y.upper() == 'C':
		return ''.join(comp)
	if y.upper() == 'R':
		return ''.join(x)[::-1]
	if y.upper() == 'RC':
		return ''.join(comp)[::-1]
	else:return ''.join(x)

#def base
base=['A','a','T','t','G','g','C','c','U','u']	
	
#def get list from input or file
def add(x):
	s = []
	n = len(x)
	#get list
	for i in range(n):
		if x[i] in base:
			s.append(x[i])
	#RNA sequence "U" warning
	if 'U' in s or 'u' in s:
			print('!!!The sequence contains "U" or "u", Using A:U pair!!!')
	return s
			
####MAIN####
#from file (arguments)
try:
	import sys
	in_file = open(sys.argv[1])
	out_file = open(sys.argv[2], 'w')
	mode = sys.argv[3]
	content = in_file.read()
	sequence = add(content)
	out_file.writelines(seq(sequence, mode))
	out_file.close()

#from raw input
except IndexError:
	while True:
		content = eval(input('Enter the input sequence:'))
		if not content: break
		#kind of output
		mode = eval(input('Reverse(r) or Complement(c) or Reverse Complement(rc):'))	
		sequence = add(content)
		print((seq(sequence, mode)))	

################ END ################
#          Created by Aone          #
#       zhaoshuoxp@whu.edu.cn       #
################ END ################