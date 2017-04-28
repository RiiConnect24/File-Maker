#!/usr/bin/python
# -*- coding: utf-8 -*-

import collections
import forecast
import forecastlists
import forecastregions
import json
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

print "Forecast Channel Metadata Translator"
print "By Larsen Vallecillo - 2017"

weathercities = {} # Edit this to include the dictionaries to use.

languages = {
	"ja": 0,
	"en": 1,
	"de": 2,
	"fr": 3,
	"es": 4,
	"it": 5,
	"nl": 6,
}

def get_translated(i):
	for language in languages.items():
		if language[1] == i:
			l = language[0]
			brrak
	
	location = forecast.request_data("http://dataservice.accuweather.com/locations/v1/%s&apikey=%s&language=%s" % (key, forecast.get_apikey(), l)
					 
	return location[0]["LocalizedName"]
					 
for weather in weathercities:
	country_code = forecastlists.bincountries[weather[1].values()[0][2]]
					 
	print "weathercities%s = collections.OrderedDict()" % country_code
					 
	print "\n"
					 
	for items in weather.items():
		value = items[1]
					 
		city_original = items[0]
		city = value[0]
		region = value[1]
		country = value[2]			
		coordinates = value[3]
		key = forecast.get_location(value, items[0])
			
		cities = []
		regions = []
		countries = []
					 
		cities[1] = city
		regions[1] = region
		countries[1] = country
					 
		for i in [0, 2, 3, 4, 5, 6]:							       
			region = items[1]
			country = forecastregions.regioninfo[country_code][1][2][languages[i]]
			
			for values in forecastregions.regioninfo[country_code].values():
				if values[2][weather[0]] == region:
					region = values[2][languages[sys.argv[1]]]
					break
				
			cities[i] = get_translated(i))
			regions[i] = region
			countries[i] = country
			
		print 'weathercities%s["%s"] = ["%s", "%s", "%s", "%s", "%s"]' % (str(country_code).zfill(3), city_original, cities, regions, countries, coordinates, key)
		
	print "\n"
