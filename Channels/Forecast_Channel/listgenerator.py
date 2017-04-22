#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import pycountry
import struct
import binascii
import requests
import time
import googlemaps

def u16(data):
	return struct.pack(">H", data)

print "Forecast Channel Metadata Generator"
print "By John Pansera - 2017"
api_key = "mKr1GCnSwRWNPGaFkqjMqlSDmOA7pA97"

bincountries = {}
bincountries["Japan"] = '01'
bincountries["Australia"] = '65'
bincountries["Anguila"] = '8'
bincountries["Antigua and Barbuda"] = '9'
bincountries["Argentina"] = '10'
bincountries["Aruba"] = '11'
bincountries["Bahamas"] = '12'
bincountries["Barbados"] = '13'
bincountries["Belize"] = '14'
bincountries["Bolivia"] = '15'
bincountries["Brazil"] = '16'
bincountries["British Virgin Islands"] = '17'
bincountries["Canada"] = '18'
bincountries["Cayman Islands"] = '19'
bincountries["Chile"] = '20'
bincountries["Colombia"] = '21'
bincountries["Costa Rica"] = '22'
bincountries["Dominica"] = '23'
bincountries["Dominican Republic"] = '24'
bincountries["Ecuador"] = '25'
bincountries["El Salvador"] = '26'
bincountries["French Guiana"] = '27'
bincountries["Grenada"] = '28'
bincountries["Guadeloupe"] = '29'
bincountries["Guatemala"] = '30'
bincountries["Guyana"] = '31'
bincountries["Haiti"] = '32'
bincountries["Honduras"] = '33'
bincountries["Jamaica"] = '34'
bincountries["Martinique"] = '35'
bincountries["Mexico"] = '36'
bincountries["Montserrat"] = '37'
bincountries["Netherlands Antilles"] = '38'
bincountries["Nicaragua"] = '39'
bincountries["Panama"] = '40'
bincountries["Paraguay"] = '41'
bincountries["Peru"] = '42'
bincountries["St. Kitts and Nevis"] = '43'
bincountries["St. Lucia"] = '44'
bincountries["St. Vincent and the Grenadines"] = '45'
bincountries["Suriname"] = '46'
bincountries["Trinidad and Tobago"] = '47'
bincountries["Turks and Caicos Islands"] = '48'
bincountries["United States"] = '49'
bincountries["Uruguay"] = '50'
bincountries["US Virgin Islands"] = '51'
bincountries["Venezuela"] = '52'
bincountries["Albania"] = '64'
bincountries["Australia"] = '65'
bincountries["Austria"] = '66'
bincountries["Belgium"] = '67'
bincountries["Bosnia and Herzegovina"] = '68'
bincountries["Botswana"] = '69'
bincountries["Bulgaria"] = '70'
bincountries["Croatia"] = '71'
bincountries["Cyprus"] = '72'
bincountries["Czech Republic"] = '73'
bincountries["Denmark"] = '74'
bincountries["Estonia"] = '75'
bincountries["Finland"] = '76'
bincountries["France"] = '77'
bincountries["Germany"] = '78'
bincountries["Greece"] = '79'
bincountries["Hungary"] = '80'
bincountries["Iceland"] = '81'
bincountries["Ireland"] = '82'
bincountries["Italy"] = '83'
bincountries["Latvia"] = '84'
bincountries["Lesotho"] = '85'
bincountries["Liechtenstein"] = '86'
bincountries["Lithuania"] = '87'
bincountries["Luxembourg"] = '88'
bincountries["F.Y.R. of Macedonia"] = '89'
bincountries["Malta"] = '90'
bincountries["Montenegro"] = '91'
bincountries["Mozambique"] = '92'
bincountries["Namibia"] = '93'
bincountries["Netherlands"] = '94'
bincountries["New Zealand"] = '95'
bincountries["Norway"] = '96'
bincountries["Poland"] = '97'
bincountries["Portugal"] = '98'
bincountries["Romania"] = '99'
bincountries["Russia"] = '100'
bincountries["Serbia"] = '101'
bincountries["Slovakia"] = '102'
bincountries["Slovenia"] = '103'
bincountries["South Africa"] = '104'
bincountries["Spain"] = '105'
bincountries["Swaziland"] = '106'
bincountries["Sweden"] = '107'
bincountries["Switzerland"] = '108'
bincountries["Turkey"] = '109'
bincountries["United Kingdom"] = '110'
bincountries["Zambia"] = '111'
bincountries["Zimbabwe"] = '112'
bincountries["Azerbaijan"] = '113'
bincountries["Mauritania"] = '114'
bincountries["Mali"] = '115'
bincountries["Niger"] = '116'
bincountries["Chad"] = '117'
bincountries["Sudan"] = '118'
bincountries["Eritrea"] = '119'
bincountries["Dijibouti"] = '120'
bincountries["Somalia"] = '121'
bincountries["Taiwan"] = '122'
bincountries["South Korea"] = '136'
bincountries["Hong Kong"] = '144'
bincountries["Macao"] = '145'
bincountries["Indonesia"] = '152'
bincountries["Singapore"] = '153'
bincountries["Thailand"] = '154'
bincountries["Philippines"] = '155'
bincountries["Malaysia"] = '156'
bincountries["China"] = '160'
bincountries["U.A.E"] = '168'
bincountries["India"] = '169'
bincountries["Egypt"] = '170'
bincountries["Oman"] = '171'
bincountries["Qatar"] = '172'
bincountries["Kuwait"] = '173'
bincountries["Saudi Arabia"] = '174'
bincountries["Syria"] = '175'
bincountries["Bahrain"] = '176'
bincountries["Jordan"] = '177'

def get_data(city, c):
	try:
		if city == "San Juan":
			country = "pl"
		elif city == "Nuuk":
			country = "gl"
		else:
			country = pycountry.countries.get(name=c).alpha2.lower()
		location = requests.get("http://dataservice.accuweather.com/locations/v1/%s/search?apikey=%s&q=%s&details=true&alias=always" % (country, api_get, search))
	except:
		location = requests.get("http://dataservice.accuweather.com/locations/v1/search?apikey=%s&q=%s&details=true&alias=always" % (api_key, city)).json()
	try: location[0]
	except:
		#print "[error] %s doesn't exist, skipping ..." % city
		return
	lat = location[0]['GeoPosition']['Latitude']
	lng = location[0]['GeoPosition']['Longitude']
	lat1 = u16(int(lat / 0.0055) & 0xFFFF)
	lng1 = u16(int(lng / 0.0055) & 0xFFFF)
	chance = random.randint(1,100)
	if chance <= 100: value = 0
	if chance <= 85: value = 1
	if chance <= 70: value = 2
	if chance <= 60: value = 3
	if chance <= 50: value = 4
	if chance <= 45: value = 5
	if chance <= 30: value = 6
	if chance <= 20: value = 7
	if chance <= 10: value = 8
	if chance <= 5: value = 9
	zoom = str(value).zfill(2)
	return '"'+binascii.hexlify(lat1)+binascii.hexlify(lng1)+zoom+'03'+'0000'+'"'

def get_region(city):
	time.sleep(0.1)
	gmaps = googlemaps.Client(key="AIzaSyBhK9KdLtE-ecLAKIm1uuCkGq2hhl6Xgo8")
	response = gmaps.geocode(city + country)
	try:
		for numbers in range(0, len(response[0]["address_components"]) - 1):
			if "administrative_area_level_1" in response[0]["address_components"][numbers]["types"]:
				return response[0]["address_components"][numbers]["long_name"]
	except:
		return

file = open('list.txt', 'r')
data = file.read()
data1 = data.split('\n')
country = data1[0]
del data1[0]
del data1[-1]
code = bincountries[country]
print "import collections\n"
print 'weathercities'+str(code).zfill(3)+' = collections.OrderedDict()\n'
for key in data1:
	search = key+' '+country
	if key == "The South Pole": search = "Amundsen-Scott South Pole Station"
	elif key == "Moloka'i": search = "Molokai"
	elif key == "San Juan": search = "San Juan"
	elif key == "Sri Jayawardenepura-Kotte": search = "Sri Jayewardenepura-Kotte"
	elif key == "Teotihuacán": search = "San Juan Teotihuacan"
	elif key == "Uluru": search = "Ayers Rock Connellan Airport"
	meta = get_data(search, country)
	if meta is not None:
		region1 = get_region(search)
		if region1 is not None:
			print 'weathercities'+str(code).zfill(3)+'["'+key.decode("utf-8")+'"] = ["'+key.decode("utf-8")+'", "'+region1+'", "'+country+'", '+meta+']'
		else:
			print 'weathercities'+str(code).zfill(3)+'["'+key.decode("utf-8")+'"] = ["'+key.decode("utf-8")+'", "", "'+country+'", '+meta+']'
	else:
		print "[error] %s doesn't exist, skipping ..." % key
			
