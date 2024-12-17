#!/usr/bin/env python
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------
import requests
from html2text import html2text
from urllib2 import HTTPError, urlopen
import urllib2
from urlparse import urlparse
from lxml.html import parse
import json
from lxml.cssselect import CSSSelector

#requirements:
#1. pip install cssselect 
#2. pip install lxml
#3. pip install requests
#4. pip install html2text

onename_id = 'ryanshea'
#onename_profile_url = 'onename.io/ryanshea'
onename_profile_url_json = 'https://onename.io/' + onename_id + '.json'

def read_link(link, server_root=None):
    try:
      #print ("read_link - link = " + link)
      #raise SystemExit
      url_parsed = urlparse(link)
      url = ""
      if url_parsed.netloc == "":
        url = NetworkIOManager.completeURL(server_root, link)
      else:
        url = link

      print ("------------------------")
      print ("read url = " + url)
      return parse(urlopen(url)).getroot()     
    except (HTTPError, IOError) as e:
      return None

def fetch_url_contents(url):
	try:
		print ("fetching url..." + url)
		r = requests.get(url)
		return r

	except Exception as e:
		print(e)
		return None 


def is_valid_proof(key, value, username):
    proof_url = get_proof_url(value["proof"], username)
    if "username" in value:
        site_username = value["username"]
        if site_username not in proof_url:
            return False
    r = requests.get(proof_url)
    search_text = html2text(r.text)
    if key == "twitter":
        search_text = search_text.replace("<s>", "").replace("</s>", "").replace("**", "")
    elif key == "github":
        pass
    elif key == "facebook":
        pass
    search_text = search_text.lower()
    if "verifymyonename" in search_text and ("+" + username) in search_text:
        return True
    return False

def get_proof_url(proof, username):
    proof_url = None
    if "url" in proof:
        proof_url = proof["url"]
    elif "id" in proof:
        if key == "twitter":
            proof_url = "https://twitter.com/" + username + "/status/" + proof["id"]
        elif key == "github":
            proof_url = "https://gist.github.com/" + username + "/" + proof["id"]
        elif key == "facebook":
            proof_url = "https://www.facebook.com/" + username + "/posts/" + proof["id"]
    return proof_url

def verify_profile_social_accounts():

	result = fetch_url_contents(onename_profile_url_json)

	result = result.json()

	proof_sites = ["twitter", "github"]

	for key, value in result.items():
		if key in proof_sites and type(value) is dict and "proof" in value:
			if is_valid_proof(key, value, "ryanshea"):
				print key + "profile verified"
			else:
				print key + "not verified"

verify_profile_social_accounts()


#to be deprecated...

""" 
print '-' * 15
print 'verfying url...'
print '-' * 15

result = fetch_url_contents(onename_profile_url_json)

result = result.json()

#print result

twitter = result['twitter']

proof_url = twitter['proof']

#print proof_url

proof_url =  proof_url['url']

print 'proof url:' + proof_url 

css_selector_for_twitter_handle = CSSSelector("p.js-tweet-text span.js-display-url")

html = read_link(proof_url)

twitter_handle = css_selector_for_twitter_handle(html)

#print(twitter_handle[0].text)

if twitter_handle[0].text == onename_profile_url:
	print '-' * 15
	print 'verified'
	print '-' * 15
else:
	print 'error: unable to verify'

"""


