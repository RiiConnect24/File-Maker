# Forecast Channel

Thanks for your interest in helping out with RiiConnect24's File Maker.

Please read on to learn how to add your own forecast city (and PR it to us).

## Files

### Scripts

+ forecast.py downloads the forecast from AccuWeather.
+ forecastlists.py has a list of the forecast cities that will be included.
+ forecastregions.py has region data for countries.

## How to Contribute

If you would like to add your own forecast city, here are some instructions.

We are not accepting new cities for these following countries:

+ Argentina
+ Brazil
+ Finland
+ France
+ Germany
+ Italy
+ Mexico
+ Portugal
+ United Kingdom
+ United States

Your city needs to be popular enough in order for it to be added. If it has a decent population, that's good.

To add a city, find the dictionary with the country code of the country you want to add a city for ([list of country codes are here](https://wiibrew.org/wiki/Country_Codes)) then make a dictionary entry. Make sure to fit it in the right place.

Then comes the entries in this order:

1. A list of the city names in 7 languages in this order: (Japanese, English, German, French, Spanish, Italian, Dutch)
1. A list of the region names in 7 languages in the same order. You can find this in forecastregions.py or from another value.
1. A list of the country names in 7 languages in the same order. You can also find this in forecastregions.py or from another value.
1. Coordinates. You can get the latitude and longitude of the city, and convert it to what the Wii uses with this Python code:

```python
def coord_decode(value):
	value = int(value,16)
	if value >= 0x8000: value -= 0x10000
	return value*0.0054931640625
```

Then comes the first zoom factor. You can put it as any value from 0x0-0x9, as it's only something trivial for how the cities appear on the Globe.
Put "030000" after that.
