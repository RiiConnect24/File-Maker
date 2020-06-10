import calendar
import MySQLdb
import time
from base64 import encodebytes
from datetime import datetime
from io import BytesIO
from json import load
from os import system, remove, path, makedirs
from PIL import Image
from random import randint
from requests import post

from textwrap import wrap

with open("/var/rc24/File-Maker/Channels/Check_Mii_Out_Channel/config.json", "r") as f:
    config = load(f)

db = MySQLdb.connect(
    'localhost', config['dbuser'], config['dbpass'], 'cmoc', charset='utf8mb4')
cursor = db.cursor()

cursor.execute('SELECT id, status, description, sent FROM contests WHERE (status != \'closed\' AND status != \'waiting\')')
contests = cursor.fetchall()

now = datetime.utcnow()
boundary = now.strftime("--BoundaryForDL%Y%m%d%H%m/" +
                        str(randint(1000000, 9999999)))
date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
message = "{}\r\nContent-Type: text/plain\r\n\r\nThis part is ignored.\r\n\r\n\r\n\r\n".format(
    boundary)


def enc(text, description):
    return str(encodebytes(text.format(description).encode("utf-16be")).replace(b'\n', b'\r\n').decode("utf-8"))


def convert_to_baseline(path):
    """If for some reason the image has an alpha channel (probably a PNG), fill the background with white."""

    with open(path, "rb") as f:
        picture = f.read()
        f.close()

    image = Image.open(BytesIO(picture))

    image = image.convert("RGB")

    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)

    buffer = BytesIO()
    image_without_exif.save(buffer, format='jpeg')

    return str(encodebytes(buffer.getvalue()).replace(b'\n', b'\r\n').decode("utf-8"))


i = 0

if contests == ():
    exit()

# get the con_detail stuff which will show on the Wii Menu icon

sorted_contests = []

for c in contests:
    sorted_contests.append(c[0])

contest_id = max(sorted_contests)

decfilename = "/var/rc24/File-Maker/Channels/Check_Mii_Out_Channel/decfiles/contests/{}/con_detail1.dec".format(str(contest_id))

if path.exists(decfilename):
    boundary2 = "----=_CMOC_Contest_Icon"

    with open(decfilename, "rb") as f:
        contest_icon = str(encodebytes(f.read()).replace(b'\n', b'\r\n').decode("utf-8"))

    message += \
        boundary + "\r\n" + \
        "Content-Type: text/plain\r\n\r\n" + \
        "Date: {}\r\n".format(date) + \
        "From: w9999999900000000@rc24.xyz\r\n" + \
        "To: allusers@rc24.xyz\r\n" + \
        "Message-ID: <776DCLBHYHD.2QBO4Y3I2Y04S@JavaMail.w9999999900000000@rc24.xyz>\r\n" + \
        "Subject: \r\n" + \
        "MIME-Version: 1.0\r\n" + \
        'Content-Type: multipart/mixed; boundary="{}"\r\n'.format(boundary2) + \
        "Content-Transfer-Encoding: base64\r\n" + \
        "X-Wii-AppID: 3-48415041-3031\r\n" + \
        "X-Wii-Tag: 00000001\r\n" + \
        "X-Wii-Cmd: 00080001\r\n\r\n" + \
        "--" + boundary2 + "\r\n" + \
        "Content-Type: application/octet-stream;\r\n" + \
        " name=storage.bin\r\n" + \
        "Content-Transfer-Encoding: base64\r\n" + \
        "Content-Disposition: attachment;\r\n" + \
        " filename=storage.bin\r\n\r\n" + \
        contest_icon + "\r\n\r\n" + \
        "--" + boundary2 + "--\r\n\r\n"

# make text, photo and attachment

for c in contests:
    i += 1
    contest_id = c[0]
    status = c[1]
    description = c[2]
    sent = c[3]

    if sent == 0:
        boundary2 = "----=_CMOC_Contest_{}".format(i)

        contest_posting = "*******************************\r\nA New Contest is Under Way\r\n*******************************\r\n\r\nCare to test your Mii-making skills\r\nby designing a Mii on a particular\r\ntheme?\r\n\r\n\u25c6Contest Theme:\r\n{}\r\n\r\n\u25c6How to Submit an Entry\r\n1. Design a Mii in the Mii\r\n   Channel.\r\n2. Go to the Check Mii Out\r\n   Channel and submit your Mii.\r\n\r\n\r\n----------------------------------\r\nThis message is regarding the\r\nCheck Mii Out Channel.\r\n\r\nIf you do not wish to receive further\r\ncommercial messages from RiiConnect24,\r\nplease click the opt-out icon on the \r\nupper-right corner of the screen.\r\n\r\nYou can opt out of either (1) \r\nmessages for the Check Mii Out\r\nChannel only or (2) all messages for\r\nall channels and games."
        contest_judging = "*******************************\r\nCome and Judge a Contest\r\n*******************************\r\n\r\nCome over to the Check Mii Out\r\nChannel and judge a few Miis\r\nfor a contest.\r\n\r\n\u25c6Contest Theme:\r\n{}\r\n\r\n\r\n----------------------------------\r\nThis message is regarding the\r\nCheck Mii Out Channel.\r\n\r\nIf you do not wish to receive further\r\ncommercial messages from RiiConnect24,\r\nplease click the opt-out icon on the \r\nupper-right corner of the screen.\r\n\r\nYou can opt out of either (1) \r\nmessages for the Check Mii Out\r\nChannel only or (2) all messages for\r\nall channels and games."
        contest_results = "*******************************\r\nContest Results\r\n*******************************\r\n\r\nWe've tallied up all the votes, and\r\nthe winners for this contest have\r\nbeen decided!\r\n\r\n\u25c6Contest Theme:\r\n{}\r\n\r\n\r\n----------------------------------\r\nThis message is regarding the\r\nCheck Mii Out Channel.\r\n\r\nIf you do not wish to receive further\r\ncommercial messages from RiiConnect24,\r\nplease click the opt-out icon on the \r\nupper-right corner of the screen.\r\n\r\nYou can opt out of either (1) \r\nmessages for the Check Mii Out\r\nChannel only or (2) all messages for\r\nall channels and games."

        if status == "open":
            contest_text = enc(contest_posting, description)
            contest_status = "A New Contest is Under Way\n\nCare to test your Mii-making skills\nby designing a Mii on a particular\ntheme?\n\nContest Theme: {}".format(description)
        elif status == "judging":
            contest_text = enc(contest_judging, description)
            contest_status = "Come and Judge a Contest\n\nCome over to the Check Mii Out\nChannel and judge a few Miis\nfor a contest.\n\nContest Theme: {}".format(description)
        elif status == "results":
            contest_text = enc(contest_results, description)
            contest_status = "Contest Results\n\nWe've tallied up all the votes, and\nthe winners for this contest have\nbeen decided!\n\nContest Theme: {}".format(description)

        message += \
            boundary + "\r\n" + \
            "Content-Type: text/plain\r\n\r\n" + \
            "Date: {}\r\n".format(date) + \
            "From: w9999999900000000@rc24.xyz\r\n" + \
            "To: allusers@rc24.xyz\r\n" + \
            "Message-ID: <776DCLBHYHD.2QBO4Y3I2Y04S@JavaMail.w9999999900000000@rc24.xyz>\r\n" + \
            "Subject: \r\n" + \
            "MIME-Version: 1.0\r\n" + \
            'Content-Type: multipart/mixed; boundary="{}"\r\n'.format(boundary2) + \
            "Content-Transfer-Encoding: base64\r\n" + \
            "X-Wii-AltName: AEMAaABlAGMAawAgAE0AaQBpACAATwB1AHQAIABDAGgAYQBuAG4AZQBs=\r\n" + \
            "X-Wii-MB-OptOut: 1\r\n" + \
            "X-Wii-MB-NoReply: 1\r\n" + \
            "X-Wii-AppID: 3-48415041-3031\r\n\r\n" + \
            "--" + boundary2 + "\r\n" + \
            "Content-Type: text/plain; charset=utf-16BE\r\n" + \
            "Content-Transfer-Encoding: base64\r\n\r\n" + \
            contest_text + "\r\n\r\n\r\n\r\n\r\n" + \
            "--" + boundary2 + "\r\n" + \
            "Content-Type: application/x-wii-msgboard;\r\n" + \
            " name=cmoc_letterform.arc\r\n" + \
            "Content-Transfer-Encoding: base64\r\n" + \
            "Content-Disposition: attachment;\r\n" + \
            " filename=cmoc_letterform.arc\r\n\r\n" + \
            "Vao4LQAAACAAAAAkAAAAYAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAIAAAABAAAAYAAAACMA\r\n" + \
            "Y2hqdW1wLmJpbgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQ2hKcAAAACMAAAABAAAAAAAB\r\n" + \
            "AAFIQVBBAAAAIAAAAANhAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\r\n\r\n"

        photo_path = "/var/rc24/photo/{}.jpg".format(contest_id)

        if status == "open" and path.exists(photo_path):
            message += \
                "--" + boundary2 + "\r\n" + \
                "Content-Type: image/jpeg;" + "\r\n" + \
                " name=contest{}.jpg\r\n".format(str(i)) + \
                "Content-Transfer-Encoding: base64\r\n" + \
                "Content-Disposition: attachment;\r\n" + \
                " filename=contest{}.jpg\r\n\r\n".format(str(i)) + \
                convert_to_baseline(photo_path) + "\r\n\r\n"

        message += "--" + boundary2 + "--\r\n\r\n"

        data = {"username": "CMOC Bot", "content": contest_status,
            "avatar_url": "http://rc24.xyz/images/logo-small.png", "attachments": [
            {"fallback": contest_status, "color": "#CB7931", "author_name": "RiiConnect24 CMOC Script",
                "author_icon": "https://miicontest.wii.rc24.xyz/apple-touch-icon.png",
                "text": contest_status, "title": "Update!",
                "fields": [{"title": "Script", "value": "Check Mii Out Channel", "short": "false"}],
                "thumb_url": "https://miicontest.wii.rc24.xyz/photo/{}.jpg".format(contest_id), "footer": "RiiConnect24 Script",
                "footer_icon": "https://rc24.xyz/images/logo-small.png",
                "ts": int(calendar.timegm(datetime.utcnow().timetuple()))}]}

        for url in config["webhook_urls"]:
            post_webhook = post(url, json=data, allow_redirects=True)

        cursor.execute('UPDATE contests SET sent = 1 WHERE id = %s', [contest_id])

db.commit()

message += boundary + "--\r\n"

path = config['miicontest_path']

task_file = "{}/150/con_task1".format(path)

print(message)

with open(task_file + ".txt", "w") as f:
    f.write(message)
    f.close()

system("python ./sign_encrypt.py -t enc -in '{}.txt' -out '{}.bin' -key BE3715C308F341A8F16F0EF4FB1497AF -rsa /var/rc24/key/cmoc.pem".format(task_file, task_file))

remove(task_file + ".txt")
