#!/usr/bin/python
# -*- coding: utf-8 -*-

# ===========================================================================
# EVERYBODY VOTES CHANNEL GENERATION SCRIPT
# VERSION 1.0
# AUTHORS: JOHN PANSERA, LARSEN VALLECILLO
# ***************************************************************************
# Copyright (c) 2015-2017 RiiConnect24, and it's (Lead) Developers
# ===========================================================================

import binascii
import collections
import datetime
import io
import json
import logging
import mysql.connector
import os
import requests
import rsa
import struct
import subprocess
import sys
import textwrap
import time
from config import *
from mysql.connector import errorcode
from raven import Client
from raven.handlers.logging import SentryHandler
from raven.conf import setup_logging
from voteslists import *

print "Everybody Votes Channel File Generator \n"
print "By John Pansera / Larsen Vallecillo / www.rc24.xyz \n"

worldwide = 0
national = 0
national_results = 0
worldwide_results = 0
question_data = collections.OrderedDict()
results = collections.OrderedDict()
country_code = 49
country_count = 0
language_code = 1
languages = {}
num = 0
number = 0
nw = ""
worldwide_q = False
national_q = False
file_type = None
write_questions = False
write_results = False

def time_convert(time): return int((time - 946684800) / 60)

def get_epoch(): return int(time.time())

def get_timestamp(mode, type, date):
    if mode == 0:
        timestamp = time_convert(get_epoch())
    elif mode == 1 or mode == 2:
        timestamp = time_convert(time.mktime(date.timetuple()))
        if mode == 2:
            if production:
                if type == "n": timestamp+=10080
                elif type == "w": timestamp+=21600
            else: timestamp+=5
    return timestamp

def days_ago():
    if national_results > 0: return 7
    elif worldwide_results > 0: return 14
    else: return 0

def get_name():
    now = datetime.datetime.now() - datetime.timedelta(days=days_ago())
    day = str(now.day).zfill(2)
    month = str(now.month).zfill(2)
    return month+day

def get_year():
    now = datetime.datetime.now() - datetime.timedelta(days=days_ago())
    year = str(now.year)
    return year

def get_poll_id(): return poll_id

def pad(amnt): return "\0"*amnt

def prepare():
    global country_count,countries,file_type,questions,poll_id,write_questions,write_results,results,position,national,worldwide
    print "Preparing ..."
    if production:
        client = Client(sentry_url)
        handler = SentryHandler(client)
        setup_logging(handler)
        logger = logging.getLogger(__name__)
    mysql_connect()
    if len(sys.argv) == 1: manual_run()
    elif len(sys.argv) >= 2:
        file_type = sys.argv[1]
        if file_type == "q": automatic_questions()
        elif file_type == "r": automatic_results()
        elif file_type == "v": automatic_votes()
    mysql_close()
    make_language_table()

"""Manually enter in what file type you want if no arguments are specified."""

def manual_run():
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
    if file_type == "r" or (file_type == "v" and write_results): poll_id = int(raw_input('Enter Result Poll ID: '))

"""Automatically run the scripts. This will be what the crontab uses."""

def automatic_questions():
    global write_questions,write_results,questions,nw
    write_questions = True
    nw = sys.argv[2]
    mysql_get_questions(1, nw)
    questions = 1

def automatic_results():
    global write_results,results,national,worldwide,questions,national_results,worldwide_results,nw
    write_results = True
    nw = sys.argv[2]
    if nw == "n": days = 7
    elif nw == "w": days = 15
    results[get_poll_id()] = mysql_get_votes(days, nw, 1)
    try: del results[None]
    except KeyError: pass
    national = 0
    worldwide = 0
    questions = 0

def automatic_votes():
    global write_questions,write_results,questions,results,national,worldwide,questions
    write_questions = True
    write_results = True
    mysql_get_questions(1, "w")
    mysql_get_questions(3, "n")
    questions = national+worldwide
    question_count = len(question_data)
    if question_count == 1: print "Loaded %s Question" % question_count
    else: print "Loaded %s Questions" % question_count
    for v in range(1, 7): results[get_poll_id()] = mysql_get_votes(7, "n", v)
    results[get_poll_id()] = mysql_get_votes(15, "w", 1)
    try: del results[None]
    except KeyError: pass

def mysql_connect():
    print "Connecting to MySQL ..."
    try:
        global cnx
        cnx = mysql.connector.connect(user=mysql_user, password=mysql_password,
                                      host='127.0.0.1',
                                      database=mysql_database,
                                      charset='utf8',
                                      use_unicode=True)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: print "Something is wrong with your user name or password"
        elif err.errno == errorcode.ER_BAD_DB_ERROR: print "Database does not exist"
        else: print err

def mysql_get_votes(days, type, index):
    cursor = cnx.cursor(dictionary=True, buffered=True)
    query = "SELECT questionID from EVC.questions WHERE DATE(date) <= CURDATE() - %s AND type = '%s' ORDER BY questionID DESC" % (days, type)
    cursor.execute(query)
    global poll_id, poll_type

    i = 0

    while i < index:
        row = cursor.fetchone()
        if row is None:
            poll_id = None
            return None
        i += 1

    poll_id = row["questionID"]
    query = "SELECT * from EVC.votes WHERE questionID = %s" % poll_id
    cursor.execute(query)

    global national_results,worldwide_results

    if type == "n": national_results+=1
    elif type == "w": worldwide_results+=1

    """Initialize blank lists to store votes in."""

    male_voters_response_1 = [0] * 33
    female_voters_response_1 = [0] * 33
    male_voters_response_2 = [0] * 33
    female_voters_response_2 = [0] * 33

    region_response_1 = [0] * 33
    region_response_2 = [0] * 33

    for k,v in region_number.items():
        region_response_1[country_codes.index(k)] = [0] * v
        region_response_2[country_codes.index(k)] = [0] * v

    predict_response_1 = [0] * 33
    predict_response_2 = [0] * 33

    """Grab the votes from the database."""

    for row in cursor:
        country_index = country_codes.index(row["countryID"])
        anscnt = str(row["ansCNT"]).zfill(4)
        region_id = row["regionID"] - 2

        if row["typeCD"] == 0:
            male_voters_response_1[country_index] += int(anscnt[0])
            female_voters_response_1[country_index] += int(anscnt[1])
            male_voters_response_2[country_index] += int(anscnt[2])
            female_voters_response_2[country_index] += int(anscnt[3])

            region_response_1[country_index][region_id] += int(anscnt[0]) + int(anscnt[1])
            region_response_2[country_index][region_id] += int(anscnt[2]) + int(anscnt[3])
        elif row["typeCD"] == 1:
            predict_response_1[country_index] += int(anscnt[0]) + int(anscnt[1])
            predict_response_2[country_index] += int(anscnt[2]) + int(anscnt[3])

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

def mysql_get_questions(count, type):
    cursor = cnx.cursor(dictionary=True, buffered=True)
    query = "SELECT * from EVC.questions WHERE date <= CURDATE() AND type = '%s' ORDER BY questionID DESC" % type

    cursor.execute(query)

    i = 0

    while i < count:
        row = cursor.fetchone()
        if row is None: break
        add_question(row)
        i += 1

    cursor.close()

def mysql_close(): cnx.close()

def num():
    global number
    num1 = number
    number += 1
    return num1

def dec(data): return int(data, 16)

def get_question(id, language_code): return question_data[id][0][language_code]

def get_response1(id, language_code): return question_data[id][1][language_code]

def get_response2(id, language_code): return question_data[id][2][language_code]

def get_category(id): return question_data[id][3]

def get_date(id): return question_data[id][5]

def is_worldwide(id):
    i = True
    if question_data[id][4] == "n": i = False
    return i

def add_question(row):
    global question_data,national,worldwide,national_q,worldwide_q
    for r in row:
        if "content" in r or "choice" in r:
            if row[r] is not None: row[r] = question_text_replace(row[r])

    question_data[row["questionID"]] = [[row["content_japanese"], row["content_english"], row["content_german"],
                                         row["content_french"], row["content_spanish"], row["content_italian"],
                                         row["content_dutch"], row["content_portuguese"], row["content_french_canada"]],
                                        [row["choice1_japanese"], row["choice1_english"], row["choice1_german"],
                                         row["choice1_french"], row["choice1_spanish"], row["choice1_italian"],
                                         row["choice1_dutch"], row["choice1_portuguese"], row["choice1_french_canada"]],
                                        [row["choice2_japanese"], row["choice2_english"], row["choice2_german"],
                                         row["choice2_french"], row["choice2_spanish"], row["choice2_italian"],
                                         row["choice2_dutch"], row["choice2_portuguese"], row["choice2_french_canada"]],
                                        row["category"], row["type"], row["date"]]

    if row["type"] == "n":
        national+=1
        national_q = True
    elif row["type"] == "w":
        worldwide+=1
        worldwide_q = True

"""This will fix the "..." on the questions, and wrap the text correctly so words aren't cut off."""

def question_text_replace(text):
    text = text.replace(u"\u2026", " . . .").replace("...", " . . .")
    text = "\\n".join(textwrap.wrap(text, 50))
    return text

def webhook():
    if nw == "n": webhook_type = "national"
    elif nw == "w": webhook_type = "worldwide"
    for q in question_data.keys():
        webhook_text = "New %s Everybody Votes Channel question is out!\n\n%s (%s / %s)" % (webhook_type, get_question(q, 1), get_response1(q, 1), get_response2(q, 1))
        if production: data = {"username": "Votes Bot", "content": "New %s Everybody Votes Channel question is out!" % type, "avatar_url": "http://rc24.xyz/images/logo-small.png", "attachments": [{"fallback": "Everybody Votes Channel Data Update", "color": "#68C7D0", "author_name": "RiiConnect24 Everybody Votes Channel Script", "author_icon": "https://rc24.xyz/images/webhooks/votes/profile.png", "text": webhook_text, "title": "Update!", "fields": [{"title": "Script", "value": "Everybody Votes Channel", "short": "false"}], "thumb_url": "https://rc24.xyz/images/webhooks/votes/vote_%s.png" % webhook_type, "footer": "RiiConnect24 Script", "footer_icon": "https://rc24.xyz/images/logo-small.png", "ts": int(time.mktime(datetime.datetime.utcnow().timetuple()))}]}
        for url in webhook_urls: post_webhook = requests.post(url, json=data, allow_redirects=True)

dictionaries = []

def u8(data): return struct.pack(">B", data)
def u16(data): return struct.pack(">H", data)
def u32(data): return struct.pack(">I", data)
def s8(data): return struct.pack(">b", data)
def s16(data): return struct.pack(">h", data)
def s32(data): return struct.pack(">i", data)

def offset_count(): return u32(12 + sum(len(values) for dictionary in dictionaries for values in dictionary.values() if values))

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
    subprocess.call(["%s/lzss" % lzss_path, "-evf", final + '-1'], stdout=subprocess.PIPE) # Compress the file with the lzss program.
    file = open(final + '-1', 'rb')
    new = file.read()
    dest = open(final, "w+")
    key = open(key_path, 'rb')
    print "RSA Signing ..."
    private_key = rsa.PrivateKey.load_pkcs1(key.read(), "PEM") # Loads the RSA key.
    signature = rsa.sign(new, private_key, "SHA-1") # Makes a SHA1 with ASN1 padding. Beautiful.
    dest.write(binascii.unhexlify(str(0).zfill(128))) # Padding. This is where data for an encrypted WC24 file would go (such as the header and IV), but this is not encrypted so it's blank.
    dest.write(signature)
    dest.write(new)
    dest.close()
    file.close()
    key.close()
    if production:
        if file_type == "q" or file_type == "r":
            folder = str(country_code).zfill(3)
            if nw == "w": folder = "world"
            subprocess.call(["mkdir", "-p", "%s/%s/%s" % (file_path, folder, get_year())]) # If folder for the year does not exist, make it.
            path = "%s/%s/%s/%s" % (file_path, folder, get_year(), final)
        elif file_type == "v": path = "%s/%s/%s" % (file_path, str(country_code).zfill(3), final)
    subprocess.call(["mv", final, path])
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
    if file_type == "v" or file_type == "r" and national_results == 0: country_table = make_country_name_table(voting)
    if write_questions: make_question_text(question_text_table)
    if file_type == "v" or file_type == "r" and national_results == 0: make_country_table(country_table)
    if file_type == "q": question_file = get_name()+'_q'
    elif file_type == "r": question_file = get_name()+'_r'
    else: question_file = "voting"
    print "Writing to %s.bin ..." % question_file

    with open(question_file, 'wb') as f:
        for dictionary in dictionaries:
            # print("Writing to %s ..." % hex(f.tell()).rstrip("L"))
            for values in dictionary.values():
                f.write(values)
        f.write(pad(16))
        f.write('RIICONNECT24'.encode("ASCII"))
        f.flush()

    if production:
        sign_file(question_file)

    print "Writing Completed"

    clean_up()

def clean_up():
    for dictionary in dictionaries: dictionary.clear()

def make_header():
    header = collections.OrderedDict()
    dictionaries.append(header)

    header["timestamp"] = u32(get_timestamp(0, None, None))
    header["country_code"] = u8(country_code)
    header["publicity_flag"] = u8(0)
    if file_type == "r":
        header["question_version"] = u8(0)
        header["result_version"] = u8(1)
    else:
        header["question_version"] = u8(1)
        header["result_version"] = u8(0)
    header["national_question_number"] = u8(national)
    header["national_question_offset"] = u32(0)
    header["worldwide_question_number"] = u8(worldwide)
    header["worldwide_question_offset"] = u32(0)
    header["question_number"] = u8(questions * len(country_language[country_code]))
    header["question_offset"] = u32(0)
    header["national_result_entry"] = u8(national_results)
    header["national_result_offset"] = u32(0)
    header["national_result_detailed_number"] = u16(national_results*region_number[country_code])
    header["national_result_detailed_offset"] = u32(0)
    if file_type == "q" or national_results == 0: header["position_number"] = u16(0)
    elif country_code in position_table.keys(): header["position_number"] = u16(len(position_table[country_code]))
    else: header["position_number"] = u16(0)
    header["position_offset"] = u32(0)
    header["worldwide_result_number"] = u8(worldwide_results)
    header["worldwide_result_offset"] = u32(0)
    header["worldwide_result_detailed_number"] = u16(0)
    header["worldwide_result_detailed_offset"] = u32(0)
    if file_type == "r" and nw == "w": header["country_name_number"] = u16(len(countries) * 7)
    elif file_type == "q" or file_type == "r": header["country_name_number"] = u16(0)
    else: header["country_name_number"] = u16(len(countries) * 7)
    header["country_name_offset"] = u32(0)

    return header

def make_national_question_table(header):
    global national
    national_question_table = collections.OrderedDict()
    dictionaries.append(national_question_table)

    question_table_count = 0
    if national_q: header["national_question_offset"] = offset_count()
    if worldwide_q:
        if file_type == "v": question_table_count += len(country_language[country_code])
        elif file_type == "q": question_table_count = 8 # Worldwide and national polls should not be in the same question file, but this is just in case for some reason it happens.

    for q in question_data.keys():
        if not is_worldwide(q):
            national_question_table["poll_id_%s" % num()] = u32(q)
            national_question_table["poll_category_1_%s" % num()] = u8(get_category(q))
            national_question_table["poll_category_2_%s" % num()] = u8(categories[get_category(q)])
            national_question_table["opening_timestamp_%s" % num()] = u32(get_timestamp(1, "n", get_date(q)))
            national_question_table["closing_timestamp_%s" % num()] = u32(get_timestamp(2, "n", get_date(q)))
            national_question_table["question_table_count_%s" % num()] = u8(len(country_language[country_code]))
            national_question_table["question_table_start_%s" % num()] = u32(question_table_count)
            question_table_count+=len(country_language[country_code])

    return national_question_table

def make_worldwide_question_table(header):
    global worldwide
    worldwide_question_table = collections.OrderedDict()
    dictionaries.append(worldwide_question_table)

    question_table_start = 0
    if worldwide_q: header["worldwide_question_offset"] = offset_count()

    if file_type == "v": question_table_count = len(country_language[country_code])
    elif file_type == "q": question_table_count = 9

    for q in question_data.keys():
        if is_worldwide(q):
            worldwide_question_table["poll_id_%s" % num()] = u32(q)
            worldwide_question_table["poll_category_1_%s" % num()] = u8(get_category(q))
            worldwide_question_table["poll_category_2_%s" % num()] = u8(categories[get_category(q)])
            worldwide_question_table["opening_timestamp_%s" % num()] = u32(get_timestamp(1, "w", get_date(q)))
            worldwide_question_table["closing_timestamp_%s" % num()] = u32(get_timestamp(2, "w", get_date(q)))
            worldwide_question_table["question_table_count_%s" % num()] = u8(question_table_count)
            worldwide_question_table["question_table_start_%s" % num()] = u32(question_table_start)
            question_table_count+=1

    return worldwide_question_table

def make_question_text_table(header):
    global questions
    question_text_table = collections.OrderedDict()
    dictionaries.append(question_text_table)

    header["question_offset"] = offset_count()

    for q in question_data.keys():
        if not is_worldwide(q): list = country_language[country_code]
        elif is_worldwide(q):
            if file_type == "v": list = country_language[country_code]
            elif file_type == "q": list = range(1, 10)
        for language_code in list:
            if get_question(q, language_code) is not None:
                num = question_data.keys().index(q)
                question_text_table["language_code_%s_%s" % (num, language_code)] = u8(language_code)
                question_text_table["question_offset_%s_%s" % (num, language_code)] = u32(0)
                question_text_table["response_1_offset_%s_%s" % (num, language_code)] = u32(0)
                question_text_table["response_2_offset_%s_%s" % (num, language_code)] = u32(0)

    return question_text_table

def make_national_result_table(header):
    table = collections.OrderedDict()
    dictionaries.append(table)

    national_result_detailed_number_count = 0
    national_result_detailed_number_tables = region_number[country_code]
    header["national_result_offset"] = offset_count()

    for i in results:
        country_index = country_codes.index(country_code)

        table["poll_id_%s" % num()] = u32(i)
        table["male_voters_response_1_num_%s" % num()] = u32(results[i][0][country_index])
        table["male_voters_response_2_num_%s" % num()] = u32(results[i][2][country_index])
        table["female_voters_response_1_num_%s" % num()] = u32(results[i][1][country_index])
        table["female_voters_response_2_num_%s" % num()] = u32(results[i][3][country_index])
        table["predictors_response_1_num_%s" % num()] = u32(results[i][4][country_index])
        table["predictors_response_2_num_%s" % num()] = u32(results[i][5][country_index])
        table["show_voter_number_flag_%s" % num()] = u8(1)
        table["detailed_results_flag_%s" % num()] = u8(1)
        table["national_result_detailed_number_number_%s" % num()] = u8(national_result_detailed_number_tables)
        table["starting_national_result_detailed_number_table_number_%s" % num()] = u32(national_result_detailed_number_count)
        national_result_detailed_number_count+=national_result_detailed_number_tables

    return table

def make_national_result_detailed_table(header):
    table = collections.OrderedDict()
    dictionaries.append(table)

    header["national_result_detailed_offset"] = offset_count()

    for i in results:
        for j in range(region_number[country_code]):
            country_index = country_codes.index(country_code)
            table["voters_response_1_num_%s" % num()] = u32(results[i][6][country_index][j])
            table["voters_response_2_num_%s" % num()] = u32(results[i][7][country_index][j])
            if results[i][6][country_index][j] == 0 and results[i][7][country_index][j] == 0: table["position_entry_table_count_%s" % num()] = u8(0)
            elif country_code in position_table.keys(): table["position_entry_table_count_%s" % num()] = u8(position_table[country_code][j])
            else: table["position_entry_table_count_%s" % num()] = u8(0)
            if country_code in position_table.keys(): table["starting_position_entry_table_%s" % num()] = u32(sum(position_table[country_code][:j]))
            else: table["starting_position_entry_table_%s" % num()] = u32(0)

    return table

def make_position_entry_table(header):
    table = collections.OrderedDict()
    dictionaries.append(table)

    if country_code in position_table.keys():
        header["position_offset"] = offset_count()
        table["data_%s" % num()] = binascii.unhexlify(position_data[country_code])

def make_worldwide_result_table(header):
    table = collections.OrderedDict()
    dictionaries.append(table)

    worldwide_detailed_table_count = 0
    header["worldwide_result_offset"] = offset_count()

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

    worldwide_region_number = 0

    for i in results:
        for j in range(len(countries)): # 33
            total = 0
            for voters in range(0, 4):
                total += results[i][voters][j]
            if total > 0:
                table["unknown_%s" % num()] = u32(0)
                table["male_voters_response_1_num_%s" % num()] = u32(results[i][0][j])
                table["male_voters_response_2_num_%s" % num()] = u32(results[i][2][j])
                table["female_voters_response_1_num_%s" % num()] = u32(results[i][1][j])
                table["female_voters_response_2_num_%s" % num()] = u32(results[i][3][j])
                table["country_table_count_%s" % num()] = u16(7)
                table["starting_country_table_number_%s" % num()] = u32(country_table_count)
                worldwide_region_number += 1
            country_table_count+=7

    header["worldwide_result_detailed_number"] = u16(worldwide_region_number)

    return table

def make_country_name_table(header):
    global countries
    country_name_table = collections.OrderedDict()
    dictionaries.append(country_name_table)

    header["country_name_offset"] = offset_count()

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
        for language_code in country_language[country_code]:
            if get_question(q, language_code) is not None:
                num = question_data.keys().index(q)
                question_text_table["question_offset_%s_%s" % (num, language_code)] = offset_count()
                question_text["question_%s_%s" % (num, language_code)] = get_question(q, language_code).encode("utf-16be")+pad(2)
                question_text_table["response_1_offset_%s_%s" % (num, language_code)] = offset_count()
                question_text["response_1_%s_%s" % (num, language_code)] = get_response1(q, language_code).encode("utf-16be")+pad(2)
                question_text_table["response_2_offset_%s_%s" % (num, language_code)] = offset_count()
                question_text["response_2_%s_%s" % (num, language_code)] = get_response2(q, language_code).encode("utf-16be")+pad(2)

    return question_text


prepare()
if nw != "w": for country_code in country_codes[1:]: make_bin(country_code)
else: make_bin(country_code)
if file_type == "q": webhook()

print "Completed Successfully"
