#!/usr/bin/env python
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

'''
    configuration file
'''

DEBUG = True
PORT = 5000
SERVER = 'localhost' 

TWEETS_NUM = 10 #no. of last tweets to check
SLEEP_TIME_INITIAL = 5 #in seconds
SLEEP_TIME_LATER = 15
SLEEP_CUTOFF = 60 

try:
	from config_local import *
except:
	pass