#!/usr/bin/python
# -*- coding: utf-8 -*-

import binascii
import collections
import os
import pickle
import sys
import collections

print "Forecast File Parser"
print "By John Pansera (2017-2019) - www.rc24.xyz"
print "Parsing ...\n"

filename = "forecast.bin"
amnt = None
offset = None
file = None
names = collections.OrderedDict()
zoom = []


def hex(data):
    return binascii.hexlify(data)


def read_int(x):
    return int(binascii.hexlify(file.read(x)), 16)


def coord_decode(value):
    value = int(value, 16)
    if value >= 0x8000:
        value -= 0x10000
    return value * 0.0054931640625


def parse_offsets(dict, count, offset):
    file.seek(offset)
    for i in range(count):
        code = read_int(1)
        padding = read_int(3)
        offset = read_int(4)
        dict[i] = [code, offset]


def get_text_by_offset(dict):
    ref = dict[0][1]
    file.seek(ref)
    for i in dict:
        try: next = dict[i + 1]
        except: next = None
        if next: dict[i][1] = next[1] - dict[i][1]
        else: dict[i][1] = 0
        data = file.read(dict[i][1])
        try: data = data.decode('utf-16be')
        except: pass


def get_text():
    str = ""
    null_last = False
    while True:
        char = file.read(1)
        str += char
        if char == '\00':
            if not null_last:
                null_last = True
            else:
                null_last = False
                break
        else: null_last = False
    return str


file = open(filename, "rb")

# Print file header information

version = read_int(4)
print "Version: %s" % version
file_size = read_int(4)
print "File Size: %s" % file_size
crc32 = hex(file.read(4))
print "CRC32: %s" % crc32
timestamp_1 = read_int(4)
timestamp_2 = read_int(4)
print "Valid until: %s (for %s minutes)" % (timestamp_1,int(timestamp_1-timestamp_2))
print "Generated at: %s" % timestamp_2

file.seek(20) # Country Code
country_code = hex(file.read(1))
print "Country Code: %s (%s)" % (country_code, str(int(country_code, 16)).zfill(3))

file.seek(21) # Language Code
language_code = read_int(4)
print "Language Code: %s" % language_code

file.seek(28) # Message Offset
message_offset = read_int(4)
if message_offset == 0: print "No Message in file"
else: print "Message exists in file"

file.seek(32) # Long Forecast Entry Number
long_count = read_int(4)
file.seek(36) # Long Forecast Table Offset
long_offset = read_int(4)
print "%s long forecast table entries @ %s" % (long_count, long_offset)

file.seek(40) # Short Forecast Entry Number
short_count = read_int(4)
file.seek(44) # Short Forecast Table Offset
short_offset = read_int(4)
print "%s short forecast table entries @ %s" % (short_count, short_offset)

file.seek(48) # Weather Condition Codes Entry Number
weatherconditions_count = read_int(4)
file.seek(52) # Weather Condition Codes Table Offset
weatherconditions_offset = read_int(4)
print "%s weather condition entries @ %s" % (weatherconditions_count, weatherconditions_offset)

file.seek(56) # UV Index Entry Number
uvindex_count = read_int(4)
file.seek(60) # UV Index Table Offset
uvindex_offset = read_int(4)
print "%s uv index entries @ %s" % (uvindex_count, uvindex_offset)

file.seek(64) # Laundry Index Entry Number
laundry_count = read_int(4)
file.seek(68) # Laundry Index Table Offset
laundry_offset = read_int(4)
print "%s laundry index entries @ %s" % (laundry_count, laundry_offset)

file.seek(72) # Pollen Count Entry Number
pollen_count = read_int(4)
file.seek(76) # Pollen Count Entry Offset
pollen_offset = read_int(4)
print "%s pollen index entries @ %s" % (pollen_count, pollen_offset)

file.seek(80) # Location Entry Number
amnt = read_int(4)
file.seek(84) # Location Table Offset
offset = read_int(4)
print "%s location entries @ %s" % (amnt, offset)

# Parse Entries
uvindex = collections.OrderedDict()
laundry = collections.OrderedDict()
pollen = collections.OrderedDict()
weather = collections.OrderedDict()
parse_offsets(uvindex, uvindex_count, uvindex_offset)
parse_offsets(laundry, laundry_count, laundry_offset)
parse_offsets(pollen, pollen_count, pollen_offset)
parse_offsets(weather, weatherconditions_count, weatherconditions_offset)

file.seek(uvindex[0][1])
print "\nUV Index Entries:"
for i in range(uvindex_count):
    uvindex[i] = get_text()
    print "    %s" % uvindex[i].decode('utf-16be')

file.seek(laundry[0][1])
for i in range(laundry_count):
    laundry[i] = get_text()

file.seek(pollen[0][1])
for i in range(pollen_count):
    pollen[i] = get_text()

print "\nWeather Conditions:"
file.seek(weather[0][1])
for i in range(weatherconditions_count / 2):
    weather[i] = get_text()
    print "    %s" % weather[i].decode('utf-16be').replace('\n', ' ')

raw_input("\nParsing location entries:")

# Parse location entries
file.seek(offset)
for _ in range(amnt):
    loc_name = file.read(4)
    city = read_int(4)
    region = read_int(4)
    country = read_int(4)
    lat = coord_decode(hex(file.read(2)))
    lng = coord_decode(hex(file.read(2)))
    zoom1 = read_int(1)
    zoom2 = read_int(1)
    file.seek(2, 1)
    names[hex(loc_name)] = [city, region, country, lat, lng, zoom1, zoom2]

for k in names.keys():
    try:
        next = names.items()[names.keys().index(k) + 1]
    except:
        next = None
    first = names[k][0]
    second = names[k][2] if names[k][1] == 0 and names[k][2] != 0 else (int(os.path.getsize(filename)) if next is None else next[1][0]) if names[k][1] == 0 and names[k][2] == 0 else names[k][1]
    file.seek(names[k][0])
    city_string = file.read(second - first)
    if names[k][1] != 0:
        first = names[k][1]
        second = names[k][2]
        file.seek(names[k][1])
        region_string = file.read(second - first)
    else:
        region_string = None
    if names[k][2] != 0:
        first = names[k][2]
        second = next[1][0]
        file.seek(names[k][2])
        country_string = file.read(second - first)
    else:
        country_string = None

    print "Location ID: %s" % k.upper()
    print "City: %s" % city_string.decode('utf-16be').encode('utf-8')
    if region_string is not None:
        print "Region: %s" % region_string.decode('utf-16be').encode('utf-8')
    else:
        print "No Region"
    if country_string is not None:
        print "Country: %s" % country_string.decode('utf-16be').encode('utf-8')
    else:
        print "No Country"
    print "Latitude Coordinate: %s" % names[k][3]
    print "Longitude Coordinate: %s" % names[k][4]
    print "Zoom 1: %s" % names[k][5]
    zoom.append(int(names[k][5]))
    print "Zoom 2: %s" % names[k][6]


print "\nDumping Locations Database ..."
if os.path.exists('locations.json'):
    os.remove('locations.json')
with open('locations.json', 'wb') as file:
    pickle.dump(names, file)

print "Completed Sucessfully"
