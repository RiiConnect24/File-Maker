import lz4.block
from base64 import b64encode, b64decode
import MySQLdb
import os
import subprocess
from json import load
from datetime import datetime

with open("/var/rc24/File-Maker/Tools/CMOC/config.json", "r") as f:
    config = load(f)

def decodeMii(data): #takes compressed and b64 encoded data, returns binary mii data
    return(lz4.block.decompress(b64decode(data.encode()), uncompressed_size = 76))

date = str(datetime.today().strftime("%B %d, %Y"))

beginning = "<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\n<link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css\">\n<link href=\"/css/style.css\" rel=\"Stylesheet\" type=\"text/css\" />\n<link href=\"/css/ctmkf.css\" rel=\"Stylesheet\" type=\"text/css\" />\n<link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/2.8.0/css/flag-icon.min.css\" />\n<title>Mii Artisan Rankings</title>\n<link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/apple-touch-icon.png\">\n<link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/favicon-32x32.png\">\n<link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/favicon-16x16.png\">\n<link rel=\"manifest\" href=\"/site.webmanifest\">\n<link rel=\"mask-icon\" href=\"/safari-pinned-tab.svg\" color=\"#89c0ca\">\n<meta name=\"msapplication-TileColor\" content=\"#2d89ef\">\n<meta name=\"theme-color\" content=\"#ffffff\">\n</head>\n<body class=\"center\">\n\n<h2><img src=\"/images/rankings.png\" id=\"icon\"> Mii Artisan Rankings</h2>\n<h4>" + date + "</h4>\n<p>Only the top 300 Mii Artisans are shown. Click on a Mii to download it.</p>\n<table class=\"striped\" align=\"center\">\n"

db = MySQLdb.connect(
    'localhost', config['dbuser'], config['dbpass'], 'cmoc', use_unicode=True, charset='utf8mb4')
cursor = db.cursor()

cursor.execute('SELECT craftsno,miidata,nickname,votes,country FROM artisan WHERE votes >= 3 AND craftsno != 100000993 ORDER BY votes DESC LIMIT 300')
list = cursor.fetchall()

month = int(datetime.now().month)
day = int(datetime.now().day)

tables = beginning + \
    "\t<tr>\n\t\t<th>Rank</th>\n\t\t<th>Mii</th>\n\t\t<th>Artisan</th>\n\t\t<th>Votes</th>\n\t</tr>\n"

countries = {1: "jp", 8: "ai", 9: "ag", 10: "ar", 11: "aw", 12: "bs", 13: "bb", 14: "bz", 15: "bo", 16: "br", 17: "vg", 18: "ca", 19: "ky", 20: "cl", 21: "co", 22: "cr", 23: "dm", 24: "do", 25: "ec", 26: "sv", 27: "gf", 28: "gd", 29: "gp", 30: "gt", 31: "gy", 32: "ht", 33: "hn", 34: "jm", 35: "mq", 36: "mx", 37: "ms", 38: "cw", 39: "ni", 40: "pa", 41: "py", 42: "pe", 43: "kn", 44: "lc", 45: "vc", 46: "sr", 47: "tt", 48: "tc", 49: "us", 50: "uy", 51: "vi", 52: "ve", 64: "al", 65: "au", 66: "at", 67: "be", 68: "ba", 69: "bw", 70: "bg", 71: "hr", 72: "cy", 73: "cz", 74: "dk", 75: "ee", 76: "fi", 77: "fr", 78: "de", 79: "gr", 80: "hu", 81: "is",
             82: "ie", 83: "it", 84: "lv", 85: "ls", 86: "li", 87: "lt", 88: "lu", 89: "mk", 90: "mt", 91: "me", 92: "mz", 93: "na", 94: "nl", 95: "nz", 96: "no", 97: "pl", 98: "pt", 99: "ro", 100: "ru", 101: "rs", 102: "sk", 103: "si", 104: "za", 105: "es", 106: "sz", 107: "se", 108: "ch", 109: "tr", 110: "gb", 111: "zm", 112: "zw", 113: "az", 114: "mr", 115: "ml", 116: "ne", 117: "td", 118: "sd", 119: "er", 120: "dj", 121: "so", 128: "tw", 136: "kr", 144: "hk", 145: "mo", 152: "id", 153: "sg", 154: "th", 155: "ph", 156: "my", 160: "cn", 168: "ae", 169: "in", 170: "eg", 171: "om", 172: "qa", 173: "kw", 174: "sa", 175: "sy", 176: "bh", 177: "jo"}

for i in range(len(list)):
    mii_filename = "/var/www/wapp.wii.com/miicontest/public_html/render/crafts-{}.mii".format(
        list[i][0])
    if not os.path.exists(mii_filename):
        with open(mii_filename, "wb") as f:
            f.write(decodeMii(list[i][1])[:-2])
        subprocess.call(["mono", "MiiRender.exe", mii_filename])
    if int(list[i][3]) >= 1000:
        master = "<img src=\"/images/master.png\" /><br>"
    else:
        master = ""
    try:
        country = "<span class=\"flag-icon flag-icon-" + \
            countries[list[i][4]] + "\"></span> "
    except KeyError:
        country = ""
    tables += "\t<tr>\n"
    tables += "\t\t<td>{}</td>\n".format(i + 1)
    tables += "\t\t<td>{}</td>\n".format(
        "<a href=\"/render/crafts-{}.mii\"><img width=\"75\" src=\"/render/crafts-{}.mii.png\"/></a>".format(list[i][0], list[i][0]))
    tables += "\t\t<td>{}</td>\n".format(master + country + list[i][2])
    tables += "\t\t<td>{}</td>\n".format(list[i][3])
    tables += "\t</tr>\n"
    #tables += str('\n' + list[i][0] + '' + str(list[i][1]))

tables += "\n</table>\n</body>\n</html>"

with open('/var/www/wapp.wii.com/miicontest/public_html/rankings.html', 'w') as file:
    file.write(tables)
