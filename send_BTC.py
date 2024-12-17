import csv
import json
from urllib import urlopen
import bitcoinrpc 
from bitcoinrpc.exceptions import *
from config import * 

bitcoind = bitcoinrpc.connect_to_remote(BITCOIND_USER, BITCOIND_PASSWD, host=BITCOIND_SERVER, port=BITCOIND_PORT, use_https=BITCOIND_USE_HTTPS)

passphrase = '<Enter passphrase here>'

#------------------------------
#helper function
def unlock_wallet(passphrase, timeout = 10):

    info = bitcoind.walletpassphrase(passphrase, timeout, True)
    return info             #info will be True or False

#------------------------------

#Step 1: Read .csv file
with open('usernames.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in csvreader:
        username = row[0]
        bitcoin_amount = row[1]

        #Step 2:get the bitcoin address using onename.io API call
        url = "http://onename.io/" + username + ".json"
        data = json.loads(urlopen(url).read())
       

        try:
            bitcoin_address = data['bitcoin']['address']
        except:
            bitcoin_address = ""

        #Step 3: send bitcoins, using bitcoind to that address  
        if bitcoin_address != "":
            print username
            print bitcoin_address
           
            #unlock the wallet 
            if not unlock_wallet(passphrase):
                print "Wallet is not unlocked"
                break

            #send the bitcoins...
            print "Sending " + bitcoin_amount + " BTC to " + bitcoin_address

            try:
                status = bitcoind.sendtoaddress(bitcoin_address, float(bitcoin_amount))
                print status
            except Exception as e:
                print str(e)

            print "\n"

            