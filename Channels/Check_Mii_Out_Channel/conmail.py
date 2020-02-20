import MySQLdb
from base64 import encodebytes
from datetime import datetime
from io import BytesIO
from json import load
from os import system, remove, path, makedirs
from PIL import Image
from random import randint

from textwrap import wrap

with open("/var/rc24/File-Maker/Channels/Check_Mii_Out_Channel/config.json", "r") as f:
        config = load(f)

db = MySQLdb.connect(
    'localhost', config['dbuser'], config['dbpass'], 'cmoc', charset='utf8mb4')
cursor = db.cursor()

cursor.execute('SELECT id, status, description FROM contests')
contests = cursor.fetchall()

now = datetime.utcnow()
boundary = now.strftime("--BoundaryForDL%Y%m%d%H%m/" +
                        str(randint(1000000, 9999999)))
date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
message = "{}\r\nContent-Type: text/plain\r\n\r\nThis part is ignored.\r\n\r\n\r\n\r\n".format(boundary)


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

for c in contests:
	i += 1
	contest_id = c[0]
	status = c[1]
	description = c[2]

	boundary2 = "----=_CMOC_Contest_{}".format(i)

	contest_posting = "*******************************\r\nA New Contest Is Under Way\r\n*******************************\r\n\r\nCare to test your Mii-making skills\r\nby designing a Mii on a particular\r\ntheme?\r\n\r\n\u25c6Contest Theme:\r\n{}\r\n\r\n\u25c6How to Submit an Entry\r\n1. Design a Mii in the Mii\r\n   Channel.\r\n2. Go to the Check Mii Out\r\n   Channel and submit your Mii.\r\n\r\n\r\n----------------------------------\r\nThis message is regarding the\r\nCheck Mii Out Channel.\r\n\r\nIf you do not wish to receive further\r\ncommercial messages from RiiConnect24,\r\nplease click the opt-out icon on the \r\nupper-right corner of the screen.\r\n\r\nYou can opt out of either (1) \r\nmessages for the Check Mii Out\r\nChannel only or (2) all messages for\r\nall channels and games."
	contest_judging = "*******************************\r\nCome and Judge a Contest\r\n*******************************\r\n\r\nCome over to the Check Mii Out\r\nChannel and judge a few Miis\r\nfor a contest.\r\n\r\n\u25c6Contest Theme:\r\n{}\r\n\r\n\r\n----------------------------------\r\nThis message is regarding the\r\nCheck Mii Out Channel.\r\n\r\nIf you do not wish to receive further\r\ncommercial messages from RiiConnect24,\r\nplease click the opt-out icon on the \r\nupper-right corner of the screen.\r\n\r\nYou can opt out of either (1) \r\nmessages for the Check Mii Out\r\nChannel only or (2) all messages for\r\nall channels and games."
	contest_results = "*******************************\r\nContest Results\r\n*******************************\r\n\r\nWe've tallied up all the votes, and\r\nthe winners for this contest have\r\nbeen decided!\r\n\r\n\u25c6Contest Theme:\r\n{}\r\n\r\n\r\n----------------------------------\r\nThis message is regarding the\r\nCheck Mii Out Channel.\r\n\r\nIf you do not wish to receive further\r\ncommercial messages from RiiConnect24,\r\nplease click the opt-out icon on the \r\nupper-right corner of the screen.\r\n\r\nYou can opt out of either (1) \r\nmessages for the Check Mii Out\r\nChannel only or (2) all messages for\r\nall channels and games."

	if status == "open":
		contest_text = enc(contest_posting, description)
	elif status == "judging":
		contest_text = enc(contest_judging, description)
	elif status == "results":
		contest_text = enc(contest_results, description)

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

	if path.exists(photo_path):
		message += \
			"--" + boundary2 + "\r\n" + \
			"Content-Type: image/jpeg;" + "\r\n" + \
			" name=contest{}.jpg\r\n".format(str(i)) + \
			"Content-Transfer-Encoding: base64\r\n" + \
			"Content-Disposition: attachment;\r\n" + \
			" filename=contest{}.jpg\r\n\r\n".format(str(i)) + \
			convert_to_baseline(photo_path) + "\r\n\r\n"

	message += "--" + boundary2 + "--\r\n\r\n"

message += boundary + "--\r\n"

print(message)

path = config['miicontest_path']

with open("{}/150/con_task1.txt".format(path), "w") as f:
	f.write(message)
	f.close()

system("python ./sign_encrypt.py -t enc -in '{}/150/con_task1.txt' -out '{}/150/con_task1.bin' -key BE3715C308F341A8F16F0EF4FB1497AF -rsa /var/rc24/key/cmoc.pem".format(path, path))

remove("{}/150/con_task1.txt".format(path))
