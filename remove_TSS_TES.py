#!/usr/bin/env python3
#####################################

import sys
of_e_i = open(sys.argv[2],'w')
of_i_e = open(sys.argv[3],'w')
of_bed = open(sys.argv[4],'w')
for line in open(sys.argv[1]):
    a = line.split()
    block_size = a[10].split(',')
    del block_size[-1]
    blocksize = list(map(int, block_size))
    block_site = a[11].split(',')
    del block_site[-1]
    blocksite = list(map(int, block_site))
    nu = int(a[9])
    assert nu == len(blocksize)
    assert nu == len(blocksite)
    
    if a[5] == '+':
        start = int(a[1])
        of_e_i.writelines(a[0]+'\t'+str(start+blocksite[0]+blocksize[0])+'\t'+a[3]+'\t'+a[4]+'\t'+a[5]+'\n')
        for i in range(1,nu-1):
            of_e_i.writelines(a[0]+'\t'+str(start+blocksite[i]+blocksize[i])+'\t'+a[3]+'\t'+a[4]+'\t'+a[5]+'\n')
            of_i_e.writelines(a[0]+'\t'+str(start+blocksite[i])+'\t'+a[3]+'\t'+a[4]+'\t'+a[5]+'\n')
            of_bed.writelines(a[0]+'\t'+str(start+blocksite[i])+'\t'+str(start+blocksite[i]+blocksize[i])+'\t'+a[3]+'\t'+a[4]+'\t'+a[5]+'\n')
        of_i_e.writelines(a[0]+'\t'+str(start+blocksite[nu-1])+'\t'+a[3]+'\t'+a[4]+'\t'+a[5]+'\n')
    else:
        start = int(a[2])
        of_e_i.writelines(a[0]+'\t'+str(start-blocksite[0]-blocksize[0])+'\t'+a[3]+'\t'+a[4]+'\t'+a[5]+'\n')
        for i in range(1,nu-1):
            of_e_i.writelines(a[0]+'\t'+str(start-blocksite[i]-blocksize[i])+'\t'+a[3]+'\t'+a[4]+'\t'+a[5]+'\n')
            of_i_e.writelines(a[0]+'\t'+str(start-blocksite[i])+'\t'+a[3]+'\t'+a[4]+'\t'+a[5]+'\n')
            of_bed.writelines(a[0]+'\t'+str(start-blocksite[i]-blocksize[i])+'\t'+str(start-blocksite[i])+'\t'+a[3]+'\t'+a[4]+'\t'+a[5]+'\n')
        of_i_e.writelines(a[0]+'\t'+str(start-blocksite[nu-1])+'\t'+a[3]+'\t'+a[4]+'\t'+a[5]+'\n')


################ END ################
#          Created by Aone          #
#     quanyi.zhao@stanford.edu      #
################ END ################