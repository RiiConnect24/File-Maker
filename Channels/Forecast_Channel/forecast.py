#!/usr/bin/python
# -*- coding: utf-8 -*-

# ===========================================================================
# FORECAST CHANNEL GENERATION SCRIPT
# VERSION 2.6
# AUTHORS: JOHN PANSERA, LARSEN VALLECILLO
# ****************************************************************************
# Copyright (c) 2015-2017 RiiConnect24, and it's (Lead) Developers
# ===========================================================================

import binascii
import collections
import forecastlists
import json
import math
import numpy
import os
import pycountry
import requests
import struct
import subprocess
import sys
import time
import io
import random
import rsa
import xmltodict
from config import *
from datetime import datetime, timedelta

apicount = 0 # API Key Count
apicycle = 0 # API Key Cycle Count
japcount = 0 # Short Forecast Table Count
seek_offset = 0 # Seek Offset Location
seek_base = 0 # Base Offset Calculation Location
number = 0 # Incremental Keys
constant = 0 # Incremental Offset Counter
apirequests = 0 # API Request Counter
citycount = 0 # City Progress Counter
cities = 0 # City Counter
retrycount = 0 # Retry Counter
cached = 0 # Count Cached Cities
total = 0
useLegacy = True # Use AccuWeather Legacy API Instead (Faster)
count = {} # Offset Storage
file = None

weathercities = [forecastlists.weathercities008, forecastlists.weathercities009, forecastlists.weathercities010, forecastlists.weathercities011, forecastlists.weathercities012, forecastlists.weathercities013, forecastlists.weathercities014, forecastlists.weathercities015, forecastlists.weathercities016, forecastlists.weathercities017, forecastlists.weathercities018, forecastlists.weathercities019, forecastlists.weathercities020, forecastlists.weathercities021, forecastlists.weathercities022, forecastlists.weathercities023, forecastlists.weathercities024, forecastlists.weathercities025, forecastlists.weathercities026, forecastlists.weathercities027, forecastlists.weathercities028, forecastlists.weathercities029, forecastlists.weathercities030, forecastlists.weathercities031, forecastlists.weathercities032, forecastlists.weathercities033, forecastlists.weathercities034, forecastlists.weathercities035, forecastlists.weathercities036, forecastlists.weathercities037, forecastlists.weathercities038, forecastlists.weathercities039, forecastlists.weathercities040, forecastlists.weathercities041, forecastlists.weathercities042, forecastlists.weathercities043, forecastlists.weathercities044, forecastlists.weathercities045, forecastlists.weathercities046, forecastlists.weathercities047, forecastlists.weathercities048, forecastlists.weathercities049, forecastlists.weathercities050, forecastlists.weathercities051, forecastlists.weathercities052, forecastlists.weathercities065, forecastlists.weathercities066, forecastlists.weathercities067, forecastlists.weathercities074, forecastlists.weathercities076, forecastlists.weathercities077, forecastlists.weathercities078, forecastlists.weathercities079, forecastlists.weathercities082, forecastlists.weathercities083, forecastlists.weathercities088, forecastlists.weathercities094, forecastlists.weathercities095, forecastlists.weathercities096, forecastlists.weathercities098, forecastlists.weathercities105, forecastlists.weathercities107, forecastlists.weathercities108, forecastlists.weathercities110]

print "Forecast Channel Downloader \n"
print "By John Pansera / Larsen Vallecillo / www.rc24.xyz \n"
print "Preparing ..."

uvindex = {}
wind = {}
weathericon = {}
locationkey = {}
times = {}
pollen = {}
today = {}
week = {}
tomorrow = {}
hourly = {}
precipitation = {}
current = {}
globe = {}
weathericonstore = {}
jpnweathericonstore = {}
weatherloc = {}
cache = {}
laundry = {}
weathervalue_text_offsets = {}

def u8(data):
	if data < 0 or data > 255:
		print "[+] Value Pack Failure: %s" % data
		data = 0
	return struct.pack(">B", data)

def u16(data):
	if data < 0 or data > 65535:
		print "[+] Value Pack Failure: %s" % data
		data = 0
	return struct.pack(">H", data)

def u32(data):
	if data < 0 or data > 4294967295:
		print "[+] Value Pack Failure: %s" % data
		data = 0
	return struct.pack(">I", data)

def s8(data):
	return struct.pack(">b", data)

def s16(data):
	return struct.pack(">h", data)

def s32(data):
	return struct.pack(">i", data)

def temp(num):
	return num & 0xFF

def to_celcius(temp):
	return int((temp-32)*5/9)

def to_fahrenheit(temp):
	return int((temp*9/5)+32)

def kmh_mph(wind):
	return int(round(wind*0.621371))

def mph_kmh(wind):
	return int(round(float(wind)*1.60934))

def time_convert(time):
	if mode == 1: return int((time - 946684800) / 60)
	elif mode == 2: return int((time - 1325376000) / 60)

def get_epoch():
	return int(time.time())

def get_city(list, key):
	return list[key][0]

def get_region(list, key):
	return list[key][1]

def get_country(list, key):
	return list[key][2]

def get_all(list, key):
	return ", ".join(filter(None, [get_city(list, key),get_region(list, key),get_country(list, key)]))

def get_lockey(key):
	return locationkey[key]

def append(list, key, data):
	list[str(key)].append(data)

def get_number(list, key):
	return list.keys().index(key)

def pad(amnt):
	buffer = ""
	for _ in range(amnt): buffer+="\0"
	return buffer

def get_index(list, key, num):
	if num != 0: return list[key][num]
	else: return list[key]

def num():
	global number
	num1 = number
	number += 1
	return num1
	
def progress(percent,list):
	bar = 35
	fill = int(round(percent*bar/100))
	sys.stdout.write("\rProgress: %s%% [%s] (%s/%s) ..." % (int(round(percent)),("="*fill)+(" "*(bar-fill)),citycount,len(list)-cached))
	sys.stdout.flush()
	
def output(text):
	sys.stdout.write("\r%s\r%s\n\n" % ((" "*66),text))
	sys.stdout.flush()

def get_icon(icon,list,key):
	if get_index(list,key,2) is 'Japan': return get_weatherjpnicon(icon)
	else: return get_weathericon(icon)

def test_keys():
	global weathercities,accuweather_api_keys
	print "Checking API Keys ..."
	total = 0
	keys = 0
	for key in accuweather_api_keys:
		invalid = False
		keys += 1
		if keys % 10 == 0 or keys == len(accuweather_api_keys): print str(keys) + " / " + str(len(accuweather_api_keys)) + " checked."
		testapi = request_data("http://dataservice.accuweather.com/locations/v1/regions?apikey=%s" % key)
		if testapi is not None:
			ratelimit_remaining = int(testapi.headers['RateLimit-Remaining'])
			if ratelimit_remaining > 0: total+=ratelimit_remaining
			else: invalid = True
		else: invalid = True
		if invalid:
			print "Warning: Key %s marked as unusable" % keys
			accuweather_api_keys[keys-1] = None
	print "%s Requests Available" % total
	print "Processed %s Keys" % len(accuweather_api_keys)

def reset_data(l): # Resets bin-specific values for next generation
	print "Reloading ..."
	global japcount,seek_offset,seek_base,number,file,constant,count,cached,citycount
	japcount = 0
	seek_offset = 0
	seek_base = 0
	number = 0
	constant = 0
	cached = 0
	citycount = 0
	count = {}
	file = None
	for k in l.keys(): del l[k][-3:]

def get_apikey():
	global apicount,apicycle,apirequests
	apirequests+=1
	key = None
	while key is None:
		key = accuweather_api_keys[apicount]
		if apicount == len(accuweather_api_keys)-1:
			apicount = 0
			apicycle += 1
		else: apicount += 1
	return key

def hex_write(where, what, offset, offset1):
	global seek_offset,file
	seek_temp = 0
	if where == 0:
		seek_temp = seek_offset
		if offset > 0: seek_offset = seek_offset + offset
	else: seek_temp = where
	if offset > 0: seek_temp = seek_temp + offset
	file.seek(seek_temp)
	file.write(u32(what))
	if offset1 > 0:
		seek_offset = seek_offset + offset1
		file.seek(seek_offset)

def offset_write(offset1, offset2, offset3):
	global seek_offset,seek_base,file
	seek_offset = seek_offset + offset1
	seek_base = seek_base + offset2
	file.seek(seek_offset)
	file.write(u32(seek_base+offset3))

def increment():
	global constant,count,file
	count[constant] = file.tell()
	constant += 1

"""This requests data from AccuWeather's API. It also retries the request if it fails."""

def request_data(url):
	global retrycount
	header = {'Accept-Encoding' : 'gzip, deflate'}
	i = 0
	c = 0
	while c == 0:
		if i == 4: return -1
		if i > 0:
			time.sleep(0.3)
			retrycount+=1
		if "regions" in url:
			data = requests.get(url, headers=header)
			status_code = data.status_code
			if status_code != 200: return None
		else:
			data = requests.get(url, headers=header)
			status_code = data.status_code
		if status_code == 200:
			if "daily" in url:
				try:
					data = data.json()
					data["DailyForecasts"]
					c = 1
				except: pass
			elif "accuwxturbotablet" in url:
				try:
					data = xmltodict.parse(data.content)
					c = 1
				except: pass
			elif "regions" in url:
				try:
						a = data.json()[0]
						c = 1
				except: pass
			else:
				try:
					data = data.json()
					data[0]
					c = 1
				except:
					if "locations" in url: return -1
		i+=1
	return data

def timestamps(mode, key):
	time = time_convert(get_epoch())
	if key != 0: citytime = time_convert(globe[key]['time'])
	if mode == 0: timestamp = time
	elif mode == 1: timestamp = citytime
	elif mode == 2: timestamp = time + 180
	return timestamp

def get_loccode(list, key):
	global weathercities
	country = get_country(list, key)
	state = get_region(list, key)
	city = get_city(list, key)
	listid = weathercities.index(list)
	if state is '' and country not in forecastlists.bincountries:
			b = 'FE'
			c = 'FE'
			a = hex(weatherloc[listid]['null'][city])[2:].zfill(4)
	else:
		a = hex(weatherloc[listid][country][state][city])[2:].zfill(4)
		b = hex(weatherloc[listid]['states'][country][state])[2:].zfill(2)
		c = hex(int(str(forecastlists.bincountries[country])))[2:].zfill(2)
	string = "".join([c, b, a])
	return string

def zoom(list, mode, key):
	if mode == 1:
		if get_index(list,key,3) == 'None':
			value = str(numpy.random.choice([0,1,2,3,4,5,6,7,8,9],p=[0.2,0.15,0.1,0.1,0.1,0.1,0.1,0.05,0.05,0.05])).zfill(2)
		elif get_index(list,key,3) != 'None': value = get_index(list,key,3)[8:][:2]
	elif mode == 2:
		if get_index(list,key,3) == 'None': value = '03'
		elif get_index(list,key,3) != 'None': value = get_index(list,key,3)[10:][:2]
	return value

def get_locationcode(list):
	global weathercities
	listid = weathercities.index(list)
	print 'Generating Location Keys ...'
	weatherloc[listid] = {}
	weatherloc[listid]['null'] = {}
	weatherloc[listid]['states'] = {}
	for k, v in list.items():
		if v[1] is "" and v[2] not in forecastlists.bincountries: weatherloc[listid]['null'].setdefault(v[0], len(weatherloc[listid]['null'])+1)
		else:
			weatherloc[listid].setdefault(v[2], {})
			weatherloc[listid][v[2]].setdefault(v[1], {})
			weatherloc[listid][v[2]][v[1]].setdefault(v[0], len(weatherloc[listid][v[2]][v[1]])+1)
			weatherloc[listid]['states'].setdefault(v[2], {})
			weatherloc[listid]['states'][v[2]].setdefault(v[1], len(weatherloc[listid]['states'][v[2]])+2)

def blank_data(list, key, clear):
	wind[key] = {}
	uvindex[key] = {}
	precipitation[key] = {}
	week[key] = {}
	hourly[key] = {}
	today[key] = {}
	tomorrow[key] = {}
	current[key] = {}
	wind[key][0] = 0
	wind[key][1] = 0
	wind[key][2] = 'N'
	wind[key][3] = 0
	wind[key][4] = 0
	wind[key][5] = 'N'
	current[key][0] = 'N'
	current[key][1] = 0
	current[key][2] = 0
	current[key][3] = 128
	current[key][4] = 128
	laundry[key] = 255
	uvindex[key] = 255
	pollen[key] = 255
	weathericon[key] = 'FFFF'
	times[key] = get_epoch()
	for k in range(0,15): precipitation[key][k] = 255
	for k in range(0,20): week[key][k] = 128
	for k in range(20,25): week[key][k] = 'FFFF'
	for k in range(25,33): week[key][k] = 128
	for k in range(33,35): week[key][k] = 'FFFF'
	for k in range(0,8): hourly[key][k] = 'FFFF'
	for k in range(0,4): today[key][k] = 128
	today[key][4] = 'FFFF'
	for k in range(5,9): today[key][k] = 128
	for k in range(0,4): tomorrow[key][k] = 128
	tomorrow[key][4] = 'FFFF'
	for k in range(5,9): tomorrow[key][k] = 128
	if clear:
		locationkey[key] = None
		globe[key]['lat'] = binascii.unhexlify(get_index(list,key,3)[:4])
		globe[key]['lng'] = binascii.unhexlify(get_index(list,key,3)[:8][4:])
		globe[key]['time'] = get_epoch()

def get_main_api(list, key):
	apidaily = request_data("http://dataservice.accuweather.com/forecasts/v1/daily/1day/%s?apikey=%s&details=true" % (get_lockey(key),get_apikey()))
	api5day = request_data("http://dataservice.accuweather.com/forecasts/v1/daily/5day/%s?apikey=%s&details=true" % (get_lockey(key),get_apikey()))
	apicurrent = request_data("http://dataservice.accuweather.com/currentconditions/v1/%s?apikey=%s&details=true" % (get_lockey(key), get_apikey()))
	week[key][0] = int(round(api5day['DailyForecasts'][1]['Temperature']['Minimum']['Value']))
	week[key][1] = int(round(api5day['DailyForecasts'][1]['Temperature']['Maximum']['Value']))
	week[key][2] = int(round(api5day['DailyForecasts'][2]['Temperature']['Minimum']['Value']))
	week[key][3] = int(round(api5day['DailyForecasts'][2]['Temperature']['Maximum']['Value']))
	week[key][4] = int(round(api5day['DailyForecasts'][3]['Temperature']['Minimum']['Value']))
	week[key][5] = int(round(api5day['DailyForecasts'][3]['Temperature']['Maximum']['Value']))
	week[key][6] = int(round(api5day['DailyForecasts'][4]['Temperature']['Minimum']['Value']))
	week[key][7] = int(round(api5day['DailyForecasts'][4]['Temperature']['Maximum']['Value']))
	for i in range(0,8): week[key][i+10] = to_celcius(week[key][i])
	week[key][20] = get_icon(api5day['DailyForecasts'][1]['Day']['Icon'],list,key)
	week[key][21] = get_icon(api5day['DailyForecasts'][2]['Day']['Icon'],list,key)
	week[key][22] = get_icon(api5day['DailyForecasts'][3]['Day']['Icon'],list,key)
	week[key][23] = get_icon(api5day['DailyForecasts'][4]['Day']['Icon'],list,key)
	current[key][3] = int(round(apicurrent[0]['Temperature']['Imperial']['Value']))
	current[key][4] = int(round(apicurrent[0]['Temperature']['Metric']['Value']))
	weathericon[key] = get_icon(int(apicurrent[0]['WeatherIcon']),list,key)
	current[key][0] = apicurrent[0]['Wind']['Direction']['English']
	current[key][1] = int(round(apicurrent[0]['Wind']['Speed']['Metric']['Value']))
	current[key][2] = int(round(apicurrent[0]['Wind']['Speed']['Imperial']['Value']))
	times[key] = apicurrent[0]['EpochTime']
	today[key][0] = int(round(apidaily['DailyForecasts'][0]['Temperature']['Minimum']['Value']))
	today[key][1] = int(round(apidaily['DailyForecasts'][0]['Temperature']['Maximum']['Value']))
	today[key][2] = to_celcius(today[key][0])
	today[key][3] = to_celcius(today[key][1])
	today[key][4] = get_icon(int(apidaily['DailyForecasts'][0]['Day']['Icon']),list,key)
	tomorrow[key][0] = int(round(api5day['DailyForecasts'][1]['Temperature']['Minimum']['Value']))
	tomorrow[key][1] = int(round(api5day['DailyForecasts'][1]['Temperature']['Maximum']['Value']))
	tomorrow[key][2] = to_celcius(tomorrow[key][0])
	tomorrow[key][3] = to_celcius(tomorrow[key][1])
	tomorrow[key][4] = get_icon(int(api5day['DailyForecasts'][1]['Day']['Icon']),list,key)
	try: uvval = int(apidaily['DailyForecasts'][0]['AirAndPollen'][5]['Value'])
	except: uvval = 255
	if uvval > 12: uvval = 12
	uvindex[key] = uvval
	wind[key][0] = mph_kmh(api5day['DailyForecasts'][0]['Day']['Wind']['Speed']['Value'])
	wind[key][1] = int(round(api5day['DailyForecasts'][0]['Day']['Wind']['Speed']['Value']))
	wind[key][2] = api5day['DailyForecasts'][0]['Day']['Wind']['Direction']['English']
	wind[key][3] = mph_kmh(api5day['DailyForecasts'][1]['Day']['Wind']['Speed']['Value'])
	wind[key][4] = int(round(api5day['DailyForecasts'][1]['Day']['Wind']['Speed']['Value']))
	wind[key][5] = api5day['DailyForecasts'][1]['Day']['Wind']['Direction']['English']
	pollen[key] = 255
	if get_index(list,keys,2) is 'Japan':
		precipitation[2] = round(apidaily['DailyForecasts'][0]['Day']['PrecipitationProbability'],-1)
		precipitation[3] = round(apidaily['DailyForecasts'][0]['Night']['PrecipitationProbability'],-1)
		precipitation[6] = round(api5day['DailyForecasts'][1]['Day']['PrecipitationProbability'],-1)
		precipitation[7] = round(api5day['DailyForecasts'][1]['Night']['PrecipitationProbability'],-1)
		grass = int(apidaily['DailyForecasts'][0]['AirAndPollen'][1]['Value'])
		tree = int(apidaily['DailyForecasts'][0]['AirAndPollen'][3]['Value'])
		ragweed = int(apidaily['DailyForecasts'][0]['AirAndPollen'][4]['Value'])
		avg = (grass+tree+ragweed)/3
		if avg < 2: avg = 2
		pollen[key] = avg

def get_legacy_api(list, key):
	week[key][0] = int(apilegacy['adc_database']['forecast']['day'][1]['daytime']['lowtemperature'])
	week[key][1] = int(apilegacy['adc_database']['forecast']['day'][1]['daytime']['hightemperature'])
	week[key][2] = int(apilegacy['adc_database']['forecast']['day'][2]['daytime']['lowtemperature'])
	week[key][3] = int(apilegacy['adc_database']['forecast']['day'][2]['daytime']['hightemperature'])
	week[key][4] = int(apilegacy['adc_database']['forecast']['day'][3]['daytime']['lowtemperature'])
	week[key][5] = int(apilegacy['adc_database']['forecast']['day'][3]['daytime']['hightemperature'])
	week[key][6] = int(apilegacy['adc_database']['forecast']['day'][4]['daytime']['lowtemperature'])
	week[key][7] = int(apilegacy['adc_database']['forecast']['day'][4]['daytime']['hightemperature'])
	for i in range(0,8): week[key][i+10] = to_celcius(week[key][i])
	week[key][20] = get_icon(int(apilegacy['adc_database']['forecast']['day'][1]['daytime']['weathericon']),list,key)
	week[key][21] = get_icon(int(apilegacy['adc_database']['forecast']['day'][2]['daytime']['weathericon']),list,key)
	week[key][22] = get_icon(int(apilegacy['adc_database']['forecast']['day'][3]['daytime']['weathericon']),list,key)
	week[key][23] = get_icon(int(apilegacy['adc_database']['forecast']['day'][4]['daytime']['weathericon']),list,key)
	current[key][3] = int(apilegacy['adc_database']['currentconditions']['temperature'])
	current[key][4] = to_celcius(current[key][3])
	weathericon[key] = get_icon(int(apilegacy['adc_database']['currentconditions']['weathericon']),list,key)
	current[key][0] = apilegacy['adc_database']['currentconditions']['winddirection']
	current[key][2] = int(apilegacy['adc_database']['currentconditions']['windspeed'])
	current[key][1] = mph_kmh(current[key][2])
	today[key][0] = int(apilegacy['adc_database']['forecast']['day'][0]['daytime']['lowtemperature'])
	today[key][1] = int(apilegacy['adc_database']['forecast']['day'][0]['daytime']['hightemperature'])
	today[key][2] = to_celcius(today[key][0])
	today[key][3] = to_celcius(today[key][1])
	today[key][4] = get_icon(int(apilegacy['adc_database']['forecast']['day'][0]['daytime']['weathericon']),list,key)
	tomorrow[key][0] = int(apilegacy['adc_database']['forecast']['day'][1]['daytime']['lowtemperature'])
	tomorrow[key][1] = int(apilegacy['adc_database']['forecast']['day'][1]['daytime']['hightemperature'])
	tomorrow[key][2] = to_celcius(tomorrow[key][0])
	tomorrow[key][3] = to_celcius(tomorrow[key][1])
	tomorrow[key][4] = get_icon(int(apilegacy['adc_database']['forecast']['day'][1]['daytime']['weathericon']),list,key)
	try: uvval = int(apilegacy['adc_database']['currentconditions']['uvindex']['@index'])
	except: uvval = 255
	if uvval > 12: uvval = 12
	uvindex[key] = uvval
	wind[key][0] = mph_kmh(apilegacy['adc_database']['forecast']['day'][0]['daytime']['windspeed'])
	wind[key][1] = int(apilegacy['adc_database']['forecast']['day'][0]['daytime']['windspeed'])
	wind[key][2] = apilegacy['adc_database']['forecast']['day'][0]['daytime']['winddirection']
	wind[key][3] = mph_kmh(apilegacy['adc_database']['forecast']['day'][1]['daytime']['windspeed'])
	wind[key][4] = int(apilegacy['adc_database']['forecast']['day'][1]['daytime']['windspeed'])
	wind[key][5] = apilegacy['adc_database']['forecast']['day'][1]['daytime']['winddirection']
	pollen[key] = 255
	lat = float(apilegacy['adc_database']['local']['lat'])
	lng = float(apilegacy['adc_database']['local']['lon'])
	globe[key]['lat'] = u16(int(lat / 0.0055) & 0xFFFF)
	globe[key]['lng'] = u16(int(lng / 0.0055) & 0xFFFF)
	globe[key]['offset'] = float(apilegacy['adc_database']['local']['currentGmtOffset'])
	globe[key]['time'] = int(get_epoch()+float(apilegacy['adc_database']['local']['currentGmtOffset'])*3600)

def get_weekly(list, key):
	week[key][25] = int(apilegacy['adc_database']['forecast']['day'][5]['daytime']['hightemperature'])
	week[key][26] = int(apilegacy['adc_database']['forecast']['day'][5]['daytime']['lowtemperature'])
	week[key][27] = int(apilegacy['adc_database']['forecast']['day'][6]['daytime']['hightemperature'])
	week[key][28] = int(apilegacy['adc_database']['forecast']['day'][6]['daytime']['lowtemperature'])
	week[key][29] = int(to_celcius(week[key][25]))
	week[key][30] = int(to_celcius(week[key][26]))
	week[key][31] = int(to_celcius(week[key][27]))
	week[key][32] = int(to_celcius(week[key][28]))
	week[key][33] = get_icon(int(apilegacy['adc_database']['forecast']['day'][5]['daytime']['weathericon']),list,key)
	week[key][34] = get_icon(int(apilegacy['adc_database']['forecast']['day'][6]['daytime']['weathericon']),list,key)

def get_search(list, key, mode):
	if mode == 0:
		if get_loccode(list, key)[:2] == hex(country_code)[2:].zfill(2): search = " ".join(filter(None, ([get_city(list, key), get_region(list, key)])))
		else: search = " ".join(filter(None, ([get_city(list, key), get_country(list, key)])))
	elif mode == 1:
		if get_loccode(list, key)[:2] == hex(country_code)[2:].zfill(2): search = " ".join(filter(None, ([get_city(list, key), get_country(list, key)])))
		else: search = get_city(list, key)
	if key in forecastlists.corrections: search = forecastlists.corrections[key]
	if get_region(list, key) in forecastlists.region_corrections: search = " ".join(filter(None, ([get_city(list, key), forecastlists.region_corrections[get_region(list, key)]])))
	if get_region(list, key) in forecastlists.region_delete_corrections: search = " ".join(filter(None, ([get_city(list, key), get_country(list, key)])))
	if "St." in search: search = search.replace('St.','Saint')
	return search

def get_location(list, key):
	location = -1
	i = 0
	while location is -1:
		if i == 0:
			try:
				country = pycountry.countries.get(name=get_country(list, key)).alpha2.lower()
				if get_city(list, key) in forecastlists.country_corrections: country = forecastlists.country_corrections[get_city(list, key)]
				location = request_data("http://dataservice.accuweather.com/locations/v1/%s/search?apikey=%s&q=%s&details=true" % (country, get_apikey(), get_search(list,key,0)))
			except: pass
		elif i == 1: location = request_data("http://dataservice.accuweather.com/locations/v1/search?apikey=%s&q=%s&details=true" % (get_apikey(), get_search(list,key,0)))
		elif i == 2: location = request_data("http://dataservice.accuweather.com/locations/v1/search?apikey=%s&q=%s&details=true" % (get_apikey(), get_search(list,key,1)))
		elif i == 3: return -1
		i+=1
	locationkey[key] = location[0]['Key']
	lat = location[0]['GeoPosition']['Latitude']
	lng = location[0]['GeoPosition']['Longitude']
	globe[key]['lat'] = u16(int(lat / 0.0055) & 0xFFFF)
	globe[key]['lng'] = u16(int(lng / 0.0055) & 0xFFFF)
	globe[key]['offset'] = location[0]['TimeZone']['GmtOffset']
	globe[key]['time'] = int(get_epoch()+location[0]['TimeZone']['GmtOffset']*3600)

def get_legacy_location(list, key):
	i = 0
	locationkey[key] = None
	while locationkey[key] is None:
		if i == 2: return -1
		location = request_data("http://accuwxturbotablet.accu-weather.com/widget/accuwxturbotablet/city-find.asp?location=%s" % get_search(list,key,i))
		try:
			if int(location['adc_database']['citylist']['@us'])+int(location['adc_database']['citylist']['@intl']) > 1: locationkey[key] = location['adc_database']['citylist']['location'][0]['@location'][7:]
			else: locationkey[key] = location['adc_database']['citylist']['location']['@location'][7:]
		except: pass
		i+=1

"""Tenki's where we're getting the laundry index for Japan."""

def get_tenki_data(key):
	laundry[key] = 255
	if key in forecastlists.jpncities:
		print "Getting Tenki Data ..."
		laundry[key] = int(os.popen("wget http://www.tenki.jp/indexes/cloth_dried/%s.html -q -O - | grep '指数:' | head -1 | awk '{print $6}' | grep -Eo '[0-9]{1,3}' | head -1" % forecastlists.jpncities[key]).read())
		tempdiff = os.popen("wget http://www.tenki.jp/forecast/%s/38210-daily.html -q -O - | grep 'tempdiff' | grep -oP '\[(.*?)\]' | sed 's/\[//' | sed 's/\]//' | sed 's/\+//'" % forecastlists.jpncities[key]).read().splitlines()
		precip = os.popen("""wget http://www.tenki.jp/forecast/%s/38210-daily.html -q -O - | grep '<td>' | head -8 | tr -d '<td>' | tr -d 'span class="grayOu"/%%'""" % forecastlists.jpncities[key]).read().splitlines()
		precip10 = os.popen("""wget http://www.tenki.jp/forecast/%s/38210-10days.html -q -O - | grep '%%' | grep '<th>' | tr -d '<th>/%%' | tr -d ' '""" % forecastlists.jpncities[key]).read().splitlines()
		today[key][5] = to_fahrenheit(int(tempdiff[0]))
		today[key][6] = to_fahrenheit(int(tempdiff[1]))
		today[key][7] = int(tempdiff[0])
		today[key][8] = int(tempdiff[1])
		tomorrow[key][5] = to_fahrenheit(int(tempdiff[2]))
		tomorrow[key][6] = to_fahrenheit(int(tempdiff[3]))
		tomorrow[key][7] = int(tempdiff[2])
		tomorrow[key][8] = int(tempdiff[3])
		for i in range(0,8): precipitation[key][i] = int(precip[i])
		for i in range(0,7): precipitation[key][i+8] = int(precip10[i])

def get_hourly_forecast(list, key):
	hourly[key] = {}
	time_index = [[3,9,15,21],[27,33,39,45]]
	hour = (datetime.utcnow()+timedelta(hours=globe[key]['offset'])).hour
	for i in range(0,4):
		temp = time_index[0][i]-hour
		if temp > -1 and temp < 24: hourly[key][i] = get_icon(int(apilegacy['adc_database']['forecast']['hourly']['hour'][temp]['weathericon']),list,key)
		else: hourly[key][i] = get_icon(int(-1),list,key)
		temp = time_index[1][i]-hour
		if temp > -1 and temp < 24: hourly[key][i+4] = get_icon(int(apilegacy['adc_database']['forecast']['hourly']['hour'][temp]['weathericon']),list,key)
		else: hourly[key][i+4] = get_icon(int(-1),list,key)

dictionaries_forecast = []
dictionaries_short = []
dictionaries_texttable = []
dictionaries_laundrytable = []
dictionaries_forecast_short = []
dictionaries_forecast_weather = []
dictionaries_uvindextable = []
dictionaries_laundryindextable = []
dictionaries_uvindextexttable = []
dictionaries_laundrytexttable = []
dictionaries_pollentexttable = []
dictionaries_pollenindextable = []
dictionaries_locationtable = []
dictionaries_weathervaluetexttable = []
dictionaries_weathervalue_offsettable = []

def make_bins(list):
	print "[-] Generating Forecast.bin ..."
	make_forecast_bin(list)
	print "[-] Generating Short.bin ..."
	make_short_bin(list)

def make_forecast_bin(list):
	global japcount,constant,count,file,seek_offset,seek_base,extension
	print "Building Binary Tables ..."
	header = make_header_forecast(list)
	long_forecast_table = make_long_forecast_table(list)
	location_table = make_location_table(list)
	text_table = make_forecast_text_table(list)
	pollenindex_table = make_pollenindex_table()
	uvindex_text_table = make_uvindex_text_table()
	laundry_text_table = make_laundry_text_table()
	pollen_text_table = make_pollen_text_table()
	uvindex_table = make_uvindex_table()
	laundryindex_table = make_laundryindex_table()
	weathervalue_text_table = make_weather_value_table()
	weathervalue_offset_table = make_weather_offset_table()
	short_japan_tables = make_forecast_short_table(list)
	print "Processing ..."
	if mode == 1: extension = "bin"
	elif mode == 2: extension = "bi2"
	file1 = 'forecast~.%s.%s_%s' % (extension, str(country_code).zfill(3), str(language_code))
	file2 = 'forecast.%s~.%s+%s' % (extension, str(country_code).zfill(3), str(language_code))
	file3 = 'forecast.%s.%s_%s' % (extension, str(country_code).zfill(3), str(language_code))
	file4 = 'forecast.%s' % extension
	with open(file1, 'ab') as file:
		file.write(pad(20))
		for k, v in header.items(): file.write(v)
		increment()
		print "Writing Long Forecast Table ..."
		for k, v in long_forecast_table.items(): file.write(v)
		count[9] = file.tell()
		if japcount > 0:
			print "Writing Short Forecast Table ..."
			for k, v in short_japan_tables.items(): file.write(v)
		increment()
		print "Writing Weather Value Offset Table ..."
		for k, v in weathervalue_offset_table.items(): file.write(v)
		increment()
		print "Writing UV Index Table ..."
		for k, v in uvindex_table.items(): file.write(v)
		increment()
		print "Writing Laundry Index Table ..."
		for k, v in laundryindex_table.items(): file.write(v)
		increment()
		print "Writing Pollen Index Table ..."
		for k, v in pollenindex_table.items(): file.write(v)
		increment()
		print "Writing Location Table ..."
		for k, v in location_table.items(): file.write(v)
		increment()
		print "Writing Weather Value Text Table ..."
		for k, v in weathervalue_text_table.items(): file.write(v)
		increment()
		print "Writing UV Index Text Table ..."
		for k, v in uvindex_text_table.items(): file.write(v)
		print "Writing Laundry Index Text Table ..."
		for k, v in laundry_text_table.items(): file.write(v)
		print "Writing Pollen Index Text Table ..."
		for k, v in pollen_text_table.items(): file.write(v)
		increment()
		print "Writing Location Text Table ..."
		for k, v in text_table.items(): file.write(v)
		file.write(pad(16))
		file.write('RIICONNECT24'.encode('ASCII'))
		file.flush()
	file.close()
	print "Processing Offsets ..."
	file = open(file1, 'r+b')
	hex_write(12,timestamps(0,0),0,0)
	hex_write(16,timestamps(2,0),0,0)
	hex_write(36,count[0],0,0)
	hex_write(32,int(len(list)-japcount),0,0)
	if japcount > 0:
		hex_write(40,japcount,0,0)
		hex_write(44,count[9],0,0)
	hex_write(48,int((len(weathervalue_offset_table))/3),0,0)
	hex_write(52,count[1],0,0)
	hex_write(60,count[2],0,0)
	hex_write(68,count[3],0,0)
	hex_write(76,count[4],0,0)
	hex_write(84,count[5],0,0)
	seek_offset = count[1]
	seek_base = count[6]
	file.seek(seek_offset)
	for i in range(int(len(weathervalue_offset_table))/3):
		hex_write(0,int(weathervalue_text_offsets[i]+seek_base),4,4)
	"""UV Index"""
	seek_offset = count[2]
	seek_base = count[7]
	file.seek(seek_offset)
	offset_write(4,0,0)
	for i in [8,8,8,18,18,18,10,10,20,20,20,16]:
		offset_write(8,i,0)
	"""Laundry Table"""
	seek_offset = count[3]
	seek_base = count[7]
	file.seek(seek_offset)
	offset_write(4,0,0)
	for i in [16,38,60,82,134,174,210,246,288,336,384]:
		offset_write(8,0,i)
	"""Pollen Table"""
	seek_offset = count[4]
	seek_base = count[7]+594
	file.seek(seek_offset)
	offset_write(4,0,0)
	for i in [8,10,6,12]:
		offset_write(8,i,0)
	"""Location Text"""
	print "Writing Location Text Offsets ..."
	seek_offset = count[5]
	file.seek(seek_offset)
	for keys in list.keys():
		city = get_index(list,keys,4)
		state = get_index(list,keys,5)
		country = get_index(list,keys,6)
		city1 = city+count[8]
		if state is 'None': state1 = 0
		else: state1 = state+count[8]
		if country is 'None': country1 = 0
		else: country1 = country+count[8]
		hex_write(0,city1,4,0)
		hex_write(0,state1,4,0)
		hex_write(0,country1,4,12)
		file.seek(seek_offset)
	file.close()
	os.system('dd if="' + file1 + '" of="' + file2 + '" bs=1 skip=12') # This cuts off the first 12 bytes.
	if production: sign_file(file2, file3, file4)
	os.remove(file1)
	print 'File Generation Successful'

def make_short_bin(list):
	print "Building Binary Tables ..."
	short_forecast_header = make_header_short(list)
	short_forecast_table = make_short_forecast_table(list)
	file1 = 'short.%s~.%s_%s' % (extension, str(country_code).zfill(3), str(language_code))
	file2 = 'short.%s.%s_%s' % (extension, str(country_code).zfill(3), str(language_code))
	file3 = 'short.%s' % extension
	with open(file1, 'ab') as file:
		file.write(u32(timestamps(0,0)))
		file.write(u32(timestamps(2,0)))
		for k, v in short_forecast_header.items(): file.write(v)
		for k, v in short_forecast_table.items(): file.write(v)
		file.flush()
	file.close()
	if production: sign_file(file1, file2, file3)
	print 'File Generation Successful'

def sign_file(name, local_name, server_name):
	print "[-] Processing " + local_name + " ..."
	file = open(name, 'rb')
	copy = file.read()
	print "Calculating CRC32 ..."
	crc32 = format(binascii.crc32(copy) & 0xFFFFFFFF, '08x')
	print "Calculating Size ..."
	size = os.path.getsize(name)+12
	dest = open(local_name, 'w+')
	dest.write(u32(0))
	dest.write(u32(size))
	dest.write(binascii.unhexlify(crc32))
	dest.write(copy)
	os.remove(name)
	dest.close()
	file.close()
	print "Compressing ..."
	subprocess.call(["mono", "--runtime=v4.0.30319", "%s/DSDecmp.exe" % dsdecmp_path, "-c", "lz10", local_name, local_name + "-1"])
	file = open(local_name + '-1', 'rb')
	new = file.read()
	dest = open(local_name, "w+")
	key = open(key_path, 'rb')
	print "RSA Signing ..."
	private_key = rsa.PrivateKey.load_pkcs1(key.read(), "PEM")
	signature = rsa.sign(new, private_key, "SHA-1")
	dest.write(binascii.unhexlify(str(0).zfill(128)))
	dest.write(signature)
	dest.write(new)
	dest.close()
	file.close()
	key.close()
	path = "%s/%s/%s/%s" % (file_path, language_code, str(country_code).zfill(3), server_name)
	subprocess.call(["cp", local_name, path])
	os.remove(local_name)
	os.remove(local_name + "-1")

def get_data(list, name):
	global citycount,cache,apilegacy,apirequests
	citycount+=1
	cache[name] = get_all(list, name)
	globe[name] = {}
	if useLegacy: apirequests+=2
	blank_data(list,name,True)
	if get_legacy_location(list, name) is None:
		apilegacy = request_data("http://accuwxturbotablet.accu-weather.com/widget/accuwxturbotablet/weather-data.asp?locationkey=%s" % get_lockey(name))
		get_tenki_data(name) # Get data for Japanese cities
		if apilegacy is not -1:
			get_legacy_api(list, name)
			get_weekly(list, name)
			get_hourly_forecast(list, name)
	else: output('No data for %s - using defaults' % name)
	progress(float(citycount)/float(len(list)-cached)*100,list)

def make_header_short(list):
	header = collections.OrderedDict()
	dictionaries_short.append(header)
	header["country_code"] = u8(country_code) # Wii Country Code.
	header["language_code"] = u32(language_code) # Wii Language Code.
	header["unknown_1"] = u8(0) # Unknown.
	header["unknown_2"] = u8(0) # Unknown.
	header["padding_1"] = u8(0) # Padding.
	header["short_forecast_number"] = u32(int(len(list))) # Number of short forecast entries.
	header["start_offset"] = u32(36)

	return header

def make_header_forecast(list):
	header = collections.OrderedDict()
	dictionaries_forecast.append(header)
	header["country_code"] = u8(country_code) # Wii Country Code.
	header["language_code"] = u32(language_code) # Wii Language Code.
	header["unknown_1"] = u8(1) # Unknown.
	header["unknown_2"] = u8(1) # Unknown.
	header["padding_1"] = u8(0) # Padding.
	header["message_offset"] = u32(0) # Offset for a message.
	header["long_forecast_number"] = u32(0) # Number of long forecast entries.
	header["long_forecast_offset"] = u32(88) # Offset for the long forecast entry table.
	header["short_forecast_number"] = u32(japcount) # Number of short forecast entries.
	header["short_forecast_offset"] = u32(0) # Offset for the short forecast entry table.
	header["weather_condition_codes_number"] = u32(0) # Number of weather condition code entries.
	header["weather_condition_codes_offset"] = u32(0) # Offset for the weather condition code table.
	header["uv_index_number"] = u32(13) # Number of UV Index entries.
	header["uv_index_offset"] = u32(0) # Offset for the UV Index table.
	header["laundry_index_number"] = u32(12) # Number of Laundry Index entries.
	header["laundry_index_offset"] = u32(0) # Offset for the Laundry Index table.
	header["pollen_count_number"] = u32(5) # Number of Pollen Count entries.
	header["pollen_count_offset"] = u32(0) # Offset for the Pollen Count table.
	header["location_number"] = u32(len(list)) # Number of location entries.
	header["location_offset"] = u32(0) # Offset for the location table.

	return header

def make_long_forecast_table(list):
	long_forecast_table = collections.OrderedDict()
	dictionaries_forecast.append(long_forecast_table)
	for key in list.keys():
		if get_loccode(list, key)[:2] == hex(country_code)[2:].zfill(2):
			numbers = get_number(list, key)
			long_forecast_table["location_code_%s" % numbers] = binascii.unhexlify(get_loccode(list, key)) # Wii Location Code.
			long_forecast_table["timestamp_1_%s" % numbers] = u32(timestamps(1,key)) # 1st timestamp.
			long_forecast_table["timestamp_2_%s" % numbers] = u32(timestamps(0,key)) # 2nd timestamp.
			long_forecast_table["unknown_1_%s" % numbers] = u32(0) # Unknown. (0xC-0xF)
			long_forecast_table["today_forecast_%s" % numbers] = binascii.unhexlify(today[key][4]) # Today's forecast.
			long_forecast_table["today_hourly_forecast_12am_6am_%s" % numbers] = binascii.unhexlify(hourly[key][0]) # Today's hourly forecast from 12am to 6am.
			long_forecast_table["today_hourly_forecast_6am_12pm_%s" % numbers] = binascii.unhexlify(hourly[key][1]) # Today's hourly forecast from 6am to 12pm.
			long_forecast_table["today_hourly_forecast_12pm_6pm_%s" % numbers] = binascii.unhexlify(hourly[key][2]) # Today's hourly forecast from 12pm to 6pm.
			long_forecast_table["today_hourly_forecast_6pm_12am_%s" % numbers] = binascii.unhexlify(hourly[key][3]) # Today's hourly forecast from 6pm to 12am.
			long_forecast_table["today_tempc_high_%s" % numbers] = u8(temp(today[key][3])) # Today's high temperature in Celsius
			long_forecast_table["today_tempc_high_difference_%s" % numbers] = u8(temp(today[key][8])) # Today's high temperature difference in Celsius
			long_forecast_table["today_tempc_low_%s" % numbers] = u8(temp(today[key][2])) # Today's low temperature in Celsius
			long_forecast_table["today_tempc_low_difference_%s" % numbers] = u8(temp(today[key][7])) # Today's low temperature difference in Celsius
			long_forecast_table["today_tempf_high_%s" % numbers] = u8(temp(today[key][1])) # Today's high temperature in Fahrenheit
			long_forecast_table["today_tempf_difference_%s" % numbers] = u8(temp(today[key][6])) # Today's high Fahrenheit difference
			long_forecast_table["today_tempf_low_%s" % numbers] = u8(temp(today[key][0])) # Today's low temperature in Fahrenheit
			long_forecast_table["today_tempf_low_difference_%s" % numbers] = u8(temp(today[key][5])) # Today's low Fahrenheit difference
			long_forecast_table["today_precipitation_1_%s" % numbers] = u8(precipitation[key][0]) # Today's precipitation 1
			long_forecast_table["today_precipitation_2_%s" % numbers] = u8(precipitation[key][1]) # Today's precipitation 2
			long_forecast_table["today_precipitation_3_%s" % numbers] = u8(precipitation[key][2]) # Today's precipitation 3
			long_forecast_table["today_precipitation_4_%s" % numbers] = u8(precipitation[key][3]) # Today's precipitation 4
			long_forecast_table["today_winddirection_%s" % numbers] = u8(int(get_wind_direction(wind[key][2]))) # Today's wind direction
			long_forecast_table["today_windkm_%s" % numbers] = u8(wind[key][0]) # Today's wind speed in km/hr
			long_forecast_table["today_windmph_%s" % numbers] = u8(wind[key][1]) # Today's wind speed in mph
			long_forecast_table["uv_index_%s" % numbers] = u8(uvindex[key]) # UV Index
			long_forecast_table["laundry_index_%s" % numbers] = u8(laundry[key]) # Laundry Index
			long_forecast_table["pollen_index_%s" % numbers] = u8(pollen[key]) # Pollen Index
			long_forecast_table["tomorrow_forecast_%s" % numbers] = binascii.unhexlify(tomorrow[key][4]) # Tomorrow's forecast.
			long_forecast_table["tomorrow_hourly_forecast_12am_6am_%s" % numbers] = binascii.unhexlify(hourly[key][4]) # Tomorrow's hourly forecast from 12am to 6am.
			long_forecast_table["tomorrow_hourly_forecast_6am_12pm_%s" % numbers] = binascii.unhexlify(hourly[key][5]) # Tomorrow's hourly forecast from 6am to 12pm.
			long_forecast_table["tomorrow_hourly_forecast_12pm_6pm_%s" % numbers] = binascii.unhexlify(hourly[key][6]) # Tomorrow's hourly forecast from 12pm to 6pm.
			long_forecast_table["tomorrow_hourly_forecast_6pm_12am_%s" % numbers] = binascii.unhexlify(hourly[key][7]) # Tomorrow's hourly forecast from 6pm to 12am.
			long_forecast_table["tomorrow_tempc_high_%s" % numbers] = u8(temp(tomorrow[key][3])) # Tomorrow's temperature in Celsius
			long_forecast_table["tomorrow_tempc_high_difference_%s" % numbers] = u8(temp(tomorrow[key][8])) # Tomorrow's temperature mean in Celsius
			long_forecast_table["tomorrow_tempc_low_%s" % numbers] = u8(temp(tomorrow[key][2])) # Tomorrow's Celsius globe value
			long_forecast_table["tomorrow_tempc_low_difference_%s" % numbers] = u8(temp(tomorrow[key][7])) # Tomorrow's Celsius globe value
			long_forecast_table["tomorrow_tempf_high_%s" % numbers] = u8(temp(tomorrow[key][1])) # Tomorrow's temperature in Fahrenheit
			long_forecast_table["tomorrow_tempf_high_difference_%s" % numbers] = u8(temp(tomorrow[key][6])) # Tomorrow's Celsius globe value
			long_forecast_table["tomorrow_tempf_low_%s" % numbers] = u8(temp(tomorrow[key][0])) # Tomorrow's temperature mean in Fahrenheit
			long_forecast_table["tomorrow_tempf_low_difference_%s" % numbers] = u8(temp(tomorrow[key][5])) # Tomorrow's Fahrenheit globe value
			long_forecast_table["tomorrow_precipitation_1_%s" % numbers] = u8(precipitation[key][4]) # Tomorrow's precipitation 1
			long_forecast_table["tomorrow_precipitation_2_%s" % numbers] = u8(precipitation[key][5]) # Tomorrow's precipitation 2
			long_forecast_table["tomorrow_precipitation_3_%s" % numbers] = u8(precipitation[key][6]) # Tomorrow's precipitation 3
			long_forecast_table["tomorrow_precipitation_4_%s" % numbers] = u8(precipitation[key][7]) # Tomorrow's precipitation 4
			long_forecast_table["tomorrow_winddirection_%s" % numbers] = u8(int(get_wind_direction(wind[key][5]))) # Tomorrow's wind direction
			long_forecast_table["tomorrow_windkm_%s" % numbers] = u8(wind[key][3]) # Tomorrow's wind speed in km/hr
			long_forecast_table["tomorrow_windmph_%s" % numbers] = u8(wind[key][4]) # Tomorrow's wind speed in mph
			long_forecast_table["uvindex_2_%s" % numbers] = u8(uvindex[key]) # UV Index (Unknown)
			long_forecast_table["laundry_index_2_%s" % numbers] = u8(laundry[key]) # Laundry Index (Unknown)
			long_forecast_table["pollen_index_2_%s" % numbers] = u8(pollen[key]) # Pollen Index (Unknown)
			long_forecast_table["5day_forecast_1_%s" % numbers] = binascii.unhexlify(week[key][20]) # 5-Day forecast day 1 weather icon
			long_forecast_table["5day_tempc_high_1_%s" % numbers] = u8(temp(week[key][11])) # 5-Day forecast day 1 high temperature in Celsius
			long_forecast_table["5day_tempc_low_1_%s" % numbers] = u8(temp(week[key][10])) # 5-Day forecast day 1 low temperature in Celsius
			long_forecast_table["5day_tempf_high_1_%s" % numbers] = u8(temp(week[key][1])) # 5-Day forecast day 1 high temperature in Fahrenheit
			long_forecast_table["5day_tempf_low_1_%s" % numbers] = u8(temp(week[key][0])) # 5-Day forecast day 1 low temperature in Fahrenheit
			long_forecast_table["5day_precipitation_1_%s" % numbers] = u8(precipitation[key][8]) # 5-Day precipitation percentage 1
			long_forecast_table["5day_forecast_padding_1_%s" % numbers] = u8(0) # Padding
			long_forecast_table["5day_forecast_2_%s" % numbers] = binascii.unhexlify(week[key][21]) # 5-Day forecast day 2 weather icon
			long_forecast_table["5day_tempc_high_2_%s" % numbers] = u8(temp(week[key][13])) # 5-Day forecast day 2 high temperature in Celsius
			long_forecast_table["5day_tempc_low_2_%s" % numbers] = u8(temp(week[key][12])) # 5-Day forecast day 2 low temperature in Celsius
			long_forecast_table["5day_tempf_high_2_%s" % numbers] = u8(temp(week[key][3])) # 5-Day forecast day 2 high temperature in Fahrenheit
			long_forecast_table["5day_tempf_low_2_%s" % numbers] = u8(temp(week[key][2])) # 5-Day forecast day 2 low temperature in Fahrenheit
			long_forecast_table["5day_precipitation_2_%s" % numbers] = u8(precipitation[key][9]) # 5-Day precipitation percentage 1
			long_forecast_table["5day_forecast_padding_2_%s" % numbers] = u8(0) # Padding
			long_forecast_table["5day_forecast_3_%s" % numbers] = binascii.unhexlify(week[key][22]) # 5-Day forecast day 3 weather icon
			long_forecast_table["5day_tempc_high_3_%s" % numbers] = u8(temp(week[key][15])) # 5-Day forecast day 3 high temperature in Celsius
			long_forecast_table["5day_tempc_low_3_%s" % numbers] = u8(temp(week[key][14])) # 5-Day forecast day 3 low temperature in Celsius
			long_forecast_table["5day_tempf_high_3_%s" % numbers] = u8(temp(week[key][5])) # 5-Day forecast day 3 high temperature in Fahrenheit
			long_forecast_table["5day_tempf_low_3_%s" % numbers] = u8(temp(week[key][4])) # 5-Day forecast day 3 low temperature in Fahrenheit
			long_forecast_table["5day_precipitation_3_%s" % numbers] = u8(precipitation[key][10]) # 5-Day precipitation percentage 1
			long_forecast_table["5day_forecast_padding_3_%s" % numbers] = u8(0) # Padding
			long_forecast_table["5day_forecast_4_%s" % numbers] = binascii.unhexlify(week[key][23]) # 5-Day forecast day 4 weather icon
			long_forecast_table["5day_tempc_high_4_%s" % numbers] = u8(temp(week[key][17])) # 5-Day forecast day 4 high temperature in Celsius
			long_forecast_table["5day_tempc_low_4_%s" % numbers] = u8(temp(week[key][16])) # 5-Day forecast day 4 low temperature in Celsius
			long_forecast_table["5day_tempf_high_4_%s" % numbers] = u8(temp(week[key][7])) # 5-Day forecast day 4 high temperature in Fahrenheit
			long_forecast_table["5day_tempf_low_4_%s" % numbers] = u8(temp(week[key][6])) # 5-Day forecast day 4 low temperature in Fahrenheit
			long_forecast_table["5day_precipitation_4_%s" % numbers] = u8(precipitation[key][11]) # 5-Day precipitation percentage 1
			long_forecast_table["5day_forecast_padding_4_%s" % numbers] = u8(0) # Padding
			long_forecast_table["5day_forecast_5_%s" % numbers] = binascii.unhexlify(week[key][33]) # 5-Day forecast day 5 weather icon
			long_forecast_table["5day_tempc_high_5_%s" % numbers] = u8(temp(week[key][29])) # 5-Day forecast day 5 high temperature in Celsius
			long_forecast_table["5day_tempc_low_5_%s" % numbers] = u8(temp(week[key][30])) # 5-Day forecast day 5 low temperature in Celsius
			long_forecast_table["5day_tempf_high_5_%s" % numbers] = u8(temp(week[key][25])) # 5-Day forecast day 5 high temperature in Fahrenheit
			long_forecast_table["5day_tempf_low_5_%s" % numbers] = u8(temp(week[key][26])) # 5-Day forecast day 5 low temperature in Fahrenheit
			long_forecast_table["5day_precipitation_5_%s" % numbers] = u8(temp(precipitation[key][12])) # 5-Day precipitation percentage 1
			long_forecast_table["5day_forecast_padding_5_%s" % numbers] = u8(0) # Padding
			long_forecast_table["5day_forecast_6_%s" % numbers] = binascii.unhexlify(week[key][34]) # 5-Day forecast day 5 weather icon (JAPAN ONLY)
			long_forecast_table["5day_tempc_high_6_%s" % numbers] = u8(temp(week[key][31])) # 5-Day forecast day 5 high temperature in Celsius (JAPAN ONLY)
			long_forecast_table["5day_tempc_low_6_%s" % numbers] = u8(temp(week[key][32])) # 5-Day forecast day 5 low temperature in Celsius (JAPAN ONLY)
			long_forecast_table["5day_tempf_high_6_%s" % numbers] = u8(temp(week[key][27])) # 5-Day forecast day 5 high temperature in Fahrenheit (JAPAN ONLY)
			long_forecast_table["5day_tempf_low_6_%s" % numbers] = u8(temp(week[key][28])) # 5-Day forecast day 5 low temperature in Fahrenheit (JAPAN ONLY)
			long_forecast_table["5day_precipitation_6_%s" % numbers] = u8(precipitation[key][13]) # 5-Day precipitation percentage 1 (JAPAN ONLY)
			long_forecast_table["5day_forecast_padding_6_%s" % numbers] = u8(0) # Padding (JAPAN ONLY)
			long_forecast_table["5day_forecast_7_%s" % numbers] = binascii.unhexlify('FFFF') # 5-Day forecast day 5 weather icon (JAPAN ONLY)
			long_forecast_table["5day_tempc_high_7_%s" % numbers] = u8(128) # 5-Day forecast day 5 high temperature in Celsius (JAPAN ONLY)
			long_forecast_table["5day_tempc_low_7_%s" % numbers] = u8(128) # 5-Day forecast day 5 low temperature in Celsius (JAPAN ONLY)
			long_forecast_table["5day_tempf_high_7_%s" % numbers] = u8(128) # 5-Day forecast day 5 high temperature in Fahrenheit (JAPAN ONLY)
			long_forecast_table["5day_tempf_low_7_%s" % numbers] = u8(128) # 5-Day forecast day 5 low temperature in Fahrenheit (JAPAN ONLY)
			long_forecast_table["5day_precipitation_7_%s" % numbers] = u8(precipitation[key][14]) # 5-Day precipitation percentage 1 (JAPAN ONLY)
			long_forecast_table["5day_forecast_padding_7_%s" % numbers] = u8(0) # Padding (JAPAN ONLY)

	return long_forecast_table

def make_short_forecast_table(list):
	short_forecast_table = collections.OrderedDict()
	dictionaries_short.append(short_forecast_table)
	for key in list.keys():
		numbers = get_number(list, key)
		short_forecast_table["location_code_%s" % numbers] = binascii.unhexlify(get_loccode(list, key)) # Wii location code for city
		short_forecast_table["timestamp_1_%s" % numbers] = u32(timestamps(1,key)) # Timestamp 1
		short_forecast_table["timestamp_2_%s" % numbers] = u32(timestamps(0,key)) # Timestamp 2
		short_forecast_table["current_forecast_%s" % numbers] = binascii.unhexlify(weathericon[key]) # Current forecast
		short_forecast_table["unknown_%s" % numbers] = u8(0) # 0xE unknown
		short_forecast_table["current_tempc_%s" % numbers] = u8(temp(current[key][4])) # Current temperature in Celsius
		short_forecast_table["current_tempf_%s" % numbers] = u8(temp(current[key][3])) # Current temperature in Fahrenheit
		short_forecast_table["current_winddirection_%s" % numbers] = u8(int(get_wind_direction(current[key][0]))) # Current wind direction
		short_forecast_table["current_windkm_%s" % numbers] = u8(current[key][1]) # Current wind in km/hr
		short_forecast_table["current_windmph_%s" % numbers] = u8(current[key][2]) # Current wind in mph
		short_forecast_table["unknown_2_%s" % numbers] = u16(0) # 00?
		short_forecast_table["unknown_3_%s" % numbers] = binascii.unhexlify('FFFF') # FFFF?

	return short_forecast_table

def make_forecast_short_table(list):
	short_forecast_table = collections.OrderedDict()
	dictionaries_forecast_short.append(short_forecast_table)
	for key in list.keys():
		if get_loccode(list, key)[:2] != hex(country_code)[2:].zfill(2):
			numbers = get_number(list, key)
			global japcount
			short_forecast_table["location_code_%s" % numbers] = binascii.unhexlify(get_loccode(list, key)) # Wii Location Code.
			short_forecast_table["timestamp_1_%s" % numbers] = u32(timestamps(1,key)) # 1st timestamp.
			short_forecast_table["timestamp_2_%s" % numbers] = u32(timestamps(0,key)) # 2nd timestamp.
			short_forecast_table["padding_%s" % numbers] = u32(0)
			short_forecast_table["today_forecast_%s" % numbers] = binascii.unhexlify(today[key][4]) # Today's forecast.
			short_forecast_table["today_hourly_forecast_12am_6am_%s" % numbers] = binascii.unhexlify(hourly[key][0]) # Today's hourly forecast from 12am to 6am.
			short_forecast_table["today_hourly_forecast_6am_12pm_%s" % numbers] = binascii.unhexlify(hourly[key][1]) # Today's hourly forecast from 6am to 12pm.
			short_forecast_table["today_hourly_forecast_12pm_6pm_%s" % numbers] = binascii.unhexlify(hourly[key][2]) # Today's hourly forecast from 12pm to 6pm.
			short_forecast_table["today_hourly_forecast_6pm_12am_%s" % numbers] = binascii.unhexlify(hourly[key][3]) # Today's hourly forecast from 6pm to 12am.
			short_forecast_table["today_tempc_high_%s" % numbers] = u8(temp(today[key][3])) # Today's high temperature in Celsius
			short_forecast_table["today_tempc_high_difference_%s" % numbers] = u8(temp(today[key][8])) # Today's high temperature difference in Celsius
			short_forecast_table["today_tempc_low_%s" % numbers] = u8(temp(today[key][2])) # Today's low temperature in Celsius
			short_forecast_table["today_tempc_low_difference_%s" % numbers] = u8(temp(today[key][7])) # Today's low temperature difference in Celsius
			short_forecast_table["today_tempf_high_%s" % numbers] = u8(temp(today[key][1])) # Today's high temperature in Fahrenheit
			short_forecast_table["today_tempf_difference_%s" % numbers] = u8(temp(today[key][6])) # Today's high Fahrenheit difference
			short_forecast_table["today_tempf_low_%s" % numbers] = u8(temp(today[key][0])) # Today's low temperature in Fahrenheit
			short_forecast_table["today_tempf_low_difference_%s" % numbers] = u8(temp(today[key][5])) # Today's low Fahrenheit difference
			short_forecast_table["today_precipitation_1_%s" % numbers] = u8(precipitation[key][0]) # Today's precipitation 1
			short_forecast_table["today_precipitation_2_%s" % numbers] = u8(precipitation[key][1]) # Today's precipitation 2
			short_forecast_table["today_precipitation_3_%s" % numbers] = u8(precipitation[key][2]) # Today's precipitation 3
			short_forecast_table["today_precipitation_4_%s" % numbers] = u8(precipitation[key][3]) # Today's precipitation 4
			short_forecast_table["today_winddirection_%s" % numbers] = u8(int(get_wind_direction(wind[key][2]))) # Today's wind direction
			short_forecast_table["today_windkm_%s" % numbers] = u8(wind[key][0]) # Today's wind speed in km/hr
			short_forecast_table["today_windmph_%s" % numbers] = u8(wind[key][1]) # Today's wind speed in mph
			short_forecast_table["unknown_value_%s" % numbers] = u8(255) # ??
			short_forecast_table["unknown_value_2_%s" % numbers] = u8(255) # ??
			short_forecast_table["unknown_value_3_%s" % numbers] = u8(255) # ??
			short_forecast_table["tomorrow_forecast_%s" % numbers] = binascii.unhexlify(tomorrow[key][4]) # Tomorrow's forecast.
			short_forecast_table["tomorrow_hourly_forecast_12am_6am_%s" % numbers] = binascii.unhexlify(hourly[key][4]) # Tomorrow's hourly forecast from 12am to 6am.
			short_forecast_table["tomorrow_hourly_forecast_6am_12pm_%s" % numbers] = binascii.unhexlify(hourly[key][5]) # Tomorrow's hourly forecast from 6am to 12pm.
			short_forecast_table["tomorrow_hourly_forecast_12pm_6pm_%s" % numbers] = binascii.unhexlify(hourly[key][6]) # Tomorrow's hourly forecast from 12pm to 6pm.
			short_forecast_table["tomorrow_hourly_forecast_6pm_12am_%s" % numbers] = binascii.unhexlify(hourly[key][7]) # Tomorrow's hourly forecast from 6pm to 12am.
			short_forecast_table["tomorrow_tempc_high_%s" % numbers] = u8(temp(tomorrow[key][3])) # Tomorrow's temperature in Celsius
			short_forecast_table["tomorrow_tempc_high_difference_%s" % numbers] = u8(temp(tomorrow[key][8])) # Tomorrow's temperature mean in Celsius
			short_forecast_table["tomorrow_tempc_low_%s" % numbers] = u8(temp(tomorrow[key][2])) # Tomorrow's Celsius globe value
			short_forecast_table["tomorrow_tempc_low_difference_%s" % numbers] = u8(temp(tomorrow[key][7])) # Tomorrow's Celsius globe value
			short_forecast_table["tomorrow_tempf_high_%s" % numbers] = u8(temp(tomorrow[key][1])) # Tomorrow's temperature in Fahrenheit
			short_forecast_table["tomorrow_tempf_high_difference_%s" % numbers] = u8(temp(tomorrow[key][6])) # Tomorrow's Celsius globe value
			short_forecast_table["tomorrow_tempf_low_%s" % numbers] = u8(temp(tomorrow[key][0])) # Tomorrow's temperature mean in Fahrenheit
			short_forecast_table["tomorrow_tempf_low_difference_%s" % numbers] = u8(temp(tomorrow[key][5])) # Tomorrow's Fahrenheit globe value
			short_forecast_table["tomorrow_precipitation_1_%s" % numbers] = u8(precipitation[key][4]) # Tomorrow's precipitation 1
			short_forecast_table["tomorrow_precipitation_2_%s" % numbers] = u8(precipitation[key][5]) # Tomorrow's precipitation 2
			short_forecast_table["tomorrow_precipitation_3_%s" % numbers] = u8(precipitation[key][6]) # Tomorrow's precipitation 3
			short_forecast_table["tomorrow_precipitation_4_%s" % numbers] = u8(precipitation[key][7]) # Tomorrow's precipitation 4
			short_forecast_table["tomorrow_winddirection_%s" % numbers] = u8(int(get_wind_direction(wind[key][5]))) # Tomorrow's wind direction
			short_forecast_table["tomorrow_windkm_%s" % numbers] = u8(wind[key][3]) # Tomorrow's wind speed in km/hr
			short_forecast_table["tomorrow_windmph_%s" % numbers] = u8(wind[key][4]) # Tomorrow's wind speed in mph
			short_forecast_table["uvindex_%s" % numbers] = u8(uvindex[key]) # Today's UV Index
			short_forecast_table["laundry_index_%s" % numbers] = u8(laundry[key]) # Today's Laundry Index
			short_forecast_table["pollen_index_%s" % numbers] = u8(pollen[key]) # Today's Pollen Index
			japcount += 1

	return short_forecast_table

"""Database of UV index values."""

def make_uvindex_table():
	uvindex_table = collections.OrderedDict()
	dictionaries_uvindextable.append(uvindex_table)
	uvindex_table["uv_0_number"] = u8(0)
	uvindex_table["uv_0_padding"] = pad(3)
	uvindex_table["uv_0_offset"] = u32(0)
	uvindex_table["uv_1_number"] = u8(1)
	uvindex_table["uv_1_padding"] = pad(3)
	uvindex_table["uv_1_offset"] = u32(0)
	uvindex_table["uv_2_number"] = u8(2)
	uvindex_table["uv_2_padding"] = pad(3)
	uvindex_table["uv_2_offset"] = u32(0)
	uvindex_table["uv_3_number"] = u8(3)
	uvindex_table["uv_3_padding"] = pad(3)
	uvindex_table["uv_3_offset"] = u32(0)
	uvindex_table["uv_4_number"] = u8(4)
	uvindex_table["uv_4_padding"] = pad(3)
	uvindex_table["uv_4_offset"] = u32(0)
	uvindex_table["uv_5_number"] = u8(5)
	uvindex_table["uv_5_padding"] = pad(3)
	uvindex_table["uv_5_offset"] = u32(0)
	uvindex_table["uv_6_number"] = u8(6)
	uvindex_table["uv_6_padding"] = pad(3)
	uvindex_table["uv_6_offset"] = u32(0)
	uvindex_table["uv_7_number"] = u8(7)
	uvindex_table["uv_7_padding"] = pad(3)
	uvindex_table["uv_7_offset"] = u32(0)
	uvindex_table["uv_8_number"] = u8(8)
	uvindex_table["uv_8_padding"] = pad(3)
	uvindex_table["uv_8_offset"] = u32(0)
	uvindex_table["uv_9_number"] = u8(9)
	uvindex_table["uv_9_padding"] = pad(3)
	uvindex_table["uv_9_offset"] = u32(0)
	uvindex_table["uv_10_number"] = u8(10)
	uvindex_table["uv_10_padding"] = pad(3)
	uvindex_table["uv_10_offset"] = u32(0)
	uvindex_table["uv_11_number"] = u8(11)
	uvindex_table["uv_11_padding"] = pad(3)
	uvindex_table["uv_11_offset"] = u32(0)
	uvindex_table["uv_12_number"] = u8(12)
	uvindex_table["uv_12_padding"] = pad(3)
	uvindex_table["uv_12_offset"] = u32(0)

	return uvindex_table

"""Database of laundry index values."""

def make_laundryindex_table():
	laundryindex_table = collections.OrderedDict()
	dictionaries_laundryindextable.append(laundryindex_table)
	laundryindex_table["laundry_00_number"] = u8(0)
	laundryindex_table["laundry_00_padding"] = pad(3)
	laundryindex_table["laundry_00_offset"] = u32(0)
	laundryindex_table["laundry_10_number"] = u8(10)
	laundryindex_table["laundry_10_padding"] = pad(3)
	laundryindex_table["laundry_10_offset"] = u32(0)
	laundryindex_table["laundry_20_number"] = u8(20)
	laundryindex_table["laundry_20_padding"] = pad(3)
	laundryindex_table["laundry_20_offset"] = u32(0)
	laundryindex_table["laundry_30_number"] = u8(30)
	laundryindex_table["laundry_30_padding"] = pad(3)
	laundryindex_table["laundry_30_offset"] = u32(0)
	laundryindex_table["laundry_40_number"] = u8(40)
	laundryindex_table["laundry_40_padding"] = pad(3)
	laundryindex_table["laundry_40_offset"] = u32(0)
	laundryindex_table["laundry_50_number"] = u8(50)
	laundryindex_table["laundry_50_padding"] = pad(3)
	laundryindex_table["laundry_50_offset"] = u32(0)
	laundryindex_table["laundry_60_number"] = u8(60)
	laundryindex_table["laundry_60_padding"] = pad(3)
	laundryindex_table["laundry_60_offset"] = u32(0)
	laundryindex_table["laundry_70_number"] = u8(70)
	laundryindex_table["laundry_70_padding"] = pad(3)
	laundryindex_table["laundry_70_offset"] = u32(0)
	laundryindex_table["laundry_80_number"] = u8(80)
	laundryindex_table["laundry_80_padding"] = pad(3)
	laundryindex_table["laundry_80_offset"] = u32(0)
	laundryindex_table["laundry_90_number"] = u8(90)
	laundryindex_table["laundry_90_padding"] = pad(3)
	laundryindex_table["laundry_90_offset"] = u32(0)
	laundryindex_table["laundry_100_number"] = u8(100)
	laundryindex_table["laundry_100_padding"] = pad(3)
	laundryindex_table["laundry_100_offset"] = u32(0)
	laundryindex_table["laundry_E7_number"] = u8(231)
	laundryindex_table["laundry_E7_padding"] = pad(3)
	laundryindex_table["laundry_E7_offset"] = u32(0)

	return laundryindex_table

"""Database of pollen index values."""

def make_pollenindex_table():
	pollenindex_table = collections.OrderedDict()
	dictionaries_pollenindextable.append(pollenindex_table)
	pollenindex_table["pollen_2_number"] = u8(2)
	pollenindex_table["pollen_2_padding"] = pad(3)
	pollenindex_table["pollen_2_offset"] = u32(0)
	pollenindex_table["pollen_3_number"] = u8(3)
	pollenindex_table["pollen_3_padding"] = pad(3)
	pollenindex_table["pollen_3_offset"] = u32(0)
	pollenindex_table["pollen_4_number"] = u8(4)
	pollenindex_table["pollen_4_padding"] = pad(3)
	pollenindex_table["pollen_4_offset"] = u32(0)
	pollenindex_table["pollen_5_number"] = u8(5)
	pollenindex_table["pollen_5_padding"] = pad(3)
	pollenindex_table["pollen_5_offset"] = u32(0)
	pollenindex_table["pollen_E7_number"] = u8(231)
	pollenindex_table["pollen_E7_padding"] = pad(3)
	pollenindex_table["pollen_E7_offset"] = u32(0)

	return pollenindex_table

"""NOTE: \n is used as line feed."""
"""Needs to be in sync with the value table below."""

def make_weather_value_table():
	weathervalue_text_table = collections.OrderedDict()
	dictionaries_weathervaluetexttable.append(weathervalue_text_table)
	weathervalue_text_table["day_sunny"] = "Sunny\0".encode("utf-16be")
	weathervalue_text_table["day_mostly_sunny"] = "Mostly Sunny\0".encode("utf-16be")
	weathervalue_text_table["day_partly_cloudy"] = "Partly Cloudy\0".encode("utf-16be")
	weathervalue_text_table["day_intermittent_clouds"] = "Intermittent Clouds\0".encode("utf-16be")
	weathervalue_text_table["day_haze"] = "Haze\0".encode("utf-16be")
	weathervalue_text_table["day_mostly_cloudy"] = "Mostly Cloudy\0".encode("utf-16be")
	weathervalue_text_table["day_cloudy"] = "Cloudy\0".encode("utf-16be")
	weathervalue_text_table["day_overcast"] = "Overcast\0".encode("utf-16be")
	weathervalue_text_table["day_fog"] = "Fog\0".encode("utf-16be")
	weathervalue_text_table["day_showers"] = "Showers\0".encode("utf-16be")
	weathervalue_text_table["day_mostly_cloudy_with_showers"] = "Mostly Cloudy\nwith Showers\0".encode("utf-16be")
	weathervalue_text_table["day_partly_sunny_with_showers"] = "Partly Sunny\nwith Showers\0".encode("utf-16be")
	weathervalue_text_table["day_thunderstorms"] = "Thunderstorms\0".encode("utf-16be")
	weathervalue_text_table["day_mostly_cloudy_with_thunderstorms"] = "Mostly Cloudy\nwith Thunderstorms\0".encode("utf-16be")
	weathervalue_text_table["day_partly_sunny_with_thunderstorms"] = "Partly Sunny\nwith Thunderstorms\0".encode("utf-16be")
	weathervalue_text_table["day_rain"] = "Rain\0".encode("utf-16be")
	weathervalue_text_table["day_flurries"] = "Flurries\0".encode("utf-16be")
	weathervalue_text_table["day_mostly_cloudy_with_flurries"] = "Mostly Cloudy\nwith Flurries\0".encode("utf-16be")
	weathervalue_text_table["day_partly_sunny_with_flurries"] = "Partly Sunny\nwith Flurries\0".encode("utf-16be")
	weathervalue_text_table["day_snow"] = "Snow\0".encode("utf-16be")
	weathervalue_text_table["day_mostly_cloudy_with_snow"] = "Mostly Cloudy\nwith Snow\0".encode("utf-16be")
	weathervalue_text_table["day_ice"] = "Ice\0".encode("utf-16be")
	weathervalue_text_table["day_sleet"] = "Sleet\0".encode("utf-16be")
	weathervalue_text_table["day_freezing_rain"] = "Freezing Rain\0".encode("utf-16be")
	weathervalue_text_table["day_rain_and_snow"] = "Rain and Snow\0".encode("utf-16be")
	weathervalue_text_table["night_clear"] = "Clear\0".encode("utf-16be")
	weathervalue_text_table["night_mostly_clear"] = "Mostly Clear\0".encode("utf-16be")
	weathervalue_text_table["night_partly_cloudy"] = "Partly Cloudy\0".encode("utf-16be")
	weathervalue_text_table["night_intermittent_clouds"] = "Intermittent Clouds\0".encode("utf-16be")
	weathervalue_text_table["night_hazy_moonlight"] = "Hazy Moonlight\0".encode("utf-16be")
	weathervalue_text_table["night_mostly_cloudy"] = "Mostly Cloudy\0".encode("utf-16be")
	weathervalue_text_table["night_partly_cloudy_with_showers"] = "Partly Cloudy\nwith Showers\0".encode("utf-16be")
	weathervalue_text_table["night_mostly_cloudy_with_showers"] = "Mostly Cloudy\nwith Showers\0".encode("utf-16be")
	weathervalue_text_table["night_partly_cloudy_with_thunderstorms"] = "Partly Cloudy\nwith Thunderstorms\0".encode("utf-16be")
	weathervalue_text_table["night_mostly_cloudy_with_thunderstorms"] = "Mostly Cloudy\nwith Thunderstorms\0".encode("utf-16be")
	weathervalue_text_table["night_mostly_cloudy_with_flurries"] = "Mostly Cloudy\nwith Flurries\0".encode("utf-16be")
	weathervalue_text_table["night_mostly_cloudy_with_snow"] = "Mostly Cloudy\nwith Snow\0".encode("utf-16be")
	weathervalue_text_table["japan_day_sunny"] = "Sunny\0".encode("utf-16be")
	weathervalue_text_table["japan_day_mostly_sunny"] = "Mostly Sunny\0".encode("utf-16be")
	weathervalue_text_table["japan_day_partly_cloudy"] = "Partly Cloudy\0".encode("utf-16be")
	weathervalue_text_table["japan_day_intermittent_clouds"] = "Intermittent Clouds\0".encode("utf-16be")
	weathervalue_text_table["japan_day_haze"] = "Haze\0".encode("utf-16be")
	weathervalue_text_table["japan_day_mostly_cloudy"] = "Mostly Cloudy\0".encode("utf-16be")
	weathervalue_text_table["japan_day_cloudy"] = "Cloudy\0".encode("utf-16be")
	weathervalue_text_table["japan_day_overcast"] = "Overcast\0".encode("utf-16be")
	weathervalue_text_table["japan_day_fog"] = "Fog\0".encode("utf-16be")
	weathervalue_text_table["japan_day_showers"] = "Showers\0".encode("utf-16be")
	weathervalue_text_table["japan_day_mostly_cloudy_with_showers"] = "Mostly Cloudy\nwith Showers\0".encode("utf-16be")
	weathervalue_text_table["japan_day_partly_sunny_with_showers"] = "Partly Sunny\nwith Showers\0".encode("utf-16be")
	weathervalue_text_table["japan_day_thunderstorms"] = "Thunderstorms\0".encode("utf-16be")
	weathervalue_text_table["japan_day_mostly_cloudy_with_thunderstorms"] = "Mostly Cloudy\nwith Thunderstorms\0".encode("utf-16be")
	weathervalue_text_table["japan_day_partly_sunny_with_thunderstorms"] = "Partly Sunny\nwith Thunderstorms\0".encode("utf-16be")
	weathervalue_text_table["japan_day_rain"] = "Rain\0".encode("utf-16be")
	weathervalue_text_table["japan_day_flurries"] = "Flurries\0".encode("utf-16be")
	weathervalue_text_table["japan_day_mostly_cloudy_with_flurries"] = "Mostly Cloudy\nwith Flurries\0".encode("utf-16be")
	weathervalue_text_table["japan_day_partly_sunny_with_flurries"] = "Partly Sunny\nwith Flurries\0".encode("utf-16be")
	weathervalue_text_table["japan_day_snow"] = "Snow\0".encode("utf-16be")
	weathervalue_text_table["japan_day_mostly_cloudy_with_snow"] = "Mostly Cloudy\nwith Snow\0".encode("utf-16be")
	weathervalue_text_table["japan_day_ice"] = "Ice\0".encode("utf-16be")
	weathervalue_text_table["japan_day_sleet"] = "Sleet\0".encode("utf-16be")
	weathervalue_text_table["japan_day_freezing_rain"] = "Freezing Rain\0".encode("utf-16be")
	weathervalue_text_table["japan_day_rain_and_snow"] = "Rain and Snow\0".encode("utf-16be")
	weathervalue_text_table["japan_night_clear"] = "Clear\0".encode("utf-16be")
	weathervalue_text_table["japan_night_mostly_clear"] = "Mostly Clear\0".encode("utf-16be")
	weathervalue_text_table["japan_night_partly_cloudy"] = "Partly Cloudy\0".encode("utf-16be")
	weathervalue_text_table["japan_night_intermittent_clouds"] = "Intermittent Clouds\0".encode("utf-16be")
	weathervalue_text_table["japan_night_hazy_moonlight"] = "Hazy Moonlight\0".encode("utf-16be")
	weathervalue_text_table["japan_night_mostly_cloudy"] = "Mostly Cloudy\0".encode("utf-16be")
	weathervalue_text_table["japan_night_partly_cloudy_with_showers"] = "Partly Cloudy\nwith Showers\0".encode("utf-16be")
	weathervalue_text_table["japan_night_mostly_cloudy_with_showers"] = "Mostly Cloudy\nwith Showers\0".encode("utf-16be")
	weathervalue_text_table["japan_night_partly_cloudy_with_thunderstorms"] = "Partly Cloudy\nwith Thunderstorms\0".encode("utf-16be")
	weathervalue_text_table["japan_night_mostly_cloudy_with_thunderstorms"] = "Mostly Cloudy\nwith Thunderstorms\0".encode("utf-16be")
	weathervalue_text_table["japan_night_mostly_cloudy_with_flurries"] = "Mostly Cloudy\nwith Flurries\0".encode("utf-16be")
	weathervalue_text_table["japan_night_mostly_cloudy_with_snow"] = "Mostly Cloudy\nwith Snow\0".encode("utf-16be")
	weathervalue_text_table["day_hot"] = "Hot\0".encode("utf-16be")
	weathervalue_text_table["day_cold"] = "Cold\0".encode("utf-16be")
	weathervalue_text_table["day_windy"] = "Windy\0".encode("utf-16be")
	weathervalue_text_table["japan_day_hot"] = "Hot\0".encode("utf-16be")
	weathervalue_text_table["japan_day_cold"] = "Cold\0".encode("utf-16be")
	weathervalue_text_table["japan_day_windy"] = "Windy\0".encode("utf-16be")
	weathervalue_text_table["end_padding"] = "\0".encode("utf-16be")

	i = 0
	bytes = 0
	for k,v in weathervalue_text_table.items():
		weathervalue_text_offsets[i] = bytes
		bytes+=len(v)
		i+=1

	return weathervalue_text_table

"""Makes the weather value offset table."""

def make_weather_offset_table():
	weathervalue_offset_table = collections.OrderedDict()
	dictionaries_weathervalue_offsettable.append(weathervalue_offset_table)
	weathervalue = collections.OrderedDict()
	weathervalue['0464'] = '0065'
	weathervalue['0462'] = '0065'
	weathervalue['0465'] = '0066'
	weathervalue['0463'] = '006B'
	weathervalue['05F4'] = '007A'
	weathervalue['04C9'] = '006B'
	weathervalue['04C8'] = '006A'
	weathervalue['0469'] = '006A'
	weathervalue['0680'] = '007C'
	weathervalue['052E'] = '0071'
	weathervalue['04CB'] = '006C'
	weathervalue['0467'] = '0067'
	weathervalue['0784'] = '007D'
	weathervalue['04CA'] = '007D'
	weathervalue['0466'] = '007D'
	weathervalue['052C'] = '006F'
	weathervalue['0592'] = '0076'
	weathervalue['04CD'] = '0076'
	weathervalue['0468'] = '0068'
	weathervalue['05E0'] = '0074'
	weathervalue['04CC'] = '006D'
	weathervalue['05AE'] = '0079'
	weathervalue['04CF'] = '0079'
	weathervalue['0549'] = '0073'
	weathervalue['052F'] = '0072'
	weathervalue['8464'] = '8065'
	weathervalue['85F4'] = '8065'
	weathervalue['8465'] = '8066'
	weathervalue['84C9'] = '806B'
	weathervalue['05F8'] = '807A'
	weathervalue['84C8'] = '806A'
	weathervalue['8466'] = '806C'
	weathervalue['852E'] = '8071'
	weathervalue['8467'] = '807D'
	weathervalue['84CA'] = '807D'
	weathervalue['8592'] = '8076'
	weathervalue['84CC'] = '806D'
	# Japan
	weathervalue['0064'] = '0001'
	weathervalue['0065'] = '0001'
	weathervalue['0066'] = '0002'
	weathervalue['0067'] = '0002'
	weathervalue['0068'] = '0001'
	weathervalue['00C4'] = '000A'
	weathervalue['00C5'] = '000A'
	weathervalue['00C6'] = '000A'
	weathervalue['00C7'] = '000A'
	weathervalue['012C'] = '0013'
	weathervalue['00C9'] = '000C'
	weathervalue['0069'] = '0003'
	weathervalue['0384'] = '0021'
	weathervalue['00D0'] = '000E'
	weathervalue['006A'] = '0005'
	weathervalue['012D'] = '0013'
	weathervalue['8190'] = '801A'
	weathervalue['00CA'] = '000C'
	weathervalue['006B'] = '0004'
	weathervalue['8191'] = '801A'
	weathervalue['00CB'] = '000C'
	weathervalue['8192'] = '801A'
	weathervalue['8193'] = '801A'
	weathervalue['8194'] = '801A'
	weathervalue['012F'] = '0016'
	weathervalue['006C'] = '8001'
	weathervalue['006D'] = '8001'
	weathervalue['00C8'] = '800A'
	weathervalue['00CC'] = '800A'
	weathervalue['00CD'] = '800A'
	weathervalue['00CE'] = '800A'
	weathervalue['00CF'] = '800C'
	weathervalue['00D1'] = '800C'
	weathervalue['00D2'] = '800E'
	weathervalue['00D3'] = '800E'
	weathervalue['00D4'] = '800D'
	weathervalue['00D5'] = '800D'
	# Extra
	weathervalue['0459'] = '0065'
	weathervalue['0460'] = '0065'
	weathervalue['0461'] = '0065'
	weathervalue['00EA'] = '0001'
	weathervalue['00EB'] = '0001'
	weathervalue['00EC'] = '0001'

	for k, v in weathervalue.items():
		weathervalue_offset_table[num()] = binascii.unhexlify(k)
		weathervalue_offset_table[num()] = binascii.unhexlify(v)
		weathervalue_offset_table[num()] = u32(0)

	return weathervalue_offset_table

def make_uvindex_text_table():
	uvindex_text_table = collections.OrderedDict()
	dictionaries_uvindextexttable.append(uvindex_text_table)
	low = 'Low'
	moderate = 'Moderate'
	high = 'High'
	veryhigh = 'Very High'
	extreme = 'Extreme'
	uvindex_text_table[0] = "\0".join([low, low, low, moderate, moderate, moderate, high, high, veryhigh, veryhigh, veryhigh, extreme, extreme]).encode("utf-16be")+pad(2)

	return uvindex_text_table

"""This makes the laundry text table. Since it's in Japanese, the strings are encoded in hex."""

def make_laundry_text_table():
	laundry_text_table = collections.OrderedDict()
	dictionaries_laundrytexttable.append(laundry_text_table)

	laundry_text_table[0] = binascii.unhexlify('5916306b5e72305b307e305b30930000')
	laundry_text_table[1] = binascii.unhexlify('59165e7230576642306f59295019306b6ce8610f0000')
	laundry_text_table[2] = binascii.unhexlify('59165e7230576642306f59295019306b6ce8610f0000')
	laundry_text_table[3] = binascii.unhexlify('59165e7230576642306f59295019306b6ce8610f0000')
	laundry_text_table[4] = binascii.unhexlify('4e7e304d3044307e30443061ff1a000a4e0065e55e723057306630824e7e304d304d3089306a30443082306e304c591a30440000')
	laundry_text_table[5] = binascii.unhexlify('4e7e304d307e3042307e3042ff1a000a4e0065e55e72305b3070304a304a3080306d4e7e304f0000')
	laundry_text_table[6] = binascii.unhexlify('4e7e304d30883057ff1a000a4e0065e55e72305b3070534152063088304f4e7e304f0000')
	laundry_text_table[7] = binascii.unhexlify('4e7e304d30883057ff1a000a534a65e55e72305b3070304a304a3080306d4e7e304f0000')
	laundry_text_table[8] = binascii.unhexlify('4e7e304d975e5e38306b30883057ff1a000a534a65e55e72305b3070534152063088304f4e7e304f0000')
	laundry_text_table[9] = binascii.unhexlify('4e7e304d975e5e38306b30883057ff1a000a003230fb0033664295935e72305b3070304a304a3080306d4e7e304f0000')
	laundry_text_table[10] = binascii.unhexlify('4e7e304d975e5e38306b30883057ff1a000a003230fb0033664295935e72305b3070534152063088304f4e7e304f0000')
	laundry_text_table[11] = binascii.unhexlify('6b206e2cff0830c730fc30bf306a3057ff090000')

	return laundry_text_table

"""This makes the pollen text table. Since it's in Japanese, the strings are encoded in hex."""

def make_pollen_text_table():
	pollen_text_table = collections.OrderedDict()
	dictionaries_pollentexttable.append(pollen_text_table)

	pollen_text_table[0] = binascii.unhexlify('5c11306a30440000')
	pollen_text_table[1] = binascii.unhexlify('30843084591a30440000')
	pollen_text_table[2] = binascii.unhexlify('591a30440000')
	pollen_text_table[3] = binascii.unhexlify('975e5e38306b591a30440000')
	pollen_text_table[4] = binascii.unhexlify('6b206e2cff0830c730fc30bf306a3057ff090000')

	return pollen_text_table

def make_location_table(list):
	location_table = collections.OrderedDict()
	dictionaries_locationtable.append(location_table)
	for keys in list.keys():
		numbers = get_number(list, keys)
		location_table["location_code_%s" % numbers] = binascii.unhexlify(get_loccode(list, keys)) # Wii Location Code.
		location_table["city_text_offset_%s" % numbers] = u32(0) # Offset for location's city text
		location_table["region_text_offset_%s" % numbers] = u32(0) # Offset for location's region text
		location_table["country_text_offset_%s" % numbers] = u32(0) # Offset for location's country text
		location_table["latitude_coordinates_%s" % numbers] = globe[keys]['lat'] # Latitude coordinates for location on globe
		location_table["longitude_coordinates_%s" % numbers] = globe[keys]['lng'] # Longitude coordinates for location on globe
		location_table["location_zoom_1_%s" % numbers] = binascii.unhexlify(str(zoom(list, 1, keys))) # Location zoom for location on globe
		location_table["location_zoom_2_%s" % numbers] = binascii.unhexlify(zoom(list, 2, keys)) # Location zoom for location on globe
		location_table["padding_%s" % numbers] = u16(0)

	return location_table

def make_forecast_text_table(list):
	text_table = collections.OrderedDict()
	dictionaries_texttable.append(text_table)
	bytes = 0
	for keys in list.keys():
		numbers = get_number(list, keys)
		if len(get_region(list, keys)) == 0: state = None
		else: state = get_region(list, keys)
		if len(get_country(list, keys)) == 0: country = None
		else: country = get_country(list, keys)
		text = "\0".join(filter(None, [get_city(list, keys), state, country])).decode("utf-8").encode("utf-16be")
		text_table["keys_%s" % numbers] = text+pad(2)
		append(list,keys,bytes)
		bytes+=len(get_city(list, keys).decode("utf-8").encode("utf-16be"))+2
		if state is not None:
			append(list,keys,bytes)
			bytes+=len(get_region(list, keys).decode("utf-8").encode("utf-16be"))+2
		else: append(list,keys,'None')
		if country is not None:
			append(list,keys,bytes)
			bytes+=len(get_country(list, keys).decode("utf-8").encode("utf-16be"))+2
		else: append(list,keys,'None')

	return text_table

def get_weathericon(icon):
	weathericonstore[-1] = 'FFFF' # None
	weathericonstore[1] = '0464' # Sunny
	weathericonstore[2] = '0462' # Mostly Sunny
	weathericonstore[3] = '0465' # Partly Cloudy
	weathericonstore[4] = '0463' # Intermittent Clouds
	weathericonstore[5] = '05F4' # Haze
	weathericonstore[6] = '04C9' # Mostly Cloudy
	weathericonstore[7] = '04C8' # Cloudy
	weathericonstore[8] = '0469' # Overcast
	weathericonstore[11] = '0680' # Fog
	weathericonstore[12] = '052E' # Showers
	weathericonstore[13] = '04CB' # Mostly Cloudy with Showers
	weathericonstore[14] = '0467' # Partly Sunny with Showers
	weathericonstore[15] = '0784' # Thunderstorms
	weathericonstore[16] = '04CA' # Mostly Cloudy with Thunderstorms
	weathericonstore[17] = '0466' # Partly Sunny with Thunderstorms
	weathericonstore[18] = '052C' # Rain
	weathericonstore[19] = '0592' # Flurries
	weathericonstore[20] = '04CD' # Mostly Cloudy with Flurries
	weathericonstore[21] = '0468' # Partly Sunny with Flurries
	weathericonstore[22] = '05E0' # Snow
	weathericonstore[23] = '04CC' # Mostly Cloudy with Snow
	weathericonstore[24] = '05AE' # Ice
	weathericonstore[25] = '04CF' # Sleet
	weathericonstore[26] = '0549' # Freezing Rain
	weathericonstore[29] = '052F' # Rain and Snow
	weathericonstore[30] = '0459' # Hot
	weathericonstore[31] = '0460' # Cold
	weathericonstore[32] = '0461' # Windy
	weathericonstore[33] = '8464' # Clear
	weathericonstore[34] = '85F4' # Mostly Clear
	weathericonstore[35] = '8465' # Partly Cloudy
	weathericonstore[36] = '84C9' # Intermittent Clouds
	weathericonstore[37] = '05F8' # Hazy Moonlight (Custom)
	weathericonstore[38] = '84C8' # Mostly Cloudy
	weathericonstore[39] = '8466' # Partly Cloudy with Showers
	weathericonstore[40] = '852E' # Mostly Cloudy with Showers
	weathericonstore[41] = '8467' # Partly Cloudy with Thunderstorms
	weathericonstore[42] = '84CA' # Mostly Cloudy with Thunderstorms
	weathericonstore[43] = '8592' # Mostly Cloudy with Flurries
	weathericonstore[44] = '84CC' # Mostly Cloudy with Snow

	return weathericonstore[icon]

def get_weatherjpnicon(icon):
	jpnweathericonstore[-1] = 'FFFF' # None
	jpnweathericonstore[1] = '0064' # Sunny
	jpnweathericonstore[2] = '0065' # Mostly Sunny
	jpnweathericonstore[3] = '0066' # Partly Cloudy
	jpnweathericonstore[4] = '0067' # Intermittent Clouds
	jpnweathericonstore[5] = '0068' # Haze
	jpnweathericonstore[6] = '00C4' # Mostly Cloudy
	jpnweathericonstore[7] = '00C5' # Cloudy
	jpnweathericonstore[8] = '00C6' # Overcast
	jpnweathericonstore[11] = '00C7' # Fog
	jpnweathericonstore[12] = '012C' # Showers
	jpnweathericonstore[13] = '00C9' # Mostly Cloudy with Showers
	jpnweathericonstore[14] = '0069' # Partly Sunny with Showers
	jpnweathericonstore[15] = '0384' # Thunderstorms
	jpnweathericonstore[16] = '00D0' # Mostly Cloudy with Thunderstorms
	jpnweathericonstore[17] = '006A' # Partly Sunny with Thunderstorms
	jpnweathericonstore[18] = '012D' # Rain
	jpnweathericonstore[19] = '8190' # Flurries
	jpnweathericonstore[20] = '00CA' # Mostly Cloudy with Flurries
	jpnweathericonstore[21] = '006B' # Partly Sunny with Flurries
	jpnweathericonstore[22] = '8191' # Snow
	jpnweathericonstore[23] = '00CB' # Mostly Cloudy with Snow
	jpnweathericonstore[24] = '8192' # Ice
	jpnweathericonstore[25] = '8193' # Sleet
	jpnweathericonstore[26] = '8194' # Freezing Rain
	jpnweathericonstore[29] = '012F' # Rain and Snow
	jpnweathericonstore[30] = '00EA' # Hot
	jpnweathericonstore[31] = '00EB' # Cold
	jpnweathericonstore[32] = '00EC' # Windy
	jpnweathericonstore[33] = '006C' # Clear
	jpnweathericonstore[34] = '006D' # Mostly Clear
	jpnweathericonstore[35] = '00C8' # Partly Cloudy
	jpnweathericonstore[36] = '00CC' # Intermittent Clouds
	jpnweathericonstore[37] = '00CD' # Hazy Moonlight (Custom)
	jpnweathericonstore[38] = '00CE' # Mostly Cloudy
	jpnweathericonstore[39] = '00CF' # Partly Cloudy with Showers
	jpnweathericonstore[40] = '00D1' # Mostly Cloudy with Showers
	jpnweathericonstore[41] = '00D2' # Partly Cloudy with Thunderstorms
	jpnweathericonstore[42] = '00D3' # Mostly Cloudy with Thunderstorms
	jpnweathericonstore[43] = '00D4' # Mostly Cloudy with Flurries
	jpnweathericonstore[44] = '00D5' # Mostly Cloudy with Snow

	return jpnweathericonstore[icon]

"""Database of wind direction values."""

def get_wind_direction(degrees):
	winddirection = {}
	winddirection["NNE"] = '01'
	winddirection["NE"] = '02'
	winddirection["ENE"] = '03'
	winddirection["E"] = '04'
	winddirection["ESE"] = '05'
	winddirection["SE"] = '06'
	winddirection["SSE"] = '07'
	winddirection["S"] = '08'
	winddirection["SSW"] = '09'
	winddirection["SW"] = '10'
	winddirection["WSW"] = '11'
	winddirection["W"] = '12'
	winddirection["WNW"] = '13'
	winddirection["NW"] = '14'
	winddirection["NNW"] = '15'
	winddirection["N"] = '16'

	return winddirection[degrees]

requests.packages.urllib3.disable_warnings() # This is so we don't get some warning about SSL.
if not useLegacy: test_keys()
for list in weathercities:
	global language_code,country_code,mode
	language_code = 1
	country_code = forecastlists.bincountries[list.values()[0][2]]
	print "Processing list #%s" % weathercities.index(list)
	for k,v in forecastlists.weathercities_international.items():
		if k not in list:
			if v[2] in forecastlists.bincountries and forecastlists.bincountries[v[2]] is not country_code: list[k] = v
			else: list[k] = v
		elif v[2] is not list[k][2]: list[k+" 2"] = v
	get_locationcode(list)
	for keys in list.keys():
		if keys in cache and cache[keys] == get_all(list,keys): cached+=1
	print "Downloading Forecast Data ...\n"
	for keys in list.keys():
		if keys not in cache or cache[keys] != get_all(list,keys): get_data(list,keys)
	print "\n\n[*] Skipped %s cached cities" % cached
	cities+=citycount
	total+=len(list)
	for i in range(1, 3):
		mode = i
		make_bins(list)
		reset_data(list)
	print "Done"
	print "\n"

print "API Requests: %s" % apirequests
if not useLegacy: print "API Key Cycles: %s" % apicycle
print "Request Retries: %s" % retrycount
print "Processed Cities: %s/%s" % (cities,total)

os.remove('forecastlists.pyc')

if production:
	"""This will use a webhook to log that the script has been ran."""
	data = {"username": "Forecast Bot", "content": "Weather Data has been updated!", "avatar_url": "http://rc24.xyz/images/logo-small.png", "attachments": [{"fallback": "Weather Data Update", "color": "#0381D7", "author_name": "RiiConnect24 Forecast Script", "author_icon": "https://rc24.xyz/images/profile_forecast.png", "text": "Weather Data has been updated!", "title": "Update!", "fields": [{"title": "Script", "value": "Forecast Channel", "short": "false"}], "thumb_url": "https://rc24.xyz/images/profile_forecast.png", "footer": "RiiConnect24 Script", "footer_icon": "https://rc24.xyz/images/logo-small.png", "ts": int(time.mktime(datetime.utcnow().timetuple()))}]}
	for url in webhook_urls: post_webhook = requests.post(url, json=data, allow_redirects=True)

print "Completed Successfully"