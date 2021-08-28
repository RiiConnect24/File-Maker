#!/usr/bin/env python
import MySQLdb
from lz4.block import decompress
from base64 import b64encode, b64decode
from os.path import exists
from subprocess import call
from json import load
from datetime import datetime
from cmoc import wii2studio
import sentry_sdk

with open("/var/rc24/File-Maker/Channels/Check_Mii_Out_Channel/config.json", "r") as f:
    config = load(f)

sentry_sdk.init(config["sentry_url"])


def decodeMii(data):
    return decompress(b64decode(data.encode()), uncompressed_size=76)


def decToEntry(num):  # takes decimal int, outputs 12 digit entry number string
    num ^= ((num << 0x1E) ^ (num << 0x12) ^ (num << 0x18)) & 0xFFFFFFFF
    num ^= (num & 0xF0F0F0F) << 4
    num ^= (num >> 0x1D) ^ (num >> 0x11) ^ (num >> 0x17) ^ 0x20070419

    crc = (num >> 8) ^ (num >> 24) ^ (num >> 16) ^ (num & 0xFF) ^ 0xFF
    if 232 < (0xD4A50FFF < num) + (crc & 0xFF):
        crc &= 0x7F

    crc &= 0xFF
    return str(int((format(crc, "08b") + format(num, "032b")), 2)).zfill(12)


date = str(datetime.today().strftime("%B %d, %Y"))
db = MySQLdb.connect(
    "localhost",
    config["dbuser"],
    config["dbpass"],
    "rc24_cmoc",
    use_unicode=True,
    charset="utf8mb4",
)
cursor = db.cursor()

headers = ["Mii", "Entry Number", "Nickname", "Initials", "Likes", "Creator"]
for h in range(len(headers)):
    headers[h] = "\t\t<th>" + headers[h] + "</th>\n"
headers = "\t<tr>\n" + "".join(headers) + "\t</tr>\n"

cursor.execute("SELECT COUNT(*) FROM mii WHERE likes > 0")
count = int(cursor.fetchone()[0])
print("Popular Count:", count)

# popular is always sorted by volatile likes first, but we combine miis ordered by permlikes to fill in the rest to equal 100 total miis
if count >= 100:
    extraCount = 0
    count = 100

else:
    extraCount = 100 - count

cursor.execute(
    "SELECT mii.entryno, mii.initial, mii.permlikes, mii.miidata, mii.nickname, mii.craftsno, artisan.nickname, artisan.master FROM mii, artisan WHERE mii.craftsno = artisan.craftsno AND likes > 0 ORDER BY likes DESC LIMIT %s",
    [count],
)
popularMiis = cursor.fetchall()

cursor.execute(
    "SELECT mii.entryno, mii.initial, mii.permlikes, mii.miidata, mii.nickname, mii.craftsno, artisan.nickname, artisan.master FROM mii, artisan WHERE mii.permlikes < 25 AND mii.craftsno=artisan.craftsno ORDER BY mii.permlikes DESC LIMIT %s",
    [extraCount],
)
extraMiis = cursor.fetchall()

row = popularMiis + extraMiis

table = (
    f'<p>These are all of the popular Miis that currently appear on the Check Mii Out Channel. Only the top 100 popular Miis are shown. Click on a Mii to download it.</p>\n<a href="https://mii.rc24.xyz/">Back to Homepage</a>\n<h4>{date}</h4>\n<table class="striped" align="center">\n'
    + headers
)
for i in range(len(row)):
    artisan = row[i][6]
    entryno = row[i][0]
    initial = row[i][1]
    mii_filename = (
        "/var/www/rc24/wapp.wii.com/miicontest/public_html/render/entry-{}.mii".format(
            entryno
        )
    )
    if not exists(mii_filename):
        with open(mii_filename, "wb") as f:
            miidata = decodeMii(row[i][3])[:-2]
            miidata = (
                miidata[:28] + b"\x00\x00\x00\x00" + miidata[32:]
            )  # remove mac address from mii data
            f.write(miidata)

    # if not exists(mii_filename + '.png'):
    # 	call(['mono', '/var/rc24/File-Maker/Channels/Check_Mii_Out_Channel/MiiRender.exe', mii_filename])

    if len(initial) == 1:
        initial += "."
    elif len(initial) == 2:
        initial = initial[0] + "." + initial[1] + "."

    if bool(row[i][7]):
        artisan += '<br><img width = 125 src="https://miicontest.wii.rc24.xyz/images/master.png" />'

    longentry = decToEntry(entryno)
    longentry = longentry[:4] + "-" + longentry[4:8] + "-" + longentry[8:12]

    table += "\t<tr>\n"
    table += f'\t\t<td><a href="/render/entry-{entryno}.mii"><img width="75" src="{wii2studio(mii_filename)}"/></a></td>\n'
    table += f"\t\t<td>{longentry}</td>\n"
    table += f"\t\t<td>{row[i][4]}</td>\n"
    table += f"\t\t<td>{initial}</td>\n"
    table += f"\t\t<td>{row[i][2]}</td>\n"
    table += f'\t\t<td><a href="https://miicontestp.wii.rc24.xyz/cgi-bin/htmlcraftsearch.cgi?query={row[i][5]}">{artisan}</a></td>\n'

    table += "\t</tr>\n"

table += "</table>\n"

with open(
    "/var/www/rc24/wapp.wii.com/miicontest/public_html/tables/popular.html", "w"
) as file:
    file.write(table)
