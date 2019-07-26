#!/usr/bin/python
# -*- coding: utf-8 -*-

# ===========================================================================
# FORECAST CHANNEL GENERATION SCRIPT
# VERSION 5.0
# AUTHORS: JOHN PANSERA, LARSEN VALLECILLO
# ***************************************************************************
# Copyright (c) 2015-2019 RiiConnect24, and its (Lead) Developers
# ===========================================================================

import queue
import binascii
import collections
import io
import json
import os
import pickle
import socket
import subprocess
import sys
import threading
import time
import xml.etree.cElementTree as ElementTree
from datetime import datetime, timedelta

import requests
import rsa
from datadog import statsd

from Channels.Forecast_Channel import forecastlists
from utils import setup_log, log, u8, u16, u32, s8, s16

VERSION = 5.0
GLOBE_CONSTANT = (360 / 65536)
apirequests = 0  # API Request Counter
seek_offset = 0  # Seek Offset Location
seek_base = 0  # Base Offset Calculation Location
citycount = 0  # City Progress Counter
cities = 0  # City Counter
elapsed_time = 0  # Elapsed Time
retrycount = 0  # Retry Counter
cached = 0  # Count Cached Cities
bw_usage = 0  # Bandwidth Usage Counter
lists = 0  # Lists Counter
errors = 0  # Errors
bandwidth = 0.0  # Bandwidth
file = None # Forecast file which is currently open

uvindex = {}
wind = {}
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


def to_celsius(temp):
    return int(round((float(temp) - 32) * 5 / 9))


def to_fahrenheit(temp, sub=True):
    return int(round(float(temp) * 9 / 5)) + (32 if sub is True else 0)


def kmh_mph(wind):
    return int(round(float(wind) * 0.621371))


def mph_kmh(wind):
    return int(round(float(wind) * 1.60934))


def time_convert(time):
    if mode == 1:
        return int((time - 946684800) / 60)
    elif mode == 2:
        return int((time - 789563880) / 60)


def get_epoch():
    return int(time.time())


def get_city(forecast_list, key):
    return forecast_list[key][0][1]


def get_region(forecast_list, key):
    return forecast_list[key][1][1]


def get_country(forecast_list, key):
    return forecast_list[key][2][1]


def get_all(forecast_list, key):
    return ", ".join(list(filter(None, [get_city(forecast_list, key), get_region(forecast_list, key), get_country(forecast_list, key)])))


def pad(amnt):
    return ("\0" * amnt).encode()


def get_lat(forecast_list, key):
    return forecast_list[key][3][:4]

def get_lng(forecast_list, key):
    return forecast_list[key][3][:8][4:]


def isJapan(forecast_list,key):
    return forecast_list[key][2][1] == "Japan"

def matches_country_code(forecast_list, key):
    v = forecast_list[key]
    if v[2][1] in forecastlists.bincountries:
        return hex(int(str(forecastlists.bincountries[v[2][1]])))[2:].zfill(2) == hex(country_code)[2:].zfill(2)
    return False


def check_coords(forecast_list, key, lat, lng):
    global errors
    """ Verify Location Coordinates """
    if config["check_coordinates"]:
        if abs(lat-coord_decode(binascii.hexlify(globe[key]['lat']))) >= 1 or abs(lng-coord_decode(binascii.hexlify(globe[key]['lng']))) >= 1:
            log("Coordinate Inaccuracy Detected: %s" % key, "WARNING")
            errors+=1


def get_bins(country_code):
    if country_code == 1:
        bins = [0]
    elif 8 <= country_code <= 52:
        bins = [1, 3, 4]
    elif 64 <= country_code <= 110:
        bins = [1, 2, 3, 4, 5, 6]
    else:
        log("Unknown country code %s - generating English only" % country_code, "WARNING")
        bins = [1]
    return bins


def get_region_flag(country_code):
    if country_code == 1:
        return 0
    elif country_code in [8,9,12,14,17,19,37,43,48,49,51]:
        return 1
    else:
        return 2


def coord_decode(value):
    value = int(value, 16)
    if value >= 0x8000:
        value -= 0x10000
    return value * GLOBE_CONSTANT

def validHour(hour):
    return True if -1 < hour < 24 else False

def mode_calc(forecast_list):
    if not forecast_list: return
    temp = {}
    for i in forecast_list:
        if i not in temp: temp[i] = 1
        else: temp[i] += 1

    largestValue = 0
    largestKey = None
    duplicate = False
    for k,v in temp.items():
        if v > largestValue:
            largestValue = v
            largestKey = k
            duplicate = False
        elif v == largestValue: duplicate = True

    if not duplicate: return largestKey


def populate_international(forecast_list):
    for k, v in forecastlists.weathercities_international.items():
            if k not in forecast_list:
                forecast_list[k] = v
            elif v[2][1] is not forecast_list[k][2][1]:
                forecast_list[k + " 2"] = v


def size(data):
    total = 2
    for k, v in data.items():
        total += len(k + v) + 4
    return total


def get_bandwidth_usage(r):
    req = len(r.request.method + r.request.path_url) + size(r.request.headers) + 12
    resp = len(r.reason) + size(r.headers) + int(r.headers['Content-Length']) + 15
    return req + resp


def worker():
    while threads_run:
        try:
            item = q.get_nowait()
            get_data(item[0], item[1])
            q.task_done()
        except queue.Empty:
            pass
        except Exception as e:
            log("A thread exception has occurred: %s" % e, "WARNING")
            continue


def spawn_threads():
    global threads
    for i in range(concurrent):
            t = threading.Thread(target=worker)
            t.daemon = True
            threads.append(t)
            t.start()

def close_threads():
    global threads_run, ui_run
    threads_run = False
    for t in threads:
        t.join(60)
        if t.isAlive():
            log("Stalled thread detected", "CRITICAL")
            exit()

    ui_run = False
    ui_thread.join()


def refresh(type):
    # Uses ANSI escape codes
    if type == 0:
        print("\033[2J")  # Erase display command
    elif type == 1:
        os.system('cls')  # Clear screen
    else:
        print("\033[F\033[K" * 20)  # Clear each line individually


def ui():
    prog = """-\|/"""  # These are characters which will make a spinning effect.
    progcount = 0
    bar = 35  # Size of progress bars
    i = 0  # Counter for building progress bar
    refresh_rate = 0.1  # Refresh rate of UI
    if os.name == 'nt': # Windows
        display = '*'
        os.system("title Forecast Downloader - v%s" % VERSION)
        ver = sys.getwindowsversion()
        if ver[0] == 6 and ver[1] == 2:
            refresh_type = 0
        else:
            refresh_type = 1
        os.system('cls')
    else:
        display = "✓"
        refresh_type = 2
        os.system('clear')
    while not ui_run:
        pass  # Wait for main loop to start
    header = "=" * 64 + "\n\n"
    header += "--- RC24 Forecast Downloader [v%s] --- www.rc24.xyz\n" % VERSION
    header += "By John Pansera / Larsen Vallecillo --- (C) 2015-2019\n\n"
    if config["production"]:
        header += " " * 13 + "*** Production Mode Enabled ***\n"
    while ui_run:
        # Calculate values to show on screen
        dl = len(forecast_list) - cached > 0
        elapsed_time = int(round(time.time() - total_time))
        bandwidth = "%.2f" % round(float(bw_usage) / 1048576, 2)
        totalpercent = int(round(float(lists) / float(len(forecastlists.weathercities)) * 100))
        totalfill = int(totalpercent * 35 / 100)
        totalprog = "[" + "#" * totalfill + " " * (35 - totalfill) + "]"
        if status == 1:
            percent = int(round(float(citycount) / float(len(forecast_list) - cached) * 100)) if dl else 0
            fill = int(round(percent * bar / 100))
            progbar = str(percent) + "% [" + "=" * fill + " " * (bar - fill) + "]"
        else:
            i = (i + 1) % (bar - 1)
            progbar = "[" + " " * i + "=" * 5 + (bar - i - 2) * " " + "]"
        # Build output
        out = header
        out += "API Requests: [%s] API Retries: [%s] Time: [%s]\n" % (apirequests, retrycount, elapsed_time)
        out += "Bandwidth Usage: [%s MiB] Cities: [%s] Errors: [%s]\n" % (bandwidth, cities, errors)
        out += "\nProcessing List #%s/%s (%s): %s %s\n\n" % (
        listid, len(forecastlists.weathercities), country_code, currentlist, "." * progcount)
        if status == 1 and dl: out += "Downloading Forecasts [%s] %s%%\n" % (prog[progcount], percent)
        else: out += "Downloading Forecasts [%s] 100%%\n" % display
        if status == 2: out += "Parsing Data [%s]\n" % prog[progcount]
        elif status == 1: out += "Parsing Data [-]\n"
        else: out += "Parsing Data [%s]" % display + "\n"
        if status == 3: out += "Generating Data [%s]\n" % prog[progcount]
        elif status == 4: out += "Generating Data [%s]" % display + "\n"
        else: out += "Generating Data [-]\n"
        if status == 4: out += "Building Files [%s]\n\n" % prog[progcount]
        else: out += "Building Files [-]\n\n"
        out += "List Progress:  %s" % progbar
        out += "\nTotal Progress: %s%% " % totalpercent + totalprog
        out += "\n\n" + "=" * 64
        progcount = (progcount + 1) % 4

        refresh(refresh_type)
        sys.stdout.write(out)
        sys.stdout.flush()
        time.sleep(refresh_rate)
    print("\n")
    """Log stuff to Datadog."""
    if config["production"] and config["send_stats"]:    
        statsd.increment("forecast.api_requests", apirequests)
        statsd.increment("forecast.retry_count", retrycount)
        statsd.increment("forecast.elapsed_time", elapsed_time)
        statsd.increment("forecast.bandwidth_usage", bandwidth)
        statsd.increment("forecast.cities", cities)
        statsd.increment("forecast.errors", errors)


def get_icon(icon, forecast_list, key):
    if icon == -1: return 'FFFF'
    if isJapan(forecast_list,key):
        return forecastlists.weatherconditions[icon][3]
    else:
        return forecastlists.weatherconditions[icon][1]


"""Resets bin-specific values for next generation."""


def reset_data():
    global seek_offset, seek_base, file, cached, citycount
    seek_offset = 0
    seek_base = 0
    cached = 0
    citycount = 0
    file = None


"""This requests data from AccuWeather's API. It also retries the request if it fails."""


def request_data(url, type=1):
    global retrycount, apirequests, bw_usage, errors
    apirequests += 1
    i = 0
    c = False
    while not c:
        if i == 3:
            errors += 1
            return -1
        if i > 0:
            retrycount += 1
        if type == 0:
            data = s.get(url)
            bw_usage += get_bandwidth_usage(data)
        else: data = requests.get(url)
        status_code = data.status_code
        if status_code == 200:
            c = True
        i += 1
    return data.content


def timestamps(mode, key=None):
    time = time_convert(get_epoch())
    if key: citytime = time_convert(globe[key]['time'])
    if mode == 0:
        timestamp = time
    elif mode == 1:
        timestamp = citytime
    elif mode == 2:
        timestamp = time + 60
    return timestamp


def get_locationkey(forecast_list, key):
    country = get_country(forecast_list, key)
    region = get_region(forecast_list, key)
    city = get_city(forecast_list, key)
    listid = forecastlists.weathercities.index(forecast_list)
    if region == '' and (country not in forecastlists.bincountries or matches_country_code(forecast_list, key)):
        a = hex(weatherloc[listid]['null'][city])[2:].zfill(4)
        b = 'FE'
        c = 'FE'
    elif region == '' and not matches_country_code(forecast_list, key):
        a = hex(weatherloc[listid]['no-region'][country][city])[2:].zfill(4)
        if weatherloc[listid]['count'][country][region] > 1:
            b = 'FE'
        else:
            b = '01'
        c = hex(forecastlists.bincountries[country])[2:].zfill(2)
    else:
        a = hex(weatherloc[listid][country][region][city])[2:].zfill(4)
        b = hex(weatherloc[listid]['regions'][country][region])[2:].zfill(2)
        c = hex(forecastlists.bincountries[country])[2:].zfill(2)
    return "".join([c, b, a])


def zoom(forecast_list, key, mode):
    if mode == 1:
        return forecast_list[key][3][8:][:2]
    if mode == 2:
        return forecast_list[key][3][10:][:2]


def generate_locationkeys(forecast_list):
    listid = forecastlists.weathercities.index(forecast_list)
    weatherloc[listid] = {}
    weatherloc[listid]['null'] = {}
    weatherloc[listid]['no-region'] = {}
    weatherloc[listid]['regions'] = {}
    weatherloc[listid]['count'] = {}
    for k, v in forecast_list.items():
        if v[1][1] == "" and (v[2][1] not in forecastlists.bincountries or matches_country_code(forecast_list, k)):
            weatherloc[listid]['null'].setdefault(v[0][1], len(weatherloc[listid]['null']) + 1)
        elif v[1][1] == "" and not matches_country_code(forecast_list, k):
            weatherloc[listid]['no-region'].setdefault(v[2][1], {})
            weatherloc[listid]['no-region'][v[2][1]].setdefault(v[0][1], len(weatherloc[listid]['no-region'][v[2][1]]) + 1)
        else:
            weatherloc[listid].setdefault(v[2][1], {})
            weatherloc[listid][v[2][1]].setdefault(v[1][1], {})
            weatherloc[listid][v[2][1]][v[1][1]].setdefault(v[0][1], len(weatherloc[listid][v[2][1]][v[1][1]]) + 1)
            weatherloc[listid]['regions'].setdefault(v[2][1], {})
            weatherloc[listid]['regions'][v[2][1]].setdefault('', 1)
            weatherloc[listid]['regions'][v[2][1]].setdefault(v[1][1], len(weatherloc[listid]['regions'][v[2][1]]) + 1)
        weatherloc[listid]['count'].setdefault(v[2][1], {})
        weatherloc[listid]['count'][v[2][1]].setdefault(v[1][1], 0)
        weatherloc[listid]['count'][v[2][1]][v[1][1]] += 1


"""If the script was unable to get forecast for a city, it's filled with this blank data."""


def blank_data(forecast_list, key):
    wind[key] = {}
    uvindex[key] = {}
    precipitation[key] = {}
    week[key] = {}
    hourly[key] = {}
    today[key] = {}
    tomorrow[key] = {}
    current[key] = {}
    globe[key] = {}
    wind[key][0] = 0
    wind[key][1] = 0
    wind[key][2] = 'N'
    wind[key][3] = 0
    wind[key][4] = 0
    wind[key][5] = 'N'
    current[key][0] = 'N'
    current[key][1] = 0
    current[key][2] = 0
    current[key][3] = -128
    current[key][4] = -128
    uvindex[key] = 255
    if isJapan(forecast_list, key):
        pollen[key] = 231 # Missing/No Data
        laundry[key] = 231 # Missing/No Data
    else:
        pollen[key] = 255
        laundry[key] = 255
    current[key][5] = 'FFFF'
    times[key] = get_epoch()
    for k in range(0, 15):
        precipitation[key][k] = 255
    for k in range(0, 28):
        week[key][k] = -128 # Week Temperature Values
    for k in range(30, 37):
        week[key][k] = 'FFFF' # Week Forecast Icons
    for k in range(0, 8):
        hourly[key][k] = 'FFFF' # Hourly Weather Icons
    for k in range(1, 9):
        today[key][k] = -128 # Today Temperature Values
    for k in range(1, 9):
        tomorrow[key][k] = -128 # Tomorrow Temperature Values
    today[key][0] = 'FFFF'
    tomorrow[key][0] = 'FFFF'
    globe[key]['lat'] = binascii.unhexlify(get_lat(forecast_list, key))
    globe[key]['lng'] = binascii.unhexlify(get_lng(forecast_list, key))
    globe[key]['time'] = get_epoch()


def get_accuweather_api(forecast_list, key):
    accuapi = weather_data[key]
    forecast = accuapi.find("{http://www.accuweather.com}forecast")
    current_conditions = accuapi.find("{http://www.accuweather.com}currentconditions")
    hourly_forecast = forecast.find("{http://www.accuweather.com}hourly")
    airandpollen = accuapi.find("{http://www.accuweather.com}airandpollen")
    current[key][3] = int(current_conditions[4].text)
    current[key][4] = to_celsius(current[key][3])
    current[key][5] = get_icon(int(current_conditions[8].text), forecast_list, key)
    current[key][0] = current_conditions[11].text
    current[key][2] = int(current_conditions[10].text)
    current[key][1] = mph_kmh(current[key][2])
    today[key][1] = int(forecast[2][6][4].text)
    today[key][2] = int(forecast[2][6][3].text)
    today[key][3] = to_celsius(today[key][1])
    today[key][4] = to_celsius(today[key][2])
    today[key][0] = get_icon(int(forecast[2][6][2].text), forecast_list, key)
    tomorrow[key][1] = int(forecast[3][6][4].text)
    tomorrow[key][2] = int(forecast[3][6][3].text)
    tomorrow[key][3] = to_celsius(tomorrow[key][1])
    tomorrow[key][4] = to_celsius(tomorrow[key][2])
    tomorrow[key][0] = get_icon(int(forecast[3][6][2].text), forecast_list, key)
    uvindex[key] = int(current_conditions[14].attrib['index'])
    if uvindex[key] > 12:
        uvindex[key] = 12
    wind[key][0] = mph_kmh(forecast[2][6][7].text)
    wind[key][1] = int(forecast[2][6][7].text)
    wind[key][2] = forecast[2][6][8].text
    wind[key][3] = mph_kmh(forecast[3][6][7].text)
    wind[key][4] = int(forecast[3][6][7].text)
    wind[key][5] = forecast[3][6][8].text
    grass = forecastlists.pollen_api[airandpollen[0].text]
    tree = forecastlists.pollen_api[airandpollen[1].text]
    ragweed = forecastlists.pollen_api[airandpollen[2].text]
    avg = int(round((grass+tree+ragweed)/3))
    pollen[key] = avg
    precipitation[key][8] = int(forecast[3][6][19].text)
    precipitation[key][9] = int(forecast[4][6][19].text)
    precipitation[key][10] = int(forecast[5][6][19].text)
    precipitation[key][11] = int(forecast[6][6][19].text)
    precipitation[key][12] = int(forecast[7][6][19].text)
    precipitation[key][13] = int(forecast[8][6][19].text)
    precipitation[key][14] = int(forecast[9][6][19].text)
    lat = float(accuapi[1].find("{http://www.accuweather.com}lat").text)
    lng = float(accuapi[1].find("{http://www.accuweather.com}lon").text)
    check_coords(forecast_list,key,lat,lng)
    globe[key]['lat'] = s16(int(lat / GLOBE_CONSTANT))
    globe[key]['lng'] = s16(int(lng / GLOBE_CONSTANT))
    globe[key]['offset'] = float(accuapi[1].find("{http://www.accuweather.com}currentGmtOffset").text)
    globe[key]['time'] = int(get_epoch() + globe[key]['offset'] * 3600)
    week[key][0] = int(forecast[3][6][3].text)
    week[key][1] = int(forecast[3][6][4].text)
    week[key][2] = int(forecast[4][6][3].text)
    week[key][3] = int(forecast[4][6][4].text)
    week[key][4] = int(forecast[5][6][3].text)
    week[key][5] = int(forecast[5][6][4].text)
    week[key][6] = int(forecast[6][6][3].text)
    week[key][7] = int(forecast[6][6][4].text)
    week[key][8] = int(forecast[7][6][3].text)
    week[key][9] = int(forecast[7][6][4].text)
    week[key][10] = int(forecast[8][6][3].text)
    week[key][11] = int(forecast[8][6][4].text)
    week[key][12] = int(forecast[9][6][3].text)
    week[key][13] = int(forecast[9][6][4].text)
    for i in range(0, 14):
        week[key][i+14] = to_celsius(week[key][i])
    week[key][30] = get_icon(int(forecast[3][6][2].text), forecast_list, key)
    week[key][31] = get_icon(int(forecast[4][6][2].text), forecast_list, key)
    week[key][32] = get_icon(int(forecast[5][6][2].text), forecast_list, key)
    week[key][33] = get_icon(int(forecast[6][6][2].text), forecast_list, key)
    week[key][34] = get_icon(int(forecast[7][6][2].text), forecast_list, key)
    week[key][35] = get_icon(int(forecast[8][6][2].text), forecast_list, key)
    week[key][36] = get_icon(int(forecast[9][6][2].text), forecast_list, key)
    
    time_index = [[3,9,15,21], [27,33,39,45]]
    hourlyAvg = [-3,-2,-1,0,1,2]
    hour = (datetime.utcnow() + timedelta(hours=globe[key]['offset'])).hour
    for i in [0,1]:
        index_offset = 0 if i == 0 else 4
        for j in range(0,4):
            temp = time_index[i][j] - hour
            precip = []
            hourlyAvgIcons = []
            for k in hourlyAvg:
                if validHour(temp+k):
                    precip.append(int(hourly_forecast[temp+k][12].text))
                    hourlyAvgIcons.append(get_icon(int(hourly_forecast[temp+k][0].text), forecast_list, key))
            if len(precip) > 0 and isJapan(forecast_list, key): precipitation[key][j + index_offset] = int(round(sum(precip)/len(precip), -1))
            modeValue = mode_calc(hourlyAvgIcons)
            if len(hourlyAvgIcons) >= 3 and modeValue: hourly[key][j + index_offset] = modeValue
            elif validHour(temp): hourly[key][j + index_offset] = get_icon(int(hourly_forecast[temp][0].text), forecast_list, key)
            else: hourly[key][j + index_offset] = get_icon(int(-1), forecast_list, key)


def parse_data(forecast_list):
    global weather_data
    for k, v in weather_data.items():
        try:
            weather_data[k] = ElementTree.fromstring(v)
            if weather_data[k].find("{http://www.accuweather.com}failure"):
                weather_data[k] = None
        except Exception as e:
            log("An API parsing exception has occurred: %s" % e, "WARNING")
            weather_data[k] = None
            continue
        if weather_data[k]:
            get_accuweather_api(forecast_list, k)
        else:
            log('Unable to retrieve forecast data for %s - using blank data' % k, "INFO")


def hex_write(loc, data):
    global file
    file.seek(loc)
    file.write(u32(data))


def offset_write(value, post=True):
    global file, seek_offset
    seek_offset += 4
    file.seek(seek_offset)
    file.write(u32(value))
    if post: seek_offset += 4


def make_bins(forecast_list, data):
    global mode, language_code
    for i in range(1, file_gen):
        mode = i
        for j in bins:
            language_code = j
            make_forecast_bin(forecast_list, data)
            make_short_bin(forecast_list, data)
            reset_data()


def generate_data(forecast_list, bins):
    global mode, language_code
    long_forecast_tables = dict.fromkeys([1, 2])
    short_japan_tables = dict.fromkeys([1, 2])
    short_forecast_tables = dict.fromkeys([1, 2])
    uvindex_text_tables = dict.fromkeys(bins)
    weathervalue_text_tables = dict.fromkeys(bins)
    text_tables = dict.fromkeys(bins)
    uvindex_table = make_uvindex_table()
    pollenindex_table = make_pollenindex_table()
    pollen_text_table = make_pollen_text_table()
    laundryindex_table = make_laundryindex_table()
    laundry_text_table = make_laundry_text_table()
    location_table = make_location_table(forecast_list)
    weathervalue_offset_table = make_weather_offset_table()
    for i in [1, 2]:
        mode = i
        long_forecast_tables[i] = make_long_forecast_table(forecast_list)
        short_japan_tables[i] = make_forecast_short_table(forecast_list)
        short_forecast_tables[i] = make_short_forecast_table(forecast_list)
    for language in bins:
        language_code = language
        uvindex_text_tables[language] = make_uvindex_text_table()
        text_tables[language] = make_forecast_text_table(forecast_list)
        weathervalue_text_tables[language] = make_weather_value_table()
    return [long_forecast_tables, uvindex_table, uvindex_text_tables, short_japan_tables, pollenindex_table,
            pollen_text_table, laundryindex_table, laundry_text_table, location_table, text_tables,
            weathervalue_offset_table, weathervalue_text_tables, short_forecast_tables]


def make_forecast_bin(forecast_list, data):
    global shortcount, constant, file, seek_offset, seek_base, extension
    constant = 0
    count = {}
    header = make_header_forecast(forecast_list)
    long_forecast_table = data[0][mode]
    uvindex_table = data[1]
    uvindex_text_table = data[2][language_code]
    short_japan_tables = data[3][mode]
    pollenindex_table = data[4]
    pollen_text_table = data[5]
    laundryindex_table = data[6]
    laundry_text_table = data[7]
    location_table = data[8]
    text_table = data[9][language_code]
    weathervalue_offset_table = data[10]
    weathervalue_text_table = data[11][language_code]
    dictionaries = [header, long_forecast_table, short_japan_tables, weathervalue_offset_table, uvindex_table,
                    laundryindex_table, pollenindex_table, location_table, weathervalue_text_table, uvindex_text_table,
                    laundry_text_table, pollen_text_table, text_table]
    if mode == 1:
        extension = "bin"
    elif mode == 2:
        extension = "bi2"
    file = io.BytesIO()
    file1 = 'forecast.{}~.{}+{}'.format(extension, str(country_code).zfill(3), str(language_code))
    file2 = 'forecast.{}.{}_{}'.format(extension, str(country_code).zfill(3), str(language_code))
    file3 = 'forecast.{}'.format(extension)
    file.write(pad(12))
    file.write(u32(timestamps(0)))
    file.write(u32(timestamps(2)))
    for i in dictionaries:
        for v in i.values():
            file.write(v)
        count[constant] = file.tell()
        constant += 1
    file.write(pad(16))
    file.write('RIICONNECT24'.encode('ASCII'))  # This can be used to identify that we made this file.
    file.seek(0)
    hex_write(36, count[0])
    if shortcount > 0:
        hex_write(44, count[1])
    hex_write(52, count[2])
    hex_write(60, count[3])
    hex_write(68, count[4])
    hex_write(76, count[5])
    hex_write(84, count[6])
    seek_offset = count[2]
    seek_base = count[7]
    for i in [list(forecastlists.weatherconditions.values())[j // 2] for j in
              range(len(forecastlists.weatherconditions.values()) * 2)]:
        offset_write(seek_base)
        seek_base += len(i[0][language_code].encode('utf-16be')) + 2
    """UV Index"""
    seek_offset = count[3]
    seek_base = count[8]
    for i in forecastlists.uvindex.values():
        offset_write(seek_base)
        seek_base += len(i[language_code].encode('utf-16be')) + 2
    """Laundry Table"""
    seek_offset = count[4]
    seek_base = count[9]
    for i in forecastlists.laundry.values():
        offset_write(seek_base)
        seek_base += len(i.encode('utf-16be')) + 2
    """Pollen Table"""
    seek_offset = count[5]
    seek_base = count[10]
    for i in forecastlists.pollen.values():
        offset_write(seek_base)
        seek_base += len(i.encode('utf-16be')) + 2
    """Location Text"""
    seek_offset = count[6]
    seek_base = count[11]
    for key in forecast_list.keys():
        offset_write(seek_base, False)
        seek_base += len(forecast_list[key][0][language_code].encode('utf-16be')) + 2
        if len(forecast_list[key][1][language_code]) > 0:
            offset_write(seek_base, False)
            seek_base += len(forecast_list[key][1][language_code].encode('utf-16be')) + 2
        else:
            offset_write(0, False)
        if len(forecast_list[key][2][language_code]) > 0:
            offset_write(seek_base, False)
            seek_base += len(forecast_list[key][2][language_code].encode('utf-16be')) + 2
        else:
            offset_write(0, False)
        seek_offset += 12
    file.seek(0)
    with open(file1, 'wb') as temp:
        temp.write(file.read()[12:])
    file.close()
    if config["production"]:
        sign_file(file1, file2, file3)


def make_short_bin(forecast_list, data):
    short_forecast_header = make_header_short(forecast_list)
    short_forecast_table = data[12][mode]
    file1 = 'short.{}~.{}_{}'.format(extension, str(country_code).zfill(3), str(language_code))
    file2 = 'short.{}.{}_{}'.format(extension, str(country_code).zfill(3), str(language_code))
    file3 = 'short.{}'.format(extension)
    file = io.BytesIO()
    file.write(u32(timestamps(0)))
    file.write(u32(timestamps(2)))
    for v in short_forecast_header.values():
        file.write(v)
    count = file.tell()
    for v in short_forecast_table.values():
        file.write(v)
    file.seek(count-4)
    file.write(u32(count+12))
    file.seek(0)
    with open(file1, 'wb') as temp:
        temp.write(file.read())
    file.close()
    if config["production"]:
        sign_file(file1, file2, file3)


def sign_file(name, local_name, server_name):
    log("Processing " + local_name + " ...", "VERBOSE")
    file = open(name, 'rb')
    copy = file.read()
    crc32 = format(binascii.crc32(copy) & 0xFFFFFFFF, '08x')
    size = os.path.getsize(name) + 12
    dest = open(local_name, 'wb')
    dest.write(u32(0))
    dest.write(u32(size))
    dest.write(binascii.unhexlify(crc32))
    dest.write(copy)
    dest.close()
    file.close()
    os.remove(name)
    log("Compressing ...", "VERBOSE")
    subprocess.call(["%s/lzss" % config["lzss_path"], "-evf", local_name], stdout=subprocess.PIPE)  # Compress the file with the lzss program.
    file = open(local_name, 'rb')
    new = file.read()
    file.close()
    dest = open(local_name, 'wb')
    key = open(config["key_path"], 'rb')
    log("RSA Signing ...", "VERBOSE")
    private_key = rsa.PrivateKey.load_pkcs1(key.read(), "PEM")  # Loads the RSA key.
    signature = rsa.sign(new, private_key, "SHA-1")  # Makes a SHA1 with ASN1 padding. Beautiful.
    dest.write(pad(64))  # Padding. This is where data for an encrypted WC24 file would go (such as the header and IV), but this is not encrypted so it's blank.
    dest.write(signature)
    dest.write(new)
    dest.close()
    key.close()
    subprocess.call(["mkdir", "-p", "{}/{}/{}".format(config["file_path"], language_code, str(country_code).zfill(3))])  # Create directory if it does not exist
    path = "{}/{}/{}/{}".format(config["file_path"], language_code, str(country_code).zfill(3), server_name)  # Path on the server to put the file.
    subprocess.call(["cp", local_name, path])
    os.remove(local_name)


def get_data(forecast_list, key):
    global citycount, cache, weather_data
    citycount += 1
    cache[key] = get_all(forecast_list, key)
    blank_data(forecast_list, key)
    lat = coord_decode(get_lat(forecast_list, key))
    lon = coord_decode(get_lng(forecast_list, key))
    weather_data[key] = request_data("http://{}/widget/accuwxandroidv3/weather-data.asp?location={},{}".format(ip, lat, lon), 0)


def make_header_short(forecast_list):
    header = collections.OrderedDict()
    header["country_code"] = u8(country_code)  # Wii Country Code.
    header["language_code"] = u32(language_code)  # Wii Language Code.
    header["region_flag"] = u8(region_flag)  # Region Flag.
    header["unknown_2"] = u8(0)  # Unknown.
    header["padding_1"] = u8(0)  # Padding.
    header["short_forecast_number"] = u32(len(forecast_list))  # Number of short forecast entries.
    header["start_offset"] = u32(0)

    return header


def make_header_forecast(forecast_list):
    header = collections.OrderedDict()
    header["country_code"] = u8(country_code)  # Wii Country Code.
    header["language_code"] = u32(language_code)  # Wii Language Code.
    header["region_flag"] = u8(region_flag)  # Region Flag.
    header["unknown_2"] = u8(1)  # Unknown.
    header["padding_1"] = u8(0)  # Padding.
    header["message_offset"] = u32(0)  # Offset for a message.
    header["long_forecast_number"] = u32(len(forecast_list) - shortcount)  # Number of long forecast entries.
    header["long_forecast_offset"] = u32(0)  # Offset for the long forecast entry table.
    header["short_forecast_number"] = u32(shortcount)  # Number of short forecast entries.
    header["short_forecast_offset"] = u32(0)  # Offset for the short forecast entry table.
    header["weather_condition_codes_number"] = u32(len(forecastlists.weatherconditions) * 2)  # Number of weather condition code entries.
    header["weather_condition_codes_offset"] = u32(0)  # Offset for the weather condition code table.
    header["uv_index_number"] = u32(len(forecastlists.uvindex))  # Number of UV Index entries.
    header["uv_index_offset"] = u32(0)  # Offset for the UV Index table.
    header["laundry_index_number"] = u32(len(forecastlists.laundry))  # Number of Laundry Index entries.
    header["laundry_index_offset"] = u32(0)  # Offset for the Laundry Index table.
    header["pollen_count_number"] = u32(len(forecastlists.pollen))  # Number of Pollen Count entries.
    header["pollen_count_offset"] = u32(0)  # Offset for the Pollen Count table.
    header["location_number"] = u32(len(forecast_list))  # Number of location entries.
    header["location_offset"] = u32(0)  # Offset for the location table.

    return header


def make_long_forecast_table(forecast_list):
    long_forecast_table = collections.OrderedDict()
    for key in forecast_list.keys():
        if matches_country_code(forecast_list, key) and get_region(forecast_list, key) != '':
            keyIndex = list(forecast_list).index(key)
            long_forecast_table["location_code_%s" % keyIndex] = binascii.unhexlify(get_locationkey(forecast_list, key))  # Wii Location Code.
            long_forecast_table["timestamp_1_%s" % keyIndex] = u32(timestamps(1, key))  # 1st timestamp.
            long_forecast_table["timestamp_2_%s" % keyIndex] = u32(timestamps(0, key))  # 2nd timestamp.
            long_forecast_table["unknown_1_%s" % keyIndex] = u32(0)  # Unknown. (0xC-0xF)
            long_forecast_table["today_forecast_%s" % keyIndex] = binascii.unhexlify(today[key][0])  # Today's forecast.
            long_forecast_table["today_hourly_forecast_12am_6am_%s" % keyIndex] = binascii.unhexlify(hourly[key][0])  # Today's hourly forecast from 12am to 6am.
            long_forecast_table["today_hourly_forecast_6am_12pm_%s" % keyIndex] = binascii.unhexlify(hourly[key][1])  # Today's hourly forecast from 6am to 12pm.
            long_forecast_table["today_hourly_forecast_12pm_6pm_%s" % keyIndex] = binascii.unhexlify(hourly[key][2])  # Today's hourly forecast from 12pm to 6pm.
            long_forecast_table["today_hourly_forecast_6pm_12am_%s" % keyIndex] = binascii.unhexlify(hourly[key][3])  # Today's hourly forecast from 6pm to 12am.
            long_forecast_table["today_tempc_high_%s" % keyIndex] = s8(today[key][4])  # Today's high temperature in Celsius
            long_forecast_table["today_tempc_high_difference_%s" % keyIndex] = s8(today[key][8])  # Today's high temperature difference in Celsius
            long_forecast_table["today_tempc_low_%s" % keyIndex] = s8(today[key][3])  # Today's low temperature in Celsius
            long_forecast_table["today_tempc_low_difference_%s" % keyIndex] = s8(today[key][7])  # Today's low temperature difference in Celsius
            long_forecast_table["today_tempf_high_%s" % keyIndex] = s8(today[key][2])  # Today's high temperature in Fahrenheit
            long_forecast_table["today_tempf_high_difference_%s" % keyIndex] = s8(today[key][6])  # Today's high Fahrenheit difference
            long_forecast_table["today_tempf_low_%s" % keyIndex] = s8(today[key][1])  # Today's low temperature in Fahrenheit
            long_forecast_table["today_tempf_low_difference_%s" % keyIndex] = s8(today[key][5])  # Today's low Fahrenheit difference
            long_forecast_table["today_precipitation_1_%s" % keyIndex] = u8(precipitation[key][0])  # Today's precipitation 1
            long_forecast_table["today_precipitation_2_%s" % keyIndex] = u8(precipitation[key][1])  # Today's precipitation 2
            long_forecast_table["today_precipitation_3_%s" % keyIndex] = u8(precipitation[key][2])  # Today's precipitation 3
            long_forecast_table["today_precipitation_4_%s" % keyIndex] = u8(precipitation[key][3])  # Today's precipitation 4
            long_forecast_table["today_winddirection_%s" % keyIndex] = u8(int(get_wind_direction(wind[key][2])))  # Today's wind direction
            long_forecast_table["today_windkm_%s" % keyIndex] = u8(wind[key][0])  # Today's wind speed in km/hr
            long_forecast_table["today_windmph_%s" % keyIndex] = u8(wind[key][1])  # Today's wind speed in mph
            long_forecast_table["uv_index_%s" % keyIndex] = u8(uvindex[key])  # UV Index
            long_forecast_table["laundry_index_%s" % keyIndex] = u8(laundry[key])  # Laundry Index
            long_forecast_table["pollen_index_%s" % keyIndex] = u8(pollen[key])  # Pollen Index
            long_forecast_table["tomorrow_forecast_%s" % keyIndex] = binascii.unhexlify(tomorrow[key][0])  # Tomorrow's forecast.
            long_forecast_table["tomorrow_hourly_forecast_12am_6am_%s" % keyIndex] = binascii.unhexlify(hourly[key][4])  # Tomorrow's hourly forecast from 12am to 6am.
            long_forecast_table["tomorrow_hourly_forecast_6am_12pm_%s" % keyIndex] = binascii.unhexlify(hourly[key][5])  # Tomorrow's hourly forecast from 6am to 12pm.
            long_forecast_table["tomorrow_hourly_forecast_12pm_6pm_%s" % keyIndex] = binascii.unhexlify(hourly[key][6])  # Tomorrow's hourly forecast from 12pm to 6pm.
            long_forecast_table["tomorrow_hourly_forecast_6pm_12am_%s" % keyIndex] = binascii.unhexlify(hourly[key][7])  # Tomorrow's hourly forecast from 6pm to 12am.
            long_forecast_table["tomorrow_tempc_high_%s" % keyIndex] = s8(tomorrow[key][4])  # Tomorrow's temperature in Celsius
            long_forecast_table["tomorrow_tempc_high_difference_%s" % keyIndex] = s8(tomorrow[key][8])  # Tomorrow's temperature mean in Celsius
            long_forecast_table["tomorrow_tempc_low_%s" % keyIndex] = s8(tomorrow[key][3])  # Tomorrow's Celsius globe value
            long_forecast_table["tomorrow_tempc_low_difference_%s" % keyIndex] = s8(tomorrow[key][7])  # Tomorrow's Celsius globe value
            long_forecast_table["tomorrow_tempf_high_%s" % keyIndex] = s8(tomorrow[key][2])  # Tomorrow's temperature in Fahrenheit
            long_forecast_table["tomorrow_tempf_high_difference_%s" % keyIndex] = s8(tomorrow[key][6])  # Tomorrow's Celsius globe value
            long_forecast_table["tomorrow_tempf_low_%s" % keyIndex] = s8(tomorrow[key][1])  # Tomorrow's temperature mean in Fahrenheit
            long_forecast_table["tomorrow_tempf_low_difference_%s" % keyIndex] = s8(tomorrow[key][5])  # Tomorrow's Fahrenheit globe value
            long_forecast_table["tomorrow_precipitation_1_%s" % keyIndex] = u8(precipitation[key][4])  # Tomorrow's precipitation 1
            long_forecast_table["tomorrow_precipitation_2_%s" % keyIndex] = u8(precipitation[key][5])  # Tomorrow's precipitation 2
            long_forecast_table["tomorrow_precipitation_3_%s" % keyIndex] = u8(precipitation[key][6])  # Tomorrow's precipitation 3
            long_forecast_table["tomorrow_precipitation_4_%s" % keyIndex] = u8(precipitation[key][7])  # Tomorrow's precipitation 4
            long_forecast_table["tomorrow_winddirection_%s" % keyIndex] = u8(int(get_wind_direction(wind[key][5])))  # Tomorrow's wind direction
            long_forecast_table["tomorrow_windkm_%s" % keyIndex] = u8(wind[key][3])  # Tomorrow's wind speed in km/hr
            long_forecast_table["tomorrow_windmph_%s" % keyIndex] = u8(wind[key][4])  # Tomorrow's wind speed in mph
            long_forecast_table["uvindex_2_%s" % keyIndex] = u8(uvindex[key])  # UV Index (Unknown)
            long_forecast_table["laundry_index_2_%s" % keyIndex] = u8(laundry[key])  # Laundry Index (Unknown)
            long_forecast_table["pollen_index_2_%s" % keyIndex] = u8(pollen[key])  # Pollen Index (Unknown)
            long_forecast_table["5day_forecast_1_%s" % keyIndex] = binascii.unhexlify(week[key][30])  # 5-Day forecast day 1 weather icon
            long_forecast_table["5day_tempc_high_1_%s" % keyIndex] = s8(week[key][14])  # 5-Day forecast day 1 high temperature in Celsius
            long_forecast_table["5day_tempc_low_1_%s" % keyIndex] = s8(week[key][15])  # 5-Day forecast day 1 low temperature in Celsius
            long_forecast_table["5day_tempf_high_1_%s" % keyIndex] = s8(week[key][0])  # 5-Day forecast day 1 high temperature in Fahrenheit
            long_forecast_table["5day_tempf_low_1_%s" % keyIndex] = s8(week[key][1])  # 5-Day forecast day 1 low temperature in Fahrenheit
            long_forecast_table["5day_precipitation_1_%s" % keyIndex] = u8(precipitation[key][8])  # 5-Day precipitation percentage 1
            long_forecast_table["5day_forecast_padding_1_%s" % keyIndex] = u8(0)  # Padding
            long_forecast_table["5day_forecast_2_%s" % keyIndex] = binascii.unhexlify(week[key][31])  # 5-Day forecast day 2 weather icon
            long_forecast_table["5day_tempc_high_2_%s" % keyIndex] = s8(week[key][16])  # 5-Day forecast day 2 high temperature in Celsius
            long_forecast_table["5day_tempc_low_2_%s" % keyIndex] = s8(week[key][17])  # 5-Day forecast day 2 low temperature in Celsius
            long_forecast_table["5day_tempf_high_2_%s" % keyIndex] = s8(week[key][2])  # 5-Day forecast day 2 high temperature in Fahrenheit
            long_forecast_table["5day_tempf_low_2_%s" % keyIndex] = s8(week[key][3])  # 5-Day forecast day 2 low temperature in Fahrenheit
            long_forecast_table["5day_precipitation_2_%s" % keyIndex] = u8(precipitation[key][9])  # 5-Day precipitation percentage 2
            long_forecast_table["5day_forecast_padding_2_%s" % keyIndex] = u8(0)  # Padding
            long_forecast_table["5day_forecast_3_%s" % keyIndex] = binascii.unhexlify(week[key][32])  # 5-Day forecast day 3 weather icon
            long_forecast_table["5day_tempc_high_3_%s" % keyIndex] = s8(week[key][18])  # 5-Day forecast day 3 high temperature in Celsius
            long_forecast_table["5day_tempc_low_3_%s" % keyIndex] = s8(week[key][19])  # 5-Day forecast day 3 low temperature in Celsius
            long_forecast_table["5day_tempf_high_3_%s" % keyIndex] = s8(week[key][4])  # 5-Day forecast day 3 high temperature in Fahrenheit
            long_forecast_table["5day_tempf_low_3_%s" % keyIndex] = s8(week[key][5])  # 5-Day forecast day 3 low temperature in Fahrenheit
            long_forecast_table["5day_precipitation_3_%s" % keyIndex] = u8(precipitation[key][10])  # 5-Day precipitation percentage 3
            long_forecast_table["5day_forecast_padding_3_%s" % keyIndex] = u8(0)  # Padding
            long_forecast_table["5day_forecast_4_%s" % keyIndex] = binascii.unhexlify(week[key][33])  # 5-Day forecast day 4 weather icon
            long_forecast_table["5day_tempc_high_4_%s" % keyIndex] = s8(week[key][20])  # 5-Day forecast day 4 high temperature in Celsius
            long_forecast_table["5day_tempc_low_4_%s" % keyIndex] = s8(week[key][21])  # 5-Day forecast day 4 low temperature in Celsius
            long_forecast_table["5day_tempf_high_4_%s" % keyIndex] = s8(week[key][6])  # 5-Day forecast day 4 high temperature in Fahrenheit
            long_forecast_table["5day_tempf_low_4_%s" % keyIndex] = s8(week[key][7])  # 5-Day forecast day 4 low temperature in Fahrenheit
            long_forecast_table["5day_precipitation_4_%s" % keyIndex] = u8(precipitation[key][11])  # 5-Day precipitation percentage 4
            long_forecast_table["5day_forecast_padding_4_%s" % keyIndex] = u8(0)  # Padding
            long_forecast_table["5day_forecast_5_%s" % keyIndex] = binascii.unhexlify(week[key][34])  # 5-Day forecast day 5 weather icon
            long_forecast_table["5day_tempc_high_5_%s" % keyIndex] = s8(week[key][22])  # 5-Day forecast day 5 high temperature in Celsius
            long_forecast_table["5day_tempc_low_5_%s" % keyIndex] = s8(week[key][23])  # 5-Day forecast day 5 low temperature in Celsius
            long_forecast_table["5day_tempf_high_5_%s" % keyIndex] = s8(week[key][8])  # 5-Day forecast day 5 high temperature in Fahrenheit
            long_forecast_table["5day_tempf_low_5_%s" % keyIndex] = s8(week[key][9])  # 5-Day forecast day 5 low temperature in Fahrenheit
            long_forecast_table["5day_precipitation_5_%s" % keyIndex] = u8(precipitation[key][12])  # 5-Day precipitation percentage 5
            long_forecast_table["5day_forecast_padding_5_%s" % keyIndex] = u8(0)  # Padding
            long_forecast_table["5day_forecast_6_%s" % keyIndex] = binascii.unhexlify(week[key][35])  # 5-Day forecast day 6 weather icon (JAPAN ONLY)
            long_forecast_table["5day_tempc_high_6_%s" % keyIndex] = s8(week[key][24])  # 5-Day forecast day 6 high temperature in Celsius (JAPAN ONLY)
            long_forecast_table["5day_tempc_low_6_%s" % keyIndex] = s8(week[key][25])  # 5-Day forecast day 6 low temperature in Celsius (JAPAN ONLY)
            long_forecast_table["5day_tempf_high_6_%s" % keyIndex] = s8(week[key][10])  # 5-Day forecast day 6 high temperature in Fahrenheit (JAPAN ONLY)
            long_forecast_table["5day_tempf_low_6_%s" % keyIndex] = s8(week[key][11])  # 5-Day forecast day 6 low temperature in Fahrenheit (JAPAN ONLY)
            long_forecast_table["5day_precipitation_6_%s" % keyIndex] = u8(precipitation[key][13])  # 5-Day precipitation percentage 6 (JAPAN ONLY)
            long_forecast_table["5day_forecast_padding_6_%s" % keyIndex] = u8(0)  # Padding (JAPAN ONLY)
            long_forecast_table["5day_forecast_7_%s" % keyIndex] = binascii.unhexlify(week[key][36])  # 5-Day forecast day 7 weather icon (JAPAN ONLY)
            long_forecast_table["5day_tempc_high_7_%s" % keyIndex] = u8(week[key][26])  # 5-Day forecast day 7 high temperature in Celsius (JAPAN ONLY)
            long_forecast_table["5day_tempc_low_7_%s" % keyIndex] = u8(week[key][27])  # 5-Day forecast day 7 low temperature in Celsius (JAPAN ONLY)
            long_forecast_table["5day_tempf_high_7_%s" % keyIndex] = u8(week[key][12])  # 5-Day forecast day 7 high temperature in Fahrenheit (JAPAN ONLY)
            long_forecast_table["5day_tempf_low_7_%s" % keyIndex] = u8(week[key][13])  # 5-Day forecast day 7 low temperature in Fahrenheit (JAPAN ONLY)
            long_forecast_table["5day_precipitation_7_%s" % keyIndex] = u8(precipitation[key][14])  # 5-Day precipitation percentage 7 (JAPAN ONLY)
            long_forecast_table["5day_forecast_padding_7_%s" % keyIndex] = u8(0)  # Padding (JAPAN ONLY)

    return long_forecast_table


def make_short_forecast_table(forecast_list):
    short_forecast_table = collections.OrderedDict()
    for key in forecast_list.keys():
        keyIndex = list(forecast_list).index(key)
        short_forecast_table["location_code_%s" % keyIndex] = binascii.unhexlify(get_locationkey(forecast_list, key))  # Wii location code for city
        short_forecast_table["timestamp_1_%s" % keyIndex] = u32(timestamps(1, key))  # Timestamp 1
        short_forecast_table["timestamp_2_%s" % keyIndex] = u32(timestamps(0, key))  # Timestamp 2
        short_forecast_table["current_forecast_%s" % keyIndex] = binascii.unhexlify(current[key][5])  # Current forecast
        short_forecast_table["unknown_%s" % keyIndex] = u8(0)  # 0xE unknown
        short_forecast_table["current_tempc_%s" % keyIndex] = s8(current[key][4])  # Current temperature in Celsius
        short_forecast_table["current_tempf_%s" % keyIndex] = s8(current[key][3])  # Current temperature in Fahrenheit
        short_forecast_table["current_winddirection_%s" % keyIndex] = u8(int(get_wind_direction(current[key][0])))  # Current wind direction
        short_forecast_table["current_windkm_%s" % keyIndex] = u8(current[key][1])  # Current wind in km/hr
        short_forecast_table["current_windmph_%s" % keyIndex] = u8(current[key][2])  # Current wind in mph
        short_forecast_table["unknown_2_%s" % keyIndex] = u16(0)  # 00?
        short_forecast_table["unknown_3_%s" % keyIndex] = binascii.unhexlify('FFFF')  # FFFF?

    return short_forecast_table


def make_forecast_short_table(forecast_list):
    short_forecast_table = collections.OrderedDict()
    for key in forecast_list.keys():
        if not matches_country_code(forecast_list, key) or get_region(forecast_list, key) == '':
            keyIndex = list(forecast_list).index(key)
            short_forecast_table["location_code_%s" % keyIndex] = binascii.unhexlify(get_locationkey(forecast_list, key))  # Wii Location Code.
            short_forecast_table["timestamp_1_%s" % keyIndex] = u32(timestamps(1, key))  # 1st timestamp.
            short_forecast_table["timestamp_2_%s" % keyIndex] = u32(timestamps(0, key))  # 2nd timestamp.
            short_forecast_table["padding_%s" % keyIndex] = u32(0)
            short_forecast_table["today_forecast_%s" % keyIndex] = binascii.unhexlify(today[key][0])  # Today's forecast.
            short_forecast_table["today_hourly_forecast_12am_6am_%s" % keyIndex] = binascii.unhexlify(hourly[key][0])  # Today's hourly forecast from 12am to 6am.
            short_forecast_table["today_hourly_forecast_6am_12pm_%s" % keyIndex] = binascii.unhexlify(hourly[key][1])  # Today's hourly forecast from 6am to 12pm.
            short_forecast_table["today_hourly_forecast_12pm_6pm_%s" % keyIndex] = binascii.unhexlify(hourly[key][2])  # Today's hourly forecast from 12pm to 6pm.
            short_forecast_table["today_hourly_forecast_6pm_12am_%s" % keyIndex] = binascii.unhexlify(hourly[key][3])  # Today's hourly forecast from 6pm to 12am.
            short_forecast_table["today_tempc_high_%s" % keyIndex] = s8(today[key][4])  # Today's high temperature in Celsius
            short_forecast_table["today_tempc_high_difference_%s" % keyIndex] = s8(today[key][8])  # Today's high temperature difference in Celsius
            short_forecast_table["today_tempc_low_%s" % keyIndex] = s8(today[key][3])  # Today's low temperature in Celsius
            short_forecast_table["today_tempc_low_difference_%s" % keyIndex] = s8(today[key][7])  # Today's low temperature difference in Celsius
            short_forecast_table["today_tempf_high_%s" % keyIndex] = s8(today[key][2])  # Today's high temperature in Fahrenheit
            short_forecast_table["today_tempf_high_difference_%s" % keyIndex] = s8(today[key][6])  # Today's high Fahrenheit difference
            short_forecast_table["today_tempf_low_%s" % keyIndex] = s8(today[key][1])  # Today's low temperature in Fahrenheit
            short_forecast_table["today_tempf_low_difference_%s" % keyIndex] = s8(today[key][5])  # Today's low Fahrenheit difference
            short_forecast_table["today_precipitation_1_%s" % keyIndex] = u8(precipitation[key][0])  # Today's precipitation 1
            short_forecast_table["today_precipitation_2_%s" % keyIndex] = u8(precipitation[key][1])  # Today's precipitation 2
            short_forecast_table["today_precipitation_3_%s" % keyIndex] = u8(precipitation[key][2])  # Today's precipitation 3
            short_forecast_table["today_precipitation_4_%s" % keyIndex] = u8(precipitation[key][3])  # Today's precipitation 4
            short_forecast_table["today_winddirection_%s" % keyIndex] = u8(int(get_wind_direction(wind[key][2])))  # Today's wind direction
            short_forecast_table["today_windkm_%s" % keyIndex] = u8(wind[key][0])  # Today's wind speed in km/hr
            short_forecast_table["today_windmph_%s" % keyIndex] = u8(wind[key][1])  # Today's wind speed in mph
            short_forecast_table["unknown_value_%s" % keyIndex] = u8(255)  # ??
            short_forecast_table["unknown_value_2_%s" % keyIndex] = u8(255)  # ??
            short_forecast_table["unknown_value_3_%s" % keyIndex] = u8(255)  # ??
            short_forecast_table["tomorrow_forecast_%s" % keyIndex] = binascii.unhexlify(tomorrow[key][0])  # Tomorrow's forecast.
            short_forecast_table["tomorrow_hourly_forecast_12am_6am_%s" % keyIndex] = binascii.unhexlify(hourly[key][4])  # Tomorrow's hourly forecast from 12am to 6am.
            short_forecast_table["tomorrow_hourly_forecast_6am_12pm_%s" % keyIndex] = binascii.unhexlify(hourly[key][5])  # Tomorrow's hourly forecast from 6am to 12pm.
            short_forecast_table["tomorrow_hourly_forecast_12pm_6pm_%s" % keyIndex] = binascii.unhexlify(hourly[key][6])  # Tomorrow's hourly forecast from 12pm to 6pm.
            short_forecast_table["tomorrow_hourly_forecast_6pm_12am_%s" % keyIndex] = binascii.unhexlify(hourly[key][7])  # Tomorrow's hourly forecast from 6pm to 12am.
            short_forecast_table["tomorrow_tempc_high_%s" % keyIndex] = s8(tomorrow[key][4])  # Tomorrow's temperature in Celsius
            short_forecast_table["tomorrow_tempc_high_difference_%s" % keyIndex] = s8(tomorrow[key][8])  # Tomorrow's temperature mean in Celsius
            short_forecast_table["tomorrow_tempc_low_%s" % keyIndex] = s8(tomorrow[key][3])  # Tomorrow's Celsius globe value
            short_forecast_table["tomorrow_tempc_low_difference_%s" % keyIndex] = s8(tomorrow[key][7])  # Tomorrow's Celsius globe value
            short_forecast_table["tomorrow_tempf_high_%s" % keyIndex] = s8(tomorrow[key][2])  # Tomorrow's temperature in Fahrenheit
            short_forecast_table["tomorrow_tempf_high_difference_%s" % keyIndex] = s8(tomorrow[key][6])  # Tomorrow's Celsius globe value
            short_forecast_table["tomorrow_tempf_low_%s" % keyIndex] = s8(tomorrow[key][1])  # Tomorrow's temperature mean in Fahrenheit
            short_forecast_table["tomorrow_tempf_low_difference_%s" % keyIndex] = s8(tomorrow[key][5])  # Tomorrow's Fahrenheit globe value
            short_forecast_table["tomorrow_precipitation_1_%s" % keyIndex] = u8(precipitation[key][4])  # Tomorrow's precipitation 1
            short_forecast_table["tomorrow_precipitation_2_%s" % keyIndex] = u8(precipitation[key][5])  # Tomorrow's precipitation 2
            short_forecast_table["tomorrow_precipitation_3_%s" % keyIndex] = u8(precipitation[key][6])  # Tomorrow's precipitation 3
            short_forecast_table["tomorrow_precipitation_4_%s" % keyIndex] = u8(precipitation[key][7])  # Tomorrow's precipitation 4
            short_forecast_table["tomorrow_winddirection_%s" % keyIndex] = u8(int(get_wind_direction(wind[key][5])))  # Tomorrow's wind direction
            short_forecast_table["tomorrow_windkm_%s" % keyIndex] = u8(wind[key][3])  # Tomorrow's wind speed in km/hr
            short_forecast_table["tomorrow_windmph_%s" % keyIndex] = u8(wind[key][4])  # Tomorrow's wind speed in mph
            short_forecast_table["uvindex_%s" % keyIndex] = u8(uvindex[key])  # Today's UV Index
            short_forecast_table["laundry_index_%s" % keyIndex] = u8(laundry[key])  # Today's Laundry Index
            short_forecast_table["pollen_index_%s" % keyIndex] = u8(pollen[key])  # Today's Pollen Index

    return short_forecast_table


"""Database of UV index values."""


def make_uvindex_table():
    uvindex = collections.OrderedDict()
    for i in forecastlists.uvindex:
        uvindex["uv_%s_number" % i] = u8(i)
        uvindex["uv_%s_padding" % i] = pad(3)
        uvindex["uv_%s_offset" % i] = u32(0)

    return uvindex


"""Database of laundry index values."""


def make_laundryindex_table():
    laundry = collections.OrderedDict()
    for i in forecastlists.laundry:
        laundry["laundry_%s_number" % i] = u8(i)
        laundry["laundry_%s_padding" % i] = pad(3)
        laundry["laundry_%s_offset" % i] = u32(0)

    return laundry


"""Database of pollen index values."""


def make_pollenindex_table():
    pollen = collections.OrderedDict()
    for i in forecastlists.pollen:
        pollen["pollen_%s_number" % i] = u8(i)
        pollen["pollen_%s_padding" % i] = pad(3)
        pollen["pollen_%s_offset" % i] = u32(0)

    return pollen


def make_location_table(forecast_list):
    location_table = collections.OrderedDict()
    for key in forecast_list.keys():
        keyIndex = list(forecast_list).index(key)
        location_table["location_code_%s" % keyIndex] = binascii.unhexlify(get_locationkey(forecast_list, key))  # Wii Location Code.
        location_table["city_text_offset_%s" % keyIndex] = u32(0)  # Offset for location's city text
        location_table["region_text_offset_%s" % keyIndex] = u32(0)  # Offset for location's region text
        location_table["country_text_offset_%s" % keyIndex] = u32(0)  # Offset for location's country text
        location_table["latitude_coordinates_%s" % keyIndex] = globe[key]['lat']  # Latitude coordinates for location on globe
        location_table["longitude_coordinates_%s" % keyIndex] = globe[key]['lng']  # Longitude coordinates for location on globe
        location_table["location_zoom_1_%s" % keyIndex] = binascii.unhexlify(zoom(forecast_list, key, 1))  # Location zoom for location on globe
        location_table["location_zoom_2_%s" % keyIndex] = binascii.unhexlify(zoom(forecast_list, key, 2))  # Location zoom for location on globe
        location_table["padding_%s" % keyIndex] = u16(0)

    return location_table


def make_forecast_text_table(forecast_list):
    text_table = collections.OrderedDict()
    for key in forecast_list.keys():
        keyIndex = list(forecast_list).index(key)
        text_table[keyIndex] = "\0".join(list(filter(None, [forecast_list[key][0][language_code],
                                                           forecast_list[key][1][language_code],
                                                           forecast_list[key][2][language_code]]))).encode("utf-16be") + pad(2)
    return text_table


def make_weather_value_table():
    weathervalue_text_table = collections.OrderedDict()
    for k,v in forecastlists.weatherconditions.items():
        keyIndex = list(forecastlists.weatherconditions).index(k)
        for i in range(2):
            weathervalue_text_table["weather_text_%s_%s" % (keyIndex, i)] = v[0][language_code].encode("utf-16be") + pad(2)
    return weathervalue_text_table


def make_weather_offset_table():
    weathervalue_offset_table = collections.OrderedDict()
    for k,v in forecastlists.weatherconditions.items():
        keyIndex = list(forecastlists.weatherconditions).index(k)
        weathervalue_offset_table["condition_code_1_international_%s" % keyIndex] = binascii.unhexlify(v[1])
        weathervalue_offset_table["condition_code_2_international_%s" % keyIndex] = binascii.unhexlify(v[2])
        weathervalue_offset_table["padding_1_%s" % keyIndex] = u32(0)
        weathervalue_offset_table["condition_code_1_japan_%s" % keyIndex] = binascii.unhexlify(v[3])
        weathervalue_offset_table["condition_code_2_japan_%s" % keyIndex] = binascii.unhexlify(v[4])
        weathervalue_offset_table["padding_2_%s" % keyIndex] = u32(0)
    return weathervalue_offset_table


def make_uvindex_text_table():
    uvindex_text_table = collections.OrderedDict()
    uvindexlist = []
    for v in forecastlists.uvindex.values():
        uvindexlist.append(v[language_code])
    uvindex_text_table[0] = "\0".join(uvindexlist).encode("utf-16be") + pad(2)
    return uvindex_text_table


def make_laundry_text_table():
    laundry = collections.OrderedDict()
    for k,v in forecastlists.laundry.items():
        keyIndex = list(forecastlists.laundry).index(k)
        laundry[keyIndex] = v.encode("utf-16be") + pad(2)
    return laundry


def make_pollen_text_table():
    pollen = collections.OrderedDict()
    for k,v in forecastlists.pollen.items():
        keyIndex = list(forecastlists.pollen).index(k)
        pollen[keyIndex] = v.encode("utf-16be") + pad(2)
    return pollen


def get_wind_direction(degrees):
    return forecastlists.winddirection[degrees]


def dump_db():
    db = {"update_time": time.time(), "location_keys": weatherloc, "local_times": times, "laundry_indexes": laundry,
          "pollen_indexes": pollen, "globe_data": globe, "wind_speed": wind, "uvindexes": uvindex,
          "current_forecast": current, "precipitation": precipitation, "hourly_forecast": hourly,
          "tomorrow_forecast": tomorrow, "week_forecast": week, "today_forecast": today, "key_cache": cache}
    with open('weather.db', 'wb') as f:
        pickle.dump(db, f)


with open("./Channels/Forecast_Channel/config.json", "rb") as f:
    config = json.load(f)
if config["production"] and config["send_logs"]:
    setup_log(config["sentry_url"], False)

s = requests.Session()  # Use session to speed up requests
s.headers.update({'Accept-Encoding': 'gzip, deflate', 'Host': 'accuwxandroidv3.accu-weather.com'})
ip = socket.gethostbyname("accuwxandroidv3.accu-weather.com")
total_time = time.time()
q = queue.Queue()
threads = []
concurrent = 10 if config["multithreaded"] else 1
file_gen = 3 if config["wii_u_generation"] else 2
ui_run = None
threads_run = True
ui_thread = threading.Thread(target=ui)
ui_thread.daemon = True
ui_thread.start()
spawn_threads()


for forecast_list in forecastlists.weathercities:
    status = 1
    language_code = 1
    shortcount = 0
    listid = forecastlists.weathercities.index(forecast_list) + 1
    currentlist = list(forecast_list.values())[0][2][1]
    ui_run = True
    weather_data = {}
    country_code = forecastlists.bincountries[currentlist]
    region_flag = get_region_flag(country_code)
    bins = get_bins(country_code)
    populate_international(forecast_list)
    generate_locationkeys(forecast_list)
    for key in forecast_list.keys():
        if not matches_country_code(forecast_list, key) or get_region(forecast_list, key) == '': shortcount += 1
        if key in cache and cache[key] == get_all(forecast_list, key): cached += 1
        else: q.put([forecast_list, key])
    q.join()
    status = 2
    parse_data(forecast_list)
    cities += citycount
    status = 3
    data = generate_data(forecast_list, bins)
    status = 4
    make_bins(forecast_list, data)
    lists += 1

time.sleep(0.1)
close_threads()
dump_db()

if config["production"] and config["send_webhooks"]:
    """This will use a webhook to log that the script has been ran."""
    data = {"username": "Forecast Bot", "content": "Weather Data has been updated!",
            "avatar_url": "http://rc24.xyz/images/logo-small.png", "attachments": [
            {"fallback": "Weather Data Update", "color": "#0381D7", "author_name": "RiiConnect24 Forecast Script",
             "author_icon": "https://rc24.xyz/images/webhooks/forecast/profile.png",
             "text": "Weather Data has been updated!", "title": "Update!",
             "fields": [{"title": "Script", "value": "Forecast Channel", "short": "false"}],
             "thumb_url": "https://rc24.xyz/images/webhooks/forecast/accuweather.png", "footer": "RiiConnect24 Script",
             "footer_icon": "https://rc24.xyz/images/logo-small.png",
             "ts": int(time.mktime(datetime.utcnow().timetuple())) + 25200}]}
    for url in config["webhook_urls"]:
        post_webhook = requests.post(url, json=data, allow_redirects=True)

print("Completed Successfully")
