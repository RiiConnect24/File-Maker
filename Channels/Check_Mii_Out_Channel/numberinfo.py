from cmoc import QuickList, Prepare, ResetList
import MySQLdb
from json import load
from time import sleep

with open("/var/rc24/File-Maker/Channels/Check_Mii_Out_Channel/config.json", "r") as f:
    config = load(f)
# get the top 50 most popular miis sorted by their permanent likes and add them to pop_list


db = MySQLdb.connect("localhost", config["dbuser"], config["dbpass"], "rc24_cmoc")
cursor = db.cursor()

cursor.execute('SELECT COUNT(*) FROM mii')
mii_count = int(cursor.fetchone()[0])

cursor.execute('SELECT COUNT(*) FROM artisan')
artisan_count = int(cursor.fetchone()[0])

ql = QuickList()
pr = Prepare()

data = ql.numberinfoBuild(mii_count, artisan_count)

with open( 
    "{}/150/number_info.ces".format(config["miicontest_path"]), "wb"
) as file:
    file.write(pr.prepare(data))
