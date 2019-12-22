import MySQLdb
from json import load
from cmoc import WSR
from os import system

with open("/var/rc24/File-Maker/Tools/CMOC/config.json", "r") as f:
        config = load(f)

wsr = WSR()

db = MySQLdb.connect('localhost', config['dbuser'], config['dbpass'], 'cmoc')
cursor = db.cursor()

cursor.execute('SELECT craftsno,entryno FROM mii WHERE likes>0 ORDER BY likes DESC LIMIT 100') #dookie
numbers = cursor.fetchall()

if len(numbers) < 100: #if less than 100 miis have received at least 1 like, order by permlikes but don't show super popular miis
	with open('./logs/wsr.log', 'a') as log:
		log.write('Popular list has only {} miis. Ordering by permlikes instead.\n'.format(len(numbers)))
	cursor.execute('SELECT craftsno,entryno FROM mii WHERE permlikes<25 ORDER BY permlikes DESC LIMIT 100')
	numbers = cursor.fetchall()

miilist = []

for i in range(len(numbers)): #add the artisan data to each mii based on their craftsno
	cursor.execute('SELECT initial,miidata FROM mii WHERE craftsno = %s AND entryno = %s', (numbers[i][0], numbers[i][1]))
	mii = cursor.fetchone()
	cursor.execute('SELECT miidata FROM artisan WHERE craftsno = %s', [numbers[i][0]])
	artisan = cursor.fetchone()
	if artisan == None:
		with open('./logs/wsr.log', 'a') as log:
			log.write('ERROR: ENTRYNO {} HAS NO EXISTING ARTISAN WITH CRAFTSNO {}\n'.format(numbers[i][1], numbers[i][0]))

		print('ERROR: ENTRYNO {} HAS NO EXISTING ARTISAN WITH CRAFTSNO {}\n'.format(numbers[i][1], numbers[i][0]))
		pass

	else:
		miilist.append(mii + artisan)

ql = WSR().build(miilist)

with open('decfiles/wiisports.dec', 'wb') as file:
	file.write(ql)

path = config['miicontest_path']

with open('{}/dd/wiisports.dec'.format(path), 'wb') as file:
	file.write(ql)

#symlink all miidd country code files to wiisports.enc with its FULL directory path
system("python ./sign_encrypt.py -t enc -in '{}/dd/wiisports.dec' -out '{}/dd/wiisports.enc' -key 91D9A5DD10AAB467491A066EAD9FDD6F -rsa /var/rc24/key/miidd.pem".format(path, path))
