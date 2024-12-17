#This script will filter users who have an email that is used for 5+ OneName profiles

from collections import defaultdict
import pymongo
from pymongo import Connection

con = Connection()
db = con['onename']
users = db.review

spammers = defaultdict(int)

for user in users.find():

    try:
        email = user['email']
        reply = users.find({"email":email})

        if reply.count() > 5:
            print email
            user['accepted'] = False
            users.save(user)
            spammers[email] += 1
            
    except:
        pass

print "\n\nhere are the spammers:\n"
print spammers