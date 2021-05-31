import MySQLdb
from json import load
from cmoc import WSR
from os import system
from base64 import b64decode, b64encode
from crc16 import crc16xmodem as crc

with open("/var/rc24/File-Maker/Channels/Check_Mii_Out_Channel/config.json", "r") as f:
    config = load(f)

db = MySQLdb.connect("localhost", config["dbuser"], config["dbpass"], "rc24_cmoc")
cursor = db.cursor()

cursor.execute("SELECT COUNT(*) FROM mii WHERE likes > 0 LIMIT 100")
count = int(cursor.fetchone()[0])
print("Popular Count:", count)

# popular is always sorted by volatile likes first, but we combine miis ordered by permlikes to fill in the rest to equal 100 total miis
if count >= 100:
    extraCount = 0
    count = 100

else:
    extraCount = 100 - count

cursor.execute(
    "SELECT mii.initial, mii.miidata, artisan.miidata, mii.entryno FROM mii, artisan WHERE mii.craftsno=artisan.craftsno ORDER BY mii.likes DESC LIMIT %s",
    [count],
)
popularMiis = cursor.fetchall()

cursor.execute(
    "SELECT mii.initial, mii.miidata, artisan.miidata, mii.entryno FROM mii, artisan WHERE mii.permlikes < 25 AND mii.craftsno=artisan.craftsno ORDER BY mii.permlikes DESC LIMIT %s",
    [extraCount],
)
extraMiis = cursor.fetchall()

db.close()

ql = WSR().build(popularMiis + extraMiis)
with open("decfiles/wiisports.dec", "wb") as file:
    file.write(ql)

path = config["miicontest_path"]

with open("{}/dd/wiisports.dec".format(path), "wb") as file:
    file.write(ql)

# symlink all miidd country code files to wiisports.enc with its FULL directory path
system(
    "python ./sign_encrypt.py -t enc -in '{}/dd/wiisports.dec' -out '{}/dd/wiisports.enc' -key 91D9A5DD10AAB467491A066EAD9FDD6F -rsa /var/rc24/key/miidd.pem".format(
        path, path
    )
)
