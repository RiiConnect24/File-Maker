#!/usr/bin/python
# -*- coding: utf-8 -*-

# ===========================================================================
# FORECAST CHANNEL GENERATION SCRIPT
# VERSION 3.0
# AUTHORS: JOHN PANSERA, LARSEN VALLECILLO
# ****************************************************************************
# Copyright (c) 2015-2017 RiiConnect24, and it's (Lead) Developers
# ===========================================================================

import binascii
import collections
import forecastlists
import io
import json
import math
import numpy
import os
import gc
import pycountry
import random
import requests
import rollbar
import rsa
import struct
import subprocess
import sys
import threading
import time
import xmltodict
import pickle
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
total = 0 # Total Amount of Cities Processed
progcount = 0 # Progress Bar Character Counter
useLegacy = True # Use AccuWeather Legacy API Instead (Speedup)
useVerbose = False # Print more verbose messages
useMultithreaded = True # Use multithreading
keyCache = False
count = {} # Offset Storage
file = None

weathercities = [forecastlists.weathercities008, forecastlists.weathercities009, forecastlists.weathercities010, forecastlists.weathercities011, forecastlists.weathercities012, forecastlists.weathercities013, forecastlists.weathercities014, forecastlists.weathercities015, forecastlists.weathercities016, forecastlists.weathercities017, forecastlists.weathercities018, forecastlists.weathercities019, forecastlists.weathercities020, forecastlists.weathercities021, forecastlists.weathercities022, forecastlists.weathercities023, forecastlists.weathercities024, forecastlists.weathercities025, forecastlists.weathercities026, forecastlists.weathercities027, forecastlists.weathercities028, forecastlists.weathercities029, forecastlists.weathercities030, forecastlists.weathercities031, forecastlists.weathercities032, forecastlists.weathercities033, forecastlists.weathercities034, forecastlists.weathercities035, forecastlists.weathercities036, forecastlists.weathercities037, forecastlists.weathercities038, forecastlists.weathercities039, forecastlists.weathercities040, forecastlists.weathercities041, forecastlists.weathercities042, forecastlists.weathercities043, forecastlists.weathercities044, forecastlists.weathercities045, forecastlists.weathercities046, forecastlists.weathercities047, forecastlists.weathercities048, forecastlists.weathercities049, forecastlists.weathercities050, forecastlists.weathercities051, forecastlists.weathercities052, forecastlists.weathercities065, forecastlists.weathercities066, forecastlists.weathercities067, forecastlists.weathercities074, forecastlists.weathercities076, forecastlists.weathercities077, forecastlists.weathercities078, forecastlists.weathercities079, forecastlists.weathercities082, forecastlists.weathercities083, forecastlists.weathercities088, forecastlists.weathercities094, forecastlists.weathercities095, forecastlists.weathercities096, forecastlists.weathercities098, forecastlists.weathercities105, forecastlists.weathercities107, forecastlists.weathercities108, forecastlists.weathercities110]

print "Forecast Channel Downloader \n"
print "By John Pansera and Larsen Vallecillo / www.rc24.xyz \n"
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
weatherloc = {}
cache = {}
laundry = {}
duplicates = {}

def u8(data):
	if data < 0 or data > 255:
		output("u8 Value Pack Failure: %s" % data, "CRITICAL")
		data = 0
	return struct.pack(">B", data)

def u16(data):
	if data < 0 or data > 65535:
		output("u16 Value Pack Failure: %s" % data, "CRITICAL")
		data = 0
	return struct.pack(">H", data)

def u32(data):
	if data < 0 or data > 4294967295:
		output("u32 Value Pack Failure: %s" % data, "CRITICAL")
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

def to_celsius(temp):
	return int((temp-32)*5/9)

def to_fahrenheit(temp):
	return int((temp*9/5)+32)

def kmh_mph(wind):
	return int(round(wind*0.621371))

def mph_kmh(wind):
	return int(round(float(wind)*1.60934))

def time_convert(time):
	if mode == 1: return int((time - 946684800) / 60)
	elif mode == 2: return int((time - 1325376000) / 60) # Still have to adjust this.

def get_epoch():
	return int(time.time())

def get_rounded_hour():
	return round(time.time()/3600)*3600

def get_city(list, key):
	return list[key][0][1]

def get_region(list, key):
	return list[key][1][1]

def get_country(list, key):
	return list[key][2][1]

def get_all(list, key):
	return ", ".join(filter(None, [get_city(list, key),get_region(list, key),get_country(list, key)]))

def get_lockey(key):
	return locationkey[key]

def append(list, key, data):
	list[str(key)].append(data)

def get_number(list, key):
	return list.keys().index(key)

def pad(amnt):
	return "\0"*amnt

def get_index(list, key, num):
	return list[key][num]

def num():
	global number
	num1 = number
	number += 1
	return num1

"""This is a progress bar to display how much of the forecast in a list has been downloaded."""
"""It actually looks pretty cool."""

def progress(percent,list):
	global progcount
	bar = 35
	prog = """-\|/""" # These are characters which will make a spinning effect.
	fill = int(round(percent*bar/100))
	if citycount/(len(list)-cached) == 1:
		if os.name == 'nt': display = '*'
		else: display = "✓"
		progcount = 0
	else: display = prog[progcount]
	sys.stdout.write("\r%s\rProgress: %s%% [%s] (%s/%s) [%s] [%s] %s" % (" "*(bar+38),int(round(percent)),("="*fill)+(" "*(bar-fill)),citycount,len(list)-cached,display,concurrent,"."*progcount))
	sys.stdout.flush()
	progcount+=1
	if progcount == 4: progcount = 0

def build_progress():
	i = 0
	while build:
		sys.stdout.write("\r"+" "*58+"\rBuilding Files: "+"["+i*" "+"="*3+(35-i-2)*" "+"] ...")
		sys.stdout.flush()
		i+=1
		if i == 34: i = 0
		time.sleep(0.05)

def output(text,level):
	if loop or build:
		if level is "INFO":
			sys.stdout.write("\r%s\r%s\n\n" % ((" "*73),text))
			sys.stdout.flush()
		elif level is "VERBOSE" and useVerbose:
			sys.stdout.write("\r%s\r%s\n\n" % ((" "*73),text))
			sys.stdout.flush()
		elif level is "WARNING" or level is "CRITICAL":
			sys.stdout.write("\r%s\r%s\n\n" % ((" "*73),text))
			sys.stdout.flush()
			if production: rollbar.report_message(text, level.lower())
	else: print text

def display_loop(list):
	while loop:
		progress(float(citycount)/float(len(list)-cached)*100,list)
		time.sleep(0.1)

def get_icon(icon,list,key):
	if list[key][2][1] is "Japan": return get_weatherjpnicon(icon)
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
			ratelimit_remaining = int(testapi.headers["RateLimit-Remaining"])
			if ratelimit_remaining > 0: total+=ratelimit_remaining
			else: invalid = True
		else: invalid = True
		if invalid:
			print "Warning: Key %s marked as unusable" % keys
			accuweather_api_keys[keys-1] = None
	print "%s Requests Available" % total
	print "Processed %s Keys" % len(accuweather_api_keys)

"""Resets bin-specific values for next generation."""

def reset_data(l):
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

def get_apikey():
	global apicount,apicycle
	key = None
	while key is None:
		key = accuweather_api_keys[apicount]
		if apicount == len(accuweather_api_keys)-1:
			apicount = 0
			apicycle += 1
		else: apicount += 1
	return key

"""This requests data from AccuWeather's API. It also retries the request if it fails."""

def request_data(url):
	global retrycount,apirequests
	header = {'Accept-Encoding' : 'gzip, deflate'} # This is to make the data download faster.
	apirequests+=1
	i = 0
	c = 0
	while c == 0:
		if i == 4: return -1
		if i > 0: retrycount+=1
		data = s.get(url, headers=header)
		status_code = data.status_code
		if "regions" in url and status_code != 200: return None
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
	elif mode == 2: timestamp = time_convert(get_rounded_hour())
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
		if v[1][1] is "" and v[2][1] not in forecastlists.bincountries: weatherloc[listid]['null'].setdefault(v[0][1], len(weatherloc[listid]['null'])+1)
		else:
			weatherloc[listid].setdefault(v[2][1], {})
			weatherloc[listid][v[2][1]].setdefault(v[1][1], {})
			weatherloc[listid][v[2][1]][v[1][1]].setdefault(v[0][1], len(weatherloc[listid][v[2][1]][v[1][1]])+1)
			weatherloc[listid]['states'].setdefault(v[2][1], {})
			weatherloc[listid]['states'][v[2][1]].setdefault(v[1][1], len(weatherloc[listid]['states'][v[2][1]])+2)

"""If the script was unable to get forecast for a city, it's filled with this blank data."""

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
	for i in range(0,8): week[key][i+10] = to_celsius(week[key][i])
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
	today[key][2] = to_celsius(today[key][0])
	today[key][3] = to_celsius(today[key][1])
	today[key][4] = get_icon(int(apidaily['DailyForecasts'][0]['Day']['Icon']),list,key)
	tomorrow[key][0] = int(round(api5day['DailyForecasts'][1]['Temperature']['Minimum']['Value']))
	tomorrow[key][1] = int(round(api5day['DailyForecasts'][1]['Temperature']['Maximum']['Value']))
	tomorrow[key][2] = to_celsius(tomorrow[key][0])
	tomorrow[key][3] = to_celsius(tomorrow[key][1])
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
	if list[key][2][1] is "Japan":
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
	for i in range(0,8): week[key][i+10] = to_celsius(week[key][i])
	week[key][20] = get_icon(int(apilegacy['adc_database']['forecast']['day'][1]['daytime']['weathericon']),list,key)
	week[key][21] = get_icon(int(apilegacy['adc_database']['forecast']['day'][2]['daytime']['weathericon']),list,key)
	week[key][22] = get_icon(int(apilegacy['adc_database']['forecast']['day'][3]['daytime']['weathericon']),list,key)
	week[key][23] = get_icon(int(apilegacy['adc_database']['forecast']['day'][4]['daytime']['weathericon']),list,key)
	current[key][3] = int(apilegacy['adc_database']['currentconditions']['temperature'])
	current[key][4] = to_celsius(current[key][3])
	weathericon[key] = get_icon(int(apilegacy['adc_database']['currentconditions']['weathericon']),list,key)
	current[key][0] = apilegacy['adc_database']['currentconditions']['winddirection']
	current[key][2] = int(apilegacy['adc_database']['currentconditions']['windspeed'])
	current[key][1] = mph_kmh(current[key][2])
	today[key][0] = int(apilegacy['adc_database']['forecast']['day'][0]['daytime']['lowtemperature'])
	today[key][1] = int(apilegacy['adc_database']['forecast']['day'][0]['daytime']['hightemperature'])
	today[key][2] = to_celsius(today[key][0])
	today[key][3] = to_celsius(today[key][1])
	today[key][4] = get_icon(int(apilegacy['adc_database']['forecast']['day'][0]['daytime']['weathericon']),list,key)
	tomorrow[key][0] = int(apilegacy['adc_database']['forecast']['day'][1]['daytime']['lowtemperature'])
	tomorrow[key][1] = int(apilegacy['adc_database']['forecast']['day'][1]['daytime']['hightemperature'])
	tomorrow[key][2] = to_celsius(tomorrow[key][0])
	tomorrow[key][3] = to_celsius(tomorrow[key][1])
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
	week[key][29] = int(to_celsius(week[key][25]))
	week[key][30] = int(to_celsius(week[key][26]))
	week[key][31] = int(to_celsius(week[key][27]))
	week[key][32] = int(to_celsius(week[key][28]))
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

"""Get the location data from the legacy API."""
"""The script currently gets data from the servers the Android app of AccuWeather uses."""
"""Please don't attack us for doing this, AccuWeather. You're my friend and I want to keep it that way."""

def get_legacy_location(list, key):
	i = 0
	if keyCache and key not in duplicates: locationkey[key] = cachefile[key]
	else: locationkey[key] = None
	while locationkey[key] is None:
		if i == 2: return -1
		location = request_data("http://accuwxturbotablet.accu-weather.com/widget/accuwxturbotablet/city-find.asp?location=%s" % get_search(list,key,i))
		try:
			if int(location['adc_database']['citylist']['@us'])+int(location['adc_database']['citylist']['@intl']) > 1: locationkey[key] = location['adc_database']['citylist']['location'][0]['@location'][7:]
			else: locationkey[key] = location['adc_database']['citylist']['location']['@location'][7:]
		except: pass
		i+=1

"""Tenki's where we're getting the laundry index for Japan."""
"""Currently, it's getting it from the webpage itself, but we might look for an API they use."""

def get_tenki_data(key):
	laundry[key] = 255
	if key in forecastlists.jpncities:
		output("Getting Tenki Data ...", "VERBOSE")
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

def hex_write(loc, data):
	global file
	file.seek(loc)
	file.write(u32(data))

def offset_write(value):
	global file,seek_offset
	seek_offset+=4
	file.seek(seek_offset)
	file.write(u32(value))

def make_bins(list):
	make_forecast_bin(list)
	make_short_bin(list)

def make_forecast_bin(list):
	global japcount,constant,count,file,seek_offset,seek_base,extension
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
	dictionaries = [header,long_forecast_table,short_japan_tables,weathervalue_offset_table,uvindex_table,laundryindex_table,pollenindex_table,location_table,weathervalue_text_table,uvindex_text_table,laundry_text_table,pollen_text_table,text_table]
	if mode == 1: extension = "bin"
	elif mode == 2: extension = "bi2"
	file = io.BytesIO()
	file1 = 'forecast~.%s.%s_%s' % (extension, str(country_code).zfill(3), str(language_code))
	file2 = 'forecast.%s~.%s+%s' % (extension, str(country_code).zfill(3), str(language_code))
	file3 = 'forecast.%s.%s_%s' % (extension, str(country_code).zfill(3), str(language_code))
	file4 = 'forecast.%s' % extension
	file.write(pad(20))
	for i in dictionaries:
		for v in i.values(): file.write(v)
		count[constant] = file.tell()
		constant+=1
	file.write(pad(16))
	file.write('RIICONNECT24'.encode('ASCII')) # This can be used to identify that we made this file.
	file.seek(0)
	hex_write(12,timestamps(0,0))
	hex_write(16,timestamps(2,0))
	hex_write(36,count[0])
	hex_write(32,int(len(list)-japcount))
	hex_write(40,japcount)
	if japcount > 0: hex_write(44,count[1])
	hex_write(48,len(forecastlists.weatherconditions)*2)
	hex_write(52,count[2])
	hex_write(60,count[3])
	hex_write(68,count[4])
	hex_write(76,count[5])
	hex_write(84,count[6])
	seek_offset = count[2]
	seek_base = count[7]
	for i in [forecastlists.weatherconditions.values()[j//2] for j in range(len(forecastlists.weatherconditions.values())*2)]:
		offset_write(seek_base)
		seek_base+=len(i[0][language_code].decode('utf-8').encode('utf-16be'))+2
		seek_offset+=4
	"""UV Index"""
	seek_offset = count[3]
	seek_base = count[8]
	for i in forecastlists.uvindex.values():
		offset_write(seek_base)
		seek_base+=len(i[language_code].decode('utf-8').encode('utf-16be'))+2
		seek_offset+=4
	"""Laundry Table"""
	seek_offset = count[4]
	seek_base = count[9]
	for i in forecastlists.laundry.values():
		offset_write(seek_base)
		seek_base+=len(i.decode('utf-8').encode('utf-16be'))+2
		seek_offset+=4
	"""Pollen Table"""
	seek_offset = count[5]
	seek_base = count[10]
	for i in forecastlists.pollen.values():
		offset_write(seek_base)
		seek_base+=len(i.decode('utf-8').encode('utf-16be'))+2
		seek_offset+=4
	"""Location Text"""
	seek_offset = count[6]
	seek_base = count[11]
	for key in list.keys():
		offset_write(seek_base)
		seek_base+=len(list[key][0][language_code].decode('utf-8').encode('utf-16be'))+2
		if len(list[key][1][language_code]) > 0:
			offset_write(seek_base)
			seek_base+=len(list[key][1][language_code].decode('utf-8').encode('utf-16be'))+2
		else: offset_write(0)
		if len(list[key][2][language_code]) > 0:
			offset_write(seek_base)
			seek_base+=len(list[key][2][language_code].decode('utf-8').encode('utf-16be'))+2
		else: offset_write(0)
		seek_offset+=12
	file.seek(0)
	with open(file1, 'wb') as temp:
		temp.write(file.read())
	file.close()
	if production:
		os.system('dd if="' + file1 + '" of="' + file2 + '" bs=1 skip=12 status=none') # This cuts off the first 12 bytes.
		sign_file(file2, file3, file4)
		os.remove(file1)

def make_short_bin(list):
	short_forecast_header = make_header_short(list)
	short_forecast_table = make_short_forecast_table(list)
	file1 = 'short.%s~.%s_%s' % (extension, str(country_code).zfill(3), str(language_code))
	file2 = 'short.%s.%s_%s' % (extension, str(country_code).zfill(3), str(language_code))
	file3 = 'short.%s' % extension
	file = io.BytesIO()
	file.write(u32(timestamps(0,0)))
	file.write(u32(timestamps(2,0)))
	for v in short_forecast_header.values(): file.write(v)
	for v in short_forecast_table.values(): file.write(v)
	file.seek(0)
	with open(file1, 'wb') as temp:
		temp.write(file.read())
	file.close()
	if production: sign_file(file1, file2, file3)

def sign_file(name, local_name, server_name):
	output("Processing " + local_name + " ...", "VERBOSE")
	file = open(name, 'rb')
	copy = file.read()
	crc32 = format(binascii.crc32(copy) & 0xFFFFFFFF, '08x')
	size = os.path.getsize(name)+12
	dest = open(local_name, 'w+')
	dest.write(u32(0))
	dest.write(u32(size))
	dest.write(binascii.unhexlify(crc32))
	dest.write(copy)
	os.remove(name)
	dest.close()
	file.close()
	output("Compressing ...", "VERBOSE")
	subprocess.call(["mv", local_name, local_name+"-1"])
	subprocess.call(["%s/lzss" % lzss_path, "-evf", local_name+"-1"], stdout=subprocess.PIPE)
	file = open(local_name + '-1', 'rb')
	new = file.read()
	dest = open(local_name, "w+")
	key = open(key_path, 'rb')
	output("RSA Signing ...", "VERBOSE")
	private_key = rsa.PrivateKey.load_pkcs1(key.read(), "PEM") # Loads the RSA key.
	signature = rsa.sign(new, private_key, "SHA-1") # Makes a SHA1 with ASN1 padding.
	dest.write(binascii.unhexlify(str(0).zfill(128))) # Padding. This is where data for an encrypted WC24 file would go (such as the header and IV), but this is not encrypted so it's blank.
	dest.write(signature)
	dest.write(new)
	dest.close()
	file.close()
	key.close()
	subprocess.call(["mkdir", "-p", "%s/%s/%s" % (file_path, language_code, str(country_code).zfill(3))]) # Create directory if it does not exist
	path = "%s/%s/%s/%s" % (file_path, language_code, str(country_code).zfill(3), server_name) # Path on the server to put the file.
	subprocess.call(["cp", local_name, path])
	os.remove(local_name)
	os.remove(local_name + "-1")

def get_data(list, name):
	global citycount,cache,apilegacy,concurrent
	citycount+=1
	cache[name] = get_all(list, name)
	globe[name] = {}
	if useMultithreaded: concurrent+=1
	blank_data(list,name,True)
	if get_legacy_location(list, name) is None:
		apilegacy = request_data("http://accuwxturbotablet.accu-weather.com/widget/accuwxturbotablet/weather-data.asp?locationkey=%s" % get_lockey(name))
		get_tenki_data(name) # Get data for Japanese cities
		if apilegacy is not -1:
			get_legacy_api(list, name)
			get_weekly(list, name)
			get_hourly_forecast(list, name)
	else:
		output('Unable to retrieve data for %s - using blank data' % name, "WARNING")
		progress(float(citycount)/float(len(list)-cached)*100,list)
	if useMultithreaded: concurrent-=1

def make_header_short(list):
	header = collections.OrderedDict()
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

def make_location_table(list):
	location_table = collections.OrderedDict()
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
	for keys in list.keys():
		text_table[num()] = "\0".join(filter(None, [list[keys][0][language_code], list[keys][1][language_code], list[keys][2][language_code]])).decode("utf-8").encode("utf-16be")+pad(2)
	return text_table

def make_weather_value_table():
	weathervalue_text_table = collections.OrderedDict()
	for k,v in forecastlists.weatherconditions.items():
		for _ in range(2): weathervalue_text_table[num()] = v[0][language_code].decode('utf-8').encode("utf-16be")+pad(2)
	return weathervalue_text_table

def make_weather_offset_table():
	weathervalue_offset_table = collections.OrderedDict()
	for k,v in forecastlists.weatherconditions.items():
		weathervalue_offset_table[num()] = binascii.unhexlify(v[1])
		weathervalue_offset_table[num()] = binascii.unhexlify(v[2])
		weathervalue_offset_table[num()] = u32(0)
		weathervalue_offset_table[num()] = binascii.unhexlify(v[3])
		weathervalue_offset_table[num()] = binascii.unhexlify(v[4])
		weathervalue_offset_table[num()] = u32(0)
	return weathervalue_offset_table

def make_uvindex_text_table():
	uvindex_text_table = collections.OrderedDict()
	uvindexlist = []
	for v in forecastlists.uvindex.values():
		uvindexlist.append(v[language_code])
	uvindex_text_table[0] = "\0".join(uvindexlist).decode('utf-8').encode("utf-16be")+pad(2)
	return uvindex_text_table

def make_laundry_text_table():
	laundry = collections.OrderedDict()
	for v in forecastlists.laundry.values():
		laundry[num()] = v.decode('utf-8').encode("utf-16be")+pad(2)
	return laundry

def make_pollen_text_table():
	pollen = collections.OrderedDict()
	for v in forecastlists.pollen.values():
		pollen[num()] = v.decode('utf-8').encode("utf-16be")+pad(2)
	return pollen

def get_weathericon(icon):
	if icon == -1: return 'FFFF'
	else: return forecastlists.weatherconditions[icon][1]

def get_weatherjpnicon(icon):
	if icon == -1: return 'FFFF'
	else: return forecastlists.weatherconditions[icon][3]

def get_wind_direction(degrees):
	return forecastlists.winddirection[degrees]

if production:
	output("Production Mode Enabled", "VERBOSE")
	rollbar.init(rollbar_key, "production")
else:
	output("Production Mode Disabled", "VERBOSE")
if not os.path.exists('locations.db'): locationkey["cache_expiration"] = time.time()+86400
else:
	file = open('locations.db','rb')
	cachefile = pickle.load(file)
	if time.time() > cachefile["cache_expiration"]:
		file.close()
		os.remove('locations.db')
	else: keyCache = True
requests.packages.urllib3.disable_warnings() # This is so we don't get some warning about SSL.
s = requests.Session() # Use session to speed up requests
if not useLegacy: test_keys()
total_time = time.time()
for list in weathercities:
	global language_code,country_code,mode,concurrent,loop
	threads = []
	concurrent = 0
	language_code = 1
	country_code = forecastlists.bincountries[list.values()[0][2][1]]
	if country_code == 0: bins = [0]
	elif country_code >= 8 and country_code <= 52: bins = [1,3,4]
	elif country_code >= 64 and country_code <= 110: bins = [1,2,3,4,5,6]
	else:
		print "Unknown country code - generating English only"
		bins = [1]
	print "Processing list #%s - %s (%s)" % (weathercities.index(list), country_code, list.values()[0][2][1])
	for k,v in forecastlists.weathercities_international.items():
		if k not in list:
			if v[2][1] in forecastlists.bincountries and forecastlists.bincountries[v[2][1]] is not country_code: list[k] = v
			else: list[k] = v
		elif v[2][1] is not list[k][2][1]: list[k+" 2"] = v
	get_locationcode(list)
	for keys in list.keys():
		if keys in cache and cache[keys] == get_all(list,keys): cached+=1
	if len(list)-cached is not 0:
		print "Downloading Forecast Data ...\n"
		loop = True
	dlthread = threading.Thread(target=display_loop,args=[list])
	dlthread.start()
	for keys in list.keys():
		if keys in cache and cache[keys] != get_all(list,keys) and keys not in duplicates: duplicates[keys] = locationkey[keys]
		if keys not in cache or cache[keys] != get_all(list,keys):
			if useMultithreaded: threads.append(threading.Thread(target=get_data, args=(list,keys)))
			else: get_data(list,keys)
	if useMultithreaded:
		for i in threads:
			while concurrent >= 2: time.sleep(0.005)
			i.start()
		for i in threads:
			i.join()
	loop = False
	dlthread.join()
	build = True
	print "\n"
	cities+=citycount
	total+=len(list)
	buildthread = threading.Thread(target=build_progress,args=[])
	buildthread.start()
	for i in range(1,3):
		mode = i
		for j in bins:
			language_code = j
			make_bins(list)
			reset_data(list)
	build = False
	buildthread.join()
	sys.stdout.write("\r"+" "*58+"\rBuilding Files: Complete")
	sys.stdout.flush()
	gc.collect()
	print "\n"

print "API Requests: %s" % apirequests
if not useLegacy: print "API Key Cycles: %s" % apicycle
print "Request Retries: %s" % retrycount
print "Processed Cities: %s/%s" % (cities,total)
print "Total Time: %s Seconds\n" % round(time.time()-total_time)

if not keyCache:
	cachefile = open('locations.db','wb+')
	for k,v in duplicates.items(): locationkey[k] = v
	pickle.dump(locationkey,cachefile)
	cachefile.flush()
	cachefile.close()

if production:
	"""This will use a webhook to log that the script has been ran."""
	data = {"username": "Forecast Bot", "content": "Weather Data has been updated!", "avatar_url": "http://rc24.xyz/images/logo-small.png", "attachments": [{"fallback": "Weather Data Update", "color": "#0381D7", "author_name": "RiiConnect24 Forecast Script", "author_icon": "https://rc24.xyz/images/webhooks/forecast/profile.png", "text": "Weather Data has been updated!", "title": "Update!", "fields": [{"title": "Script", "value": "Forecast Channel", "short": "false"}], "thumb_url": "https://rc24.xyz/images/webhooks/forecast/accuweather.png", "footer": "RiiConnect24 Script", "footer_icon": "https://rc24.xyz/images/logo-small.png", "ts": int(time.mktime(datetime.utcnow().timetuple()))}]}
	for url in webhook_urls: post_webhook = requests.post(url, json=data, allow_redirects=True)

print "Completed Successfully"
