from cmoc import NumberedList, Prepare
import MySQLdb
from json import load

with open("/var/rc24/File-Maker/Channels/Check_Mii_Out_Channel/config.json", "r") as f:
    config = load(f)

ql = NumberedList()
pr = Prepare()

db = MySQLdb.connect("localhost", config["dbuser"], config["dbpass"], "rc24_cmoc")
cursor = db.cursor()

# grab bag is extremely unpredictable and can cause server spam or crash wiis if done incorrectly
# the code below is basically all just trial and error

a = [150, 150, 150, 0, 0, 0, 0, 0, 0, 0]

bl = 0
for n in a:
    bl += 1

    cursor.execute(
        "SELECT mii.entryno, mii.initial, mii.permlikes, mii.skill, mii.country, mii.miidata, artisan.miidata, artisan.craftsno, artisan.master FROM mii, artisan WHERE mii.craftsno = artisan.craftsno AND mii.permlikes<25 ORDER BY RAND() LIMIT %s",
        [n],
    )  # idk how this works it needs to be figured out
    miilist = cursor.fetchall()

    list_type = "RL" + str(bl)

    for country in [0, 150]:
        ql = NumberedList()

        data = ql.build(list_type, miilist, country)

        with open(
            "{}/{}/bargain_list{}.ces".format(
                config["miicontest_path"], country, str(bl).zfill(2)
            ),
            "wb",
        ) as file:
            file.write(pr.prepare(data))

    with open(
        "decfiles/bargain_list/bargain_list{}.dec".format(str(bl).zfill(2)), "wb"
    ) as file:
        file.write(data)

a = [150, 150, 150, 0, 0, 0, 0, 0, 0, 0]
nl = 0
for t in a:
    nl += 1

    cursor.execute(
        "SELECT mii.entryno, mii.initial, mii.permlikes, mii.skill, mii.country, mii.miidata, artisan.miidata, artisan.craftsno, artisan.master FROM mii, artisan WHERE mii.craftsno = artisan.craftsno ORDER BY entryno DESC LIMIT %s",
        [t],
    )
    miilist = cursor.fetchall()

    list_type = "NL" + str(nl)

    for country in [0, 150]:
        ql = NumberedList()
        
        data = ql.build(list_type, miilist, country)

        with open(
            "{}/{}/new_list{}.ces".format(
                config["miicontest_path"], country, str(nl).zfill(2)
            ),
            "wb",
        ) as file:
            file.write(pr.prepare(data))

    with open(
        "decfiles/bargain_list/new_list{}.dec".format(str(nl).zfill(2)), "wb"
    ) as file:
        file.write(data)

db.close()
