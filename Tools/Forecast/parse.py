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
crc32 = binascii.hexlify(file.read(4))
print "CRC32: %s" % crc32
timestamp_1 = read_int(4)
timestamp_2 = read_int(4)
print "Valid until: %s (for %s minutes)" % (timestamp_1,int(timestamp_1-timestamp_2))
print "Generated at: %s" % timestamp_2

file.seek(20) # Country Code
country_code = binascii.hexlify(file.read(1))
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
print "%s long forecast table entries @ %s" % (long_count, hex(long_offset))

file.seek(40) # Short Forecast Entry Number
short_count = read_int(4)
file.seek(44) # Short Forecast Table Offset
short_offset = read_int(4)
print "%s short forecast table entries @ %s" % (short_count, hex(short_offset))

file.seek(48) # Weather Condition Codes Entry Number
weatherconditions_count = read_int(4)
file.seek(52) # Weather Condition Codes Table Offset
weatherconditions_offset = read_int(4)
print "%s weather condition entries @ %s" % (weatherconditions_count, hex(weatherconditions_offset))

file.seek(56) # UV Index Entry Number
uvindex_count = read_int(4)
file.seek(60) # UV Index Table Offset
uvindex_offset = read_int(4)
print "%s uv index entries @ %s" % (uvindex_count, hex(uvindex_offset))

file.seek(64) # Laundry Index Entry Number
laundry_count = read_int(4)
file.seek(68) # Laundry Index Table Offset
laundry_offset = read_int(4)
print "%s laundry index entries @ %s" % (laundry_count, hex(laundry_offset))

file.seek(72) # Pollen Count Entry Number
pollen_count = read_int(4)
file.seek(76) # Pollen Count Entry Offset
pollen_offset = read_int(4)
print "%s pollen index entries @ %s" % (pollen_count, hex(pollen_offset))

file.seek(80) # Location Entry Number
amnt = read_int(4)
file.seek(84) # Location Table Offset
offset = read_int(4)
print "%s location entries @ %s" % (amnt, hex(offset))

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
for i in range(amnt):
    loc_name = binascii.hexlify(file.read(4))
    city = read_int(4)
    region = read_int(4)
    country = read_int(4)
    lat = coord_decode(binascii.hexlify(file.read(2)))
    lng = coord_decode(binascii.hexlify(file.read(2)))
    zoom1 = read_int(1)
    zoom2 = read_int(1)
    file.seek(2, 1)
    names[i] = [loc_name, city, region, country, lat, lng, zoom1, zoom2]


file.seek(names[0][1])
for k in names.keys():
    names[k][1] = get_text()
    if names[k][2] != 0: names[k][2] = get_text()
    if names[k][3] != 0: names[k][3] = get_text()

    print "Location ID: %s" % names[k][0].upper()
    print "City: %s" % names[k][1].decode('utf-16be').encode('utf-8')
    if names[k][2] != 0: print "Region: %s" % names[k][2].decode('utf-16be').encode('utf-8')
    else: print "No Region"
    if names[k][3] != 0: print "Country: %s" % names[k][3].decode('utf-16be').encode('utf-8')
    else: print "No Country"
    print "Latitude Coordinate: %s" % names[k][4]
    print "Longitude Coordinate: %s" % names[k][5]
    print "Zoom 1: %s" % names[k][6]
    print "Zoom 2: %s" % names[k][7]


print "\nDumping Locations Database ..."
with open('locations.db', 'wb') as file:
    pickle.dump(names, file)

print "Completed Sucessfully"
