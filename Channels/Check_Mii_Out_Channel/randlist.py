from cmoc import NumberedList, Prepare
import MySQLdb
from json import load

with open("/var/rc24/File-Maker/Tools/CMOC/config.json", "r") as f:
        config = load(f)

ql = NumberedList()
pr = Prepare()

db = MySQLdb.connect('localhost', config['dbuser'], config['dbpass'], 'cmoc')
cursor = db.cursor()

#grab bag is extremely unpredictable and can cause server spam or crash wiis if done incorrectly
#the code below is basically all just trial and error

a = ([150, 150 ,150, 100, 100, 100, 100, 50, 0, 0])

bl = 0
for n in (a):
	bl += 1
	miilist = []
	artisanlist = []

	cursor.execute('SELECT craftsno,entryno FROM mii WHERE permlikes<25 ORDER BY RAND() LIMIT %s', [n]) #idk how this works it needs to be figured out
	numbers = cursor.fetchall()

	for i in range(len(numbers)): #add the artisan data to each mii based on their craftsno
		cursor.execute('SELECT entryno,initial,permlikes,skill,country,miidata FROM mii WHERE craftsno = %s AND entryno = %s', (numbers[i][0], numbers[i][1]))
		mii = cursor.fetchone()
		cursor.execute('SELECT miidata,craftsno,master FROM artisan WHERE craftsno = %s', [numbers[i][0]])
		artisan = cursor.fetchone()
		if artisan == None:
			with open('./logs/randlist.log', 'a') as log:
				log.write('ERROR: ENTRYNO {} HAS NO EXISTING ARTISAN WITH CRAFTSNO {}\n'.format(numbers[i][1], numbers[i][0]))

			print('ERROR: ENTRYNO {} HAS NO EXISTING ARTISAN WITH CRAFTSNO {}\n'.format(numbers[i][1], numbers[i][0]))
			pass

		else:
			miilist.append(mii + artisan)

	list_type = ('RL' + str(bl)) 
	print('{}/150/bargain_list{}.ces'.format(config['miicontest_path'], str(bl).zfill(2)))
	print(n)
	ql = NumberedList()

	data = ql.build(list_type, miilist)

	with open('{}/150/bargain_list{}.ces'.format(config['miicontest_path'], str(bl).zfill(2)), 'wb') as file:
		file.write(pr.prepare(data))

	with open('decfiles/bargain_list/bargain_list{}.dec'.format(str(bl).zfill(2)), 'wb') as file:
		file.write(data)

a = ([150, 150 ,150, 100, 100, 100, 100, 50, 0, 0])
nl = 0
for t in (a):
	nl += 1
	miilist = []
	artisanlist = []

	cursor.execute('SELECT craftsno,entryno FROM mii ORDER BY entryno DESC LIMIT %s',[t]) #idk how this works it needs to be figured out
	numbers = cursor.fetchall()

	for i in range(len(numbers)): #add the artisan data to each mii based on their craftsno
		cursor.execute('SELECT entryno,initial,permlikes,skill,country,miidata FROM mii WHERE craftsno = %s AND entryno = %s', (numbers[i][0], numbers[i][1]))
		mii = cursor.fetchone()
		cursor.execute('SELECT miidata,craftsno,master FROM artisan WHERE craftsno = %s', [numbers[i][0]])
		artisan = cursor.fetchone()
		miilist.append(mii + artisan)

	list_type = ('NL' + str(nl)) 
	ql = NumberedList()
	print('{}/150/new_list{}.ces'.format(config['miicontest_path'], str(nl).zfill(2)))

	data = ql.build(list_type, miilist)
	with open('{}/150/new_list{}.ces'.format(config['miicontest_path'], str(nl).zfill(2)), 'wb') as file:
		file.write(pr.prepare(data))

	with open('decfiles/bargain_list/new_list{}.dec'.format(str(nl).zfill(2)), 'wb') as file:
		file.write(data)

db.close()