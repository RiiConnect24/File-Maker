from cmoc import ConDetail, Prepare, Thumbnail, Photo
import MySQLdb
from json import load
from os import path, makedirs
import requests

with open("/var/rc24/File-Maker/Channels/Check_Mii_Out_Channel/config.json", "r") as f:
    config = load(f)

db = MySQLdb.connect(
    "localhost", config["dbuser"], config["dbpass"], "rc24_cmoc", charset="utf8mb4"
)
cursor = db.cursor()
cd = ConDetail()
pr = Prepare()
th = Thumbnail()
ph = Photo()

cursor.execute(
    "SELECT id, start, end, status, entrycount, topic_japanese, topic, topic_german, topic_french, topic_spanish, topic_italian, topic_dutch, description_japanese, description, description_german, description_french, description_spanish, description_italian, description_dutch, thumbnail_url, souvenir_url FROM contests WHERE status != 'closed' AND status != 'waiting'"
)
contests = cursor.fetchall()

for i in contests:
    id = i[0]
    start = i[1]
    end = i[2]
    status = i[3]
    entrycount = i[4] - i[4] % 10  # must be rounded down to nearest 10
    topics = [i[5], i[6], i[7], i[8], i[9], i[10], i[11]]
    descriptions = [i[12], i[13], i[14], i[15], i[16], i[17], i[18]]
    thumbnail_url = i[19]
    souvenir_url = i[20]

    for language in range(0, 7):
        if not topics[language] or not descriptions[language]:
            continue

        data = cd.build(id, start, end, status, entrycount, topics[language], descriptions[language])

        if not path.exists("{}/contest/{}".format(config["miicontest_path"], id)):
            makedirs("{}/contest/{}".format(config["miicontest_path"], id))

        with open(
            "{}/contest/{}/con_detail{}.ces".format(config["miicontest_path"], id, language), "wb"
        ) as file:
            file.write(pr.prepare(data))

        if not path.exists("decfiles/contests/{}".format(id)):
            makedirs("decfiles/contests/{}".format(id))

        with open("decfiles/contests/{}/con_detail{}.dec".format(id, language), "wb+") as file:
            file.write(data)

    if path.exists("/var/rc24/thumbnail/{}.jpg".format(id)) or thumbnail_url:
        if thumbnail_url:
            thumbnail = requests.get(thumbnail_url).content

            with open("/var/rc24/thumbnail/{}.jpg".format(id), "wb") as f:
                f.write(thumbnail)

        data = th.build(id)

        with open(
            "{}/contest/{}/thumbnail.ces".format(config["miicontest_path"], id), "wb"
        ) as file:
            file.write(pr.prepare(data))

        if not path.exists("decfiles/thumbnails/{}".format(id)):
            makedirs("decfiles/thumbnails/{}".format(id))

        with open("decfiles/thumbnails/{}/thumbnail.dec".format(id), "wb+") as file:
            file.write(data)

    if path.exists("/var/rc24/souvenir/{}.jpg".format(id)):
        if souvenir_url:
            souvenir = requests.get(souvenir_url).content

            with open("/var/rc24/souvenir/{}.jpg".format(id), "wb") as f:
                f.write(souvenir)

        data = ph.build(id)

        with open(
            "{}/contest/{}/photo.ces".format(config["miicontest_path"], id), "wb"
        ) as file:
            file.write(pr.prepare(data))

        if not path.exists("decfiles/souvenirs/{}".format(id)):
            makedirs("decfiles/souvenirs/{}".format(id))

        with open("decfiles/souvenirs/{}/photo.dec".format(id), "wb+") as file:
            file.write(data)


db.close()
