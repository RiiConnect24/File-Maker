from cmoc import QuickList, Prepare
import MySQLdb
from json import load
from time import sleep

with open("/var/rc24/File-Maker/Tools/CMOC/config.json", "r") as f:
        config = load(f)

#gets the most popular miis ordered by their volatile likes which resets to 0 when spot_list resets
ql = QuickList()
pr = Prepare()

db = MySQLdb.connect('localhost', config['dbuser'], config['dbpass'], 'cmoc')
cursor = db.cursor()

cursor.execute('SELECT craftsno,entryno FROM mii WHERE permlikes<30 ORDER BY permlikes DESC LIMIT 100')
#cursor.execute('SELECT craftsno,entryno FROM mii WHERE likes>0 ORDER BY likes DESC LIMIT 100')
numbers = cursor.fetchall()

miilist = []

for i in range(len(numbers)): #add the artisan data to each mii based on their craftsno
	cursor.execute('SELECT entryno,initial,permlikes,skill,country,miidata FROM mii WHERE craftsno = %s AND entryno = %s', (numbers[i][0], numbers[i][1]))
	mii = cursor.fetchone()
	cursor.execute('SELECT miidata,craftsno,master FROM artisan WHERE craftsno = %s', [numbers[i][0]])
	artisan = cursor.fetchone()
	if artisan == None:
		with open('./logs/popular.log', 'a') as log:
			log.write('ERROR: ENTRYNO {} HAS NO EXISTING ARTISAN WITH CRAFTSNO {}\n'.format(numbers[i][1], numbers[i][0]))

		print('ERROR: ENTRYNO {} HAS NO EXISTING ARTISAN WITH CRAFTSNO {}\n'.format(numbers[i][1], numbers[i][0]))
		pass

	else:
		miilist.append(mii + artisan)

cursor.execute('UPDATE mii SET likes = 0') #reset everyone's likes, but not their permlikes

db.commit()
db.close()

data = ql.build('SL', miilist)

sleep(5) #5 seconds for the other scripts to finish
with open('{}/150/spot_list.ces'.format(config['miicontest_path']), 'wb') as file:
	file.write(pr.prepare(data))

with open('decfiles/spot_list.dec', 'wb') as file:
	file.write(data)
