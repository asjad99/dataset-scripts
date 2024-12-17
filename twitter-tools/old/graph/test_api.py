#!/usr/bin/env python
#-----------------------
# Copyright 2013 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

'''
	For testing the twitter API from command line 
'''

from unix.common import *
import requests
import json  

#-------------------------
def token_save(server):
	
	url = 'http://localhost:5000/twitter/api/v1.0/token'

	if(server == 'remote'):
		url = 'http://66.175.214.243/twitter/api/v1.0/token'
	
	print url 

	data = {}
	data['handle'] = 'muneeb'
	#data['access_key'] = 'test'
	#data['access_secret'] = 'test'
	
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Basic'}

	r = requests.post(url, data=json.dumps(data), headers=headers, auth=('scopeapp','password'))

	pretty_print(r.json())

	print '-' * 10

#-------------------------
def intro(server,base_user,target_user):

	url = 'http://localhost:5000/twitter/api/v1.0/twitter_users/'

	if(server == 'remote'):
		url = 'http://66.175.214.243/twitter/api/v1.0/twitter_users/'
	
	url += base_user + '/followers'
	
	print url 

	data = {}
	data['followed_by'] = target_user
	
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

	print url 

	r = requests.get(url, params=data, headers=headers)

	pretty_print(r.json())

	print '-' * 10

#-------------------------
def get_user(twitter_handle,server):

	url = 'http://localhost:5000/twitter/api/v1.0/twitter_users/'

	if(server == 'remote'):
		url = 'http://66.175.214.243/twitter/api/v1.0/twitter_users/'
	
	print url 

	data = {}
	data['handle'] = twitter_handle
	
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

	r = requests.get(url + twitter_handle, headers=headers)

	pretty_print(r.json())

	print '-' * 10

#-------------------------    
if __name__ == "__main__":

	try:

		if(len(sys.argv) < 2): raise UsageException(100)

		server = 'local'		

		try:
			#twitter_handle = sys.argv[1]
			server = sys.argv[1]
		except:
			pass

		#token_save(server)
		#intro(server,'muneeb','Billclinton')
		get_user('muneeb',server)
			
	except UsageException as e:
		print e 

	except Exception as e:
		print_exception(log)
