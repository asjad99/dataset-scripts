#!/usr/bin/env python
#-----------------------
# Copyright 2013 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

import tweepy

from common import *
from graph.twitter.config import *  

c = MongoClient()

twitter_graph = c['twitter_graph']

#---------------------------------------
#making the queue global, so it gets reused
from twitter_auth import TwitterQueues
twitter_q = TwitterQueues()

#get an appropriate account from the pool
users_handle = twitter_q.get_new_handle('users')

#---------------------------------------
class TwitterUser(object):
    '''
        a class for Twitter users
    '''

    def __init__(self, twitter_handle,user_type="normal",data=None):

        #internally always use lower case for twitter_handles
        twitter_handle = twitter_handle.lower() 

        self.twitter_handle = twitter_handle
        self.user = twitter_graph.users.find_one({'twitter_handle':twitter_handle})
        
        #--------------------------------
        #if no local user, create one and fetch details from API
        if(self.user is None):

            if(user_type == "minimal"):
                self.user = data 
            else:
                self.user = user_details_from_handle(twitter_handle)
            
            twitter_graph.users.save(self.user)
        #--------------------------------

        #don't fetch friends/followers by default 
        fetch_friends = False
        fetch_followers = False 

        if(user_type == "normal"):

            #if normal user and no friends in cache, fetch
            if(len(self.user['friends']) == 0):
                fetch_friends = True

            if(len(self.user['followers']) == 0):
                fetch_followers = True 

        elif(user_type == "target"):

            if(len(self.user['friends']) == 0):
                fetch_friends = True

        #--------------------------
        if(fetch_friends):
            self.save_friends()

        if(fetch_followers):
            self.save_followers()

    #---------------------------------------
    def should_fetch(self, graph_type):

        now = datetime.now()

        if(graph_type == 'followers'):
            fetched_time = self.user['followers_fetch_time']
        elif(graph_type == 'friends'):
            fetched_time = self.user['friends_fetch_time']

        #if fetched more than a month back, yes go fetch
        if(now - fetched_time > timedelta(days = FETCHED_RESULTS_EXPIRY)):
            return True 
        else:
            return False

    #---------------------------------------
    def fetch_if_stale(self):

        if(self.should_fetch('friends')):
            if(DEBUG): log.debug("%s: Yes, should fetch friends", self.twitter_handle)
            self.save_friends()
        else:
            if(DEBUG): log.debug("%s: No, should not fetch friends", self.twitter_handle)
        
        if(self.should_fetch('followers')):
            if(DEBUG): log.debug("%s: Yes, should fetch followers", self.twitter_handle)
            self.save_followers()
        else:
            if(DEBUG): log.debug("%s: No, should not fetch followers", self.twitter_handle)

    #---------------------------------------
    def save_friends(self):

        limit_reached = False

        results, limit_reached = get_graph(self.twitter_handle,'friends')
        self.user['friends'] = results
        
        self.user['friends_fetch_time'] = datetime.now()

        if(limit_reached):
            self.user['friends_limit_reached'] = True
        else:
            self.user['friends_limit_reached'] = False

        twitter_graph.users.save(self.user)

    #---------------------------------------
    def save_followers(self):

        limit_reached = False

        results, limit_reached = get_graph(self.twitter_handle,'followers')
        self.user['followers'] = results
        
        self.user['followers_fetch_time'] = datetime.now()

        if(limit_reached):
            self.user['followers_limit_reached'] = True
        else:
            self.user['followers_limit_reached'] = False

        twitter_graph.users.save(self.user)

#---------------------------------------
def get_graph(twitter_handle,graph_type):
        
    results = []
    handle = twitter_q.get_new_handle(graph_type)

    if(DEBUG): log.debug("Using account: %s", handle.print_twitter_handle())

    #----------------------------
    #internal function
    def get_results(handle,next_cursor):

        partial_results = []

        if(graph_type == 'followers'):
            cursor = tweepy.Cursor(handle.api.followers_ids, screen_name=twitter_handle)
        elif(graph_type == 'friends'):
            cursor = tweepy.Cursor(handle.api.friends_ids, screen_name=twitter_handle)
        else:
            cursor = None 
        
        iterator= cursor.pages()

        iterator.next_cursor=next_cursor

        for page in cursor.pages():

            partial_results += page

            next_cursor=iterator.next_cursor

            if handle.is_valid():
                pass
            else:
                #if handle is no longer valid, come back with a new one
                break 
                
        return partial_results, next_cursor
    #----------------------------

    # -1 tells twitter that this is the start
    next_cursor = -1

    limit_reached = False 

    while(1):
 
        partial_results, next_cursor = get_results(handle,next_cursor)

        if(next_cursor > 0):
            handle = twitter_q.get_new_handle(graph_type)
            if(DEBUG): log.debug("Switching to account: %s", handle.print_twitter_handle())
            results += partial_results

            #if a user has too many friends/followers, limit to some number
            #mainly there because of API limits, can remove later
            if(len(results) >= MAX_CONNECTIONS and ONLINE_FETCH):
                limit_reached = True 
                break
        else:
            # next_cursor of 0 means all pages are done
            results += partial_results
            break

    if(DEBUG): log.debug("Fetched: %s", len(results))

    return results, limit_reached 

#---------------------------------------

def get_tweets(twitter_handle):

    results = []
    handle = twitter_q.get_new_handle('timeline')

    if(DEBUG): log.debug("Using account: %s", handle.print_twitter_handle())

    #-------------------------------
    #for status in tweepy.Cursor(api.user_timeline).items(200):
    #user = tweepy.api.get_user('BobMetcalfe')

    #flags
    counter = 0
    calls_made = 0
    errors_got = 0
    in_error = False

    output = ""

    try:
        result = handle.api.user_timeline(id=tweet_user, count=TWEETS_PERCALL, include_rts=1)
        print "Call #" + str(calls_made)
        calls_made += 1
    except TweepError as e:
        print str(e)
        return

    length = len(result) 
    if(length == 0):
        return

    for tweet in result:
        print tweet 
        counter += 1

    temp = result[length-1]
    last_id = temp.id

    print last_id

#----------------------------------
def user_details_from_handle(twitter_handle):
  
    import requests

    API_URL = 'https://api.twitter.com/1.1/users/lookup.json'
    
    global users_handle
    #get an appropriate account from the pool
    if users_handle.is_valid(): 
        pass
    else:
        users_handle = twitter_q.get_new_handle('users')

    oauth = users_handle.perform_requests_auth()

    lookup = []
    lookup.append(twitter_handle)

    r = requests.get(url=API_URL, auth=oauth, params = {'screen_name':lookup})

    if(r.status_code == 404):
        pass
    else:
    
        full_result = r.json()

        i = full_result[0]

        temp_user = {}
        
        temp_user['profile_image_url'] = i['profile_image_url']
        temp_user['twitter_handle'] = i['screen_name'].lower()
        temp_user['full_name'] = i['name'] 
        temp_user['twitter_id'] = i['id']
        temp_user['friends'] = []
        temp_user['followers'] = []
        
    return temp_user

#---------------------------------------
def get_user_details(lookup_list):

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
        pass
    else: 
        users_handle = twitter_q.get_new_handle('users')

    print "Using handle: " + users_handle.print_twitter_handle()

    oauth = users_handle.perform_requests_auth()

    r = requests.get(url=API_URL, auth=oauth, params = {'screen_name':lookup_ids})
    r = requests.get(url=API_URL, auth=oauth, params = {'user_id':lookup_ids})

    reply = []

    if(r.status_code == 404):
        pass
    else:
    
        full_result = r.json()

        for i in full_result:

            temp_user = {}
        
            temp_user['profile_image_url'] = i['profile_image_url']
            temp_user['twitter_handle'] = i['screen_name'].lower()
            temp_user['full_name'] = i['name'] 
            temp_user['twitter_id'] = i['id']
            #new_user = TwitterUser(temp_user['twitter_handle'],user_type="minimal",data=temp_user)

            reply.append(temp_user)
    
    return reply

#---------------------------------------
def get_connection_details(lookup_list):

    '''
        given a list of relationships with Twitter users (for current authenticated user)
        e.g., if folowing that user
    '''

    import requests

    API_URL = 'https://api.twitter.com/1.1/friendships/lookup.json'
    
    screen_names = "" 

    for i in lookup_list:
        screen_names += str(i) + ', '

    screen_names = screen_names.rstrip(' ')

    
    oauth = handle.perform_requests_auth()

    r = requests.get(url=API_URL, auth=oauth, params = {'screen_name':screen_names})

    reply = []

    if(r.status_code == 404):
        pass
    else: 
        return r.json()

#---------------------------------------
def debug():

    new_user = TwitterUser('to',user_type="minimal")

    return 

#---------------------------------------
    
if __name__ == "__main__":

    debug()
