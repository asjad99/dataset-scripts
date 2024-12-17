#!/usr/bin/env python
#-----------------------
# Copyright 2013 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

from common import *
from graph.twitter.config import *  

from pymongo import MongoClient
c = MongoClient()
db = c['twitter_graph']

from get_graph import TwitterUser

#---------------------------------------
def get_connections(base_user_handle,target_user_handle):

	base_user = TwitterUser(base_user_handle)

	target_user = TwitterUser(target_user_handle,user_type="target")

	base_user.fetch_if_stale()
	target_user.fetch_if_stale()

	#people that the target follows/respects and who also follow you
	a = base_user.user['followers']
	b = target_user.user['friends']

	import collections

	a_multiset = collections.Counter(a)
	b_multiset = collections.Counter(b)

	overlap = list((a_multiset & b_multiset).elements())
	
	return overlap

#---------------------------------------
def check_direct_link(base_user_handle,target_user_handle):

	base_user = TwitterUser(base_user_handle)
	target_user = TwitterUser(target_user_handle,user_type="target")

	base_user.fetch_if_stale()
	target_user.fetch_if_stale()

	#check if target follows the base user
	a = base_user.user['twitter_id']
	b = target_user.user['friends']

	if a in b:
		return True 
	else:
		return False
	
#---------------------------------------
def fetch_with_wait(twitter_list,user_type="target"):

	for i in twitter_list:

		user = TwitterUser(i,user_type)
		user.fetch_if_stale()
		print i

#---------------------------------------
def debug():
	
	overlap = get_connections('muneeb','ryaneshea')

	print overlap 
	
#---------------------------------------
	
if __name__ == "__main__":

	import sys

	twitter_list = []

	temp = sys.argv[1]
	temp = temp.rsplit(',')

	user_type = "target"

	try:
		user_type = sys.argv[2]
	except:
		pass

	for i in temp:
		twitter_list.append(i)

	fetch_with_wait(twitter_list,user_type)

