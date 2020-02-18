from cmoc import BestList, Prepare
import MySQLdb
from json import load

with open("/var/rc24/File-Maker/Tools/CMOC/config.json", "r") as f:
        config = load(f)

db = MySQLdb.connect('localhost', config['dbuser'], config['dbpass'], 'cmoc', charset='utf8mb4')
cursor = db.cursor()
bl = BestList()
pr = Prepare()	

cursor.execute('SELECT id FROM contests WHERE status = \'results\'')
ids = cursor.fetchall()

for id in ids:
	id = id[0]
	cursor.execute('SELECT entryno, craftsno, miidata FROM conmiis WHERE contest = %s ORDER BY RAND() LIMIT 50', [id])
	miis = cursor.fetchall()

	miilist = []
	for mii in miis:
		cursor.execute('SELECT miidata, country, master FROM artisan WHERE craftsno = %s', [mii[1]])
		miilist.append(mii + cursor.fetchone())

	build = bl.build(id, miilist)
	with open('{}/contest/{}/best_list.ces'.format(config['miicontest_path'], id), 'wb') as file:
		file.write(pr.prepare(build))

	with open('decfiles/contests/{}/best_list.dec'.format(id), 'wb+') as file:
		file.write(build)

db.close()