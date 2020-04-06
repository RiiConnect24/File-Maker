from cmoc import EntryList, Prepare
import MySQLdb
from json import load

with open("/var/rc24/File-Maker/Channels/Check_Mii_Out_Channel/config.json", "r") as f:
        config = load(f)

db = MySQLdb.connect('localhost', config['dbuser'], config['dbpass'], 'cmoc', charset='utf8mb4')
cursor = db.cursor()
el = EntryList()
pr = Prepare()

cursor.execute('SELECT id FROM contests WHERE status = \'judging\'')
ids = cursor.fetchall()

for id in ids:
	id = id[0]
	cursor.execute('SELECT craftsno, miidata FROM conmiis WHERE contest = %s ORDER BY RAND()', [id])
	result = cursor.fetchall()
	miis = []
	for i in result:
		miis.append((i[0], i[1]))

	build = el.build(id, miis)

	for e in range(len(build)):
		with open('{}/contest/{}/entry_list{}.ces'.format(config['miicontest_path'], id, e + 1), 'wb') as file:
			file.write(pr.prepare(build[e]))

		with open('decfiles/contests/{}/entry_list{}.dec'.format(id, e + 1), 'wb+') as file:
			file.write(build[e])

db.close()
