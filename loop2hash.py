#!/usr/bin/env python
#-*- coding=utf-8
import sys,re
import pprint
#-------- a naive config parser
def loop2hash(file,sep=None): # set config in param-list to enable config update.
	'''
	Loop a config file, split each line into key & value.

	Usage: python $0 data/example.config

	A config file is merely a plain text file with a key ~ value pair in each line.
	In our situation, a config file follows guidelines below:

	1. Text after '#' mark is regarded as annotation, empty lines will be ignored.
	2. Field separator is either '\s+' or '=', choose and choose only one within a file,specify the corresponding one in loop2hash(file,sep=XX)
	3. Wrap string with quotes: '0755-625384' or 'Shenzhen-08732'. leave digital value as it is.
	4. Nested Python data structure 'tuple' & 'dictionary' is 'evaled' inside config parser,but don't use '=' as separator inside a dictionary.
	5. Non-ascii key is supported but not recommended.
	'''
	config = {}
	lines = open(file,'r').readlines()
	for line in lines:
		# ignore with annotations & empty lines
		if re.search(r"(^\s*#)|(^\s$)",line):
			continue
		line = re.sub("#.*?$","",line)
		# split line into key~value
		key,value = line.strip().split(sep,1)
		key = key.strip()
		value = value.strip()
		# if value is nested structure,evaluate it into Python tuple or dictionary
		if '(' or '[' or '{' in value:
			config[key] = eval(value)
		# if value is simple string,read value as it is, '(,[,{' is abondoned
		else:
			config[key] = value
	return config	


if __name__=='__main__':
	config_file = sys.argv[1]
	print "===Now I'll read config from a plain text: %s." %  config_file
	GLOBAL_CONFIG = loop2hash(config_file)
	pprint.pprint (GLOBAL_CONFIG)
