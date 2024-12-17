
#!/usr/bin/env python
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------
import json
import requests
import logging
import sys
import logging
import datetime
import relativedelta

"""
README:

About:
Script loads btc_address from 'addresses.txt' file and
fetches balance and transactions details...finally prints the overall account stats 

Input:
	addresses.txt file in the same directory as that of this file.

Output:
script products Five output files if you run it the following way:

	fetch_account-details.py > all_account_details.json

all_account_details.json (contains all account balances and no. of transactions)
balance_info.txt (contains account  details with balances > 0)
error_accounts_details.txt (contains error stats)
stats.txt (contains overall stats related to all accounts balance)
"""

addresses_list = []
results_list = []
error_list = []
postive_balance_accounts = []

hasBalance_counter = 0
Total_accounts= 0
Total_sum = 0
average_balance = 0
active_account_counter = 0


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_balance(address):
	logger.info('--------fetching balance for address-------' + address)
	
	try:
		r = requests.get('http://blockchain.info/address/' + address + '?format=json')
		return r.json()
	
	except Exception as e:
		error_list.append(address)
		return None 

#load addresses
f = open('addresses.txt')

for line in f.readlines():≠
    addresses_list.append(line.strip())
f.close()


#remove dublicates
addresses_list = list(set(addresses_list))

temp_count = 0 

#fetch account balances
sys.stdout.write('[')
for address in addresses_list:
	"""
	#for debugging uncomment"
	if temp_count > 10:
		break
	else:
		temp_count += 1
	"""
	

	account_balance = {} 

	result = fetch_balance(address)

	if result:
		account_balance['address'] = address 
		account_balance['balance'] = result['final_balance']
		account_balance['total_transcations'] = result['n_tx']
		

		recent_transaction_counter = 0 
		if result['final_balance'] > 0:
			
			Total_sum += result['final_balance']
			
			hasBalance_counter += 1

			transactions_list = result['txs']
			
			for val in transactions_list:
				dt1 = datetime.datetime.fromtimestamp(val['time']) # 1973-11-29 22:33:09
				dt2 = datetime.datetime.fromtimestamp(1398781255) # 1977-06-07 23:44:50
				rd = relativedelta.relativedelta (dt2, dt1)

				if rd.months < 2:
					recent_transaction_counter += 1
				elif rd.months == 2 and rd.days == 0:
					recent_transaction_counter += 1
				
				if recent_transaction_counter > 0:
					active_account_counter += 1
			account_balance['recent_transcations'] = recent_transaction_counter
			postive_balance_accounts.append(account_balance)

		account_balance['recent_transcations'] = recent_transaction_counter

		print account_balance
		sys.stdout.write(',')
		#print('rd.months' + str(rd.months) + 'days:' + str(rd.days))


sys.stdout.write(']')

#dumps account details of balances 
account_info = {}
account_info['account_details'] = postive_balance_accounts

error_account_info = {}
error_account_info['account_details'] = error_list

with open('balance_info.txt', 'w') as outfile:
  json.dump(account_info, outfile)

with open('error_accounts_details.txt', 'w') as outfile:
	error_list = list(set(error_list))
	line = '\nNumber of addresses whose balance couldnt be fetched: ' + str(len(error_list))
	outfile.write(line)

	outfile.write('\nError Account details: \n')
	
	json.dump(error_account_info,outfile)

with open('stats.txt', 'w') as outfile:
	#print '\n\n\n'
	outfile.write('overall stats:') 

	outfile.write('total number of accounts: ' + str(len(addresses_list))) 

	outfile.write('\ntotal balance: ' + str(Total_sum))

	#excludes errornous addresses
	outfile.write('\nAverage balance: ' + str(Total_sum/(len(addresses_list)-len(error_list))))

	outfile.write('\nActive number of accounts(having done a transcation in last 60days): ' + str(active_account_counter)) 

#print '\nTotal number of accounts with a positive balance: ' + str(hasBalance_counter)
#print 'Their details:' + str(postive_balance_addresses)