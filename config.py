#!/usr/bin/env python
#-----------------------
# Copyright 2013 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

'''
    configuration file for bitcoind_api
'''

import os
DEBUG = True

DEFAULT_PORT = 5000
DEFAULT_HOST = '127.0.0.1'

BITCOIND_PORT = os.environ['BITCOIND_PORT']
BITCOIND_SERVER = os.environ['BITCOIND_SERVER']
BITCOIND_USER = os.environ['BITCOIND_USER'] 
BITCOIND_PASSWD = os.environ['BITCOIND_PASSWD']
BITCOIND_USE_HTTPS = False 
