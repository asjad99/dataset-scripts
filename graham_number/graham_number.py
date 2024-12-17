
#!/usr/bin/env python
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

import tweepy
import time
import tweepy
import json
import twitter
from ast import literal_eval


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

# * uncomment for testing * If the authentication was successful, you should
# see the name of the account print out
#print api.me().name

def fetch_friends_ids(twitter_handle):

	ids_list = []
	attempts = 0 
	print "fetching followers of account :" + twitter_handle

	while True:

		try:
			attempts = attempts + 1
			
			for page in tweepy.Cursor(api.friends_ids, screen_name=twitter_handle).pages():
				ids_list.extend(page)
				print "number of ids fetched so far = " + str(len(ids_list))
			
			break
	
		except:
			if attempts < 10
				print "limit reached....sleeping..."
				time.sleep(60)
			else 
				print "limited reached...exiting..."
				break 	

	print "total account ids feteched:" + str(len(ids_list))

	return ids_list

"""
#-------------------------------------
#fetching twitter followers list of paulg's account
#output will be a list of twitter_account_ids of the followers 
#-------------------------------------

ids_list = fetch_friends_ids()

with open('paulg_followers_list.txt', 'w') as outfile:
		json.dump(ids_list,outfile)

"""


"""
#-------------------------------------
#2. fetch user
#-------------------------------------

with open('paulg_followers_list.txt') as f:
    ids_list = [list(literal_eval(line)) for line in f]

ids_list = ids_list[0]

#fetch the account details 

user_details_list = []

counter = 0
for id in ids_list: 
	user = api.get_user(id)
	
	print user.name,user.screen_name
	
	counter = counter + 1
	
	if (counter % 30) == 0:
		print "feteched:" + len(user_details_list)
		print "sleeping..."	
		time.sleep(60)	

	user_details_list.append({"name":user.name,"twitter_handle":user.screen_name})

with open('paulg_followers_list_detailed.txt', 'w') as outfile:
	json.dump(user_details_list,outfile) 
"""

#-------------------------------------
#load the list of verified twitter ids
#-------------------------------------
with open('paulg_followers_list_detailed_cleaned.txt') as f:
    paulg_followers = [list(literal_eval(line)) for line in f]

counter = 0 

paulg_followers_list_level1 = []

paulg_followers = paulg_followers[0]

for follower in paulg_followers:
	
	follower_dict = {}

	twitter_handle = follower['twitter_handle'] 

	ids_list = fetch_friends_ids(twitter_handle)

	counter = counter + 1 

	follower_dict["twitter_handle"]  = twitter_handle
	
	follower_dict["follower_ids_list"] = ids_list

	paulg_followers_list_level1.append(follower_dict)

	if counter % 4 == 0:
		time.sleep(60)

with open('paulg_followers_list_level1_take2.txt', 'w') as outfile:
	json.dump(paulg_followers_list_level1,outfile) 



