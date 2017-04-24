#!/usr/bin/python
# -*- coding: utf-8 -*-

import collections
import forecastlists
import forecastregions

weathercities = [] # Edit this to include the dictionaries to use.

for weather in weathercities:
	weathercity = collections.OrderedDict()
	
	for items in weather.values():
		country_code = forecastlists.bincountries[weather.values()[0][2]]
		
		try:
			bincountry = forecastlists.bincountries[items[2]]
		except:
			bincountry = ""
			
		if bincountry == country_code:
			weathercity[items[1] + " " + items[0]] = [items[0], items[1], items[2], items[3]]
	
	i = 0
	
	regiondata = forecastregions.regioninfo[forecastlists.bincountries[weather.values()[0][2]]]
	
	missing = []
	
	for region in regiondata:
		i += 1
		newregion = collections.OrderedDict()
		if i > 1:
			j = 0
			for items in weather.items():
				if items[1][1] == regiondata[region][2][1]:
					j += 1
					
					newregion[items[0]] = items[1]
					

			for weatherlist in sorted(newregion):
				print 'weathercities%s["%s"] = ["%s", "%s", "%s", "%s"]' % (str(country_code).zfill(3), newregion[weatherlist][0], newregion[weatherlist][0], newregion[weatherlist][1], newregion[weatherlist][2], newregion[weatherlist][3])
			
			if j == 0:
				missing.append(regiondata[region][2][1])
			
	for miss in missing:
		print "A city for the %s region could not be found, please add one." % miss
	
	print "\n"
