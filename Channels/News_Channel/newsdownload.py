#!/usr/bin/python
# -*- coding: utf-8 -*-

# ===========================================================================
# NEWS CHANNEL GENERATION SCRIPT
# AUTHORS: LARSEN VALLECILLO
# ****************************************************************************
# Copyright (c) 2015-2020 RiiConnect24, and its (Lead) Developers
# ===========================================================================

import binascii
import collections
import json
import random
import sys
import textwrap
import time
from html.parser import HTMLParser
from io import BytesIO, StringIO
from datetime import datetime

import feedparser
import ftfy
import googlemaps
import newspaper
import requests
from PIL import Image
from bs4 import BeautifulSoup
from unidecode import unidecode

from utils import setup_log, log, u8, u16, u32, u32_littleendian, s16
import importlib

with open("./Channels/News_Channel/config.json", "rb") as f:
    config = json.load(f)

if config["production"]: setup_log(config["sentry_url"], True)

# define information about news sources

sources = {
    # urls string argument is category key
    # reference parse_feed

    "ap_english": {
        "name": "AP",
        "url": "https://afs-prod.appspot.com/api/v2/feed/tag?tags=%s",
        "lang": "en",
        "cat": collections.OrderedDict([
            ("apf-usnews", "national"),
            ("apf-intlnews", "world"),
            ("apf-sports", "sports"),
            ("apf-entertainment", "entertainment"),
            ("apf-business", "business"),
            ("apf-science", "science"),
            ("apf-Health", "science"),
            ("apf-technology", "technology"),
            ("apf-oddities", "oddities")
        ])
    },
    "ap_spanish": {
        "name": "AP",
        "url": "https://afs-prod.appspot.com/api/v2/feed/tag?tags=%s",
        "lang": "es",
        "cat": collections.OrderedDict([
            ("apf-Noticias", "general"),
            ("apf-Finanzas", "finance"),
            ("apf-Deportes", "sports"),
            ("apf-Entretenimiento", "shows")
        ])
    },
    "reuters_europe_english": {
        "name": "Reuters",
        "url": "http://feeds.reuters.com/reuters/%s.rss",
        "lang": "en",
        "cat": collections.OrderedDict([
            ("UKWorldNews", "world"),
            ("UKdomesticNews", "uk"),
            ("UKHealthNews", "health"),
            ("UKScienceNews", "science"),
            ("technology", "technology"),
            ("UKEntertainment", "entertainment"),
            ("UKSportsNews", "sports"),
            ("lifestyle", "lifestyle")
        ])
    },
    "afp_french": {
        "name": "AFP_French",
        "url": "https://www.lepoint.fr/24h-infos/rss.xml",
        "lang": "fr",
        "cat": collections.OrderedDict([
            ("monde", "world"),
            ("sport", "sports"),
            ("societe", "society"),
            ("culture", "culture"),
            ("economie", "economy"),
            ("politique", "politics")
        ])
    },
    "dtoday_german": {
        "name": "AFP",
        "url": "http://www.dtoday.de/feed/%s.xml",
        "lang": "de",
        "cat": collections.OrderedDict([
            ("16-nachrichten-ueberregional", "world"),
            ("12-panorama-ueberregional", "panorama"),
            ("14-politik-ueberregional", "politics"),
            ("13-wirtschaft-ueberregional", "economy"),
            ("15-sport-ueberregional", "sports")
        ])
    },
    "ansa_italian": {
        "name": "ANSA",
        "url": "http://ansa.it/sito/notizie/%s/%s_rss.xml",
        "url2": "http://ansa.it/%s/notizie/%s_rss.xml",
        "lang": "it",
        "cat": collections.OrderedDict([
            ("mondo", "world"),
            ("sport", "sports"),
            ("economia", "economy"),
            ("tecnologia", "technology"),
            # yeah this is a mess, shame on ANSA for seemingly not having an all-Italian feed
            ("italy", ["abruzzo", "basilicata", "calabria", "campania", "emiliaromagna", "friuliveneziagiulia", "lazio", "liguria", "lombardia",
              "marche", "molise", "piemonte", "puglia", "sardegna", "sicilia", "toscana", "trentino", "umbria", "valledaosta", "veneto"])
        ])
    },
    "nu_dutch": {
        "name": "NU.nl",
        "url": "https://www.nu.nl/rss/%s",
        "lang": "nl",
        "cat": collections.OrderedDict([
            ("Algemeen", "algemeen"),
            ("Economie", "economy"),
            ("Sport", "sports"),
            ("Tech", "technology"),
            ("Entertainment", "entertainment"),
            ("Lifestyle", "lifestyle"),
            ("Opmerkelijk", "noteworthy")
        ])
    },
    "reuters_japanese": {
        "name": "Reuters",
        "url": "http://feeds.reuters.com/reuters/%s.rss",
        "lang": "ja",
        "cat": collections.OrderedDict([
            ("JPWorldNews", "world"),
            ("JPBusinessNews", "business"),
            ("JPSportsNews", "sports"),
            ("JPTechnologyNews", "technology"),
            ("JPEntertainment", "entertainment")
        ])
    }
}

# encode the text

def enc(text):
    if text:
        return ftfy.fix_encoding(HTMLParser().unescape(text)).encode("utf-16be", "replace")

# resize the image and strip metadata (to make the image size smaller)

def shrink_image(data, resize, source): # Resize the image and strip metadata (to make the image size smaller).
    if data == "" or data is None: return None

    try:
        picture = requests.get(data).content
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
    image_without_exif.save(buffer, format='jpeg')

    return buffer.getvalue()

# these are common locations for cities so we don't have to waste API calls if they're used a lot

cities = collections.OrderedDict() 

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
cities["UNITED NATIONS"] = ["1cf0cb78", "United Nations"] # maps to the UN offices in New York
cities["VATICAN CITY"] = ["1dcc08db", "Vatican City"]
cities["VIENNA"] = ["223d0ba0", "Vienna"]
cities["WASHINGTON"] = ["1ba8c938", "Washington D.C."]
cities["ZURICH"] = ["21a40610", "Zürich"]


def locations_download(language_code, data): # using Google Maps API is so much better than the crap Nintendo used for say, AP news.
    locations = collections.OrderedDict()
    gmaps = googlemaps.Client(key=config["google_maps_api_key"])

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

        if location is not None and location is not "":
            if location not in locations:
                locations[location] = [None, None, []]

            locations[location][2].append(keys)

    for name in list(locations.keys()):
        if name == "":
            continue

        uni_name = name if languages[language_code] == "ja" else unidecode(name) # if using unidecode with Japanese, it'll translate all the characters to English

        print(uni_name)

        coordinates = None

        if name not in cities:
            try:
                read = gmaps.geocode(uni_name, language=languages[language_code])
                loc_name = read[0]["address_components"][0]["long_name"]

                if languages[language_code] == "ja":
                    loc_name = enc(loc_name)
                else:
                    loc_name = enc(unidecode(loc_name))

                """Not doing anything with these."""

                country = u8(0)
                region = u8(0)
                location = u16(0)
                zoom_factor = u32_littleendian(6) # Nintendo used the value of 3 for states and countries but we probably don't have any articles that are just states or countries

                coordinates = s16(int(read[0]["geometry"]["location"]["lat"] / (360 / 65536))) + \
                                s16(int(read[0]["geometry"]["location"]["lng"] / (360 / 65536))) + \
                                country + region + location + zoom_factor # latitude and longitude is divided by the value of 360 (degrees of a full circle) divided by the max int for a 16-bit int
            except:
                log("There was a error downloading the location data.", "INFO")

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


# get location from geocode
# geocode sucks and it doesn't seem to be working right now

def geoparse(article):
    location = requests.post("https://geocode.xyz/",
                data={
                    "scantext": article.split("\n")[0],
                    "json": "1",
                    "auth": config["geocode_key"]
                }).json()
    try:
        return location["match"][0]["location"]
    except:
        return None

# download the news

class News:
    def __init__(self, source):
        self.source = source
        self.sourceinfo = sources[self.source]
        self.url = self.sourceinfo["url"]
        self.language = self.sourceinfo["lang"]
        self.newsdata = collections.OrderedDict()

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
                for v in random.sample(value, len(value)): # reverse and mix up the list
                    i = self.parse_feed(v, key, i)
            else:
                i = self.parse_feed(key, value, i)
            
    def parse_feed(self, key, value, i):
        if self.source == "AP":
            try:
                ap_json = requests.get(self.url % key).json() # we use AP's API to download their news, it's epic and it uses JSON
            except:
                return i

        feed = ap_json if self.source == "AP" \
                else feedparser.parse(self.url) if self.source == "AFP_French" \
                else feedparser.parse(self.sourceinfo["url2"] % (key, key)) if self.source == "ANSA" and value == "italy" \
                else feedparser.parse(self.url % (key, key)) if self.source == "ANSA" \
                else feedparser.parse(self.url % key) # I know this is a mess

        j = 0

        entries = feed["cards"] if self.source == "AP" else feed.entries

        for entry in entries:
            if self.source == "AP":
                try:
                    entry = entry["contents"][0]
                except:
                    continue

            current_time = int((time.mktime(datetime.utcnow().timetuple()) - 946684800) / 60)
            try:
                updated_time = int((time.mktime(time.strptime(entry["updated"], "%Y-%m-%d %H:%M:%S") if self.source == "AP" else entry["updated_parsed"]) - 946684800) / 60)
            except:
                print("Failed to parse RSS feed.")
                continue

            if current_time - updated_time < 60: # if it's a new article since the last hour
                i += 1
                j += 1
                
                if i > 25: # in case we have too many articles, we don't want the news file to get too big, there's a limit
                    break

                if self.source == "AFP_French" and key not in entry["link"]:
                    continue
                elif self.source == "AFP" and "SID" in entry["description"]:
                    self.source = "SID"
                elif self.source == "NU.nl" and entry["author"] == "ANP":
                    self.source = "ANP"

                title = entry["headline"] if self.source == "AP" else entry["title"]

                print(title)

                downloaded_news = Parse(entry["gcsUrl"] if self.source == "AP" else entry["link"], self.source, updated_time,
                                        title, self.language).get_news()

                if downloaded_news:
                    self.newsdata[value + str(j)] = downloaded_news
                
        return i



class Parse(News):
    def __init__(self, url, source, updated_time, headline, language, article=None, picture=None, credits=None, caption=None,
                 location=None, resize=None, html=None, soup=None):
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

        if self.source != "AP":
            init = self.newspaper_init()
            if init == []:
                return None

        {
            "AP": self.parse_ap,
            "Reuters": self.parse_reuters,
            "AFP_French": self.parse_afp,
            "AFP": self.parse_dtoday,
            "SID": self.parse_dtoday,
            "ANSA": self.parse_ansa,
            "NU.nl": self.parse_nu,
            "ANP": self.parse_nu,
        }[self.source]()

        self.get_news()

    def get_news(self):
        if self.headline == "" or self.headline is None:
            return []
        elif self.article == "" or self.article is None:
            return []
        return [u32(self.updated_time), u32(self.updated_time), enc(self.article), enc(self.headline),
                shrink_image(self.picture, self.resize, self.source), enc(self.credits), enc(self.caption),
                self.location, self.source]

    def newspaper_init(self):
        self.newsdata = newspaper.Article(self.url, language=self.language)
        self.newsdata.download()
        try:
            self.newsdata.parse()
        except newspaper.article.ArticleException: # trying again
            self.newsdata.parse()
        except newspaper.article.ArticleException:
            return []

        self.article = self.newsdata.text
        self.picture = self.newsdata.top_image
        self.html = self.newsdata.html
        self.soup = BeautifulSoup(self.html, "lxml")

    def parse_ap(self):
        try:
            self.newsdata = requests.get(self.url).json()
        except:
            return []

        if self.newsdata["localMemberName"] is not None:
            return []

        if self.newsdata["localLinkUrl"]:
            if "apnews" not in self.newsdata["localLinkUrl"]:
                return []
        else:
            return []
        
        try:
            self.article = newspaper.fulltext(self.newsdata["storyHTML"], language=self.language)
        except AttributeError:
            return []

        self.article = self.article.replace("\n\nYour browser does not support the iframe HTML tag. Try viewing this in a modern browser like Chrome, Safari, Firefox or Internet Explorer 9 or later.", "")

        if self.article[-2:] == "\n":
            self.article = self.article[:-2]

        if self.newsdata["bylines"] != "" and self.newsdata["bylines"] != None:
            self.article += "\n\n" + self.newsdata["bylines"]

        if self.article is None:
            return []
        
        if self.newsdata["mediaCount"] > 0 and self.newsdata["media"] != []:
            if self.newsdata["media"][0]["imageMimeType"] == "image/jpeg":
                self.resize = True

                self.picture = self.newsdata["media"][0]["gcsBaseUrl"] + "400" + self.newsdata["media"][0]["imageFileExtension"]

                self.caption = self.newsdata["media"][0]["flattenedCaption"]

                self.credits = self.caption.rsplit("(")[-1][:-1]
            else:
                self.picture = None
        else:
            self.picture = None

        if " (AP)" in self.article:
            self.location = self.article.split(" (AP)")[0]

    def parse_reuters(self):
        try:
            self.caption = self.soup.find("div", {"class": "Image_caption"}).text.replace("  REUTERS/", " REUTERS/")
             
            if self.caption in self.article:
                self.article = self.article.replace(self.caption + "\n\n", "")
        except AttributeError:
            pass

        if self.picture is not None:
            if "rcom-default.png" in self.picture: # Default picture
                self.picture = None
            else:
                self.resize = True

        if "(Reuters)" in self.article and self.article[:9] != "(Reuters)":
            self.location = self.article.split(" (Reuters)")[0]
        elif "\uff3b" in self.article and "\u3000" in self.article:
            self.location = self.article.split("\uff3b")[1].split("\u3000")[0]
        elif "\uff3b" in self.article and "\u0020" in self.article:
            self.location = self.article.split("\uff3b")[1].split("\u0020")[0]

    def parse_afp(self):
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
                self.article = line.strip()[22:-10] + buf.readlines()[1:].replace("\n\n" + line, "")
        except AttributeError:
            pass

    def parse_dtoday(self):
        if " (SID)" in self.article.split("\n")[2] or " (AFP)" in self.article.split("\n")[4]:
            split = self.article.split("\n")
            for s in split: # remove caption text from being the first paragraph of the article
                if "© AFP" in s or "© SID" in s:
                    del split[split.index(s) - 1]
                    del split[split.index(s)]
            if self.source == "AFP":
                self.article = "\n".join(split[4:])
            elif self.source == "SID":
                self.article = "\n".join(split[2:])

        try:
            self.resize = True
            self.caption = self.soup.find("div", {"class": "articleimg_full"}).find("span").text
            self.picture = self.soup.find("div", {"class": "articleimg_full"}).find("img")["src"]
        except AttributeError:
            pass

        try:
            if self.source == "AFP":
                self.location = self.article.split(" (AFP)")[0]
            elif self.source == "SID":
                self.location = self.article.split(" (SID)")[0]
        except AttributeError:
            pass

    def parse_ansa(self):
        try:
            self.resize = True
            self.credits = self.soup.find("div", {"class": "news-caption hidden-phone"}).find("em").text
        except AttributeError:
            pass

        try:
            self.location = self.soup.find("span", {"itemprop": "dateline"}, {"class": "location"}).text
        except AttributeError:
            pass

    def parse_nu(self):
        if "Video" in self.headline or "Liveblog" in self.headline: # not an article
            return None

        try:
            self.resize = True
            self.credits = self.soup.find("span", {"class": "photographer"}).text
        except AttributeError:
            pass

        try:
            self.location = geoparse(self.article)
        except:
            pass
