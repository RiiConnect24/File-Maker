#!/usr/bin/python
# -*- coding: utf-8 -*-

from mtranslate import translate
import collections
import forecastlists
import forecastregions
import list
import googlemaps
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

print "Forecast Channel Metadata Translator"
print "By Larsen Vallecillo - 2017"

gmaps = googlemaps.Client(key="AIzaSyC8el52F4O5ifu10XA3DoQvm2NykAbw7FE")
		
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
			city = translate(items[0] + " city", sys.argv[1]).replace(" city", "")
			region = items[1]
			country = forecastregions.regioninfo[country_code][1][2][languages[sys.argv[1]]]
			
			for values in forecastregions.regioninfo[country_code].values():
				if values[2][weather[0]] == region:
					region = values[2][languages[sys.argv[1]]]
					break
					
			coordinates = items[3]
			
			print 'weathercities%s_%s["%s"] = ["%s", "%s", "%s", "%s"]' % (str(country_code).zfill(3), str(languages[sys.argv[1]]), city, city, region, country, coordinates)
