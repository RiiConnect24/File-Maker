from cmoc import QuickList, Prepare
import MySQLdb
from json import load
from time import sleep
from random import shuffle

with open("/var/rc24/File-Maker/Channels/Check_Mii_Out_Channel/config.json", "r") as f:
    config = load(f)

db = MySQLdb.connect("localhost", config["dbuser"], config["dbpass"], "rc24_cmoc")
cursor = db.cursor()

cursor.execute("SELECT COUNT(*) FROM mii WHERE likes > 0")
count = int(cursor.fetchone()[0])
print("Popular Count:", count)

# popular is always sorted by volatile likes first, but we combine miis ordered by permlikes to fill in the rest to equal 100 total miis
if count >= 1000:
    extraCount = 0
    count = 1000

else:
    extraCount = 1000 - count

cursor.execute(
    "SELECT mii.entryno, mii.initial, mii.permlikes, mii.skill, mii.country, mii.miidata, artisan.miidata, artisan.craftsno, artisan.master FROM mii, artisan WHERE mii.craftsno=artisan.craftsno ORDER BY mii.likes DESC LIMIT %s",
    [count],
)
popularMiis = cursor.fetchall()

cursor.execute(
    "SELECT mii.entryno, mii.initial, mii.permlikes, mii.skill, mii.country, mii.miidata, artisan.miidata, artisan.craftsno, artisan.master FROM mii, artisan WHERE mii.permlikes > 21 AND mii.craftsno=artisan.craftsno ORDER BY mii.entryno DESC LIMIT %s",
    [extraCount],
)
extraMiis = cursor.fetchall()

cursor.execute(
    "UPDATE mii SET likes = 0"
)  # reset everyone's likes, but not their permlikes

db.commit()
db.close()

res = []
combined = list(set(popularMiis + extraMiis))[:500]
shuffle(combined)
combined = tuple(combined)

for country in [0, 150]:
    # gets the most popular miis ordered by their volatile likes which resets to 0 when spot_list resets
    ql = QuickList()
    pr = Prepare()
    
    data = ql.build("SL", combined, country)

    with open(
        "{}/{}/spot_list.ces".format(config["miicontest_path"], country), "wb"
    ) as file:
        file.write(pr.prepare(data))

with open("decfiles/spot_list.dec", "wb") as file:
    file.write(data)
