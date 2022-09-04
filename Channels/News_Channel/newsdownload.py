#!/usr/bin/python
# -*- coding: utf-8 -*-

# ===========================================================================
# NEWS CHANNEL GENERATION SCRIPT
# AUTHORS: LARSEN VALLECILLO
# ****************************************************************************
# Copyright (c) 2015-2022 RiiConnect24, and its (Lead) Developers
# ===========================================================================

import binascii
import collections
import json
import locale
import random
import re
import sys
import textwrap
import time
from html.parser import unescape
from io import BytesIO, StringIO
from datetime import datetime, date

import feedparser
import ftfy
import googlemaps
import newspaper
import requests
import zlib
from PIL import Image
from bs4 import BeautifulSoup
from unidecode import unidecode

from utils import setup_log, log, u8, u16, u32, u32_littleendian, s16
import importlib

with open("./Channels/News_Channel/config.json", "rb") as f:
    config = json.load(f)

if config["production"]:
    setup_log(config["sentry_url"], True)

# define information about news sources

sources = {
    # urls string argument is category key
    # reference parse_feed
    "ap_english": {
        "name": "AP",
        "url": "https://afs-prod.appspot.com/api/v2/feed/tag?tags=%s",
        "lang": "en",
        "cat": {
            "us-news": "national",
            "world-news": "world",
            "oddities": "oddities",
            "technology": "technology",
            "science": "science",
            "health": "science",
            "sports": "sports",
            "entertainment": "entertainment",
            "business": "business",
        },
    },
    "ap_spanish": {
        "name": "AP",
        "url": "https://afs-prod.appspot.com/api/v2/feed/tag?tags=%s",
        "lang": "es",
        "cat": {
            "apf-Noticias": "general",
            "apf-Finanzas": "finance",
            "apf-Deportes": "sports",
            "apf-Entretenimiento": "shows",
        },
    },
    "ap_canada": {
        "name": "AP",
        "url": "https://afs-prod.appspot.com/api/v2/feed/tag?tags=%s",
        "url2": "https://www.thestar.com/content/thestar/feed.RSSManagerServlet.articles.news.canada.rss",
        "lang": "en",
        "cat": {
            "canada": ["canada_", "canada"],
            "world-news": "world",
            "oddities": "oddities",
            "technology": "technology",
            "science": "science",
            "health": "science",
            "sports": "sports",
            "entertainment": "entertainment",
            "business": "business",
        },
    },
    "ap_australia": {
        "name": "AP",
        "url": "https://afs-prod.appspot.com/api/v2/feed/tag?tags=%s",
        "lang": "en",
        "cat": {
            "national": ["australia", "new-zealand"],
            "world-news": "world",
            "oddities": "oddities",
            "technology": "technology",
            "science": "science",
            "health": "science",
            "sports": "sports",
            "entertainment": "entertainment",
            "business": "business",
        },
    },
    "reuters_europe_english": {
        "name": "Reuters",
        "url": "https://wireapi.reuters.com/v7/feed/rapp/uk/tabbar/feeds/%s",
        "lang": "en",
        "cat": {
            "world": "world",
            "uk": "uk",
            "science": "science",
            "tech": "technology",
            "entertainment": "entertainment",
            "sports": "sports",
            "lifestyle": "lifestyle",
            "business": "business",
        },
    },
    "afp_french": {
        "name": "AFP_French",
        "url": "https://www.lepoint.fr/tags/rss/AFP.xml",
        "url2": "https://www.lepoint.fr/24h-infos/rss.xml",
        "lang": "fr",
        "cat": {
            "monde": "world",
            "sport": "sports",
            "societe": "society",
            "culture": "culture",
            "economie": "economy",
            "politique": "politics",
        },
    },
    "afp_german": {
        "name": "AFP_German",
        "url": "https://tah.de/%s",
        "lang": "de",
        "cat": {
            "politik": "politics",
            "wirtschaft": "economy",
            "medizingesundheit": "health",
            "weltimspiegel": "panorama",
            "sport": "sports",
        },
    },
    "afp_spanish": {
        "name": "AFP_Spanish",
        "url": "https://www.rfi.fr/es/más-noticias/rss",
        "lang": "es",
        "cat": {
            "mundo": "world",
            "cultura": "cultura",
            "sociedad": "society",
            "economía": "economy",
            "deportes": "sports",
            "gente": "people",
        },
    },
    "ansa_italian": {
        "name": "ANSA",
        "url": "http://ansa.it/sito/notizie/%s/%s_rss.xml",
        "url2": "http://ansa.it/%s/notizie/%s_rss.xml",
        "lang": "it",
        "cat": {
            "mondo": "world",
            "sport": "sports",
            "economia": "economy",
            "tecnologia": "technology",
            # yeah this is a mess, shame on ANSA for seemingly not having an all-Italian feed
            "italy": [
                "abruzzo",
                "basilicata",
                "calabria",
                "campania",
                "emiliaromagna",
                "friuliveneziagiulia",
                "lazio",
                "liguria",
                "lombardia",
                "marche",
                "molise",
                "piemonte",
                "puglia",
                "sardegna",
                "sicilia",
                "toscana",
                "trentino",
                "umbria",
                "valledaosta",
                "veneto",
            ],
        },
    },
    "anp_dutch": {
        "name": "ANP",
        "url": "https://nieuws.nl/%s/feed/",
        "lang": "nl",
        "cat": {
            "algemeen": "general",
            "nl12": "national",
            "economie": "economy",
            "sport": "sports",
            "entertainment": "entertainment",
            "lifestyle": "lifestyle",
        },
    },
    "reuters_japanese": {
        "name": "Reuters",
        "url": "https://wireapi.reuters.com/v7/feed/rapp/jp/tabbar/feeds/%s",
        "lang": "ja",
        "cat": {
            "world": "world",
            "business": "business",
            "sports": "sports",
            "technology": "technology",
            "entertainment": "entertainment",
        },
    },
}

# encode the text


def enc(text):
    if text:
        return ftfy.fix_encoding(unescape(text)).encode("utf-16be", "replace")


# resize the image and strip metadata (to make the image size smaller)


def shrink_image(
    data, resize, source, session
):  # Resize the image and strip metadata (to make the image size smaller).
    if not data or data == "":
        return None

    try:
        if source == "AFP_Spanish":
            picture = session.get(data, headers={"User-Agent": "Python"}).content
        else:
            picture = session.get(data).content
    except requests.exceptions.ReadTimeout:
        return None
    except requests.exceptions.MissingSchema:
        return None

    try:
        image = Image.open(BytesIO(picture))
    except IOError:
        return None

    maxsize = (200, 200)

    # if for some reason the image has an alpha channel (probably a PNG), fill the background with white

    image = image.convert("RGB")

    if resize:
        image.thumbnail(maxsize, Image.ANTIALIAS)

    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)

    buffer = BytesIO()
    image_without_exif.save(buffer, format="jpeg")

    return buffer.getvalue()


# these are common locations for cities so we don't have to waste API calls if they're used a lot

cities = {}

cities["AMSTERDAM"] = ["253d0379", "Amsterdam"]
cities["ATLANTA"] = ["17ffc3fe", "Atlanta"]
cities["BAGHDAD"] = ["17b71f95", "Baghdad"]
cities["BALTIMORE"] = ["1bf0c986", "Baltimore"]
cities["BANGKOK"] = ["09c7477a", "Bangkok"]
cities["BEIJING"] = ["1c6252cc", "Beijing"]
cities["BEIRUT"] = ["1818193e", "Beirut"]
cities["BERLIN"] = ["25590988", "Berlin"]
cities["BOSTON"] = ["1e1fcd78", "Boston"]
cities["BRUSSELS"] = ["2427031b", "Brussels"]
cities["CAIRO"] = ["155e1638", "Cairo"]
cities["CHICAGO"] = ["1dc2c1ac", "Chicago"]
cities["CINCINNATI"] = ["1bd9c3f2", "Cincinnati"]
cities["CLEVELAND"] = ["1d82c5e8", "Cleveland"]
cities["DALLAS"] = ["1750bb2b", "Dallas"]
cities["DENVER"] = ["1c42b559", "Denver"]
cities["DETROIT"] = ["1e1ac4f2", "Detroit"]
cities["DJIBOUTI"] = ["083f1eaf", "Djibouti"]
cities["DUBLIN"] = ["25e2fb8d", "Dublin"]
cities["GENEVA"] = ["20d0045c", "Geneva"]
cities["GIBRALTAR"] = ["19b3fc32", "Gibraltar"]
cities["GUATEMALA CITY"] = ["0a61bfb5", "Guatemala City"]
cities["HAVANA"] = ["1076c571", "Havana"]
cities["HELSINKI"] = ["2ac911bb", "Helsinki"]
cities["HONG KONG"] = ["0ff95147", "Hong Kong"]
cities["HONOLULU"] = ["0f268fbf", "Honolulu"]
cities["HOUSTON"] = ["152abc30", "Houston"]
cities["INDIANAPOLIS"] = ["1c47c2bc", "Indianapolis"]
cities["ISLAMABAD"] = ["17f63407", "Islamabad"]
cities["ISTANBUL"] = ["1d32149f", "Istanbul"]
cities["JERUSALEM"] = ["1696190a", "Jerusalem"]
cities["JOHANNESBURG"] = ["ed6913f2", "Johannesburg"]
cities["KUWAIT CITY"] = ["14e2221e", "Kuwait City"]
cities["LAS VEGAS"] = ["19b9ae21", "Las Vegas"]
cities["LONDON"] = ["24a0ffeb", "London"]
cities["LOS ANGELES"] = ["1837abeb", "Los Angeles"]
cities["LUXEMBOURG"] = ["2347045b", "Luxembourg"]
cities["MACAU"] = ["0fcc50c8", "Macau"]
cities["MADRID"] = ["1cb3fd62", "Madrid"]
cities["MEXICO CITY"] = ["0dd1b981", "Mexico City"]
cities["MIAMI"] = ["1253c6fa", "Miami"]
cities["MILAN"] = ["20550688", "Milan"]
cities["MILWAUKEE"] = ["1e9ac17e", "Milwaukee"]
cities["MINNEAPOLIS"] = ["1ffcbdae", "Minneapolis"]
cities["MONACO"] = ["1f160549", "Monaco"]
cities["MONTREAL"] = ["2051cbbf", "Montréal"]
cities["MOSCOW"] = ["27a81abf", "Moscow"]
cities["MUNICH"] = ["223a0837", "Munich"]
cities["NEW DELHI"] = ["145636e5", "New Delhi"]
cities["NEW ORLEANS"] = ["154dbff3", "New Orleans"]
cities["NEW YORK"] = ["1cf3cb60", "New York"]
cities["OKLAHOMA CITY"] = ["1938baa8", "Oklahoma City"]
cities["PANAMA CITY"] = ["0664c787", "Panama City"]
cities["PARIS"] = ["22bd01ab", "Paris"]
cities["PHILADELPHIA"] = ["1c69ca8d", "Philadelphia"]
cities["PHOENIX"] = ["17c9b04e", "Phoenix"]
cities["PITTSBURGH"] = ["1cc1c71e", "Pittsburgh"]
cities["PRAGUE"] = ["239b0a43", "Prague"]
cities["QUEBEC CITY"] = ["214ccd6b", "Quebec City"]
cities["RIO DE JANEIRO"] = ["efb8e142", "Rio de Janeiro"]
cities["ROME"] = ["1dca08e1", "Rome"]
cities["SALT LAKE CITY"] = ["1cfcb06f", "Salt Lake City"]
cities["SAN ANTONIO"] = ["14ecb9f6", "San Antonio"]
cities["SAN DIEGO"] = ["1743acb1", "San Diego"]
cities["SAN FRANCISCO"] = ["1adca8f3", "San Francisco"]
cities["SAN MARINO"] = ["1f3d08d7", "San Marino"]
cities["SAO PAULO"] = ["ef44deda", "São Paulo"]
cities["SEATTLE"] = ["21daa903", "Seattle"]
cities["SHANGHAI"] = ["16385661", "Shanghai"]
cities["SINGAPORE"] = ["00eb49da", "Singapore"]
cities["ST. LOUIS"] = ["1b77bfdc", "St. Louis"]
cities["STOCKHOLM"] = ["2a200cd5", "Stockholm"]
cities["SYDNEY"] = ["e7e76b8c", "Sydney"]
cities["TOKYO"] = ["19606363", "Tokyo"]
cities["TORONTO"] = ["1f13c787", "Toronto"]
cities["UNITED NATIONS"] = [
    "1cf0cb78",
    "United Nations",
]  # maps to the UN offices in New York
cities["VATICAN CITY"] = ["1dcc08db", "Vatican City"]
cities["VIENNA"] = ["223d0ba0", "Vienna"]
cities["WASHINGTON"] = ["1ba8c938", "Washington D.C."]
cities["ZURICH"] = ["21a40610", "Zürich"]


def locations_download(
    language_code, data
):  # using Google Maps API is so much better than the crap Nintendo used for say, AP news.
    locations = {}
    gmaps = googlemaps.Client(key="AIzaSyAC4YJleigYdZe3Bkw7QTcFUxilDL8BAeI")

    languages = {  # corresponds to the Wii's language codes
        0: "ja",
        1: "en",
        2: "de",
        3: "fr",
        4: "es",
        5: "it",
        6: "nl",
    }

    for keys, values in list(data.items()):
        location = values[7]

        if location and location != "":
            if location not in locations:
                locations[location] = [None, None, []]

            locations[location][2].append(keys)

    for name in list(locations.keys()):
        if name == "":
            continue

        print(name)

        coordinates = None

        if name not in cities:
            try:
                read = gmaps.geocode(name, language=languages[language_code])
                loc_name = read[0]["address_components"][0]["long_name"]
                for loc in read[0]["address_components"]:
                    if "locality" in loc["types"]:
                        loc_name = loc["long_name"]

                loc_name = enc(loc_name)

                """Not doing anything with these."""

                country = u8(0)
                region = u8(0)
                location = u16(0)
                zoom_factor = u32_littleendian(
                    6
                )  # Nintendo used the value of 3 for states and countries but we probably don't have any articles that are just states or countries

                coordinates = (
                    s16(int(read[0]["geometry"]["location"]["lat"] / (360 / 65536)))
                    + s16(int(read[0]["geometry"]["location"]["lng"] / (360 / 65536)))
                    + country
                    + region
                    + location
                    + zoom_factor
                )  # latitude and longitude is divided by the value of 360 (degrees of a full circle) divided by the max int for a 16-bit int
            except Exception as e:
                ex = "There was a error downloading the location data - line {}: {}".format(
                    sys.exc_info()[-1].tb_lineno, str(e)
                )
                print(ex)
                log(ex, "INFO")

        else:
            coordinates = binascii.unhexlify(cities[name][0] + "0000000006000000")
            loc_name = enc(cities[name][1])

        if locations[name][0] is None and coordinates is not None:
            locations[name][0] = coordinates
        else:
            del locations[name]
            continue

        if locations[name][1] is None:
            locations[name][1] = loc_name

    return locations


# download the news


class News:
    def __init__(self, source):
        self.source = source
        self.sourceinfo = sources[self.source]
        self.url = self.sourceinfo["url"]
        self.language = self.sourceinfo["lang"]
        self.newsdata = {}
        self.headlines = []

        self.source = self.sourceinfo["name"]

        self.feed()

        print("\n")

    def __dict__(self):
        return self.newsdata

    def feed(self):
        print("Downloading News from {}...\n".format(self.source))

        i = 0

        for key, value in list(self.sourceinfo["cat"].items()):
            if isinstance(value, list):
                for v in random.sample(
                    value, len(value)
                ):  # reverse and mix up the list
                    i = self.parse_feed(v, key, i)
            else:
                i = self.parse_feed(key, value, i)

    def parse_feed(self, key, value, i):
        if self.source == "AP" or self.source == "Reuters":
            try:
                if key == "canada_":
                    feed = feedparser.parse(requests.get(self.sourceinfo["url2"]).text)
            except:
                pass

            try:
                if key != "canada_":
                    news_url = self.url % key

                    feed = requests.get(
                        news_url
                    ).json()  # we use AP's API to download their news, it's epic and it uses JSON
            except:
                return i
        elif self.source == "AFP_French" or self.source == "ANP":
            feed = feedparser.parse(self.url)
        elif self.source == "AFP_German":
            webpage = requests.get(self.url % key).content
            soup = BeautifulSoup(webpage, "lxml")
        elif self.source == "AFP_Spanish":
            feed = feedparser.parse(
                requests.get(self.url, headers={"User-Agent": "Python"}).text
            )
        elif self.source == "ANSA" and value == "italy":
            feed = feedparser.parse(self.sourceinfo["url2"] % (key, key))
        elif self.source == "ANSA":
            feed = feedparser.parse(self.url % (key, key))
        else:
            feed = feedparser.parse(self.url % key)

        j = 0

        if self.source == "AP" and key != "canada_":
            entries = feed["cards"]
        elif self.source == "Reuters":
            entries = []
            entries2 = feed["wireitems"]
            for entry in entries2:
                try:
                    entry = entry["templates"][1]
                    if entry["type"] == "story":
                        entries.append(entry)
                    elif entry["type"] == "headlines":
                        for entry2 in entry["headlines"]:
                            entries.append(entry2)
                except:
                    continue
        elif self.source == "AFP_French":
            entries = feed.entries + feedparser.parse(self.sourceinfo["url2"]).entries
        elif self.source == "AFP_German":
            entries = soup.find_all("div", {"class": "article articletype-0 mb-4 mt-5"})
        else:
            entries = feed.entries

        for entry in entries:
            try:
                if self.source == "AP" and key != "canada_":
                    try:
                        entry = entry["contents"][0]
                    except:
                        continue
                elif self.source == "AP" and key == "canada_":
                    if entry["author"] != "The Canadian Press":
                        continue

                current_time = int(
                    (time.mktime(datetime.utcnow().timetuple()) - 946684800) / 60
                )

                if self.source == "AP" and key != "canada_":
                    update = time.strptime(entry["updated"], "%Y-%m-%d %H:%M:%S")
                elif self.source == "Reuters":
                    update = time.strptime(
                        entry["story"]["updated_at"], "%Y-%m-%dT%H:%M:%SZ"
                    )
                elif self.source == "AFP_German":
                    locale.setlocale(locale.LC_ALL, "de_DE")
                    update = time.strptime(
                        entry.find("i").text.strip(), "%A, %d. %B %Y %H:%M"
                    )
                    locale.setlocale(locale.LC_ALL, "en_US")
                else:
                    update = entry["updated_parsed"]

                updated_time = int((time.mktime(update) - 946684800) / 60)

                if self.source == "AFP_German" and current_time - updated_time < 0:
                    updated_time -= 120
                elif self.source == "AFP_French" and current_time - updated_time < 0:
                    updated_time -= 180

                if (
                    current_time - updated_time < 60
                ):  # if it's a new article since the last hour
                    i += 1
                    j += 1

                    if (
                        i > 25
                    ):  # in case we have too many articles, we don't want the news file to get too big, there's a limit
                        break

                    if self.source == "AFP_French" or self.source == "ANP_Dutch":
                        if key not in entry["link"]:
                            continue
                    elif self.source == "AFP_Spanish":
                        if key not in entry["category"].lower():
                            continue
                    elif self.source == "NU.nl" and entry["author"] == "ANP":
                        self.source = "ANP"

                    if self.source == "AP" and key != "canada_":
                        title = entry["headline"]
                    elif self.source == "Reuters":
                        title = entry["story"]["hed"]
                    elif self.source == "AFP_German":
                        title = entry.find("a")["title"]
                    else:
                        title = entry["title"]

                    if title not in self.headlines:
                        self.headlines.append(title)

                        print(title)

                        if self.source == "AP" and key != "canada_":
                            entry_url = json.dumps(entry)
                        elif self.source == "Reuters":
                            entry_url = (
                                self.url[:30] + entry["template_action"]["api_path"]
                            )
                        elif self.source == "AFP_German":
                            entry_url = "https://tah.de" + entry.find("a")["href"]
                        else:
                            entry_url = entry["link"]

                        if key == "canada_":
                            self.source = "CanadianPress"

                        downloaded_news = Parse(
                            entry_url, self.source, updated_time, title, self.language
                        ).get_news()

                        if key == "canada_":
                            self.source = "AP"

                        if downloaded_news:
                            self.newsdata[value + str(j)] = downloaded_news
            except Exception as e:
                ex = "Failed to parse feed - line {}: {}".format(
                    sys.exc_info()[-1].tb_lineno, str(e)
                )
                print(ex)
                log(ex, "INFO")
                continue

        return i


class Parse(News):
    def __init__(
        self,
        url,
        source,
        updated_time,
        headline,
        language,
        article=None,
        picture=None,
        credits=None,
        caption=None,
        location=None,
        resize=None,
        html=None,
        soup=None,
    ):
        self.url = url
        self.source = source
        self.updated_time = updated_time
        self.headline = headline
        self.language = language
        self.article = article
        self.picture = picture
        self.credits = credits
        self.caption = caption
        self.location = location
        self.resize = resize
        self.html = html
        self.soup = soup
        self.session = requests.Session()

        if self.source != "AP" and self.source != "Reuters":
            init = self.newspaper_init()
            if init == []:
                return None

        {
            "AP": self.parse_ap,
            "CanadianPress": self.parse_canadian_press,
            "Reuters": self.parse_reuters,
            "AFP_French": self.parse_afp_french,
            "AFP_German": self.parse_afp_german,
            "AFP_Spanish": self.parse_afp_spanish,
            "ANSA": self.parse_ansa,
            "ANP": self.parse_anp,
        }[self.source]()

        self.get_news()

    def get_news(self):
        if self.headline == "" or self.headline is None:
            return []
        elif self.article == "" or self.article is None:
            return []
        try:
            _ = enc(self.headline).replace(b"\n", b"").decode("utf-16be")
            _ = enc(self.article).replace(b"\n", b"").decode("utf-16be")
        except:
            return []
        return [
            u32(self.updated_time),
            u32(self.updated_time),
            enc(self.article),
            enc(self.headline),
            shrink_image(self.picture, self.resize, self.source, self.session),
            enc(self.credits),
            enc(self.caption),
            self.location,
            self.source,
        ]

    def newspaper_init(self):
        self.newsdata = newspaper.Article(self.url, language=self.language)
        self.newsdata.download()
        try:
            self.newsdata.parse()
        except newspaper.article.ArticleException:  # trying again
            self.newsdata.parse()
        except newspaper.article.ArticleException:
            return []

        self.article = self.newsdata.text
        self.picture = self.newsdata.top_image
        self.html = self.newsdata.html
        self.soup = BeautifulSoup(self.html, "lxml")

    def parse_ap(self):
        try:
            self.newsdata = json.loads(self.url)
        except:
            self.article = None
            return

        if self.newsdata["localMemberName"] is not None:
            self.article = None
            return

        if self.newsdata["localLinkUrl"]:
            if "apnews" not in self.newsdata["localLinkUrl"]:
                self.article = None
                return
        else:
            self.article = None
            return

        try:
            self.article = newspaper.fulltext(
                self.newsdata["storyHTML"], language=self.language
            )
        except AttributeError:
            self.article = None
            return

        self.article = self.article.replace(
            "\n\nYour browser does not support the iframe HTML tag. Try viewing this in a modern browser like Chrome, Safari, Firefox or Internet Explorer 9 or later.",
            "",
        )

        self.article = re.sub(
            "\n\nHub peek embed ((.*)) - Compressed layout ((.*))", "", self.article
        )

        if self.article[-2:] == "\n":
            self.article = self.article[:-2]

        if self.newsdata["bylines"] != "" and self.newsdata["bylines"] != None:
            self.article += "\n\n" + self.newsdata["bylines"]

        if (
            "storyHTML" in self.article
        ):  # get rid of broken articles that have the headline and article both matching
            self.article = None
            return

        if self.newsdata["mediaCount"] > 0 and self.newsdata["media"] != []:
            if self.newsdata["media"][0]["imageMimeType"] == "image/jpeg":
                self.resize = True

                self.picture = (
                    self.newsdata["media"][0]["gcsBaseUrl"]
                    + "400"
                    + self.newsdata["media"][0]["imageFileExtension"]
                )

                self.caption = newspaper.fulltext(
                    self.newsdata["media"][0]["caption"] + "<p></p>",
                    language=self.language,
                )

                self.credits = self.caption.rsplit("(")[-1][:-1]
            else:
                self.picture = None
        else:
            self.picture = None

        if " (AP)" in self.article:
            self.location = (
                self.article.split(" (AP)")[0].split("\u2014")[0].split("\n")[-1]
            )
        elif "Live Updates" in self.headline:
            self.location = self.article.split(" \u2014")[0]

    def parse_canadian_press(self):
        self.article = self.article.replace("\n\nRead more about:", "").replace(
            "\n\nSHARE:", ""
        )

        self.resize = True

        self.location = self.article.split(" - ")[0] + ", Canada"

    def parse_reuters(self):
        try:
            self.newsdata = self.session.get(self.url).json()["wireitems"][0][
                "templates"
            ][0]["story"]

            self.article = newspaper.fulltext(
                self.newsdata["body"], language=self.language
            )
        except Exception as e:
            print(e)
            return []

        try:
            self.caption = self.newsdata["images"][0]["caption"]

            self.picture = self.newsdata["images"][0]["url"] + "&w=200.0"

            self.resize = False
        except:
            pass

        try:
            location = self.newsdata["dateline"]

            if " (Reuters)" in location:
                self.location = location.split(" (Reuters)")[0].split("/")[0]
            elif "［" in self.article and "］" in self.article:
                self.location = self.article.split("［")[1].split("］")[0].split(" ")[0]

            if self.location == "":
                self.location = None
        except:
            pass

    def parse_afp_french(self):
        try:
            self.resize = True
            self.caption = self.soup.find("figcaption", {"class": "art-caption"}).text
        except AttributeError:
            pass

        # the location is at the end of the article

        try:
            if "(AFP)" in self.article:
                buf = StringIO(self.article)
                line = buf.readlines()[-1]
                buf = StringIO(self.article)
                self.location = line.strip()[22:-19]
                self.article = line.strip()[22:-10] + buf.readlines()[1:].replace(
                    "\n\n" + line, ""
                )
        except AttributeError:
            pass

    def parse_afp_german(self):
        self.location = self.soup.find("span", {"itemprop": "name"}).get_text()

        if "(SID)" in self.location:
            self.source = "SID"
            self.location = self.location.split(" (SID)")[0]
            self.article = self.location + " (SID) " + self.article
        elif "(AFP)" in self.location:
            self.location = self.location.split(" (AFP)")[0]
            self.article = self.location + " (AFP) " + self.article

        try:
            self.resize = True
            self.caption = (
                self.soup.find(
                    "p",
                    {"class": "news-img-caption text-small text-white p-2 mb-0 w-100"},
                )
                .get_text()
                .strip()
                .split(" - (")[0]
            )
            self.credits = (
                self.soup.find(
                    "p",
                    {"class": "news-img-caption text-small text-white p-2 mb-0 w-100"},
                )
                .get_text()
                .strip()
                .split("(")[1]
                .split(")")[0]
                .split(" / SID")[0]
                .split(" / AFP")[0]
            )
        except AttributeError:
            pass

    def parse_afp_spanish(self):
        if "(AFP)" not in self.article:
            return

        for i in range(1, 10):
            self.article = self.article.replace("\n\n#photo" + str(i), "")

        self.article = self.article.replace(
            "\n\n© " + str(date.today().year) + " AFP", ""
        )

        try:
            self.resize = True
            self.credits = self.soup.find_all("span", {"class": "a-media-legend"})[
                1
            ].get_text()
            self.caption = self.soup.find_all("span", {"class": "a-media-legend"})[
                0
            ].get_text()
        except AttributeError:
            pass

        self.location = self.article.split(" (AFP)")[0].split("\n\n")[1]

    def parse_ansa(self):
        try:
            self.resize = True
            self.credits = (
                self.soup.find("div", {"class": "news-caption hidden-phone"})
                .find("em")
                .text
            )
        except AttributeError:
            pass

        try:
            self.location = self.soup.find(
                "span", {"itemprop": "dateline"}, {"class": "location"}
            ).text
        except AttributeError:
            pass

    def parse_anp(self):
        try:
            self.resize = True
            self.credits = self.soup.find("div", {"class": "credits"}).text
        except AttributeError:
            pass

        try:
            self.location = self.soup.find("meta", {"property": "og:description"})[
                "content"
            ].split(" (ANP) - ")[0]
            self.article = self.location + " (ANP) - " + self.article
        except:
            pass
