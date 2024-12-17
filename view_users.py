#This script will only returns profile that has been filtered out by email (step 1)

import json
import pymongo
from pymongo import Connection

con = Connection()
db = con['onename']
users = db.review

count = 0
start = 2499
end = 3000

for user in users.find():
    if 'accepted' in user and user.get('accepted') == False:
        continue

    if count >= start and count < end:
        
        print count, "=> ", user.get('username'), user.get('email'), json.loads(user.get('profile')).get('name').get('formatted')
        print "\n"
        
    count +=1
    
    if count >= end:
        break

#print "\ncount=" + str(count)


"""user = users.find_one({'username' : <name>})
user['accepted'] = False , 
users.save(user)"""

"""user = users.find_one({'username' : <name>})
user['unverified'] = True , 
users.save(user)"""

