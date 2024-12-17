
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


from twitter_auth import TwitterQueues
twitter_q = TwitterQueues()

#get an appropriate account from the pool
users_handle = twitter_q.get_new_handle('users')

#-------------------------------------------------------
def get_user_details(lookup_list):

    #print lookup_list

    '''
        given a list of Twitter IDs (or screen names) returns the actual Twitter users
    '''

    import requests

    API_URL = 'https://api.twitter.com/1.1/users/lookup.json'
    
    lookup_ids = ""
    
    for i in lookup_list:
        lookup_ids += str(i) + ', '

    lookup_ids = lookup_ids.rstrip(' ')

    global users_handle
    if users_handle.is_valid():
        print ("handle is valid")
        pass
    else: 
        users_handle = twitter_q.get_new_handle('users')
        print ("got here")
        print "Using handle: " + users_handle.print_twitter_handle()

    oauth = users_handle.perform_requests_auth()

    r = requests.get(url=API_URL, auth=oauth, params = {'screen_name':lookup_ids})
    r = requests.get(url=API_URL, auth=oauth, params = {'user_id':lookup_ids})

    reply = []

    if(r.status_code == 404):
        pass
    else:
    
        full_result = r.json()
       
        try:

            for i in full_result:

                temp_user = {}
        
                temp_user['twitter_handle'] = i['screen_name'].lower()
                temp_user['full_name'] = i['name'] 
                print temp_user

                reply.append(temp_user)
        except:
            print full_result
            exit()
            return None 
    
    return reply

def fetch_account_details(friend_list):
    """fetch the accounts details, 200 accounts at a time.  """

    counter = 0
    #to avoid api limits per call of 100. 
    temp_counter = 98
    user_details_list = [] 
    user_details = []

    while True:
        if temp_counter < len(friend_list):
            user_details = get_user_details(friend_list[counter:temp_counter])
            
            if user_details:
                user_details_list.extend(user_details)
            temp_counter += 98
            counter +=98
        else:
            user_details = get_user_details(friend_list[counter:len(friend_list)])     
            user_details_list.extend(user_details) 
            
            break

    return user_details_list

#load list of friends of friends of paulg
#-------------------------------------------------------
with open('paulg_followers_list_level1.txt') as f:
    fof_list = [list(literal_eval(line)) for line in f]

fof_list = fof_list[0]

print 'listed loaded with items:'
print len(fof_list)

fof_list_detailed = []

for friend in fof_list:
    twitter_handle = friend["twitter_handle"]
    
    print "fetching friend details of..." + twitter_handle

    #Note: follower_ids_list key is misleading. THey are basically friends of friends
    friends_ids_list = friend["follower_ids_list"]

    friends_list_detailed = fetch_account_details(friends_ids_list)

    #------------
    #append the fetched values

    fof_dict = {}

    fof_dict["twitter_handle"] = twitter_handle

    if friends_list_detailed:
        fof_dict["friends_list"] = friends_list_detailed

    fof_list_detailed.append(fof_dict)


# save the list containing details of fof of paulg
#-------------------------------------------------------
with open('fof_list_detailed.txt', 'w') as outfile:
    json.dump(fof_list_detailed,outfile) 




