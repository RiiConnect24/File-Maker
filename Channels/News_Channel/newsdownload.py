#!/usr/bin/python
# -*- coding: utf-8 -*-

# ===========================================================================
# NEWS CHANNEL GENERATION SCRIPT
# AUTHORS: LARSEN VALLECILLO
# ****************************************************************************
# Copyright (c) 2015-2018 RiiConnect24, and it's (Lead) Developers
# ===========================================================================

import binascii
import collections
import json
import sys
import textwrap
import time
from HTMLParser import HTMLParser
from StringIO import StringIO
from datetime import datetime

import feedparser
import ftfy
import googlemaps
import newspaper
import requests
from PIL import Image
from bs4 import BeautifulSoup
from resizeimage import resizeimage
from unidecode import unidecode

from utils import setup_log, log, u8, u16, u32, u32_littleendian

reload(sys)
sys.setdefaultencoding("utf-8")

with open("./Channels/News_Channel/config.json", "rb") as f:
    config = json.load(f)

if config["production"]: setup_log(config["sentry_url"], True)

"""Define information about news sources"""

sources = {
    # urls string argument is category key
    # for example: national on ap_english would go to http://hosted.ap.org/lineups/USHEADS-rss_2.0.xml?SITE=AP&SECTION=HOME&TEMPLATE=DEFAULT
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
            ("apf-science,apf-Health", "science"),
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
        "url": "http://www.lepoint.fr/24h-infos/rss.xml",
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
    "donaukurier_german": {
        "name": "AFP",
        "url": "http://www.donaukurier.de/storage/rss/rss/%s.xml",
        "lang": "de",
        "cat": collections.OrderedDict([
            ("nachrichten", "world"),
            ("wirtschaft", "economy"),
            ("kultur", "culture")
        ])
    },
    "sid_german": {
        "name": "SID",
        "url": "http://feed43.com/sid.xml",
        "lang": "de",
        "cat": collections.OrderedDict([
            ("sport", "sport")
        ])
    },
    "ansa_italian": {
        "name": "ANSA",
        "url": "http://ansa.it/sito/notizie/%s/%s_rss.xml",
        "lang": "it",
        "cat": collections.OrderedDict([
            ("mondo", "world"),
            ("sport", "sports"),
            ("economia", "economy"),
            ("tecnologia", "technology"),
            ("cultura", "culture")
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
        "name": "Reuters_Japanese",
        "url": "https://twitrss.me/twitter_user_to_rss/?user=%s",
        "lang": "en",  # newspaper does not support japanese
        "cat": collections.OrderedDict([
            ("ReutersJpWorld", "world"),
            ("ReutersJpBiz", "business"),
            ("ReutersJpSports", "sports"),
            ("ReutersJpTech", "technology"),
            ("ReutersJpEnt", "entertainment")
        ])
    }
}


"""Encode the text."""

def enc(text):
    if text:
        return ftfy.fix_encoding(HTMLParser().unescape(text).decode("utf-8")).encode("utf-16be", "replace")


"""Resize the image and strip metadata (to make the image size smaller)."""

def shrink_image(data, resize, source):
    if data == "" or data is None: return None

    picture = requests.get(data).content
    image = Image.open(StringIO(picture))

    try:
        if resize: image = resizeimage.resize_width(image, 200)

        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)

        buffer = StringIO()
        image_without_exif.save(buffer, format='jpeg')
    except:
        return None

    return buffer.getvalue()


"""Get the location data."""


def locations_download(language_code, data):
    locations = collections.OrderedDict()
    locations_return = collections.OrderedDict()
    gmaps = googlemaps.Client(key=config["google_maps_api_key"])

    """This dictionary is used to determine languages."""

    languages = {
        0: "ja",
        1: "en",
        2: "de",
        3: "fr",
        4: "es",
        5: "it",
        6: "nl",
    }

    """Small list of cities to correct."""

    corrections = {
        "UNITED NATIONS": ["1cf0cb780000000006000000", "United Nations"],
        "WASHINGTON": ["1ba2c94a0000000006000000", "Washington"],
    }

    for keys, values in data.items():
        location = values[7]

        if location is not None:
            if location not in locations: locations[location] = []

            locations[location].append(keys)

    for name in locations.keys():
        read = None

        if name == "": continue

        if name not in corrections:
            try:
                print unidecode(name)
                read = gmaps.geocode(unidecode(name), language=languages[language_code])
            except:
                log("There was a error downloading the location data.", "WARNING")

        if read is None:
            if name in corrections:
                coordinates = binascii.unhexlify(corrections[name][0])
                new_name = enc(corrections[name][1])

                for filenames in locations[name]:
                    if new_name not in locations_return: locations_return[new_name] = [coordinates, []]

                    locations_return[new_name][1].append(filenames)

        elif read is not None:
            try:
                new_name = read[0]["address_components"][0]["long_name"].encode("utf-16be")

                """Not doing anything with these at this time."""

                country = u8(0)
                region = u8(0)
                location = u16(0)
                zoom_factor = u32_littleendian(6)

                coordinates = u16(int(read[0]["geometry"]["location"]["lat"] / 0.0054931640625) & 0xFFFF) + u16(int(
                    read[0]["geometry"]["location"][
                        "lng"] / 0.0054931640625) & 0xFFFF) + country + region + location + zoom_factor

                for filenames in locations[name]:
                    if new_name not in locations_return: locations_return[new_name] = [coordinates, []]

                    locations_return[new_name][1].append(filenames)
            except:
                log("There was a error downloading the location data.", "WARNING")

    return locations_return


"""Get location from Geoparser."""


def geoparser_get(article):
    i = 0
    for key in config["geoparser_keys"]:
        url = 'https://geoparser.io/api/geoparser'
        headers = {'Authorization': "apiKey %s" % key}
        data = {'inputText': article}
        response = requests.post(url, headers=headers, data=data)
        status_code = response.status_code
        if response.status_code == 402:
            continue
        else:
            try:
                property = response.json()["features"][0]["properties"]
                i += 1
                return property["name"] + ", " + property["country"]
            except:
                return None
    log("Out of Geoparser requests.", "WARNING")
    return None

"""Download the news."""

class News:
    def __init__(self, source):
        self.source = source
        self.sourceinfo = sources[self.source]
        self.url = self.sourceinfo["url"]
        self.language = self.sourceinfo["lang"]
        self.newsdata = collections.OrderedDict()

        self.source = self.sourceinfo["name"]

        self.parse_feed()

        print "\n"

    def __dict__(self):
        return self.newsdata

    def parse_feed(self):
        print "Downloading News from " + self.source + "...\n"

        for key, value in self.sourceinfo["cat"].items():
            feed = requests.get(self.url % key).json() if self.source == "AP" \
                    else feedparser.parse(self.url) if self.source == "SID" \
                    else feedparser.parse(self.url) if self.source == "AFP_French" \
                    else feedparser.parse(self.url % (key, key)) if self.source == "ANSA" \
                    else feedparser.parse(self.url % key)

            i = 0

            entries = feed["cards"] if self.source == "AP" else feed.entries

            for entry in entries:
                if self.source == "AP":
                    entry = entry["contents"][0]

                current_time = int((time.mktime(datetime.utcnow().timetuple()) - 946684800) / 60)
                try:
                    updated_time = int((time.mktime(time.strptime(entry["updated"], "%Y-%m-%d %H:%M:%S") if self.source == "AP" else entry["updated_parsed"]) - 946684800) / 60)
                except:
                    print "Failed to parse RSS feed."
                    continue

                if current_time - updated_time < 60:
                    i += 1

                    if self.source == "AFP_French" and key not in entry["link"]:
                        continue
                    elif self.source == "AFP" and "dpa" in entry["description"]:
                        self.source = "dpa"
                    elif self.source == "NU.nl" and entry["author"] == "ANP":
                        self.source = "ANP"
                    elif self.source == "Reuters_Japanese":
                        entry["link"] = requests.get(
                            "http://bit.ly/" + entry["description"].split("http://bit.ly/", 1)[1][:7]).url
                        entry["title"] = entry["title"].split("  http://bit.ly/", 1)[0]

                    title = entry["headline"] if self.source == "AP" else entry["title"]

                    print title

                    downloaded_news = Parse(entry["gcsUrl"] if self.source == "AP" else entry["link"], self.source, updated_time,
                                            title, self.language).get_news()

                    if downloaded_news:
                        self.newsdata[value + str(i)] = downloaded_news



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
            self.newspaper_init()

        {
            "AP": self.parse_ap,
            "Reuters": self.parse_reuters,
            "AFP_French": self.parse_afp,
            "AFP": self.parse_donaukurier,
            "dpa": self.parse_donaukurier,
            "SID": self.parse_sid,
            "ANSA": self.parse_ansa,
            "NU.nl": self.parse_nu,
            "ANP": self.parse_nu,
            "Reuters_Japanese": self.parse_reuters_japanese
        }[self.source]()

        self.get_news()

    def get_news(self):
        if self.headline == "":
            log("Headline is blank.", "WARNING")
            return []
        elif self.article == "":
            log("Article is blank.", "WARNING")
            return []
        else:
            return [u32(self.updated_time), u32(self.updated_time), enc(self.article), enc(self.headline),
                    shrink_image(self.picture, self.resize, self.source), enc(self.credits), enc(self.caption),
                    self.location, self.source]

    def newspaper_init(self):
        self.newsdata = newspaper.Article(self.url, language=self.language)
        self.newsdata.download()
        self.newsdata.parse()

        self.article = self.newsdata.text
        self.picture = self.newsdata.top_image
        self.html = self.newsdata.html
        self.soup = BeautifulSoup(self.html, "lxml")

    def parse_ap(self):
        self.newsdata = requests.get(self.url).json()

        if self.newsdata["localMemberName"] != None:
            return

        self.article = BeautifulSoup(self.newsdata["storyHTML"], "lxml").get_text(separator="\n").replace("\n\n", "\n")

        if self.newsdata["bylines"] != "":
            self.article += "\n\n" + self.newsdata["bylines"]

        if self.newsdata["mediaCount"] > 0 and self.newsdata["media"][0]["imageMimeType"] == "image/jpeg":
            self.resize = True

            self.picture = self.newsdata["media"][0]["gcsBaseUrl"] + "400" + self.newsdata["media"][0]["imageFileExtension"]

            self.caption = self.newsdata["media"][0]["flattenedCaption"]

            self.credits = self.caption.split("(")[1][:-1]
        else:
            self.picture = None

        if self.newsdata["dateline"] != None:
            self.location = self.newsdata["dateline"]

    def parse_reuters(self):
        try:
            self.soup.find("div", {"class": "trustBadgeContainer_1gqgJ"}).decompose()
        except:
            pass

        try:
            self.caption = self.soup.find("span", {"class": "caption_KoNH1"}).text.replace("  REUTERS/",
                                                                                           " REUTERS/")
        except:
            pass

        try:
            self.soup.findall("div", {"class": "caption_KoNH1"}).decompose()
        except:
            pass

        self.article = BeautifulSoup(
            str(self.soup.find("div", {"class": "body_1gnLA"})).replace("</p>", "\n\n</p>"),
            "lxml").text

        if self.picture is not None:
            if "rcom-default.png" in self.picture:
                self.picture = None
            else:
                self.resize = False
                try:
                    self.picture += "&w=200"
                except:
                    pass

        if "(Reuters)" in self.article:
            self.location = self.article.split(" (Reuters)")[0]

    def parse_afp(self):
        try:
            self.resize = True
            self.caption = self.soup.find("figcaption", {"class": "art-caption"}).text
        except:
            pass

        try:
            """The location is at the end of the article, I couldn't find anything better to parse it."""

            if "(AFP)" in self.article:
                buf = StringIO(self.article)
                line = buf.readlines()[-1]
                buf = StringIO(self.article)
                self.location = line.strip()[22:-19]
                self.article = line.strip()[22:-10] + buf.readlines()[1:].replace("\n\n" + line, "")
        except:
            pass

    def parse_donaukurier(self):
        try:
            self.resize = True
            self.caption = self.soup.find("figcaption").text
        except:
            pass

        if self.caption is not None:
            buf = StringIO(self.article)
            self.article = "".join(buf.readlines()[1:])

        try:
            if self.source == "AFP":
                self.location = self.soup.find("em").text.split(" (AFP)")[0]
            elif self.source == "dpa":
                self.location = self.article.split(" (dpa)")[0]
        except:
            pass

    def parse_sid(self):
        try:
            self.resize = True
            self.caption = self.soup.find("small").text
        except:
            pass

        try:
            self.location = geoparser_get(self.article)
        except:
            pass

    def parse_ansa(self):
        try:
            self.resize = True
            self.credits = self.soup.find("div", {"class": "news-caption hidden-phone"}).find("em").text
        except:
            pass

        try:
            self.location = self.soup.find("span", {"itemprop": "dateline"}, {"class": "location"}).text
        except:
            pass

    def parse_nu(self):
        if "Video" in self.headline or "Liveblog" in self.headline:
            return None

        try:
            self.resize = True
            self.credits = self.soup.find("span", {"class": "photographer"}).text
        except:
            pass

        try:
            self.location = geoparser_get(self.article)
        except:
            pass

    def parse_reuters_japanese(self):
        try:
            self.headline = self.soup.find("h1", {"class": "headline_2zdFM"}).text
        except:
            return None

        try:
            self.caption = self.soup.find("span", {"class": "caption_KoNH1"}).text.replace("  REUTERS/",
                                                                                           " REUTERS/")
        except:
            pass

        try:
            self.soup.findall("div", {"class": "caption_KoNH1"}).decompose()
        except:
            pass

        article_text = BeautifulSoup(
            str(self.soup.find("div", {"class": "body_1gnLA"})).replace("</p>", "\n\n</p>"),
            "lxml").text

        self.article = "\n".join(textwrap.wrap(article_text, 25))

        if self.picture is not None:
            if "rcom-default.png" in self.picture:
                self.picture = None
            else:
                self.resize = False
                try:
                    self.picture += "&w=200"
                except:
                    pass

        try:
            self.location = self.article.split("[")[1].split("　")[0]
        except:
            pass
