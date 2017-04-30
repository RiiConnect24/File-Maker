#!/usr/bin/python
# -*- coding: utf-8 -*-

import config
import collections
import forecastlists
import forecastregions
import googlemaps
import json
import pycountry
import requests
import sys
from config import *
from unidecode import unidecode
reload(sys)
sys.setdefaultencoding("UTF-8")

print "Forecast Channel Metadata Translator"
print "By Larsen Vallecillo - 2017"

languages = {
	"ja": 0,
	"en": 1,
	"de": 2,
	"fr": 3,
	"es": 4,
	"it": 5,
	"nl": 6,
}

def get_translated(weather, city_original, l, geocode):
	for language in languages.items():
		if language[1] == i:
			l = language[0]
			break

	return gmaps.reverse_geocode(geocode[0]["place_id"], language=l)

for weather in config.weathercities:
	country_code = forecastlists.bincountries[weather.values()[0][2]]

	print "weathercities%s = collections.OrderedDict()" % str(country_code).zfill(3)

	print "\n"

	for items in weather.items():
		value = items[1]

		city_original = items[0]
		city = value[0]
		region = value[1]
		country = value[2]
		coordinates = value[3]

		cities = ["", "", "", "", "", "", ""]
		regions = ["", "", "", "", "", "", ""]
		countries = ["", "", "", "", "", "", "",]

		cities[1] = city
		regions[1] = region
		countries[1] = country

		gmaps = googlemaps.Client(key=google_maps_api_key)

		if country == "St. Lucia":
			country_code2 = "LC"
		elif country == "St. Kitts and Nevis":
			country_code2 = "KN"
		elif country == "St. Vincent and the Grenadines":
			country_code2 = "VC"
		else:
			country_code2 = pycountry.countries.get(name=country).alpha2.upper()

		geocode = gmaps.geocode(unidecode(city.decode("utf-8")), components={"country": country_code2})

		for i in [0, 2, 3, 4, 5, 6]:
			country = forecastregions.regioninfo[country_code][1][2][i]

			if region != "":
				for values in forecastregions.regioninfo[country_code].values():
					if values[2] == region:
						region = values[2][i]
						break

			translated = get_translated(weather, city_original, i, geocode)

			cities[i] = str(translated[0]["address_components"][0]["long_name"])
			regions[i] = region
			countries[i] = country

		print 'weathercities%s["%s"] = [%s, %s, %s, "%s"]' % (str(country_code).zfill(3), city_original, cities, regions, countries, coordinates)

	print "\n"
