#!/usr/bin/env python
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

import json
from time import sleep
import tweepy
import requests

#app config...
CONSUMER_KEY = '294LA7eke4ZPLyTNsg8R8A'
CONSUMER_SECRET = '1dWCXhNhvfwxzcKdzdXkGtKrRFga9sHGgrMCNT7u78'

ACCESS_TOKEN = '184058498-bgt6cCnAzLfIzoGMUW5evZ0L6vZfrO9LDB7bTQm4'
ACCESS_SECRET = '5kR4QfcbZrQn5RjpxKPvH9VNWPWH00okspPxqIv7FU'

api = None


#-------------------------------------------------------
"""Connect to twitter using the provided credentials"""
def connect():
    
    #setup tweepy...
    global api
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)

#-------------------------------------------------------
def check_recent_tweets(onename_username, twitter_handle, call_back_url, time_out):
    
    response = {} 
    global api

    response["tweet_found"] = False 
    response["tweet_url"] = None 
    response["onename_username"] = onename_username 

    #fetch last 10 tweets, check if verification tweet was one of them (probably wasn't)
    statuses = api.user_timeline(count=10)
    for status in statuses:
        if onename_found(status.text, onename_username):
            response["tweet_found"] = True
            response["tweet_url"] = "https://twitter.com/" + twitter_handle + "/status/" + status.id_str
            #return response
            requests.post(call_back_url, data=response)
            
    #no tweet found with verification data; lets poll the api time and again
    sleep_time = 30
    sleep_track = 0

    while(True):
        sleep(sleep_time)
        sleep_track = sleep_track + sleep_time

        #call the api again...
        statuses = api.user_timeline(count=5)
        for status in statuses:
            if onename_found(status.text, onename_username):
                response["tweet_found"] = True
                response["tweet_url"] = "https://twitter.com/" + twitter_handle + "/status/" + status.id_str
                return response

        if sleep_track >= time_out:
            break

    #return response
    requests.post(call_back_url, data=response)

#-------------------------------------------------------
def onename_found(search_text, username):
    
    search_text = search_text.lower()

    if "verifymyonename" in search_text and ("+" + username) in search_text:
        return True
    elif "verifying myself" in search_text and "bitcoin username" in search_text and ("+" + username) in search_text:
        return True
    elif "verifying myself" in search_text and "bitcoin username" in search_text and username in search_text:
        return True

    return False


#call the connect function right at the start...
connect()    

check_recent_tweets('ibrahimahmed443', 'ibrahimahmed443', "http://127.0.0.1:5000/", 15 * 60)