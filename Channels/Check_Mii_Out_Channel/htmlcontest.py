import MySQLdb
from json import load
from time import mktime
from datetime import date, datetime

with open("/var/rc24/File-Maker/Channels/Check_Mii_Out_Channel/config.json", "r") as f:
        config = load(f)
date = str(datetime.today().strftime("%B %d, %Y"))

beginning = "<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\n<link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css\">\n<link href=\"/css/style.css\" rel=\"Stylesheet\" type=\"text/css\" />\n<link href=\"/css/ctmkf.css\" rel=\"Stylesheet\" type=\"text/css\" />\n<title>Contest Info</title>\n<link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/apple-touch-icon.png\">\n<link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/favicon-32x32.png\">\n<link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/favicon-16x16.png\">\n<link rel=\"manifest\" href=\"/site.webmanifest\">\n<link rel=\"mask-icon\" href=\"/safari-pinned-tab.svg\" color=\"#89c0ca\">\n<meta name=\"msapplication-TileColor\" content=\"#2d89ef\">\n<meta name=\"theme-color\" content=\"#ffffff\">\n</head>\n<body class=\"center\">\n\n<h2><img src=\"/images/envelope.png\">Contest Info</h2>\n<h4>" + date + "</h4>\n<p>All times are measured in UTC</p>\n<table class=\"striped\" align=\"center\">\n"

db = MySQLdb.connect('localhost', config['dbuser'], config['dbpass'], 'cmoc', use_unicode=True, charset='utf8mb4')
cursor = db.cursor()

cursor.execute('SELECT start,end,status,description FROM contests WHERE status != \'closed\' AND status != \'waiting\' ORDER BY end ASC')
list = cursor.fetchall()

month = int(datetime.now().month)
day = int(datetime.now().day)

tables = beginning + "\t<tr>\n\t\t<th>Start</th>\n\t\t<th>Next Rotation</th>\n\t\t<th>Status</th>\n\t\t<th>Description</th>\n"

for i in range(len(list)):
	start = datetime.fromtimestamp(int(list[i][0]) + 946684800)
	end = datetime.fromtimestamp(int(list[i][1]) + 946684800)
	startDate = start.date()
	endDate = end.date()
	startTime = str(start.time())[:-3]
	endTime = str(end.time())[:-3]

	tables += "\t<tr>\n"
	tables += "\t\t<td>{} {}</td>\n".format(startDate, startTime)
	tables += "\t\t<td>{} {}</td>\n".format(endDate, endTime)
	tables += "\t\t<td>{}</td>\n".format(list[i][2].capitalize())
	tables += "\t\t<td>{}</td>\n".format(list[i][3])

	tables += "\t</tr>\n"
	#tables += str('\n' + list[i][0] + '' + str(list[i][1]))

tables += "\n</table>\n</body>\n</html>"

with open('/var/www/wapp.wii.com/miicontest/public_html/contest.html', 'w') as file:
	file.write(tables)
