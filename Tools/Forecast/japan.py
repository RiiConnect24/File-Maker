#!/usr/bin/python
# -*- coding: utf-8 -*-

import collections
import json
import googlemaps

gmaps = googlemaps.Client(key="AIzaSyD8ouvQPlFAdVrThJ_wvmA6QZh-Y4whGzY")

langs = ["ja", "en", "de", "fr", "es", "it", "nl"]

list = ""

for l in langs:
    if l != "ja":
        geocode_result = gmaps.geocode("溝辺町", language=l)
        name = geocode_result[0]["address_components"][0]["long_name"]
        list += name.encode("utf-8")
        if l != "nl":
            list += ", "
    else:
        list += "溝辺"
        list += ", "

print list