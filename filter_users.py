#This script will mark the users accepted/unverified based on a given list

import json
import pymongo
from pymongo import Connection

con = Connection()
db = con['onename']
users = db.review

count = 0
start = 0
end = 1500

unaccepted = [
            'ffssixtynine', 'donation', 'root', 'jijojv', 'flickr', 'test2', 'pornhub', 'test3', 'redtube',
            'xvideo', 'test4', 'bskyb', 'acer', 'oracle', 'orange', 'laura', 'hitachi', 'reporter', 'bloomberg',
            'canon', 'coke', 'test1231234', 'love', 'mcdonalds','lolloloolol', 'jmg', 'webcamgirl', 'nyc',
            'ibrahim_shafi', 'moscow', 'gap', 'pizzahut', 'nsa', 'charity', '420', 'amex', 'wow', 'blackrock',
            'gamestop', 'coinsetter', 'dominos', 'salesforce', 'discover', 'circle', 'help', 'buttercoin',
            'cointerra', 'armory', 'whatsapp', 'payme', 'bitinstant', 'bitcoinity', 'sucker', 'nokia',
            'goldsilverbitcoin', 'rtbtc', 'cydia', 'whitehouse', 'macdonalds', 'bitcointalk', 'coinlab',
            'coinmarketcap', 'secondmarket', 'coinkite', 'bitcoin_otc', 'coinmarket', 'cryptostreet', 'theguardian',
            'zeroblock', 'bitcoinotc', 'macbookpro', 'coloredcoins', 'coinvalidation', 'bitcoincharts', 'btc_e',
            'vircurex', 'ripple', 'ghash', 'eligius', 'btcguild', 'discusfish', 'slush', 'campbx', 'hackforums',
            'bitmessage', 'bitcoinmillionaires', 'bitcoinbillionaires', 'bitcoinbillionaire','bitcoinmillionaire',
            'buy','slots','realestate','payments','escrow','hotel','cruises','12345','celebrity','vegas','lasvegas',
            'payday','lottery','roulette','jobs','investing','paper','banks','albi','loan','vacationrentals','diamonds',
            'vodka','yellow','testtest4','testtest5','testtest6','testtest7','testtest8','game','epic','kdog','arsenal' ,
            'lalu' ,'pikachu' ,'marcm','peace' ,'c01db33f' ,'price' ,'porntube' ,'cow' ,'baccarat' ,'caleb' ,'qqrqer','satoshi_nakamoto'
            ,'richie','markbot','mox','jespow','elad','h1d','mindsplit','freeroute','cmc','cooke','samo','asdasdasd','barack_obama','abqbitcoins'
            ,'jh','boobs4bitcoin','sexvideo','maroon5','lameduck','thanks','just4u','presidentbarackobama','doug222','hotfun','chadbean'
            ,'googleadvertising','taxes','thereisamajorprobleminaustralia','budapest','ether','csiga','bitcoinbillionaires','bitcoinbillionaire'
            ,'bitcoinmillionaire','sir','wiz','jedi','yolo','eleven','yoyo','conan','elrond','minniemouse','donaldduck','mickeymouse',
            'tinkerbell','mylesfong','gavinhall','bitcorati','cia','fbi','tradehill','ios','mikerowesoft','windowsphone','googlemaps',
            'satoshidice','java','redhat','googleplus','julianassange','cavirtex','microcenter','nvidia','amd','zip',
            'foursquare','pistos' ,'opus','shazam','coco','burt','kirk','reserve','atlas','abc123','abcd','alfred','mix','unicorn',
            'coffee','tea','trix','monkey','elf','geronimo','wamp','mine','myself','magic','pocket','save','eero'
        ]


unverified = [
            'btc', 'dicko', 'chairman', 'poker', 'hackjealousy', 'gu3', 'banglashi', 'drink', 'newyorktimes',
            'ruggero', 'eddwrx', 'cominariess', 'gabridome', 'lauri_love', 'seo', 'evol', 'the', 'xyz', 'treats_io',
            'dannyr', 'mediakoers', 'chill', 'mjh','tommaso','chyatt','oekie','morad', 'eyliad','ltc','todu','salmito','mist','hendrikjo',
            'patricia','deepa','tons0fun','tarin','douglasinc','midas','nhusuper','piro','gigcast','arnosenoner','emirates','kian','blizzard'
            ,'qp','mo','developers','ipsylon','mollyb','lem','mircea_popescu','jsw','bitly','princess','miguel','svi','elephant','lzr1900'
            ,'stefanix','tomriddle','benfeldman','nairne','basten','hideki','hshimo','satoshiart','snakies','greta','marta','ybot',
            'rciobani' ,'swordandscale','jff' ,'blackja','forkbomb','womanbrain','kevinz','bea','joed','draco18s','julienicole','pcboy' ,'nicson','tibet' ,'gmaxwell'
        ]

#mark all unaccepted users with accepted = False
for name in unaccepted:
    user = users.find_one({'username' : name})
    user['accepted'] = False
    users.save(user)

#mark all unverified users with unverified = True
for name in unverified:
    user = users.find_one({'username' : name})
    user['unverified'] = True
    users.save(user)
    