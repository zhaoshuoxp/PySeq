#!/usr/bin/env pypy
################################
# Usage
# Manual
################################
nat=[]
ca=[]
import numpy
from scipy import stats
for line in open('/Users/Aone/Desktop/aaa.txt'):
	a=line.split()
	ca.append(a[0])
	nat.append(a[1])
nat_a=numpy.array(map(float,nat))
ca_a=numpy.array(map(float,ca))
f,p=stats.f_oneway(nat_a, ca_a)
print p

######### END #########
# zhaoshuoxp@whu.edu.cn
######### END #########