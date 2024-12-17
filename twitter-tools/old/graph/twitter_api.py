#!/usr/bin/env python
#-----------------------
# Copyright 2013 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

'''
	a simple Flask based api for twitter fuctions 
'''

from flask import request, Blueprint

twitter_api = Blueprint('twitter_api', __name__)

from common import pretty_dump
from graph.twitter.config import APP_USERNAME, APP_PASSWORD

import json

from functools import wraps

#---------------------------------
def check_auth(username, password):
	return username == APP_USERNAME and password == APP_PASSWORD

#---------------------------------
def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth: 
			return error_reply("invalid username/password")

		elif not check_auth(auth.username, auth.password):
			return error_reply("invalid auth username/password")
		return f(*args, **kwargs)

	return decorated

#---------------------------------
def error_reply(msg):
	reply = {}
	reply['status'] = -1
	reply['message'] = "ERROR: " + msg
	return pretty_dump(reply)

#---------------------------------
import threading
from graph_analysis import get_connections, check_direct_link
from get_graph import get_user_details

#-------------------------
class GetConnectionsThread(threading.Thread):
	def __init__(self,base_user,target_user):
		threading.Thread.__init__(self)
		self.reply = {}
		self.reply['twitter_handle'] = base_user
		self.reply['direct_link'] = check_direct_link(base_user,target_user)

		connections = get_connections(base_user,target_user)

		lookup_list = []

		counter = 0
		for i in connections: 
			lookup_list.append(i)
			counter += 1
			#not getting more than 100 connections for now 
			if(counter == 100):
				break

		if(len(lookup_list) == 0):
			self.reply['connections'] = []
		else:
			self.reply['connections'] = get_user_details(lookup_list)

#-----------------------------------
@twitter_api.route('/twitter/api/v1.0/token', methods = ['POST'])
@requires_auth
def save_twitter_token():

	reply = {} 

	#---------------------------------
	#check if proper user data was sent		
	try: 
		handle = request.json['handle']
		access_key = request.json['access_key']
		access_secret = request.json['access_secret']
	except:
		return error_reply("missing user data")
	else:
		reply['status'] = 1 
		reply['message'] = "Successfully saved user data"

		from twitter_auth import save_user_auth
		save_user_auth(handle,access_key,access_secret)
	
	return pretty_dump(reply)

#-----------------------------------
@twitter_api.route('/twitter/api/v1.0/twitter_users/<string:twitter_handle>', methods = ['GET'])
def get_twitter_user(twitter_handle):

	if twitter_handle is None:
		return error_reply('missing twitter_handle')
	
	from get_graph import TwitterUser

	new_user = TwitterUser(twitter_handle)
	new_user.fetch_if_stale()

	temp_user = {}

	saved_user = new_user.user

	temp_user['profile_image_url'] = saved_user['profile_image_url']
	temp_user['twitter_handle'] = saved_user['twitter_handle']
	temp_user['full_name'] = saved_user['full_name'] 
	temp_user['twitter_id'] = saved_user['twitter_id']

	return json.dumps(temp_user)

#-----------------------------------
@twitter_api.route('/twitter/api/v1.0/twitter_users/<string:twitter_handle>/followers', methods = ['GET'])
def get_best_intro(twitter_handle):

	base_user = twitter_handle
	target_user = request.values['followed_by']

	reply = []
	lookup_list = []

	from graph_analysis import get_connections
	connections = get_connections(base_user,target_user)

	for i in connections: 
		lookup_list.append(i) 

	from get_graph import get_user_details
	reply = get_user_details(lookup_list)


	fat = ctan 
	
	return json.dumps(reply)

#-----------------------------------
@twitter_api.route('/twitter/api/v1.0/twitter_users/<string:twitter_handle>/intro', methods = ['GET'])
def get_group_intro(twitter_handle):

	target_user = twitter_handle
	check_list = request.values['list']

	check_list = check_list.rsplit(',')

	reply = []
	
	threads = [] 

	for base_user in check_list:
		threads.append(GetConnectionsThread(base_user,target_user)) 

	[x.start() for x in threads]
	[x.join() for x in threads] 
	
	for thread in threads:

		temp_reply = thread.reply
		
		reply.append(temp_reply)
	
	return json.dumps(reply)

#-------------------------
def debug():

	return

#------------------
if __name__ == '__main__':

	import sys 
	debug()