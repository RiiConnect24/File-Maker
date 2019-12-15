from cmoc import QuickList, Prepare
from cmoc import QuickList, Prepare
import MySQLdb
from json import load
from time import sleep

with open("/var/rc24/File-Maker/Tools/CMOC/config.json", "r") as f:
        config = load(f)

#get the top 99 artisans and adds them to popcrafts_list

ql = QuickList()
pr = Prepare()

db = MySQLdb.connect('localhost', config['dbuser'], config['dbpass'], 'cmoc', charset='utf8mb4')
cursor = db.cursor()

cursor.execute('SELECT craftsno FROM artisan ORDER BY votes DESC LIMIT 100')
count = cursor.fetchall()

artisanlist = []

for i in range(len(count)): #add the artisan data to each mii based on their craftsno
	cursor.execute('SELECT craftsno,miidata,master,popularity,country FROM artisan WHERE craftsno = %s', [count[i][0]])
	artisanlist.append(cursor.fetchone())

data = ql.popcraftsBuild(artisanlist)
sleep(10) #10 seconds for the other scripts to finish
with open('{}/150/popcrafts_list.ces'.format(config['miicontest_path']), 'wb') as file:
	file.write(pr.prepare(data))

with open('decfiles/popcrafts_list.dec', 'wb') as file:
	file.write(data)
