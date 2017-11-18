#!/usr/bin/python
# -*- coding: utf-8 -*-

# ===========================================================================
# EVERYBODY VOTES CHANNEL GENERATION SCRIPT
# VERSION 0.5
# AUTHORS: JOHN PANSERA, LARSEN VALLECILLO
# ***************************************************************************
# Copyright (c) 2015-2017 RiiConnect24, and it's (Lead) Developers
# ===========================================================================

import binascii
import collections
import json
import math
import mysql.connector
import os
import platform
import struct
import subprocess
import sys
import time
import io
import rsa
import random
import datetime
from config import *
from mysql.connector import errorcode

print "Everybody Votes Channel File Generator \n"
print "By John Pansera / Larsen Vallecillo / www.rc24.xyz \n"

worldwide = 0
national = 0
results = 0
national_results = 0
worldwide_results = 0
question_data = {}
country_code = 49
country_count = 0
language_code = 1
languages = {}
results = {}
num = 0
number = 0
poll_id = 1414 # Same as Nintendo's original question poll ID
worldwide_q = False
national_q = False
file_type = None
write_questions = False
write_results = False
countries = collections.OrderedDict()
countries["Japan"] = ["日本", "Japan", "Japan", "Japon", "Japón", "Giappone", "Japan"]
countries["Argentina"] = ["アルゼンチン", "Argentina", "Argentinien", "Argentine", "Argentina", "Argentina", "Argentinië"]
countries["Brazil"] = ["ブラジル", "Brazil", "Brasilien", "Brésil", "Brasil", "Brasile", "Brazilië"]
countries["Canada"] = ["カナダ", "Canada", "Kanada", "Canada", "Canadá", "Canada", "Canada"]
countries["Chile"] = ["チリ", "Chile", "Chile", "Chili", "Chile", "Cile", "Chili"]
countries["Colombia"] = ["コロンビア", "Colombia", "Kolumbien", "Colombie", "Colombia", "Colombia", "Colombia"]
countries["Costa Rica"] = ["コスタリカ", "Costa Rica", "Costa Rica", "Costa Rica", "Costa Rica", "Costa Rica", "Costa Rica"]
countries["Ecuador"] = ["エクアドル", "Ecuador", "Ecuador", "Equateur", "Ecuador", "Ecuador", "Ecuador"]
countries["Guatemala"] = ["グアテマラ", "Guatemala", "Guatemala", "Guatemala", "Guatemala", "Guatemala", "Guatemala"]
countries["Mexico"] = ["メキシコ", "Mexico", "Mexiko", "Mexique", "México", "Messico", "Mexico"]
countries["Panama"] = ["パナマ", "Panama", "Panama", "Panama", "Panamá", "Panamá", "Panama"]
countries["Peru"] = ["ペルー", "Peru", "Peru", "Pérou", "Perú", "Perù", "Peru"]
countries["United States"] = ["アメリカ", "United States", "Vereinigte Staaten", "Etats-Unis d’Amérique", "Estados Unidos de América", "Stati Uniti d'America", "Verenigde Staten"]
countries["Venezuela"] = ["ベネズエラ", "Venezuela", "Venezuela", "Venezuela", "Venezuela", "Venezuela", "Venezuela"]
countries["Australia"] = ["オーストラリア", "Australia", "Australien", "Australie", "Australia", "Australia", "Australië"]
countries["Austria"] = ["オーストリア", "Austria", "Österreich", "Autriche", "Austria", "Austria", "Oostenrijk"]
countries["Belgium"] = ["ベルギー", "Belgium", "Belgien", "Belgique", "Bélgica", "Belgio", "België"]
countries["Denmark"] = ["デンマーク", "Denmark", "Dänemark", "Danemark", "Dinamarca", "Danimarca", "Denemarken"]
countries["Finland"] = ["フィンランド", "Finland", "Finnland", "Finlande", "Finlandia", "Finlandia", "Finland"]
countries["France"] = ["フランス", "France", "Frankreich", "France", "Francia", "Francia", "Frankrijk"]
countries["Germany"] = ["ドイツ", "Germany", "Deutschland", "Allemagne", "Alemania", "Germania", "Duitsland"]
countries["Greece"] = ["ギリシャ", "Greece", "Griechenland", "Grèce", "Grecia", "Grecia", "Griekenland"]
countries["Ireland"] = ["アイルランド", "Ireland", "Irland", "Irlande", "Irlanda", "Irlanda", "Ierland"]
countries["Italy"] = ["イタリア", "Italy", "Italien", "Italie", "Italia", "Italia", "Italië"]
countries["Luxembourg"] = ["ルクセンブルク", "Luxembourg", "Luxemburg", "Luxembourg", "Luxemburgo", "Lussemburgo", "Luxemburg"]
countries["Netherlands"] = ["オランダ", "Netherlands", "Niederlande", "Pays-Bas", "Países Bajos", "Paesi Bassi", "Nederland"]
countries["New Zealand"] = ["ニュージーランド", "New Zealand", "Neuseeland", "Nouvelle-Zélande", "Nueva Zelanda", "Nuova Zelanda", "Nieuw-Zeeland"]
countries["Norway"] = ["ノルウェー", "Norway", "Norwegen", "Norvège", "Noruega", "Norvegia", "Noorwegen"]
"""We have a few users in Poland, so we'll consider supporting Poland for the EVC."""
# countries["Poland"] = ["ポーランド", "Poland", "Polen", "Pologne", "Polonia", "Polonia", "Polen"]
countries["Portugal"] = ["ポルトガル", "Portugal", "Portugal", "Portugal", "Portugal", "Portogallo", "Portugal"]
countries["Spain"] = ["スペイン", "Spain", "Spanien", "Espagne", "España", "Spagna", "Spanje"]
countries["Sweden"] = ["スウェーデン", "Sweden", "Schweden", "Suède", "Suecia", "Svezia", "Zweden"]
countries["Switzerland"] = ["スイス", "Switzerland", "Schweiz", "Suisse", "Suiza", "Svizzera", "Zwitserland"]
countries["United Kingdom"] = ["イギリス", "United Kingdom", "Großbritannien", "Royaume-Uni", "Reino Unido", "Regno Unito", "Verenigd Koninkrijk"]
country_codes = [1, 10, 16, 18, 20, 21, 22, 25, 30, 36, 40, 42, 49, 52, 65, 66, 67, 74, 76, 77, 78, 79, 82, 83, 88, 94, 95, 96, 98, 105, 107, 108, 110]
region_list = collections.OrderedDict()
region_list[49] = 52
position_test_us = [1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
categories = collections.OrderedDict()
categories[0] = 3
categories[1] = 5
categories[2] = 7
categories[3] = 9
categories[4] = 10

def time_convert(time): return int((time-946684800)/60)

def get_epoch(): return int(time.time())

def get_randint(): return random.randint(50,255)

def get_timestamp(mode):
	time = time_convert(get_epoch())
	if mode == 1: time+=5
	return time

def get_name():
	now = datetime.datetime.now()
	day = str(now.day).zfill(2)
	month = str(now.month).zfill(2)
	return month+day

def get_poll_id():
	return poll_id

def pad(amnt): return "\0"*amnt

def prepare():
	global country_count,countries,file_type,questions,poll_id,write_questions,write_results,results,position,national,worldwide
	print "Preparing ..."
	country_count = len(countries)
	mysql_connect()
	mysql_get_questions()
	print "Loaded %s Countries" % country_count
	question_count = len(question_data)
	if question_count == 1: print "Loaded %s Question" % question_count
	else: print "Loaded %s Questions" % question_count
	file_type = raw_input('Enter File Type (q/r/v): ')
	if file_type == "q": write_questions = True
	elif file_type == "r": write_results = True
	elif file_type == "v":
		if raw_input('Write Questions? (y/n): ') == "y": write_questions = True
		if raw_input('Write Results? (y/n): ') == "y": write_results = True
	else:
		print "Error: Invalid file type selected"
		exit()
	if country_code == 49: question_languages = [1,4,8]
	else: question_languages = [1]
	# National questions are written first, then worldwide
	# \n is used as line break
	if file_type == "r" or (file_type == "v" and write_results): poll_id = int(raw_input('Enter Result Poll ID: '))
	if write_questions == False:
		national = 0
		worldwide = 0
		questions = 0
	else: questions = national+worldwide
	if write_results: position = 58
	else: position = 0
	if write_results: results[get_poll_id()] = mysql_get_votes()
	mysql_close()
	make_language_table()

def mysql_connect():
	print "Connecting to MySQL ..."
	try:
		global cnx
		cnx = mysql.connector.connect(user=mysql_user, password=mysql_password,
									  	  host='127.0.0.1',
									  	  database=mysql_database)
	except mysql.connector.Error as err:
		 if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: print "Something is wrong with your user name or password"
		 elif err.errno == errorcode.ER_BAD_DB_ERROR: print "Database does not exist"
		 else: print err

def mysql_get_votes():
	cursor = cnx.cursor(dictionary=True)
	question_id = get_poll_id()
	query = ("SELECT * from EVC.votes WHERE questionID = %s" % str(question_id))
	cursor.execute(query)

	global national_results,worldwide_results

	male_voters_response_1 = [0] * 33
	female_voters_response_1 = [0] * 33
	male_voters_response_2 = [0] * 33
	female_voters_response_2 = [0] * 33

	"""77 is the largest number of regions I have found, I'll make this better later."""

	region_response_1 = [0] * 52
	region_response_2 = [0] * 52

	predict_response_1 = [0] * 33
	predict_response_2 = [0] * 33

	poll_type = raw_input("Enter poll type for %s (n/w): " % question_id)
	if poll_type is "n": national_results=1
	elif poll_type is "w": worldwide_results=1

	for row in cursor:
		if row["typeCD"] == 0:
			male_voters_response_1[country_codes.index(row["countryID"])] += int(row["ansCNT"][0])
			female_voters_response_1[country_codes.index(row["countryID"])] += int(row["ansCNT"][1])
			male_voters_response_2[country_codes.index(row["countryID"])] += int(row["ansCNT"][2])
			female_voters_response_2[country_codes.index(row["countryID"])] += int(row["ansCNT"][3])

			region_response_1[row["regionID"]] += int(row["ansCNT"][0]) + int(row["ansCNT"][1])
			region_response_2[row["regionID"]] += int(row["ansCNT"][2]) + int(row["ansCNT"][3])
		elif row["typeCD"] == 1:
			predict_response_1[country_codes.index(row["countryID"])] += int(row["ansCNT"][0]) + int(row["ansCNT"][1])
			predict_response_2[country_codes.index(row["countryID"])] += int(row["ansCNT"][2]) + int(row["ansCNT"][2])

	print "Male Voters Response 1: %s" % male_voters_response_1
	print "Female Voters Response 1: %s" % female_voters_response_1
	print "Male Voters Response 2: %s" % male_voters_response_2
	print "Female Voters Response 2: %s" % female_voters_response_2
	print "Predict Response 1: %s" % predict_response_1
	print "Predict Response 2: %s" % predict_response_2
	print "Region Response 1: %s" % region_response_1
	print "Region Response 2: %s" % region_response_2

	cursor.close()

	return [male_voters_response_1, female_voters_response_1,
			male_voters_response_2, female_voters_response_2,
			predict_response_1, predict_response_2,
			region_response_1, region_response_2]

def mysql_get_questions():
	cursor = cnx.cursor(dictionary=True)
	query = "SELECT * from EVC.questions WHERE active = 1"
	cursor.execute(query)

	for row in cursor:
		if row["type"] == "n":
			add_question(int(row["questionID"]),row["content_english"],row["choice1_english"],row["choice2_english"],0,row["category"])
			print "ID: "+str(row["questionID"])+" Question: "+row["content_english"]+" Choice 1: "+row["choice1_english"]+" Choice 2: "+row["choice2_english"]+" Type: National"
		elif row["type"] == "w":
			add_question(int(row["questionID"]),row["content_english"],row["choice1_english"],row["choice2_english"],1,row["category"])
			print "ID: "+str(row["questionID"])+" Question: "+row["content_english"]+" Choice 1: "+row["choice1_english"]+" Choice 2: "+row["choice2_english"]+" Type: Worldwide"

	cursor.close()

def mysql_close(): cnx.close()

def num():
	global number
	num1 = number
	number += 1
	return num1

def dec(data): return int(data, 16)

def question():
	if raw_input('Would you like to enter a question? (Y/N) ') is 'Y':
		add_question(raw_input('Enter Question: '),raw_input('Enter Answer 1: '),raw_input('Enter Answer 2: '),int(raw_input('Is this a national (0) or a worldwide (1) question? ')), 0)

def get_question(id): return question_data[id][0]

def get_response1(id): return question_data[id][1]

def get_response2(id): return question_data[id][2]

def get_category(id): return question_data[id][4]

def is_worldwide(id):
	i = True
	if question_data[id][3] == 0: i = False
	return i

def add_question(poll_id,q,r1,r2,f,c):
	global question_data,national,worldwide,national_q,worldwide_q
	question_data[poll_id] = [question_text_replace(q),question_text_replace(r1),question_text_replace(r2),f,c]
	if f == 0:
		national+=1
		national_q = True
	elif f == 1:
		worldwide+=1
		worldwide_q = True

def question_text_replace(text):
	text = text.decode("utf-16be").replace("...", " . . .").encode("utf-16be")
	return text

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

def sign_file(name):
	final = name+'.bin'
	print "Processing " + final + " ..."
	file = open(name, 'rb')
	copy = file.read()
	print "Calculating CRC32 ..."
	crc32 = format(binascii.crc32(copy) & 0xFFFFFFFF, '08x')
	print "Calculating Size ..."
	size = os.path.getsize(name)+12
	dest = open(final + '-1', 'w+')
	dest.write(u32(0))
	dest.write(u32(size))
	dest.write(binascii.unhexlify(crc32))
	dest.write(copy)
	os.remove(name)
	dest.close()
	file.close()
	print "Compressing ..."
	subprocess.call(["%s/lzss" % lzss_path, "-evf", final + '-1'], stdout=subprocess.PIPE)
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
	os.remove(final + '-1')

def make_bin(country_code):
	global countries,file_type
	print "Processing ..."
	voting = make_header()
	if write_questions:
		make_national_question_table(voting)
		make_worldwide_question_table(voting)
		question_text_table = make_question_text_table(voting)
	if write_results and national_results > 0:
		make_national_result_table(voting)
		make_national_result_detailed_table(voting)
		make_position_entry_table(voting)
	if write_results and worldwide_results > 0:
		make_worldwide_result_table(voting)
		make_worldwide_result_detailed_table(voting)
	if file_type == "v" or "r": country_table = make_country_name_table(voting)
	if write_questions: make_question_text(question_text_table)
	if file_type == "v" or "r": make_country_table(country_table)
	if file_type == "q": question_file = get_name()+'_q'
	elif file_type == "r": question_file = get_name()+'_r'
	else: question_file = "voting"
	print "Writing to %s.bin ..." % question_file

	with open(question_file, 'wb') as f:
		for dictionary in dictionaries:
			print("Writing to %s ..." % hex(f.tell()).rstrip("L"))
			for values in dictionary.values():
				f.write(values)
		f.write(pad(16))
		f.write('RIICONNECT24'.encode("ASCII"))
		f.flush()

	if production: sign_file(question_file)

	print "Writing Completed"

def make_header():
	header = collections.OrderedDict()
	dictionaries.append(header)

	header["timestamp"] = u32(get_timestamp(0))
	header["country_code"] = u8(country_code)
	header["publicity_flag"] = u8(0)
	if file_type == "r":
		header["question_version"] = u8(0)
		header["result_version"] = u8(1)
	else:
		header["question_version"] = u8(1)
		header["result_version"] = u8(0)
	header["nqen_entry_number"] = u8(national)
	header["nqen_header_offset"] = u32(0)
	header["worldwide_question_num"] = u8(worldwide)
	header["worldwide_question_offset"] = u32(0)
	header["question_entry_number"] = u8(questions)
	header["question_table_offset"] = u32(0)
	header["national_result_entry"] = u8(national_results)
	header["national_result_offset"] = u32(0)
	header["national_result_detailed"] = u16(national_results*52)
	header["national_result_detailed_offset"] = u32(0)
	header["position_entry_number"] = u16(position)
	header["position_header_offset"] = u32(0)
	header["worldwide_result_entry_num"] = u8(worldwide_results)
	header["worldwide_result_table_offset"] = u32(0)
	header["worldwide_result_detailed_num"] = u16(worldwide_results*33)
	header["worldwide_result_detailed_offset"] = u32(0)
	header["country_name_entry_num"] = u16(country_count * 7)
	header["country_name_header_offset"] = u32(0)

	return header

def make_national_question_table(header):
	global national
	national_question_table = collections.OrderedDict()
	dictionaries.append(national_question_table)

	question_table_count = 0
	if national_q: header["nqen_header_offset"] = offset_count()

	for q in question_data.keys():
		if not is_worldwide(q):
			national_question_table["poll_id_%s" % num()] = u32(q)
			national_question_table["poll_category_1_%s" % num()] = u8(get_category(q))
			national_question_table["poll_category_2_%s" % num()] = u8(categories[get_category(q)])
			national_question_table["opening_timestamp_%s" % num()] = u32(get_timestamp(0))
			national_question_table["closing_timestamp_%s" % num()] = u32(get_timestamp(1))
			national_question_table["question_table_count_%s" % num()] = u8(1)
			national_question_table["question_table_start_%s" % num()] = u32(question_table_count)
			question_table_count+=1

	return national_question_table

def make_worldwide_question_table(header):
	global worldwide
	worldwide_question_table = collections.OrderedDict()
	dictionaries.append(worldwide_question_table)

	question_table_count = 0
	if worldwide_q: header["worldwide_question_offset"] = offset_count()

	for q in question_data.keys():
		if is_worldwide(q):
			worldwide_question_table["poll_id_%s" % num()] = u32(q)
			worldwide_question_table["poll_category_1_%s" % num()] = u8(get_category(q))
			worldwide_question_table["poll_category_2_%s" % num()] = u8(categories[get_category(q)])
			worldwide_question_table["opening_timestamp_%s" % num()] = u32(get_timestamp(0))
			worldwide_question_table["closing_timestamp_%s" % num()] = u32(get_timestamp(1))
			worldwide_question_table["question_table_count_%s" % num()] = u8(1)
			worldwide_question_table["question_table_start_%s" % num()] = u32(question_table_count)
			question_table_count+=1

	return worldwide_question_table

def make_question_text_table(header):
	global questions
	question_text_table = collections.OrderedDict()
	dictionaries.append(question_text_table)

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

	national_result_detailed_count = 0
	national_result_detailed_tables = 52
	header["national_result_offset"] = offset_count()

	for i in results:
		results_country_code = country_codes.index(country_code)

		total_resp1 = 0
		total_resp2 = 0
		total_resp1+=results[i][0][results_country_code]+results[i][1][results_country_code]
		total_resp2+=results[i][2][results_country_code]+results[i][3][results_country_code]

		table["poll_id_%s" % num()] = u32(i)
		table["male_voters_response_1_num_%s" % num()] = u32(results[i][0][results_country_code])
		table["male_voters_response_2_num_%s" % num()] = u32(results[i][2][results_country_code])
		table["female_voters_response_1_num_%s" % num()] = u32(results[i][1][results_country_code])
		table["female_voters_response_2_num_%s" % num()] = u32(results[i][3][results_country_code])
		if total_resp1 > total_resp2: # response 1 won
			table["accurate_prediction_voters_num_%s" % num()] = u32(results[i][4][results_country_code])
			table["inaccurate_prediction_voters_num_%s" % num()] = u32(results[i][5][results_country_code])
		else: # response 2 won - or tie
			table["accurate_prediction_voters_num_%s" % num()] = u32(results[i][5][results_country_code])
			table["inaccurate_prediction_voters_num_%s" % num()] = u32(results[i][4][results_country_code])
		table["unknown_%s" % num()] = u16(1)
		table["national_result_detailed_number_%s" % num()] = u8(national_result_detailed_tables)
		table["starting_national_result_detailed_table_number_%s" % num()] = u32(national_result_detailed_count)
		national_result_detailed_count+=national_result_detailed_tables

	return table

def make_national_result_detailed_table(header):
	table = collections.OrderedDict()
	dictionaries.append(table)

	header["national_result_detailed_offset"] = offset_count()

	for i in results:
		for j in range(region_list[country_code]):
			table["voters_response_1_num_%s" % num()] = u32(results[i][6][j])
			table["voters_response_2_num_%s" % num()] = u32(results[i][7][j])
			table["position_entry_table_count_%s" % num()] = u8(position_test_us[j])
			table["starting_position_entry_table_%s" % num()] = u32(sum(position_test_us[:j]))

	return table

def make_position_entry_table(header):
	table = collections.OrderedDict()
	dictionaries.append(table)

	header["position_header_offset"] = offset_count()

	position_table_data = 'D25E78D252E748E1AA87917D3C7819645A64E04EDC5FC8A0BE872EE628DF18D98C5A3C46A064AA5F7869B46C9191E249DC64EB37A53FAF5087419169A08C5037D2737337735AE440DC55557D2D5AD746E254B95D7D7D2341CD55E84CC87D714BAA7878914164CD69DC3F272F9B46C3645550F0BE'

	table["data_%s" % num()] = binascii.unhexlify(position_table_data)

	#table["response_1_%s" % num()] = u8(0)
	#table["response_2_%s" % num()] = u8(0)

def make_worldwide_result_table(header):
	table = collections.OrderedDict()
	dictionaries.append(table)

	worldwide_detailed_table_count = 0
	header["worldwide_result_table_offset"] = offset_count()

	for i in results:
		male_resp1=sum(results[i][0])
		female_resp1=sum(results[i][1])
		male_resp2=sum(results[i][2])
		female_resp2=sum(results[i][3])
		resp1=male_resp1+female_resp1
		resp2=male_resp2+female_resp2
		predict1=sum(results[i][4])
		predict2=sum(results[i][5])

		table["poll_id_%s" % num()] = u32(i)
		table["male_voters_response_1_num_%s" % num()] = u32(male_resp1)
		table["male_voters_response_2_num_%s" % num()] = u32(female_resp1)
		table["female_voters_response_1_num_%s" % num()] = u32(male_resp2)
		table["female_voters_response_2_num_%s" % num()] = u32(female_resp2)
		if resp1 > resp2: # response 1 won
			table["accurate_prediction_voters_num_%s" % num()] = u32(predict1)
			table["inaccurate_prediction_voters_num_%s" % num()] = u32(predict2)
		else: # response 2 won - or tie
			table["accurate_prediction_voters_num_%s" % num()] = u32(predict2)
			table["inaccurate_prediction_voters_num_%s" % num()] = u32(predict1)
		table["total_worldwide_detailed_tables_%s" % num()] = u8(33)
		table["starting_worldwide_detailed_table_number_%s" % num()] = u32(worldwide_detailed_table_count)
		worldwide_detailed_table_count+=33

	return table

def make_worldwide_result_detailed_table(header):
	table = collections.OrderedDict()
	dictionaries.append(table)

	country_table_count = 0
	header["worldwide_result_detailed_offset"] = offset_count()

	for i in results:
		for j in range(len(countries)): # 33
			table["unknown_%s" % num()] = u32(0)
			table["male_voters_response_1_num_%s" % num()] = u32(results[i][0][j])
			table["male_voters_response_2_num_%s" % num()] = u32(results[i][2][j])
			table["female_voters_response_1_num_%s" % num()] = u32(results[i][1][j])
			table["female_voters_response_2_num_%s" % num()] = u32(results[i][3][j])
			table["country_table_count_%s" % num()] = u16(7)
			table["starting_country_table_number_%s" % num()] = u32(country_table_count)
			country_table_count+=7

	return table

def make_country_name_table(header):
	global countries
	country_name_table = collections.OrderedDict()
	dictionaries.append(country_name_table)

	header["country_name_header_offset"] = offset_count()

	for k in countries.keys():
		num = countries.keys().index(k)
		for i in range(len(languages)):
			country_name_table["language_code_%s_%s" % (num,i)] = u8(i)
			country_name_table["text_offset_%s_%s" % (num,i)] = u32(0)

	return country_name_table

def make_language_table(): # Default channel language table
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
		for i in range(len(languages)):
			country_name_table["text_offset_%s_%s" % (num,i)] = offset_count()
			country_table[j] = countries[k][i].decode('utf-8').encode("utf-16be")+pad(2)
			j+=1

	return country_table

def make_question_text(question_text_table):
	global question_data
	question_text = collections.OrderedDict()
	dictionaries.append(question_text)

	for q in question_data.keys():
		num = question_data.keys().index(q)
		question_text_table["question_offset_%s" % num] = offset_count()
		question_text["0_%s" % num] = get_question(q).encode("utf-16be")+pad(2)
		question_text_table["response_1_offset_%s" % num] = offset_count()
		question_text["1_%s" % num] = get_response1(q).encode("utf-16be")+pad(2)
		question_text_table["response_2_offset_%s" % num] = offset_count()
		question_text["2_%s" % num] = get_response2(q).encode("utf-16be")+pad(2)

	return question_text


prepare()
make_bin(country_code)
