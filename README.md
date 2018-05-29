# File-Maker
[![License](https://img.shields.io/github/license/riiconnect24/file-maker.svg?style=flat-square)](http://www.gnu.org/licenses/agpl-3.0)
![Production List](https://img.shields.io/discord/206934458954153984.svg?style=flat-square)

These scripts will create static data files for these Wii Channels:

- Everybody Votes Channel
- Forecast Channel
- News Channel

These files are downloaded on the Wii, and they are important as they contain forecast data, news data, etc. that the Channel displays.

## Services and Modules

We use the following services for this project:

- [Datadog](https:/datadoghq.com/) for analytics.
- [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding/intro) to get location coordinates. (for News Channel)
- [MySQL](https://www.mysql.com/) to hold votes and suggestions. (for Everybody Votes Channel)
- [Sentry](https://sentry.io/) for error logging.
- Webhooks to log when a script has been ran.

Here are some notable Python modules used in the project:

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing.
- [ElementTree](https://docs.python.org/2/library/xml.etree.elementtree.html) to parse XML.
- [feedparser](https://pypi.python.org/pypi/feedparser) to parse RSS feeds.
- [newspaper](http://newspaper.readthedocs.io/en/latest/) for article scraping.
- [requests](http://docs.python-requests.org/en/master/) for various HTTP requests.
- [rsa](https://pypi.python.org/pypi/rsa) to create an RSA signed SHA-1 (that the Wii verifies downloaded files with).

[AccuWeather](https://accuweather.com/) is used as the weather source for the Forecast Channel. For a list of news sources we use for the News Channel, [refer to this webpage](https://rc24.xyz/services/news.html).

All files are LZ10 compressed. We use `lzss` from the set of [Nintendo DS/GBA compressors by CUE](http://www.romhacking.net/utilities/826/), because it can compress the files pretty fast.

If you want to know the format of the files used by the Channels, you can [look at our Kaitais](https://github.com/RiiConnect24/Kaitai-Files), check the wiki, or look at the code.

## Installing Requirements

These scripts run on Python 3.6.5.

Just run `pip install -r requirements.txt` in the root folder and it'll install. You might have to run as `sudo`.

It's required to have a `config.json` for each Channel in the `Channels` folder. Fill out `config.json.template` for the Channels you want to run this script for.

Run the scripts as modules, e.g. `python -m Channels.Forecast_Channel.forecast`.
