# File-Maker
[![License](https://img.shields.io/github/license/riiconnect24/file-maker.svg?style=flat-square)](http://www.gnu.org/licenses/agpl-3.0)
![Discord](https://img.shields.io/discord/206934458954153984.svg?style=flat-square)

These scripts will create static data files for these Wii Channels:

- Everybody Votes Channel
- Forecast Channel
- News Channel
- Nintendo Channel
- Check Mii Out Channel/ Mii Contest Channel

These files are downloaded on the Wii, and contain news, weather info, etc that the Channel(s) display, as well as influencing some games' environments.

## Services and Modules

We use the following services for this project:

- [Datadog](https:/datadoghq.com/) for analytics.
- For News Channel, [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding/intro) to get location coordinates.
- For Everybody Votes Channel, [MySQL](https://www.mysql.com/) to hold votes and suggestions.
- [Sentry](https://sentry.io/) for error logging.
- Webhooks to log when a script has been ran.

Some notable Python modules used in the project are:

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing.
- [ElementTree](https://docs.python.org/2/library/xml.etree.elementtree.html) to parse XML.
- [feedparser](https://pypi.python.org/pypi/feedparser) to parse RSS feeds.
- [newspaper](http://newspaper.readthedocs.io/en/latest/) for article scraping.
- [requests](http://docs.python-requests.org/en/master/) for various HTTP requests.
- [rsa](https://pypi.python.org/pypi/rsa) to create an RSA signed SHA-1 (that the Wii verifies downloaded files with).

[AccuWeather](https://accuweather.com/) is used as the weather source for the Forecast Channel. For a list of news sources we use for the News Channel, [refer to this webpage](https://rc24.xyz/services/news.html).

All files are LZ10 compressed; we use `lzss` from the set of [Nintendo DS/GBA compressors by CUE](http://www.romhacking.net/utilities/826/), because it can compress the files quite fast, which is desirable for our usage.

If you want to know the format of the files used by the Channels, you can [look at our Kaitais](https://github.com/RiiConnect24/Kaitai-Files), check the wiki, or look at the code.

## Installing Requirements

These scripts run on Python 2.

Just run `pip install -r requirements.txt` in the root folder and it'll install. You might have to run as `sudo` due to permissions.

It's required to have a `config.json` for each Channel in the `Channels` folder. Fill out `config.json.template` for the Channels you want to run this script for, and rename it to `config.json`.

Run the scripts as modules, e.g. `python -m Channels.Forecast_Channel.forecast`.
