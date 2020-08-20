#!/usr/bin/env python
import MySQLdb
from lz4.block import decompress
from base64 import b64encode, b64decode
from os.path import exists
from subprocess import call
from json import load
from datetime import datetime
from cmoc import wii2studio

with open('/var/rc24/File-Maker/Channels/Check_Mii_Out_Channel/config.json', 'r') as f:
		config = load(f)

def decodeMii(data):
		return(decompress(b64decode(data.encode()), uncompressed_size = 76))

date = str(datetime.today().strftime('%B %d, %Y'))
db = MySQLdb.connect('localhost', config['dbuser'], config['dbpass'], 'cmoc', use_unicode=True, charset='utf8mb4')
cursor = db.cursor()

countries = {1: "jp", 8: "ai", 9: "ag", 10: "ar", 11: "aw", 12: "bs", 13: "bb", 14: "bz", 15: "bo", 16: "br", 17: "vg", 18: "ca", 19: "ky", 20: "cl", 21: "co", 22: "cr", 23: "dm", 24: "do", 25: "ec", 26: "sv", 27: "gf", 28: "gd", 29: "gp", 30: "gt", 31: "gy", 32: "ht", 33: "hn", 34: "jm", 35: "mq", 36: "mx", 37: "ms", 38: "cw", 39: "ni", 40: "pa", 41: "py", 42: "pe", 43: "kn", 44: "lc", 45: "vc", 46: "sr", 47: "tt", 48: "tc", 49: "us", 50: "uy", 51: "vi", 52: "ve", 64: "al", 65: "au", 66: "at", 67: "be", 68: "ba", 69: "bw", 70: "bg", 71: "hr", 72: "cy", 73: "cz", 74: "dk", 75: "ee", 76: "fi", 77: "fr", 78: "de", 79: "gr", 80: "hu", 81: "is",
			 82: "ie", 83: "it", 84: "lv", 85: "ls", 86: "li", 87: "lt", 88: "lu", 89: "mk", 90: "mt", 91: "me", 92: "mz", 93: "na", 94: "nl", 95: "nz", 96: "no", 97: "pl", 98: "pt", 99: "ro", 100: "ru", 101: "rs", 102: "sk", 103: "si", 104: "za", 105: "es", 106: "sz", 107: "se", 108: "ch", 109: "tr", 110: "gb", 111: "zm", 112: "zw", 113: "az", 114: "mr", 115: "ml", 116: "ne", 117: "td", 118: "sd", 119: "er", 120: "dj", 121: "so", 128: "tw", 136: "kr", 144: "hk", 145: "mo", 152: "id", 153: "sg", 154: "th", 155: "ph", 156: "my", 160: "cn", 168: "ae", 169: "in", 170: "eg", 171: "om", 172: "qa", 173: "kw", 174: "sa", 175: "sy", 176: "bh", 177: "jo"}

headers = ['Rank', 'Mii', 'Artisan', 'Votes', 'Posts']
for h in range(len(headers)):
	headers[h] = '\t\t<th>' + headers[h] + '</th>\n'
headers = '\t<tr>\n' + ''.join(headers) + '</tr>\n'

cursor.execute('SELECT artisan.craftsno, artisan.miidata, artisan.nickname, artisan.country, artisan.votes, (SELECT COUNT(*) FROM mii WHERE mii.craftsno = artisan.craftsno) FROM artisan WHERE votes >= 3 AND craftsno != 100000993 ORDER BY votes DESC LIMIT 300')
row = cursor.fetchall()

table = f'<p>Only the top 300 Mii Artisans are shown. Click on a Mii to download it.</p>\n<h4>{date}</h4>\n<table class="striped" align="center">\n' + headers
for i in range(len(row)):
	master = ''
	nickname = row[i][2]
	craftsno = row[i][0]
	mii_filename = '/var/www/wapp.wii.com/miicontest/public_html/render/crafts-{}.mii'.format(craftsno)
	if not exists(mii_filename):
		with open(mii_filename, 'wb') as f:
			miidata = decodeMii(row[i][3])[:-2]
			miidata = miidata[:28] + b'\x00\x00\x00\x00' + miidata[32:] #remove mac address from mii data
			f.write(miidata)

	# if not exists(mii_filename + '.png'):
	#	call(['mono', 'MiiRender.exe', mii_filename])

	if int(row[i][4]) >= 1000:
		master = "<img src=\"/images/master.png\" /><br>"

	try:
		country = "<span class=\"flag-icon flag-icon-" + \
			countries[row[i][3]] + "\"></span> "

	except KeyError:
		country = ""

	table += '\t<tr>\n'
	table += f'\t\t<td>{i + 1}</td>\n'
	table += f'\t\t<td><a href="/render/crafts-{craftsno}.mii"><img width="75" src="{wii2studio(mii_filename)}"/></a></td>\n'
	table += f'\t\t<td><a href="https://miicontestp.wii.rc24.xyz/cgi-bin/htmlcraftsearch.cgi?query={craftsno}">{country + nickname}<br>{master}</a></td>\n'
	table += f'\t\t<td>{row[i][4]}</td>\n'
	table += f'\t\t<td>{row[i][5]}</td>\n'
	table += '\t</tr>\n'

table += '</table>\n'

with open('/var/www/wapp.wii.com/miicontest/public_html/tables/rankings.html', 'w') as file:
	file.write(table)
