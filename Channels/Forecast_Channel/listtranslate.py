#!/usr/bin/python
# -*- coding: utf-8 -*-

import collections
import forecast
import forecastlists
import forecastregions
import json
import googlemaps
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

print "Forecast Channel Metadata Translator"
print "By Larsen Vallecillo - 2017"
		
if len(sys.argv) != 2:
	print "Usage: listtranslate.py <output language>"
	
print "import collections"

print "\n"

print "weathercities = collections.OrderedDict()"

print "\n"

weathercities = {} # Edit this to include the dictionaries to use. The key must be the language the dictionary is in, the value must be the dictionary.

languages = {
	"ja": 0,
	"en": 1,
	"de": 2,
	"fr": 3,
	"es": 4,
	"it": 5,
	"nl": 6,
}
	
for weather in weathercities.items():
	for items in weather[1].values():
		country_code = forecastlists.bincountries[weather[1].values()[0][2]]
		
		try:
			bincountry = forecastlists.bincountries[items[2]]
		except:
			bincountry = ""
		
		if bincountry == country_code:
			key = forecast.get_location(weather, items[0])
			
			for i in range(2, 7):
				location = forecast.request_data("http://dataservice.accuweather.com/locations/v1/%s&apikey=%s&language=%s" % (key, forecast.get_apikey(), languages[i])
													       
				region = items[1]
				country = forecastregions.regioninfo[country_code][1][2][languages[sys.argv[1]]]
			
				for values in forecastregions.regioninfo[country_code].values():
					if values[2][weather[0]] == region:
						region = values[2][languages[sys.argv[1]]]
						break
					
				coordinates = items[3]
			
				print 'weathercities%s_%s["%s"] = ["%s", "%s", "%s", "%s". "%s"]' % (str(country_code).zfill(3), str(languages[sys.argv[1]]), city, city, region, country, coordinates, key)
