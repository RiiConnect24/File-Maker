from cmoc import BestList, Prepare
import MySQLdb
from json import load

with open("/var/rc24/File-Maker/Channels/Check_Mii_Out_Channel/config.json", "r") as f:
    config = load(f)

db = MySQLdb.connect(
    "localhost", config["dbuser"], config["dbpass"], "cmoc", charset="utf8mb4"
)
cursor = db.cursor()
bl = BestList()
pr = Prepare()

cursor.execute("SELECT id FROM contests WHERE status = 'results'")
ids = cursor.fetchall()

for id in ids:
    id = id[0]
    cursor.execute(
        "SELECT conmiis.entryno, conmiis.craftsno, conmiis.miidata, artisan.miidata, artisan.country, artisan.master FROM conmiis, artisan WHERE conmiis.craftsno = artisan.craftsno AND conmiis.contest = %s ORDER BY conmiis.likes DESC LIMIT 50",
        [id],
    )
    miis = cursor.fetchall()

    build = bl.build(id, miis)

    with open(
        "{}/contest/{}/best_list.ces".format(config["miicontest_path"], id), "wb"
    ) as file:
        file.write(pr.prepare(build))

    with open("decfiles/contests/{}/best_list.dec".format(id), "wb+") as file:
        file.write(build)

db.close()
