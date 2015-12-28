#!/usr/bin/env pypy
####################################
#Usage: ATGC.py input_file output_file r/c/rc
#r/R: reverse c/C:complement rc/RC: reverse complement
####################################

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
	if y == 'c' or y == 'C':
		return ''.join(comp)
	if y == 'r' or y == 'R':
		return ''.join(x)[::-1]
	if y == 'rc' or y == 'RC':
		return ''.join(comp)[::-1]
	else:return ''.join(x)

#def base
base=['A','a','T','t','G','g','C','c','U','u']	
	
#def get list from input or file
def add(x):
	n = len(x)
	#get list
	for i in range(n):
		if x[i] in base:
			ins.append(x[i])
	#RNA sequence "U" warning
	if 'U' in ins or 'u' in ins:
			print '!!!The sequence contains "U" or "u", Using A:U pair!!!'
			
####MAIN####
#from file (arguments)
try:
	import sys
	in_file = sys.argv[1]
	inf = open(in_file,'r')
	out_file = sys.argv[2]
	outf = open(out_file,'w')
	s = sys.argv[3]
	ins = []
	a = inf.read()
	add(a)
	outf.writelines(seq(ins,s))

#from raw input
except:
	while True:
		a = raw_input('Enter the input sequence:')
		if not a:break
		#kind of output
		b = raw_input('Reverse(r) or Complement(c) or Reverse Complement(rc):')	
		ins = []
		add(a)
		print seq(ins,b)		