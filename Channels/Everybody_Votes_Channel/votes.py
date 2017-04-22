#!/usr/bin/python
# -*- coding: utf-8 -*-

# ===========================================================================
# EVERYBODY VOTES CHANNEL GENERATION SCRIPT
# VERSION 0.5
# AUTHORS: JOHN PANSERA
# ****************************************************************************
# Copyright (c) 2015-2017 RiiConnect24, and it's (Lead) Developers
# ===========================================================================

import binascii
import collections
import json
import math
import os
import platform
import struct
import subprocess
import sys
import time
import io
import rsa
import datetime
from config import *

print "Everybody Votes Channel File Generator \n"
print "By John Pansera / Larsen Vallecillo / www.rc24.xyz \n"

MYSQL_HOSTNAME = ''
MYSQL_USERNAME = ''
MYSQL_PASSWORD = ''
MYSQL_DATABASE = ''

questions = 0
worldwide = 0
national = 0
question_data = {}
country_code = 49
country_count = 0
language_code = 1
languages = {}
num = 0
number = 0
poll_id = 955 # Same as Nintendo's original question poll ID
worldwide_q = False
national_q = False
voting = False
countries = {}
countries["United States"] = ['United States', 'United States', 'United States', 'United States', 'United States', 'United States', 'United States']

def time_convert(time):
	return int((time-946684800)/60)

def get_epoch():
	return int(time.time())

def get_timestamp(mode):
	time = time_convert(get_epoch())
	if mode == 1: time+=10080 # Seems to be what Nintendo used
	return time
	
def get_name():
	now = datetime.datetime.now()
	day = str(now.day).zfill(2)
	month = str(now.month).zfill(2)
	return month+day

def get_poll_id():
	global poll_id
	i = poll_id
	poll_id+=1
	return i
	
def pad(amnt):
	buffer = ""
	for _ in range(amnt): buffer+="\0"
	return buffer
	
def prepare():
	global country_count
	global countries
	global voting
	print "Preparing ..."
	country_count = len(countries)*7
	if raw_input('Is this a voting or an _q file? (v/q): ') is 'v': voting = True
	# National questions are listed first, then worldwide
	# \n is used as line break
	add_question("Do you like the Everybody Votes Channel?", "Yes", "No", 0)
	#add_question("What is for dinner?", "Meat", "Vegetables", 0)
	#add_question("Which kind of weather do you prefer?", "Cold", "Hot", 1)
	#add_question("Do you like RiiConnect24?", "Yes", "No", 1)
	
def num():
	global number
	num1 = number
	number += 1
	return num1
	
def dec(data):
	return int(data, 16)
	
def question():
	if raw_input('Would you like to enter a question? (Y/N) ') is 'Y':
		add_question(raw_input('Enter Question: '),raw_input('Enter Answer 1: '),raw_input('Enter Answer 2: '),int(raw_input('Is this a national (0) or a worldwide (1) question? ')))
	
def get_question(q):
	return question_data[q][0]
	
def get_response1(q):
	return question_data[q][1]
	
def get_response2(q):
	return question_data[q][2]
	
def is_worldwide(q):
	i = True
	if question_data[q][3] == 0: i = False
	return i
	
def add_question(q,r1,r2,f):
	global question_data
	global questions
	global national
	global worldwide
	global national_q
	global worldwide_q
	question_data[num()] = [q,r1,r2,f]
	questions+=1
	if f == 0:
		national+=1
		national_q = True
	elif f == 1:
		worldwide+=1
		worldwide_q = True

dictionaries = []

def u8(data):
	return struct.pack(">B", data)

def u16(data):
	return struct.pack(">H", data)

def u32(data):
	return struct.pack(">I", data)

def s8(data):
	return struct.pack(">b", data)

def s16(data):
	return struct.pack(">h", data)

def s32(data):
	return struct.pack(">i", data)
	
def offset_count():
	return u32(12 + sum(len(values) for dictionary in dictionaries for values in dictionary.values() if values))
	
def connect_mysql(value):
	connection = mysql.connector.connect( host=mysql_hostname, user=mysql_username, passwd=mysql_password, db=mysql_database )
	doQuery(connection)
	connection.close()
	
def sign_file(name):
	final = name+'.bin'
	print "Processing " + final + " ..."
	file = open(name, 'rb')
	copy = file.read()
	print "Calculating CRC32 ..."
	crc32 = format(binascii.crc32(copy) & 0xFFFFFFFF, '08x')
	print "Calculating Size ..."
	size = os.path.getsize(name)+12
	dest = open(final, 'w+')
	dest.write(u32(0))
	dest.write(u32(size))
	dest.write(binascii.unhexlify(crc32))
	dest.write(copy)
	os.remove(name)
	dest.close()
	file.close()
	print "Compressing ..."
	subprocess.call(["mono", "--runtime=v4.0.30319", "DSDecmp.exe", "-c", "lz10", final, final + "-1"])
	file = open(final + '-1', 'rb')
	new = file.read()
	dest = open(final, "w+")
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
	os.remove(final + "-1")
	
def make_bin(country_code):
	global countries
	print "Processing ..."
	voting = make_header()
	national_table = make_national_question_table(voting)
	worldwide_question = make_worldwide_question_table(voting)
	question_text_table = make_question_text_table(voting)
	country_table = make_country_name_table(voting)
	question_text = make_question_text(question_text_table)
	if voting: country_text = make_country_table(country_table)
	
	question_file = get_name()+'_q'
	print "Writing voting.bin ..."
	
	with open(question_file, 'wb') as f:
		for dictionary in dictionaries:
			print("Writing to %s ..." % hex(f.tell()))
			for values in dictionary.values():
				f.write(values)
		f.write(pad(10))
		f.write('RIICONNECT24'.encode("ascii"))
		f.flush()
	
	sign_file(question_file)
	
	print "Writing Completed"
	
def make_header():
	header = collections.OrderedDict()
	dictionaries.append(header)
	
	header["timestamp"] = u32(get_timestamp(0))
	header["country_code"] = u8(country_code)
	header["publicity_flag"] = u8(0)
	header["question_version"] = u8(1)
	header["result_version"] = u8(0)
	header["nqen_entry_number"] = u8(national)
	header["nqen_header_offset"] = u32(0)
	header["worldwide_question_num"] = u8(worldwide)
	header["worldwide_question_offset"] = u32(0)
	header["question_entry_number"] = u8(0)
	header["question_table_offset"] = u32(0)
	header["national_result_entry"] = u8(0)
	header["national_result_offset"] = u32(0)
	header["national_result_detailed"] = u16(0)
	header["national_result_detailed_offset"] = u32(0)
	header["position_entry_number"] = u16(0)
	header["position_header_offset"] = u32(0)
	header["worldwide_result_entry_num"] = u8(0)
	header["worldwide_result_table_offset"] = u32(0)
	header["worldwide_result_detailed_num"] = u16(0)
	header["worldwide_result_detailed_offset"] = u32(0)
	header["country_name_entry_num"] = u16(0)
	header["country_name_header_offset"] = u32(0)
	
	return header

def make_national_question_table(header):
	global national
	national_question_table = collections.OrderedDict()
	dictionaries.append(national_question_table)
	
	if national_q:
		header["nqen_header_offset"] = offset_count()
	
	for q in question_data.keys():
		if not is_worldwide(q):
			national_question_table["poll_id_%s" % num()] = u32(get_poll_id())
			national_question_table["unknown_%s" % num()] = u16(0)
			national_question_table["opening_timestamp_%s" % num()] = u32(get_timestamp(0))
			national_question_table["closing_timestamp_%s" % num()] = u32(get_timestamp(1))
			national_question_table["unknown_1_%s" % num()] = u8(1)
			national_question_table["unknown_2_%s" % num()] = u32(0)
	
	return national_question_table

def make_worldwide_question_table(header):
	global worldwide
	worldwide_question_table = collections.OrderedDict()
	dictionaries.append(worldwide_question_table)
	
	if worldwide_q:
		header["worldwide_question_offset"] = offset_count()
	
	for q in question_data.keys():
		if is_worldwide(q):
			worldwide_question_table["poll_id_%s" % num()] = u32(get_poll_id())
			worldwide_question_table["unknown_%s" % num()] = u16(0)
			worldwide_question_table["opening_timestamp_%s" % num()] = u32(get_timestamp(0))
			worldwide_question_table["closing_timestamp_%s" % num()] = u32(get_timestamp(1))
			worldwide_question_table["unknown_1_%s" % num()] = u8(1)
			worldwide_question_table["unknown_2_%s" % num()] = u32(0)
	
	return worldwide_question_table

def make_question_text_table(header):
	global questions
	question_text_table = collections.OrderedDict()
	dictionaries.append(question_text_table)
	
	header["question_entry_number"] = u8(questions)
	header["question_table_offset"] = offset_count()
	
	for q in question_data.keys():
		num = question_data.keys().index(q)
		question_text_table["language_code_%s" % num] = u8(language_code)
		question_text_table["question_offset_%s" % num] = u32(0)
		question_text_table["response_1_offset_%s" % num] = u32(0)
		question_text_table["response_2_offset_%s" % num] = u32(0)
	
	return question_text_table

def make_national_result_table(header):
	table = collections.OrderedDict()
	dictionaries.append(table)
	
	header["national_result_entry"] = u8(0)
	header["national_result_offset"] = offset_count()
	
	table["poll_id"] = u32(get_poll_id())
	table["male_voters_response_1_num"] = u32(0)
	table["male_voters_response_2_num"] = u32(0)
	table["female_voters_response_1_num"] = u32(0)
	table["female_voters_response_2_num"] = u32(0)
	table["accurate_prediction_voters_num"] = u32(0)
	table["inaccurate_prediction_voters_num"] = u32(0)
	table["total_number_voters"] = u32(0)
	
	return table

def make_national_result_detailed_table(header):
	table = collections.OrderedDict()
	dictionaries.append(table)
	
	header["national_result_detailed"] = u16(0)
	header["national_result_detailed_offset"] = offset_count()
	
	table["voters_response_1_num"] = u32(0)
	table["voters_response_2_num"] = u32(0)
	table["unknown"] = u8(0)
	table["region_code"] = u32(0)
	
	return table

def make_position_entry_table(header):
	table = collections.OrderedDict()
	dictionaries_position.append(table)
	
	header["position_entry_number"] = u16(0)
	header["position_header_offset"] = offset_count()
	
	table["response_1"] = u8(0)
	table["response_2"] = u8(0)

def make_worldwide_result_table(header):
	table = collections.OrderedDict()
	dictionaries.append(table)
	
	header["worldwide_result_entry_num"] = u8(0)
	header["worldwide_result_table_offset"] = offset_count()
	
	table["poll_id"] = u32(get_poll_id())
	table["male_voters_response_1_num"] = u32(0)
	table["male_voters_response_2_num"] = u32(0)
	table["female_voters_response_1_num"] = u32(0)
	table["female_voters_response_2_num"] = u32(0)
	table["accurate_prediction_voters_num"] = u32(0)
	table["inaccurate_prediction_voters_num"] = u32(0)
	table["total_number_voters"] = u32(0)
	
	return table

def make_worldwide_result_detailed_table(header):
	table = collections.OrderedDict()
	dictionaries.append(table)
	
	header["worldwide_result_detailed_num"] = u16(0)
	header["worldwide_result_detailed_offset"] = offset_count()
	
	table["unknown"] = u32(0)
	table["male_voters_response_1_num"] = u32(0)
	table["male_voters_response_2_num"] = u32(0)
	table["female_voters_response_1_num"] = u32(0)
	table["female_voters_response_2_num"] = u32(0)
	table["language_number"] = u16(0)
	table["language_offset"] = u32(0) # Unknown
	
	return table

def make_country_name_table(header):
	global countries
	country_name_table = collections.OrderedDict()
	dictionaries.append(country_name_table)
	
	header["country_name_entry_num"] = u16(country_count/7)
	header["country_name_header_offset"] = offset_count()
	
	for k in countries.keys():
		num = countries.keys().index(k)
		i = 0
		for _ in range(7):
			country_name_table["language_code_%s_%s" % (num,i)] = u32(i)
			country_name_table["text_offset_%s_%s" % (num,i)] = offset_count()
			i+=1
	
	return country_name_table
	
def make_language_table():
	global languages
	languages["Japanese"] = 0
	languages["English"] = 1
	languages["German"] = 2
	languages["French"] = 3
	languages["Spanish"] = 4
	languages["Italian"] = 5
	languages["Dutch"] = 6
	
def make_country_table(country_name_table):
	country_table = collections.OrderedDict()
	dictionaries.append(country_table)
	
	j = 0
	for k in countries.keys():
		num = countries.keys().index(k)
		i = 0
		for _ in range(7):
			country_name_table["language_code_%s_%s" % (num,i)] = u32(i)
			country_name_table["text_offset_%s_%s" % (num,i)] = offset_count()
			country_table[j] = countries[k][i].encode("utf-16be")+pad(2)
			i+=1
			j+=1
		
	return country_table
	
def make_question_text(question_text_table):
	global question_data
	question_text = collections.OrderedDict()
	dictionaries.append(question_text)
	
	for q in question_data.keys():
		num = question_data.keys().index(q)
		question_text_table["question_offset_%s" % num] = u32(dec(binascii.hexlify(offset_count())))
		question_text["0_%s" % num] = get_question(q).encode("utf-16be")+pad(2)
		question_text_table["response_1_offset_%s" % num] = u32(dec(binascii.hexlify(offset_count())))
		question_text["1_%s" % num] = get_response1(q).encode("utf-16be")+pad(2)
		question_text_table["response_2_offset_%s" % num] = u32(dec(binascii.hexlify(offset_count())))
		question_text["2_%s" % num] = get_response2(q).encode("utf-16be")+pad(2)
	
	return question_text
	
	
prepare()
make_bin(country_code)