from cmoc import ConDetail, Prepare
import MySQLdb
from json import load
from os import path, makedirs

with open("/var/rc24/File-Maker/Channels/Check_Mii_Out_Channel/config.json", "r") as f:
    config = load(f)

db = MySQLdb.connect(
    "localhost", config["dbuser"], config["dbpass"], "rc24_cmoc", charset="utf8mb4"
)
cursor = db.cursor()
cd = ConDetail()
pr = Prepare()

cursor.execute(
    "SELECT id, start, end, status, entrycount, topic, description FROM contests WHERE status != 'closed' AND status != 'waiting'"
)
contests = cursor.fetchall()

for i in contests:
    id = i[0]
    start = i[1]
    end = i[2]
    status = i[3]
    entrycount = i[4] - i[4] % 10  # must be rounded down to nearest 10
    print(entrycount)
    topic = i[5]
    description = i[6]
    data = cd.build(id, start, end, status, entrycount, topic, description)

    if not path.exists("{}/contest/{}".format(config["miicontest_path"], id)):
        makedirs("{}/contest/{}".format(config["miicontest_path"], id))

    with open(
        "{}/contest/{}/con_detail1.ces".format(config["miicontest_path"], id), "wb"
    ) as file:
        file.write(pr.prepare(data))

    if not path.exists("decfiles/contests/{}".format(id)):
        makedirs("decfiles/contests/{}".format(id))

    with open("decfiles/contests/{}/con_detail1.dec".format(id), "wb+") as file:
        file.write(data)

db.close()
