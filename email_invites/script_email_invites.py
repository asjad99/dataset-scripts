#!/usr/bin/env python
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------
from ast import literal_eval
from pymongo import Connection
import pymongo
import sys
import json 

con = Connection()

#returns a twitter handle, given a twitter_url
def gethandle(twitter_url):

	handle = ""
	index = 0

	#print 'twitter_url' + twitter_url 

	index = twitter_url.find('.com/',index)

	handle = twitter_url[index + 5:]

	#recheck for any additional symbols after primary url 'http://twitter.com/'' string. 
	index = 0
	index = handle.find('/',index)

	while True:

			if handle.find('/',index) == -1:
				break
			else:
				handle = handle[index + 1:]
				#print handle
				if handle.find('&',index) != -1:
					break
				index = handle.find('/',0)

	#print 'final handle:'+ handle

	return handle

angellist_twitter_handles_list = []
#-------------------------------------------------------

#load angellist data(people having >1000 twitter followers)
with open('angel_list_with_follower_count.txt') as f:
    angellist_data = [list(literal_eval(line)) for line in f]


# angellist_data is a list of dictionaries with the following format:
#{"follower_count": 1252, "twitter_handle": "tommaxwelll", "full_name": "Tom Maxwell"}
angellist_data = angellist_data[0]

print 'total items loaded:' + str(len(angellist_data))
print 'memory usage(in bytes):' + str(sys.getsizeof(angellist_data))

#-------------------------------------------------------
#find crunchbase_url by using twitter_handles(of user with >1000 followers)
db = con['crunchbase_people_detail']	
posts = db.posts

posts.ensure_index("data.twitter_username")

counter_crunchbase_url = 0
#crunchbase_data = []
for entry in angellist_data:
	item = posts.find_one({"data.twitter_username":entry['twitter_handle']})
	
	if item:
		data = item['data']
		entry['crunchbase_url'] = data['crunchbase_url']
		counter_crunchbase_url = counter_crunchbase_url + 1 

print 'counter_crunchbase_url:'
print counter_crunchbase_url

#-------------------------------------------------------
#fetch email using the crunchbase_url and append to angellist_data(original)

db = con['crunchbase_people_emails']
users = db.posts

users.ensure_index("person_url")

final_list = [] 
counter = 0
for entry in angellist_data:
	crunchbase_url = entry.get('crunchbase_url', None)

	if crunchbase_url:
		user = users.find_one({"person_url":crunchbase_url})

		if user:
			counter = counter + 1
			email = user['email']
			entry['email'] = email
			final_list.append(entry)


print "counter:"
print counter 

#-------------------------------------------------------
#dump the entries with valid email and >1000 followers into a file
with open('email_invites_dataset.txt', 'w') as outfile:
    json.dump(final_list,outfile) 
#-------------------------------------------------------




