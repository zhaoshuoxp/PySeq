#!/usr/bin/env python
#####################################
# Usage:                            #
# Manual:                           #
#####################################

import os,re,commands

def pip_upgrade():
	#get packages
	cmd_list = 'pip list -o'
	out_put = commands.getoutput(cmd_list)
	#need to be upgraded:
	if out_put:
		pattern = re.compile('[a-z]+\s+[0-9]')
		matched = pattern.findall(out_put)
		#make package list
		lists = []
		for i in matched:
			name = i.split()[0]
			lists.append(name)
		#upgrade
		cmd_upgrade = 'sudo -H pip install -U %s' % ' '.join(lists)
		os.system(cmd_upgrade)
		print 'Pip packages upgraded.'
	#no need to be upgraded:	
	else:
		print 'All pip packages up-to-date.'

def brew_upgrade():
	cmd1 = 'brew update'
	cmd2 = 'brew upgrade'
	cmd3 = 'brew cleanup --force'
	cmd4 = 'brew doctor'
	os.system(cmd1)
	os.system(cmd2)
	os.system(cmd3)
	os.system(cmd4)
	
pip_upgrade()
brew_upgrade()

################ END ################
#          Created by Aone          #
#       Quanyi.Zhao@ucsf.edu        #
################ END ################