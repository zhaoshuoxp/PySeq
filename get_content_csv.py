#!/usr/bin/env python
######################################
#Usage: get_content_csv.py	path result
#get the line3, row 4 and 5 from all file of a path
######################################
#get all file path and name
import os
import sys
path=sys.argv[1]
file1=sys.argv[2]
#get all file path and name
#def get_recursive_file_list(path):
#	current_files = os.listdir(path)
#	all_files = []
#	for file_name in current_files:
#		full_file_name = os.path.join(path, file_name)
#		all_files.append(full_file_name)
#		if os.path.isdir(full_file_name):
#			next_level_files = get_recursive_file_list(full_file_name)
#			all_files.extend(next_level_files)
#	return all_files
def get_filename_oswalk(path):
	import os
	import os.path
	rootdir=path
	for parent,directory,filename in os.walk(rootdir):
		return filename
	
files = get_filename_oswalk(path)
result=file(file1,'w')
for i in files:
	f=open(i,'r')
	for line in f.readlines()[2:3]:
		a=line.split(',')
		result.writelines(a[3]+'\t'+a[4])
		