#!/usr/bin/env python
#-----------------------
# Copyright 2013 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

from twitter_api import app
from config import DEFAULT_PORT, DEFAULT_HOST, DEBUG 

#----------------------
def runserver():
	app.run(host=DEFAULT_HOST, port=DEFAULT_PORT,debug=DEBUG)

#----------------------
if __name__ == '__main__':
	runserver()
