from cmoc import QuickList, Prepare
import MySQLdb
from json import load
from time import sleep

with open("/var/rc24/File-Maker/Channels/Check_Mii_Out_Channel/config.json", "r") as f:
        config = load(f)
#get the top 50 most popular miis sorted by their permanent likes and add them to pop_list

ql = QuickList()
pr = Prepare()

db = MySQLdb.connect('localhost', config['dbuser'], config['dbpass'], 'cmoc')
cursor = db.cursor()

cursor.execute('SELECT mii.entryno, mii.initial, mii.permlikes, mii.skill, mii.country, mii.miidata, artisan.miidata, artisan.craftsno, artisan.master FROM mii, artisan WHERE mii.craftsno=artisan.craftsno ORDER BY permlikes DESC LIMIT 50')
miilist = cursor.fetchall()

data = ql.build('PL', miilist)
with open('{}/150/pop_list.ces'.format(config['miicontest_path']), 'wb') as file:
	file.write(pr.prepare(data))
