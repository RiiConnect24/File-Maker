from cmoc import QuickList, Prepare
from datetime import timezone, datetime
import MySQLdb
from json import load

with open("/var/rc24/File-Maker/Tools/CMOC/config.json", "r") as f:
        config = load(f)

#get the top 99 artisans and adds them to popcrafts_list

ql = QuickList()
pr = Prepare()

db = MySQLdb.connect('localhost', config['dbuser'], config['dbpass'], 'cmoc', charset='utf8mb4')
cursor = db.cursor()

#100000993 is the RC24 gold pants artisan
cursor.execute('SELECT craftsno FROM artisan WHERE craftsno !=100000993 ORDER BY votes DESC LIMIT 100')
count = cursor.fetchall()

artisanlist = []

for i in range(len(count)): #add the artisan data to each mii based on their craftsno
	cursor.execute('SELECT master,lastpost FROM artisan WHERE craftsno = %s', [count[i][0]])
	result = cursor.fetchone()

	lastpost = int((datetime.now().replace(tzinfo=timezone.utc).timestamp() - result[1].replace(tzinfo=timezone.utc).timestamp())/60/60) #hours since artisan last posted
	master = int(result[0])

	if lastpost < 24: #if a new mii was uploaded within 24 hours, add new mii flag
		if master == 1:
			master = 3 #master artisan with new mii flag
		
		else:
			master = 2 #new mii flag

	cursor.execute('SELECT craftsno,miidata,popularity,country FROM artisan WHERE craftsno = %s', [count[i][0]])
	artisanData = cursor.fetchone()
	artisanData = artisanData[:2] + (master,) + artisanData[2:] #insert master into the tuple where it would normally be retrieved from the db lmao
	artisanlist.append(artisanData)

data = ql.popcraftsBuild(artisanlist)
with open('{}/150/popcrafts_list.ces'.format(config['miicontest_path']), 'wb') as file:
	file.write(pr.prepare(data))

with open('decfiles/popcrafts_list.dec', 'wb') as file:
	file.write(data)
