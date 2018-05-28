#!/usr/bin/python
# -*- coding: utf-8 -*-

import binascii
import collections
import os
import pickle

print("Forecast Locations Parser")
print("By John Pansera (2017) - www.rc24.xyz")
print("Parsing ...")

filename = "forecast.bin"
amnt = None
offset = None
file = None
current = 0
names = collections.OrderedDict()
zoom = []


def seek(value):
    global current, file
    current += value
    file.seek(current)


def hex(data):
    return binascii.hexlify(data)


def dec(a):
    return int(a, 16)


def coord_decode(value):
    value = int(value, 16)
    if value >= 0x8000: value -= 0x10000
    return value * 0.0054931640625


file = open(filename, "rb")
file.seek(0)
file.seek(80)
amnt = int(binascii.hexlify(file.read(4)), 16)
print("Processing %s Entries" % amnt)
file.seek(84)
offset = int(binascii.hexlify(file.read(4)), 16)
seek(offset)
for _ in range(amnt):
    loc_name = file.read(4)
    seek(4)
    city = file.read(4)
    seek(4)
    region = file.read(4)
    seek(4)
    country = file.read(4)
    seek(4)
    lat = coord_decode(hex(file.read(2)))
    seek(2)
    lng = coord_decode(hex(file.read(2)))
    seek(2)
    zoom1 = dec(hex(file.read(1)))
    seek(1)
    zoom2 = dec(hex(file.read(1)))
    seek(3)
    names[hex(loc_name)] = [dec(hex(city)), dec(hex(region)), dec(hex(country)), lat, lng, zoom1, zoom2]

for k in list(names.keys()):
    try:
        next = list(names.items())[list(names.keys()).index(k) + 1]
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

    print("Location ID: %s" % k.upper())
    print("City: %s" % city_string)
    if region_string is not None:
        print("Region: %s" % region_string)
    else:
        print("No Region")
    if country_string is not None:
        print("Country: %s" % country_string)
    else:
        print("No Country")
    print("Latitude Coordinate: %s" % names[k][3])
    print("Longitutde Coordinate: %s" % names[k][4])
    print("Zoom 1: %s" % names[k][5])
    zoom.append(int(names[k][5]))
    print("Zoom 2: %s" % names[k][6])

    print("\n")

print("Dumping Database ...")
if os.path.exists('locations.json'): os.remove('locations.json')
with open('locations.json', 'wb') as file:
    pickle.dump(names, file)

print("Completed Sucessfully")
