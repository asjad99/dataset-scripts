twitter-tools
=============

Tools/scripts for working with Twitter's API 

monitor/
==========

Monitor a given twitter_handle for a verification tweet. 

> http://twitter-tools.halfmoonlabs.com/monitor/tweets?onename_username=roundedbygravity&twitter_handle=ilikevests&call_back_url=http://onename.io&time_out=1

Call to this end-point returns immediately and runs a background thread to do the polling. In the first minute polling is done at the interval of 5 seconds (fast polling) and after one minute at the interval of 15 seconds (normal polling). Polling timeouts after the specific timeout period. Input parameters:

* "onename_username" -- the OneName username for which we need to check the tweet
* "twitter_handle" -- twitter handle to monitor the tweets 
* "call_back_url" -- this is where the POST request is sent
* "time_out" -- in minutes (a time_out of 1 will result in polling for 1 minute and so on, time_out of zero turns repeated polling off and only one check is performed)

Response from background polling is in the format {"url":"","api_key":""} and no response is posted if no tweet was found.
