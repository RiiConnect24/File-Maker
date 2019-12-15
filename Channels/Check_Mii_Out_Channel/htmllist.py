import MySQLdb
from json import load
from datetime import datetime

with open("/var/rc24/File-Maker/Tools/CMOC/config.json", "r") as f:
        config = load(f)

date = str(datetime.today().strftime("%B %d, %Y"))

beginning = "<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\n<style>\ntable {\n  font-family: arial, sans-serif;\n  border-collapse: collapse;\n  width: 30%;\n}\n\ntd, th {\n  border: 5px solid #555753;\n  text-align: left;\n  padding: 8px;\n}\n\ntr:nth-child(even) {\n  background-color: #EAEAEA;\n}\n</style>\n</head>\n<body>\n\n<h2>Artisan Rankings</h2>\n<h2>" + date + "</h2>\n<p>Only users with 3 or more likes are shown.</p>\n<table>\n"

db = MySQLdb.connect('localhost', config['dbuser'], config['dbpass'], 'cmoc', use_unicode=True, charset='utf8mb4')
cursor = db.cursor()

cursor.execute('SELECT nickname,votes FROM artisan WHERE votes >= 3 ORDER BY votes DESC')
list = cursor.fetchall()

month = int(datetime.now().month)
day = int(datetime.now().day)

tables = beginning + "\t<tr>\n\t\t<th>Rank</th>\n\t\t<th>Artisan</th>\n\t\t<th>Votes</th>\n\t</tr>\n"

for i in range(len(list)):
	tables += "\t<tr>\n"
	tables += "\t\t<td>{}</td>\n".format(i + 1)
	tables += "\t\t<td>{}</td>\n".format(list[i][0])
	tables += "\t\t<td>{}</td>\n".format(list[i][1])
	tables += "\t</tr>\n"
	#tables += str('\n' + list[i][0] + '' + str(list[i][1]))

tables += "\n</table>\n</body>\n</html>"

with open('/var/www/wapp.wii.com/miicontest/public_html/rankings.html', 'w') as file:
	file.write(tables)
