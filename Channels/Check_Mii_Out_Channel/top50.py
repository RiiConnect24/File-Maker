from cmoc import QuickList, Prepare, ResetList
import MySQLdb
from json import load
from time import sleep

with open("/var/rc24/File-Maker/Channels/Check_Mii_Out_Channel/config.json", "r") as f:
    config = load(f)
# get the top 50 most popular miis sorted by their permanent likes and add them to pop_list


db = MySQLdb.connect("localhost", config["dbuser"], config["dbpass"], "cmoc")
cursor = db.cursor()

cursor.execute(
    "SELECT mii.entryno, mii.initial, mii.permlikes, mii.skill, mii.country, mii.miidata, artisan.miidata, artisan.craftsno, artisan.master FROM mii, artisan WHERE mii.craftsno=artisan.craftsno ORDER BY permlikes DESC LIMIT 50"
)
miilist = cursor.fetchall()

for country in [0, 150]:
    ql = QuickList()
    pr = Prepare()

    data = ql.build("PL", miilist, country)

    with open( 
        "{}/{}/pop_list.ces".format(config["miicontest_path"], country), "wb"
    ) as file:
        file.write(pr.prepare(data))