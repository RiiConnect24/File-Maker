#!/usr/bin/python
# -*- coding: utf-8 -*-

# ===========================================================================
# ACCUWEATHER API KEY GENERATION SCRIPT
# VERSION 1.0 - RELEASE
# **********************************************************
# © 2017 JOHN PANSERA - ALL RIGHTS RESERVED
# **********************************************************
# WWW.RC24.XYZ
# ===========================================================================

import mechanize
import sys
import os
import random
import time

# CONFIGURATION VALUES
URL_USER_ADD = 'http://developer.accuweather.com/user/9344/apps/add' #<--- COPY LINK FROM 'ADD A NEW APP' BUTTON
USER_NAME = 'USER NAME HERE'
PASSWORD = 'PASSWORD HERE'
cooldown = 5 # Cooldown (seconds) for key generation
# === DO NOT EDIT PAST THIS LINE ===
URL_LOGIN = 'http://developer.accuweather.com/user'
URL_MY_APPS = 'http://developer.accuweather.com/user/me/apps'
br = mechanize.Browser()
first = False

def connect():
	print "Connecting ..."
	br.set_handle_redirect(True)
	br.open(URL_LOGIN)
	print "Logging in ..."
	br.form = list(br.forms())[2]
	br.form['name'] = USER_NAME
	br.form['pass'] = PASSWORD
	br.submit()
	br.open(URL_MY_APPS)
	
def get_results():
	global first
	if first:
		f = open('temp.rc24', 'rb')
		oldlist = f.read()
		f.close()
		os.remove('temp.rc24')
	f = open('temp.rc24', 'wb')
	f.write(br.response().read())
	f.flush()
	f.close()
	command = """cat temp.rc24 | grep '<span">' | cut -c 36- | cut -c -32"""
	results = os.popen(command).read().split('\n')
	del results[-1]
	if first:
		for key in results:
			if key not in oldlist:
				print key
	else:
		print "Currently there are %s keys active:" % len(results)
		for key in results: print key
		first = True
	
def add_key():
	br.open(URL_USER_ADD)
	br.form = list(br.forms())[1]
	rndstring = 'Forecast-Application-%s' % random.randint(0,100000)
	br.form['human'] = rndstring
	br.form['machine'] = rndstring
	a = random.randint(1,4)
	if a == 1: br.find_control('attribute_create_with_api[partnerapp]').items[0].selected=True
	if a == 2: br.find_control('attribute_create_with_api[internalapp]').items[0].selected=True
	if a == 3: br.find_control('attribute_create_with_api[productivityapp]').items[0].selected=True
	if a == 4: br.find_control('attribute_create_with_api[weatherapp]').items[0].selected=True
	br.submit()
	
print "AccuWeather API Key Generator\n"
print "By John Pansera / WWW.RC24.XYZ"
connect()
get_results()
count = raw_input('Enter Amount of Keys to Generate (Cooldown: %s Seconds): ' % cooldown)
print "Processing ..."
for _ in range(int(count)):
	time.sleep(cooldown)
	add_key()
	get_results()
print "Cleaning Up ..."
os.remove('temp.rc24')
print "Operation Completed Successfully"
