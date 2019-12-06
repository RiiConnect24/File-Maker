from cmoc import QuickList, Prepare
import MySQLdb
from json import load
from time import sleep

with open("/var/rc24/File-Maker/Tools/CMOC/config.json", "r") as f:
        config = load(f)
#get the top 50 most popular miis sorted by their permanent likes and add them to pop_list

ql = QuickList()
pr = Prepare()

db = MySQLdb.connect('localhost', config['dbuser'], config['dbpass'], 'cmoc')
cursor = db.cursor()

cursor.execute('SELECT craftsno,entryno FROM mii ORDER BY permlikes DESC LIMIT 50')
numbers = cursor.fetchall()

miilist = []

for i in range(len(numbers)): #add the artisan data to each mii based on their craftsno
	cursor.execute('SELECT entryno,initial,permlikes,skill,country,miidata FROM mii WHERE craftsno = %s AND entryno = %s', (numbers[i][0], numbers[i][1]))
	mii = cursor.fetchone()
	cursor.execute('SELECT miidata,craftsno,master FROM artisan WHERE craftsno = %s', [numbers[i][0]])
	artisan = cursor.fetchone()
	if artisan == None:
		with open('./logs/top50.log', 'a') as log:
			log.write('ERROR: ENTRYNO {} HAS NO EXISTING ARTISAN WITH CRAFTSNO {}\n'.format(numbers[i][1], numbers[i][0]))
			
		print('ERROR: ENTRYNO {} HAS NO EXISTING ARTISAN WITH CRAFTSNO {}\n'.format(numbers[i][1], numbers[i][0]))
		pass

	else:
		miilist.append(mii + artisan)

data = ql.build('PL', miilist)
sleep(30)
with open('{}/150/pop_list.ces'.format(config['miicontest_path']), 'wb') as file:
	file.write(pr.prepare(data))
