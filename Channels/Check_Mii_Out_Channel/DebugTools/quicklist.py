from cmoc import QuickList, Prepare
import MySQLdb
from json import load

with open("./config.json", "r") as f:
	config = load(f)
	
#example script gets every single mii in the DB, then adds it to spot_list

ql = QuickList()
pr = Prepare()

db = MySQLdb.connect('localhost', config['dbuser'], config['dbpass'], 'cmoc')
cursor = db.cursor()

cursor.execute('SELECT craftsno,entryno FROM mii ORDER BY permlikes')
numbers = cursor.fetchall()

miilist = []
artisanlist = []

for i in range(len(numbers)): #add the artisan data to each mii based on their craftsno
	cursor.execute('SELECT entryno,initial,permlikes,skill,country,miidata FROM mii WHERE craftsno = %s AND entryno = %s ORDER BY permlikes', (numbers[i][0], numbers[i][1]))
	mii = cursor.fetchone()
	cursor.execute('SELECT miidata,craftsno,master FROM artisan WHERE craftsno = %s', [numbers[i][0]])
	artisan = cursor.fetchone()
	miilist.append(mii + artisan)

list_type = 'SL'

data = ql.build(list_type, miilist)

with open('{}/150/spot_list.ces'.format(config['miicontest_path']), 'wb') as file:
	file.write(pr.prepare(data))

with open('{}/150/spot_list.dec'.format(config['miicontest_path']), 'wb') as file:
	file.write(data)
