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
import struct
import sys
import textwrap
import time
from datetime import datetime
from StringIO import StringIO

import feedparser
import googlemaps
import logging
import newspaper
import requests
from bs4 import BeautifulSoup
from PIL import Image
from raven import Client
from raven.conf import setup_logging
from raven.handlers.logging import SentryHandler
from resizeimage import resizeimage
from unidecode import unidecode

from config import *

reload(sys)
sys.setdefaultencoding("utf-8")

"""Set up Sentry for error logging."""

if production:
    client = Client(sentry_url)
    handler = SentryHandler(client)
    setup_logging(handler)
    logger = logging.getLogger(__name__)


def capture_message(text, mode):
    if production:
        print text
        if mode is "warning":
            logger.warning(text)
        elif mode is "error":
            logger.error(text)


"""This will pack the integers."""


def u8(data):
    if data < 0 or data > 255:
        capture_message("u8 Value Pack Failure: %s" % data, "error")
        data = 0
    return struct.pack(">B", data)


def u16(data):
    if data < 0 or data > 65535:
        capture_message("u16 Value Pack Failure: %s" % data, "error")
        data = 0
    return struct.pack(">H", data)


def u32(data):
    if data < 0 or data > 4294967295:
        capture_message("u32 Value Pack Failure: %s" % data, "error")
        data = 0
    return struct.pack(">I", data)


def u32_littleendian(data):
    if data < 0 or data > 4294967295:
        capture_message("u32 Value Pack Failure: %s" % data, "error")
        data = 0
    return struct.pack("<I", data)


"""Resize the image and strip metadata (to make the image size smaller)."""


def shrink_image(data, resize):
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
    gmaps = googlemaps.Client(key=google_maps_api_key)

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
                capture_message("There was a error downloading the location data.", "warning")

        if read is None:
            if name in corrections:
                coordinates = binascii.unhexlify(corrections[name][0])
                new_name = corrections[name][1].encode("utf-16be")

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
                capture_message("There was a error downloading the location data.", "warning")

    return locations_return


"""Get location from Geoparser."""


def geoparser_get(article):
    i = 0
    for key in geoparser_keys:
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
    capture_message("Out of Geoparser requests.", "warning")
    return None


"""Download the news."""


class News:
    def __init__(self, source):
        self.source = source
        self.url = None
        self.newsdata = collections.OrderedDict()
        self.category = collections.OrderedDict()

        self.urls()
        self.languages()
        self.categories()

        if self.source == "afp_french_laprovence":
            self.newsdata.copy().update(News("afp_french_lobs").newsdata)

        self.new_source()

        self.parse_feed()

        print "\n"

    def __dict__(self):
        return self.newsdata

    """Get the URL for the RSS feed."""

    def urls(self):
        if self.source == "ap_english" or self.source == "ap_spanish":
            self.url = "http://hosted.ap.org/lineups/%s-rss_2.0.xml?SITE=AP&SECTION=HOME&TEMPLATE=DEFAULT"
        elif self.source == "reuters_europe_english":
            self.url = "http://feeds.reuters.com/reuters/%s.rss"
        elif self.source == "afp_french_laprovence":
            self.url = "http://www.laprovence.com/rss/%s.xml"
        elif self.source == "afp_french_lobs":
            self.url = "http://www.nouvelobs.com/depeche/%s/rss.xml"
        elif self.source == "donaukurier_german":
            self.url = "http://www.donaukurier.de/storage/rss/rss/%s.xml"
        elif self.source == "sid_german":
            self.url = "http://feed43.com/sid.xml"
        elif self.source == "ansa_italian":
            self.url = "http://ansa.it/sito/notizie/%s/%s_rss.xml"
        elif self.source == "nu_dutch":
            self.url = "https://www.nu.nl/rss/%s"
        elif self.source == "reuters_japanese":
            self.url = "https://twitrss.me/twitter_user_to_rss/?user=%s"

    """Get languages."""

    def languages(self):
        self.languages = collections.OrderedDict()

        self.languages["ap_english"] = "en"
        self.languages["ap_spanish"] = "es"
        self.languages["reuters_europe_english"] = "en"
        self.languages["afp_french_laprovence"] = "fr"
        self.languages["afp_french_lobs"] = "fr"
        self.languages["donaukurier_german"] = "de"
        self.languages["sid_german"] = "de"
        self.languages["ansa_italian"] = "it"
        self.languages["nu_dutch"] = "nl"
        self.languages["reuters_japanese"] = "en" # Unfortunately newspaper doesn't support Japanese.

        self.language = self.languages[self.source]

    """Get a proper category name."""

    def categories(self):
        if self.source == "ap_english":
            self.category["USHEADS"] = "national"
            self.category["WORLDHEADS"] = "world"
            self.category["SPORTSHEADS"] = "sports"
            self.category["ENTERTAINMENTHEADS"] = "entertainment"
            self.category["BUSINESSHEADS"] = "business"
            self.category["SCIENCEHEADS"] = "science"
            self.category["HEALTHHEADS"] = "science"
            self.category["TECHNOLOGY"] = "technology"
            self.category["STRANGEHEADS"] = "oddities"
        elif self.source == "ap_spanish":
            self.category["NOTICIAS_GENERALES"] = "general"
            self.category["NOTICIAS_FINANCIERAS"] = "finance"
            self.category["NOTICIAS_DEPORTIVAS"] = "sports"
            self.category["NOTICIAS_ENTRETENIMIENTOS"] = "shows"
        elif self.source == "reuters_europe_english":
            self.category["UKWorldNews"] = "world"
            self.category["UKdomesticNews"] = "uk"
            self.category["UKHealthNews"] = "health"
            self.category["UKScienceNews"] = "science"
            self.category["technology"] = "technology"
            self.category["UKEntertainment"] = "entertainment"
            self.category["UKSportsNews"] = "sports"
            self.category["lifestyle"] = "lifestyle"
        elif self.source == "afp_french_laprovence":
            self.category["France-monde"] = "world"
            self.category["Sports"] = "sports"
        elif self.source == "donaukurier_german":
            self.category["nachrichten"] = "world"
            self.category["wirtschaft"] = "economy"
            self.category["kultur"] = "culture"
        elif self.source == "sid_german":
            self.category["sport"] = "sport"
        elif self.source == "ansa_italian":
            self.category["mondo"] = "world"
            self.category["sport"] = "sports"
            self.category["economia"] = "economy"
            self.category["tecnologia"] = "technology"
            self.category["cultura"] = "culture"
        elif self.source == "nu_dutch":
            self.category["Algemeen"] = "algemeen"
            self.category["Economie"] = "economy"
            self.category["Sport"] = "sports"
            self.category["Tech"] = "technology"
            self.category["Entertainment"] = "entertainment"
            self.category["Lifestyle"] = "lifestyle"
            self.category["Opmerkelijk"] = "noteworthy"
        elif self.source == "reuters_japanese":
            self.category["ReutersJpWorld"] = "world"
            self.category["ReutersJpBiz"] = "business"
            self.category["ReutersJpSports"] = "sports"
            self.category["ReutersJpTech"] = "technology"
            self.category["ReutersJpEnt"] = "entertainment"

    def new_source(self):
        sources = collections.OrderedDict()

        sources["ap_english"] = "AP"
        sources["ap_spanish"] = "AP"
        sources["reuters_europe_english"] = "Reuters"
        sources["afp_french_laprovence"] = "AFP_french"
        sources["afp_french_lobs"] = "AFP_french"
        sources["donaukurier_german"] = "AFP"
        sources["sid_german"] = "SID"
        sources["ansa_italian"] = "ANSA"
        sources["nu_dutch"] = "NU.nl"
        sources["reuters_japanese"] = "Reuters_japanese"

        self.source = sources[self.source]

    def parse_feed(self):
        print "Downloading News from " + self.source + "...\n"

        for category in self.category.keys():
            if self.source is "SID":
                feed = feedparser.parse(self.url)
            elif self.source is "ANSA":
                feed = feedparser.parse(self.url % (category, category))
            elif self.source is "AFP" and "nouvelobs" in self.url:
                feed = feedparser.parse("http://www.nouvelobs.com/depeche/rss.xml")
            else:
                feed = feedparser.parse(self.url % category)

            i = 0

            for entries in feed.entries:
                current_time = int((time.mktime(datetime.utcnow().timetuple()) - 946684800) / 60)
                try:
                    updated_time = int((time.mktime(entries["updated_parsed"]) - 946684800) / 60)
                except:
                    print "Failed to parse RSS feed."
                    continue

                if current_time - updated_time < 60:
                    i += 1

                    title = entries["title"]
                    print title

                    if self.source is "AFP" and "dpa" in entries["description"]:
                        self.source = "dpa"
                    elif self.source is "NU.nl" and entries["author"] is "ANP":
                        self.source = "ANP"
                    elif self.source is "AFP" and "nouvelobs" in self.url:
                        self.category[category] = entries["category"].lower()
                    elif self.source is "Reuters_japanese":
                        entries["link"] = requests.get(
                            "http://bit.ly/" + entries["description"].split("http://bit.ly/", 1)[1][:7]).url

                    downloaded_news = Parse(entries["link"], self.source, updated_time,
                                                                            title, self.language).get_news()

                    if downloaded_news:
                        self.newsdata[self.category[category] + str(i)] = downloaded_news


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

        self.newspaper_init()

        if self.source is "AP":
            self.parse_ap()
        elif self.source is "Reuters":
            self.parse_reuters()
        elif self.source is "AFP_french":
            self.parse_afp()
        elif self.source is "AFP" or self.source is "dpa":
            self.parse_donaukurier()
        elif self.source is "SID":
            self.parse_sid()
        elif self.source is "ANSA":
            self.parse_ansa()
        elif self.source is "NU.nl" or self.source is "ANP":
            self.parse_nu()
        elif self.source is "Reuters_japanese":
            self.parse_reuters_japanese()

        self.get_news()

    def get_news(self):
        if self.headline == "":
            capture_message("Headline is blank.", "warning")
            return []
        elif self.article == "":
            capture_message("Article is blank.", "warning")
            return []
        else:
            return [u32(self.updated_time), u32(self.updated_time), self.article.encode("utf-16be"), self.headline.encode("utf-16be"),
                    shrink_image(self.picture, self.resize), self.credits.encode("utf-16be") if self.credits else None, self.caption.encode("utf-16be") if self.caption else None,
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
        try:
            self.article += "\n\n" + self.soup.find("span", {"class": "byline"}).text + ", " + self.soup.find("span", {
                "class": "bylinetitle"}).text
        except:
            pass

        if "ap-smallphoto-img" in self.html:
            self.resize = False

            self.picture = "http://staging.hosted.ap.org/" + self.soup.find("img", {"class": "ap-smallphoto-img"})[
                                                                 "src"][:-10] + "-small.jpg"
            self.credits = self.soup.find("span", {"class": "apCaption"}).text

            """The Associated Press stores the picture caption on a different page, so we are navigating to that page."""

            captions_page = requests.get(
                "http://staging.hosted.ap.org/" + self.soup.find("a", {"class": "ap-smallphoto-a"})['href']).text
            soup_caption = BeautifulSoup(captions_page, "lxml")

            try:
                self.caption = soup_caption.find("font", {"class": "photo"}).text
            except:
                self.picture = None
                self.credits = None
                self.caption = None
        else:
            self.picture = None

        if "(AP)" in self.article:
            self.location = self.article.split(" (AP)", 1)[0]

    def parse_reuters(self):
        try:
            self.soup.find("div", {"class": "StandardArticleBody_trustBadgeContainer_1gqgJ"}).decompose()
        except:
            pass

        try:
            self.soup.find("div", {"class": "Slideshow_inline-container_1QqKC Slideshow_mega_19SOz"}).decompose()
        except:
            pass

        self.article = BeautifulSoup(
            str(self.soup.find("div", {"class": "StandardArticleBody_body_1gnLA"})).replace("</p>", "\n\n</p>"),
            "lxml").text

        if "rcom-default.png" in self.picture:
            self.picture = None
        else:
            self.resize = False
            try:
                self.picture += "&w=200"
                self.caption = self.soup.find("span", {"class": "Image_caption_KoNH1"}).text.replace("  REUTERS/",
                                                                                                     " REUTERS/")
                self.article = self.article.replace("\n\n" + self.caption, "")
            except:
                pass

        if "(Reuters)" in self.article:
            self.location = self.article.split(" (Reuters)")[0]

    def parse_afp(self):
        if self.source == "afp_french_laprovence":
            self.soup.find("div", {"id": "id_article_corps"}).decompose()

            if "logo-lp-facebook.jpg" in self.picture:
                self.picture = None
            else:
                self.resize = True
                self.credits = self.soup.find("span", {"class": "credit"}).text
                self.caption = self.soup.find("figcaption").text
        elif self.source == "afp_french_lobs":
            if "http://referentiel.nouvelobs.com/logos/og/logo-nobstr.jpg" in self.picture:
                self.picture = None
            else:
                self.resize = True
                self.caption = self.soup.find("figcaption").text

        if "(AFP)" in self.article:
            self.location = self.article.split(" (AFP)")[0]

    def parse_donaukurier(self):
        try:
            self.resize = True
            self.caption = self.soup.find("figcaption").text
        except:
            pass

        try:
            if source is "AFP_de":
                self.location = self.soup.find("em").split(" (AFP)")[0]
            elif source is "dpa":
                self.location = self.article.split(" (dpa")[0]
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
            self.headline = self.soup.find("h1", {"class": "ArticleHeader_headline_2zdFM"}).text
        except:
            return None

        article_text = BeautifulSoup(
            str(self.soup.find("div", {"class": "StandardArticleBody_body_1gnLA"})).replace("</p>", "\n\n</p>"),
            "lxml").text

        self.article = "\n".join(textwrap.wrap(article_text, 25))

        if "rcom-default.png" in self.picture:
            self.picture = None
        else:
            self.resize = False
            self.picture += "&w=200"
            self.caption = self.soup.find("span", {"class": "Image_caption_KoNH1"}).text.replace("  REUTERS/",
                                                                                                 " REUTERS/")

            self.article = self.article.replace("\n\n" + self.caption, "")

        try:
            self.location = self.article.split("[")[1].split("　")[0]
        except:
            pass
