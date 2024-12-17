#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

from config import DEBUG, PORT, SERVER, TWEETS_NUM, SLEEP_TIME_INITIAL, SLEEP_TIME_LATER, SLEEP_CUTOFF
from config import TWITTER_APP_ID, TWITTER_APP_SECRET, MASTER_API_KEY

from common import log

import json
import tweepy
from time import sleep

from flask import Flask, render_template, url_for, request, session, redirect, jsonify, make_response

app = Flask(__name__)

token_counter = 0

from pymongo import MongoClient
client = MongoClient()
twitter_db = client['twitter-tools']
twitter_tokens = twitter_db.tokens

from threading import Thread, current_thread
import requests 

#-----------------------------------------
@app.route('/')
def index():
	return '<hmtl><body>Welcome to the twitter-tools server of <a href="http://halfmoonlabs.com">Halfmoon Labs</a>.</body></html>'

#-----------------------------------------
@app.route('/monitor/tweets')
def check_tweets():

	onename_username = request.args.get('onename_username')
	twitter_handle = request.args.get('twitter_handle')
	call_back_url = request.args.get('call_back_url')
	time_out = request.args.get('time_out') 

	response = {}
		
	if onename_username is None or twitter_handle is None or call_back_url is None or time_out is None:
		response['message'] = 'Error: required: onename_username, twitter_handle, call_back_url, time_out'
		response['success'] = False
	else:
		response["message"] = "Request received"
		response['success'] = True 

		log.debug("New request: %s %s %s %s",onename_username,twitter_handle,call_back_url,time_out)
		thread = Thread(target=check_tweets_loop, args=(onename_username,twitter_handle,call_back_url,time_out))
		thread.start()
	
	return json.dumps(response)

#-----------------------------------------
def check_tweets_loop(onename_username,twitter_handle,call_back_url,time_out):

	thread = current_thread()

	log.debug("In %s", thread.name)

	time_out = 60 * int(time_out) #convert to seconds

	api = get_api()

	response = {} 

	headers = {'content-type': 'application/json'}
  
	response["url"] = None 
	response["api_key"] = MASTER_API_KEY 

	#no tweet found with verification data; lets poll the api time and again
	sleep_track = 0
	sleep_time = SLEEP_TIME_INITIAL

	while(True):

		try:

			#fetch last 10 tweets, check if verification tweet was one of them
			statuses = api.user_timeline(twitter_handle,count=TWEETS_NUM)
		
			for status in statuses: 
		
				if onename_found(status.text, onename_username):
					response["url"] = "https://twitter.com/" + twitter_handle + "/status/" + status.id_str
					requests.post(call_back_url, data=json.dumps(response), headers=headers)
					log.debug(json.dumps(response))            
					log.debug("%s exiting", thread.name)
					log.debug('-' * 5)
					return response
		except:
			api = get_api()

		#throlle down poll rate after the initial polling
		if sleep_track > SLEEP_CUTOFF:
			sleep_time = SLEEP_TIME_LATER

		if sleep_track >= time_out:
			break

		log.debug("sleeping: %s", sleep_time) 
		sleep(sleep_time)
		
		sleep_track = sleep_track + sleep_time 

	log.debug("%s exiting", thread.name)
	log.debug('-' * 5)
	return response

#-----------------------------------
@app.errorhandler(500)
def internal_error(error):

	reply = []
	return json.dumps(reply)

#-----------------------------------
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'error': 'Not found' } ), 404)

#-----------------------------------------
def read_tokens():

	"""reads auth tokens from mongoDB and returns in a list"""
	
	tokens = []
	
	for token in twitter_tokens.find():
		item = {}
		item['token'] = token['oauth_token']
		item['secret'] = token['oauth_token_secret']
		item['username'] = token['username']
		tokens.append(item)

	return tokens

tokens = read_tokens()

#-----------------------------------------
def get_token():

	global token_counter

	if token_counter < len(tokens) - 1:
		token_counter += 1
	else:
		token_counter = 0

	return tokens[token_counter]

#-----------------------------------------
def get_api():
   
	#Use the tokens one after the other in a serial fashion
	token = get_token()

	auth = tweepy.OAuthHandler(TWITTER_APP_ID, TWITTER_APP_SECRET)
	auth.set_access_token(token['token'], token['secret'])

	api = tweepy.API(auth)
	
	try:
		status = api.rate_limit_status(resources='statuses')
	except:
		return get_api()

	remaining = status['resources']['statuses']['/statuses/user_timeline']['remaining']

	if remaining > 10:

		log.debug("using user: %s", token['username'])
		log.debug("token counter: %s", token_counter)

		return api
	else:
		log.debug("%s got rate-limited", token['username'])
		return get_api()

#-----------------------------------------
def onename_found(search_text, username):
	
	search_text = search_text.lower()

	if "verifymyonename" in search_text and ("+" + username) in search_text:
		return True
	elif "verifying myself" in search_text and "bitcoin username" in search_text and ("+" + username) in search_text:
		return True
	elif "verifying myself" in search_text and "bitcoin username" in search_text and username in search_text:
		return True

	return False

#------------------------------------------

if __name__ == '__main__':
	app.run(debug = DEBUG, host = SERVER, port= PORT)