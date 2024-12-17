
#!/usr/bin/env python
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------


import tweepy
import tweepy
import json
import twitter
from ast import literal_eval


#limit on no. of friends/followers of a single user
#works only when ONLINE_FETCH is True
MAX_CONNECTIONS = 100000

#change to False to remove limit on fetching followers/friends
ONLINE_FETCH = True 
#---------------------------------------------

from twitter_auth import TwitterQueues
twitter_q = TwitterQueues()

#get an appropriate account from the pool
users_handle = twitter_q.get_new_handle('friends')

"""
About: fetches twitter friends ids list of people with graham number = 2
Note: be sure to to put twitter_auth module in the same directory when running the script. 
and specify resources(to be checked for api rate limit) 
accordingly in the constructor of ratelimitthread class and inside the check_rate_limit function.
"""
#---------------------------------------------

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="HzlxMlfbLyPnMFslJ3aW51XpQ"
consumer_secret="ZhuAkiAs19c1tPqmfg1jq9wzd2NKaIw61qaIb9EhzzsrzQkK5e"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located 
# under "Your access token")
access_token="133430191-o5ouFcL7AZupJo9pAuyPC9gW20gejSkentmsZEBd"
access_token_secret="YNHEgwKH6fZFO9PUpn2TqeXf0yNxy1vPpGmpSJfsWO8fw"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


#---------------------------------------------
def fetch_friends_ids(twitter_handle):
	"""returns the friends id, given a twitter handle."""

	#--------------------
	#check if api limit has been reached. 

	global users_handle
	if users_handle.is_valid():
		pass
	else:
		users_handle = twitter_q.get_new_handle('friends')
		print "Using handle: " + users_handle.print_twitter_handle()

	#-------------------
	friends_ids_list = []

	print "fetch ids list of handle:" + twitter_handle

	for page in tweepy.Cursor(api.friends_ids, screen_name=twitter_handle).pages():
		friends_ids_list.extend(page)

	print "total friends ids feteched:" + str(len(friends_ids_list))

	return friends_ids_list

#-------------------------------------
print "loading file contents..." 

with open('fof_list_detailed.txt') as f:
    fof_list_detailed = [list(literal_eval(line)) for line in f]

fof_list_detailed = fof_list_detailed[0]

print "file loaded with items:" + str(len(fof_list_detailed))

#-------------------------------------
g3_friends_list = [] 

for friend in fof_list_detailed:
	friends_list = friend.get("friends_list",None)

	if friends_list:
		for user in friends_list:
			friends_dict = {}

			friends_dict["twitter_handle"] = user["twitter_handle"]
			friends_dict["graham_number"] = 2

			#friends_ids_list will have graham_number = 3
			friends_dict["friends_ids_list"] = fetch_friends_ids(user["twitter_handle"])

			g3_friends_list.append(friends_dict)


#-------------------------------------
#dump the fetched data
with open('g3_friends_ids_list.txt', 'w') as outfile:
	json.dump(g3_friends_list,outfile) 

			
	