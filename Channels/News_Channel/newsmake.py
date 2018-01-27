#!/usr/bin/python
# -*- coding: utf-8 -*-

# ===========================================================================
# NEWS CHANNEL GENERATION SCRIPT
# AUTHORS: LARSEN VALLECILLO
# ****************************************************************************
# Copyright (c) 2015-2018 RiiConnect24, and it's (Lead) Developers
# ===========================================================================

import binascii
import calendar
import collections
import errno
import glob
import json
import logging
import os
import pickle
import struct
import subprocess
import sys
import time
from datetime import timedelta, datetime, date  # Used to get time stuff.

import cachetclient.cachet
import requests
import rsa
from raven import Client
from raven.conf import setup_logging
from raven.handlers.logging import SentryHandler

import newsdownload
from config import *
import imp

requests.packages.urllib3.disable_warnings()

header = collections.OrderedDict()
topics_table = collections.OrderedDict()
articles_table = collections.OrderedDict()
source_table = collections.OrderedDict()
locations_table = collections.OrderedDict()
pictures_table = collections.OrderedDict()

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


def u8(value):
    if value < 0 or value > 255:
        capture_message("u8 Value Pack Failure: %s" % data, "error")
        return 0
    return struct.pack(">B", value)


def u16(value):
    if value < 0 or value > 65535:
        capture_message("u16 Value Pack Failure: %s" % data, "error")
        return 0
    return struct.pack(">H", value)


def u32(value):
    if value < 0 or value > 4294967295:
        capture_message("u32 Value Pack Failure: %s" % data, "error")
        return 0
    return struct.pack(">I", value)


def u32_littleendian(value):
    if value < 0 or value > 4294967295:
        capture_message("u32 Value Pack Failure: %s" % data, "error")
        return 0
    return struct.pack("<I", value)


# http://stackoverflow.com/a/600612/3874884
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
    else:
        return


def process_news(name, mode, language, countries, d):
    print "News Channel File Generator \nBy Larsen Vallecillo / www.rc24.xyz\n\nMaking news.bin for %s...\n" % name

    """If there are more than 22 news articles, delete the rest. This is so the file doesn't get too large."""

    global language_code, data, system

    language_code = language
    data = d.newsdata

    i = 0

    for key in data.keys():
        i += 1
        if i > 22:
            del data[key]

    # data = remove_duplicates()

    for system in ["wii", "wii_u"]:
        make_news_bin(mode, system)

    if production:
        """Tell Cachet how many news articles it downloaded."""

        points = cachetclient.cachet.Points(endpoint=cachet_url, api_token=cachet_key)
        json.loads(points.post(id="2", value=len(data)))

        """This will use a webhook to log that the script has been ran."""

        webhook = {"username": "News Bot", "content": "News Data has been updated!",
                   "avatar_url": "https://rc24.xyz/images/logo-small.png", "attachments": [
                {"fallback": "News Data Update", "color": "#1B691E", "author_name": "RiiConnect24 News Script",
                 "author_icon": "https://rc24.xyz/images/webhooks/news/profile.png", "text": make_news,
                 "title": "Update!",
                 "fields": [{"title": "Script", "value": "News Channel (" + name + ")", "short": "false"}],
                 "thumb_url": "https://rc24.xyz/images/webhooks/news/%s.png" % mode, "footer": "RiiConnect24 Script",
                 "footer_icon": "https://rc24.xyz/images/logo-small.png",
                 "ts": int(time.mktime(datetime.utcnow().timetuple()))}]}

        for url in webhook_urls:
            requests.post(url, json=webhook, allow_redirects=True)

        filesize = sum(os.path.getsize(f) - 320 for f in
                       glob.glob("/var/www/wapp.wii.com/news/v2/%s/%s/news.bin.*" % (language_code, countries[0])))

        if filesize > 3712000:
            capture_message("News files exceed the maximum file size amount.", "error")

        for country in countries:
            copy_file(mode, "wii", country)
            copy_file(mode, "wii_u", country)

        newsfilename = "news.bin." + str(datetime.utcnow().hour).zfill(2) + "." + mode + "."
        os.remove(newsfilename + "wii")
        os.remove(newsfilename + "wii_u")


"""Copy the temp files to the correct path that the Wii will request from the server."""


def copy_file(mode, console, country):
    if force_all:
        for hours in range(0, 24):
            newsfilename = "news.bin.%s.%s.%s" % (str(datetime.utcnow().hour).zfill(2), mode, console)
            newsfilename2 = "news.bin.%s" % (str(hours).zfill(2))
            path = "%s/%s/%s/%s" % (file_path, "v3" if console == "wii_u" else "v2", language_code, country)
            mkdir_p(path)
            path = "%s/%s" % (path, newsfilename2)
            subprocess.call(["cp", newsfilename, path])
    else:
        newsfilename = "news.bin.%s.%s.%s" % (str(datetime.utcnow().hour).zfill(2), mode, console)
        newsfilename2 = "news.bin.%s" % (str(datetime.utcnow().hour).zfill(2))
        path = "%s/%s/%s/%s" % (file_path, "v3" if console == "wii_u" else "v2", language_code, country)
        mkdir_p(path)
        path = "%s/%s" % (path, newsfilename2)
        subprocess.call(["cp", newsfilename, path])


"""Run the functions to make the news."""


def make_news_bin(mode, console):
    global system, dictionaries, topics_news, languages, make_news, data, country_code, language_code, locations_data, header, topics_table, articles_table, source_table, locations_table, pictures_table

    if mode == "ap_english":
        topics_news = collections.OrderedDict()

        topics_news["National News"] = "national"
        topics_news["International News"] = "world"
        topics_news["Sports"] = "sports"
        topics_news["Arts/Entertainment"] = "entertainment"
        topics_news["Business"] = "business"
        topics_news["Science/Health"] = "science"
        topics_news["Technology"] = "technology"
        topics_news["Oddities"] = "oddities"

        languages = [1, 3, 4]

        language_code = 1

        country_code = 49

    elif mode == "ap_spanish":
        topics_news = collections.OrderedDict()

        topics_news["Generales"] = "general"
        topics_news["Financieras"] = "finance"
        topics_news["Deportivas"] = "sports"
        topics_news["Espectáculos"] = "shows"

        languages = [1, 3, 4]

        language_code = 4

        country_code = 49

    elif mode == "reuters_europe_english":
        topics_news = collections.OrderedDict()

        topics_news["World"] = "world"
        topics_news["UK"] = "uk"
        topics_news["Health"] = "health"
        topics_news["Science"] = "science"
        topics_news["Technology"] = "technology"
        topics_news["Entertainment"] = "entertainment"
        topics_news["Sports"] = "sports"
        topics_news["Lifestyle"] = "lifestyle"

        languages = [1, 2, 3, 4, 5, 6]

        language_code = 1

        country_code = 110

    elif mode == "afp_french":
        topics_news = collections.OrderedDict()

        topics_news["Monde"] = "world"
        topics_news["Sports"] = "sports"
        topics_news["Politique"] = "politics"
        topics_news["Top News"] = "topnews"

        languages = [1, 2, 3, 4, 5, 6]

        language_code = 3

        country_code = 110

    elif mode == "donaukurier_german":
        topics_news = collections.OrderedDict()

        topics_news["Nachrichten"] = "world"
        topics_news["Wirtschaft"] = "economy"
        topics_news["Kultur"] = "culture"

        languages = [1, 2, 3, 4, 5, 6]

        language_code = 2

        country_code = 110

    elif mode == "ansa_italian":
        topics_news = collections.OrderedDict()

        topics_news["Dal mondo"] = "world"
        topics_news["Sport"] = "sports"
        topics_news["Economia"] = "economy"
        topics_news["Tecnologia"] = "technology"
        topics_news["Cultura"] = "culture"

        languages = [1, 2, 3, 4, 5, 6]

        language_code = 5

        country_code = 110

    elif mode == "nu_dutch":
        topics_news = collections.OrderedDict()

        topics_news["Algemeen"] = "general"
        topics_news["Economie"] = "economy"
        topics_news["Sport"] = "sports"
        topics_news["Tech"] = "technology"
        topics_news["Entertainment"] = "entertainment"
        topics_news["Lifestyle"] = "lifestyle"
        topics_news["Opmerkelijk"] = "noteworthy"

        languages = [1, 2, 3, 4, 5, 6]

        language_code = 6

        country_code = 110

    elif mode == "reuters_japanese":
        topics_news = collections.OrderedDict()

        topics_news["ワールド"] = "world"
        topics_news["ビジネス"] = "business"
        topics_news["スポーツ"] = "sports"
        topics_news["テクノロジー"] = "technology"
        topics_news["エンタテインメント"] = "entertainment"

        languages = [0]

        language_code = 0

        country_code = 1

    numbers = 0

    if not os.path.exists("newstime"):
        os.mkdir("newstime")

    for topics in topics_news.values():
        newstime = collections.OrderedDict()

        for keys in data.keys():
            if topics in keys:
                numbers += 1

                newstime[data[keys][3]] = get_timestamp(1) + u32(numbers)

        pickle.dump(newstime,
                    open("newstime/newstime.%s-%s-%s-%s" % (str(datetime.now().hour).zfill(2), mode, topics, console),
                         "wb"))

    dictionaries = []

    header = collections.OrderedDict()
    topics_table = collections.OrderedDict()
    articles_table = collections.OrderedDict()
    source_table = collections.OrderedDict()
    locations_table = collections.OrderedDict()
    pictures_table = collections.OrderedDict()

    locations_data = newsdownload.locations_download(language_code, data)

    make_header(0, 30)
    make_wiimenu_articles()
    make_topics_table()
    make_timestamps_table(mode)
    make_articles_table()
    make_source_table()
    make_locations_table()
    make_pictures_table()
    make_articles()
    make_topics(0, 0)
    make_source_name_copyright()
    make_locations()
    make_source_pictures()
    make_pictures()
    make_riiconnect24_text()

    write_dictionary(mode)

    headlines = []

    for article in data.values():
        if article[3].decode("utf-16be") not in headlines:
            headlines.append(article[3].decode("utf-16be") + "\n")

    make_news = "".join(headlines)

    return make_news


"""This is a function used to count offsets."""


def offset_count(): return u32(
    12 + sum(len(values) for dictionary in dictionaries for values in dictionary.values() if values))


"""Return a timestamp."""


def get_timestamp(mode):
    global seconds

    if system == "wii":
        seconds = 946684800
    elif system == "wii_u":
        seconds = 789563880

    if mode == 1:
        return u32(int((calendar.timegm(datetime.utcnow().timetuple()) - seconds) / 60))
    elif mode == 2:
        return u32(int((calendar.timegm(datetime.utcnow().timetuple()) - seconds) / 60) + 1500)


"""Make the news.bin."""


def remove_duplicates():
    data_dupe = collections.OrderedDict()

    headlines = []

    for k, v in data.items():
        if v[3] not in headlines:
            headlines.append(v[3])
            data_dupe[k] = v
        elif v[3] in headlines:
            for k2, v2 in data_dupe.items():
                if v[3] == v2[3]:
                    del data_dupe[k2]
                    data_dupe[k + k2] = v2

    return data_dupe


"""First part of the header."""


def make_header(language_select_screen_flag, download_interval):
    dictionaries.append(header)

    header["updated_timestamp_1"] = get_timestamp(1)  # Updated time.
    header["term_timestamp"] = get_timestamp(2)  # Timestamp for the term.
    header["country_code"] = u32_littleendian(country_code)  # Wii Country Code.
    header["updated_timestamp_2"] = get_timestamp(1)  # 3rd timestamp.

    """List of languages that appear on the language select screen."""

    numbers = 0

    for language in languages:
        numbers += 1

        header[numbers] = u8(language)

    """Fills the rest of the languages as null."""

    while numbers < 16:
        numbers += 1

        header[numbers] = u8(255)

    header["language_code"] = u8(language_code)  # Wii language code.
    header["goo_flag"] = u8(0)  # Flag to make the Globe display "Powered by Goo".
    header["language_select_screen_flag"] = u8(
        language_select_screen_flag)  # Flag to bring up the language select screen.
    header["download_interval"] = u8(
        download_interval)  # Interval in minutes to check for new articles to display on the Wii Menu.
    header["message_offset"] = u32(0)  # Offset for a message.
    header["topics_number"] = u32(0)  # Number of entries for the topics table.
    header["topics_offset"] = u32(0)  # Offset for the topics table.
    header["articles_number"] = u32(0)  # Number of entries for the articles table.
    header["articles_offset"] = u32(0)  # Offset for the articles table.
    header["source_number"] = u32(0)  # Number of entries for the source table.
    header["source_offset"] = u32(0)  # Offset for the source table.
    header["locations_number"] = u32(0)  # Number of entries for the locations.
    header["locations_offset"] = u32(0)  # Offset for the locations table.
    header["pictures_number"] = u32(0)  # Number of entries for the pictures table.
    header["pictures_offset"] = u32(0)  # Offset for the pictures table.
    header["count"] = u16(480)  # Count value.
    header["unknown"] = u16(0)  # Unknown.
    header["wiimenu_articles_number"] = u32(0)  # Number of Wii Menu article entries.
    header["wiimenu_articles_offset"] = u32(0)  # Offset for the Wii Menu article table.
    header["wiimenu_articles_offset"] = offset_count()  # Offset for the Wii Menu article table.

    numbers = 0

    headlines = []

    for article in data.values():
        if numbers < 11:
            if article[3] not in headlines:
                numbers += 1
                headlines.append(article[3])
                header["headline_%s_size" % numbers] = u32(0)  # Size of the headline.
                header["headline_%s_offset" % numbers] = u32(0)  # Offset for the headline.

    return header


"""Headlines to display on the Wii Menu."""


def make_wiimenu_articles():
    wiimenu_articles = collections.OrderedDict()
    dictionaries.append(wiimenu_articles)

    numbers = 0

    headlines = []

    for article in data.values():
        if numbers < 11:
            if article[3] not in headlines:
                numbers += 1
                headlines.append(article[3])
                header["headline_%s_size" % numbers] = u32(len(article[3]))  # Size of the headline.
                header["headline_%s_offset" % numbers] = offset_count()  # Offset for the headline.
                wiimenu_articles["headline_%s" % numbers] = article[3]  # Headline.

                """For some reason, the News Channel uses this padding to separate news articles."""

                if (int(binascii.hexlify(offset_count()), 16) + 2) % 4 == 0:
                    wiimenu_articles["padding_%s" % numbers] = u16(0)  # Padding.
                elif (int(binascii.hexlify(offset_count()), 16) + 4) % 4 == 0:
                    wiimenu_articles["padding_%s" % numbers] = u32(0)  # Padding.

    header["wiimenu_articles_number"] = u32(numbers)  # Number of Wii Menu article entries.

    return wiimenu_articles


"""Topics table."""


def make_topics_table():
    dictionaries.append(topics_table)
    header["topics_offset"] = offset_count()  # Offset for the topics table.
    topics_table["new_topics_offset"] = u32(0)  # Offset for the newest topic.
    topics_table["new_topics_article_size"] = u32(0)  # Size for the amount of articles to choose for the newest topic.
    topics_table["new_topics_article_offset"] = u32(0)  # Offset for the articles to choose for the newest topic.

    numbers = 0

    for _ in topics_news.values():
        numbers += 1
        topics_table["topics_%s_offset" % str(numbers)] = u32(0)  # Offset for the topic.
        topics_table["topics_%s_article_number" % str(numbers)] = u32(
            0)  # Number of articles that will be in a certain topic.
        topics_table["topics_%s_article_offset" % str(numbers)] = u32(
            0)  # Offset for the articles to choose for the topic.

    header["topics_number"] = u32(numbers + 1)  # Number of entries for the topics table.

    return topics_table


"""Timestamps table."""


def make_timestamps_table(mode):
    timestamps_table = collections.OrderedDict()
    dictionaries.append(timestamps_table)

    def timestamps_table_add(topics):
        times = collections.OrderedDict()
        times_files = []

        for numbers in range(0, 24):
            start_time = datetime.today() - timedelta(hours=numbers)
            times_files.append("newstime/newstime.%s-%s-%s-%s" % (str(start_time)[11:-13], str(mode), topics, system))

        for files in times_files:
            if os.path.exists(files):
                newstime = pickle.load(open(files, "rb"))

                for keys in newstime.keys():
                    if keys not in times:
                        times[keys] = newstime[keys]

        times_list = []

        for values in list(times.values()):
            times_list.append(str(values))

        timestamps = ''.join(times_list)  # Timestamps.

        return timestamps

    numbers = 0

    for topics in topics_news.values():
        numbers += 1
        timestamps_add = timestamps_table_add(topics)
        if timestamps_add != 0:
            topics_table["topics_%s_article_number" % numbers] = u32(len(
                timestamps_add) / 8)  # Number of articles that will be in a certain topic. Also, I don't like how it divides the thing by 8 but whatever.
            topics_table[
                "topics_%s_article_offset" % numbers] = offset_count()  # Offset for the articles to choose for the topic.
            timestamps_table["timestamps_%s" % numbers] = timestamps_add  # Timestamps.

    return timestamps_table


"""Articles table."""


def make_articles_table():
    dictionaries.append(articles_table)

    pictures_number = 0
    numbers = 0

    header["articles_offset"] = offset_count()

    for keys, article in data.items():
        numbers += 1
        articles_table["article_%s_number" % numbers] = u32(numbers)  # Number for the article.
        articles_table["source_%s_number" % numbers] = u32(0)  # Number for the source.
        articles_table["location_%s_number" % numbers] = u32(4294967295)  # Number for the location.

        for locations in locations_data.keys():
            for article_name in locations_data[locations][1]:
                if keys == article_name:
                    articles_table["location_%s_number" % numbers] = u32(
                        locations_data.keys().index(locations))  # Number for the location.

        if article[4] is not None:
            articles_table["term_timestamp_%s" % numbers] = get_timestamp(1)  # Timestamp for the term.
            articles_table["picture_%s_number" % numbers] = u32(pictures_number)  # Number for the picture.
            pictures_number += 1
        else:
            articles_table["term_timestamp_%s" % numbers] = u32(0)  # Timestamp for the term.
            articles_table["picture_%s_number" % numbers] = u32(4294967295)  # Number for the picture.

        articles_table["published_time_%s" % numbers] = article[0]  # Published time.
        articles_table["updated_time_%s" % numbers] = get_timestamp(1)  # Updated time.
        articles_table["headline_%s_size" % numbers] = u32(len(article[3]))  # Size of the headline.
        articles_table["headline_%s_offset" % numbers] = u32(0)  # Offset for the headline.
        articles_table["article_%s_size" % numbers] = u32(len(article[2]))  # Size of the article.
        articles_table["article_%s_offset" % numbers] = u32(0)  # Offset for the article.

    header["articles_number"] = u32(numbers)  # Number of entries for the articles table.

    return articles_table


"""Source table."""


def make_source_table():
    dictionaries.append(source_table)
    header["source_offset"] = offset_count()  # Offset for the source table.

    source_articles = []

    """These are the picture and position values."""

    sources = {
        "AP": [0, 1],
        "Reuters": [0, 4],
        "AFP": [4, 4],
        "AFP_French": [4, 4],
        "ANP": [0, 5],
        "ANSA": [6, 6],
        "dpa": [0, 4],
        "SID": [0, 4],
        "NU.nl": [0, 5],
        "Reuters_Japanese": [0, 4],
    }

    numbers = 0

    numbers_article = 0

    for article in data.values():
        if article[8] not in source_articles:
            source_articles.append(article[8])

            source = sources[article[8]]

            source_table["source_picture_%s" % article[8]] = u8(source[0])  # Picture for the source.
            source_table["source_position_%s" % article[8]] = u8(source[1])  # Position for the source.
            source_table["padding_%s" % article[8]] = u16(0)  # Padding.

            source_table["pictures_size_%s" % article[8]] = u32(0)  # Size of the source picture.
            source_table["pictures_offset_%s" % article[8]] = u32(0)  # Offset for the source picture.

            source_table["name_size_%s" % article[8]] = u32(0)  # Size of the source name.
            source_table["name_offset_%s" % article[8]] = u32(0)  # Offset for the source name.

            source_table["copyright_size_%s" % article[8]] = u32(0)  # Size of the copyright.
            source_table["copyright_offset_%s" % article[8]] = u32(0)  # Offset for the copyright.

            numbers += 1

    for article in data.values():
        numbers_article += 1

        articles_table["source_%s_number" % numbers_article] = u32(
            source_articles.index(article[8]))  # Number for the source.

    header["source_number"] = u32(numbers)  # Number of entries for the source table.

    return source_table


"""Locations data table."""


def make_locations_table():
    dictionaries.append(locations_table)
    header["locations_offset"] = offset_count()  # Offset for the locations table.

    locations_number = 0

    for locations_coordinates in locations_data.keys():
        locations_number += 1
        numbers = locations_data.keys().index(locations_coordinates)
        locations_table["location_%s_offset" % numbers] = u32(0)  # Offset for the locations.
        locations_table["location_%s_coordinates" % numbers] = locations_data[locations_coordinates][
            0]  # Coordinates of the locations.

    header["locations_number"] = u32(locations_number)  # Number of entries for the locations.

    return locations_table


"""Pictures table."""


def make_pictures_table():
    dictionaries.append(pictures_table)
    header["pictures_offset"] = offset_count()  # Offset for the pictures table.

    real_numbers = 0

    numbers = 0

    for article in data.values():
        numbers += 1
        if article[4] is not None:
            if article[5] is not None:
                pictures_table["credits_%s_size" % numbers] = u32(len(article[5]))  # Size of the credits.
                pictures_table["credits_%s_offset" % numbers] = u32(0)  # Offset for the credits.
            else:
                pictures_table["credits_%s_size" % numbers] = u32(0)  # Size of the credits.
                pictures_table["credits_%s_offset" % numbers] = u32(0)  # Offset for the credits.

            if article[6] is not None:
                pictures_table["captions_%s_size" % numbers] = u32(len(article[6]))  # Size of the captions.
                pictures_table["captions_%s_offset" % numbers] = u32(0)  # Offset for the captions.
            else:
                pictures_table["captions_%s_size" % numbers] = u32(0)  # Size of the credits.
                pictures_table["captions_%s_offset" % numbers] = u32(0)  # Offset for the captions.

            real_numbers += 1
            pictures_table["pictures_%s_size" % numbers] = u32(len(article[4]))  # Size of the pictures.
            pictures_table["pictures_%s_offset" % numbers] = u32(0)  # Offset for the pictures.

    header["pictures_number"] = u32(real_numbers)  # Number of entries for the pictures table.

    return pictures_table


"""Add the articles."""


def make_articles():
    articles = collections.OrderedDict()
    dictionaries.append(articles)

    numbers = 0

    for article in data.values():
        numbers += 1
        articles_table["headline_%s_offset" % numbers] = offset_count()  # Offset for the headline.
        articles["headline_%s_read" % numbers] = article[3]  # Read the headline.
        articles["padding_%s_headline" % numbers] = u16(0)  # Padding for the headline.
        articles_table["article_%s_offset" % numbers] = offset_count()  # Offset for the article.
        articles["article_%s_read" % numbers] = article[2]  # Read the article.
        articles["padding_%s_article" % numbers] = u16(0)  # Padding for the article.

        if article[6] is not None:
            pictures_table["captions_%s_offset" % numbers] = offset_count()  # Offset for the caption.
            articles["captions_%s_read" % numbers] = article[6]  # Read the caption.
            articles["padding_%s_captions" % numbers] = u16(0)  # Padding for the caption.
        if article[5] is not None:
            pictures_table["credits_%s_offset" % numbers] = offset_count()  # Offset for the credits.
            articles["credits_%s_read" % numbers] = article[5]  # Read the credits.
            articles["padding_%s_credits" % numbers] = u16(0)  # Padding for the credits.

    return articles


"""Add the topics."""


def make_topics(message, message_flag):
    topics = collections.OrderedDict()
    dictionaries.append(topics)

    numbers = 0

    for keys in topics_news.keys():
        numbers += 1
        topics_table["topics_%s_offset" % str(numbers)] = offset_count()  # Offset for the topics.
        topics["topics_%s_read" % numbers] = keys.decode("utf-8").encode("utf-16be")  # Read the topics.
        topics["padding_%s_topics" % numbers] = u16(0)  # Padding for the topics.

    if message_flag == 1:
        header["message_offset"] = offset_count()  # Offset for a message.
        topics["message"] = message  # Message.

    return topics


def make_source_name_copyright():
    source_name_copyright = collections.OrderedDict()
    dictionaries.append(source_name_copyright)

    sources = []

    source_names = {}

    """Text for the copyright. Some of these I had to make up, because if you don't specify a copyright there will be a line that will be in the way in the news article."""

    copyrights = {
        "AP": (
                "Copyright %s The Associated Press. All rights reserved. This material may not be published, broadcast, rewritten or redistributed." % date.today().year).decode(
            "utf-8").encode("utf-16be"),
        "Reuters": (
                "© %s Thomson Reuters. All rights reserved. Republication or redistribution of Thomson Reuters content, including by framing or similar means, is prohibited without the prior written consent of Thomson Reuters. Thomson Reuters and the Kinesis logo are trademarks of Thomson Reuters and its affiliated companies." % date.today().year).decode(
            "utf-8").encode("utf-16be"),
        "AFP": (
                "All reproduction and representation rights reserved. © %s Agence France-Presse" % date.today().year).decode(
            "utf-8").encode("utf-16be"),
        "AFP_French": (
                "Tous droits de reproduction et de diffusion réservés. © %s Agence France-Presse" % date.today().year).decode(
            "utf-8").encode("utf-16be"),
        "ANP": (
                "All reproduction and representation rights reserved. © %s B.V. Algemeen Nederlands Persbureau ANP" % date.today().year).decode(
            "utf-8").encode("utf-16be"),
        "ANSA": (
                "© %s ANSA, Tutti i diritti riservati. Testi, foto, grafica non potranno essere pubblicali, riscritti, commercializzati, distribuiti, videotrasmessi, da parte dagli tanti e del terzi in genere, in alcun modo e sotto qualsiasi forma." % date.today().year).decode(
            "utf-8").encode("utf-16be"),
        "SID": (
                "Alle Rechte für die Wiedergabe, Verwertung und Darstellung reserviert. © %s SID" % date.today().year).decode(
            "utf-8").encode("utf-16be"),
        "dpa": (
                "Alle Rechte für die Wiedergabe, Verwertung und Darstellung reserviert. © %s dpa" % date.today().year).decode(
            "utf-8").encode("utf-16be"),
        "NU.nl": (
                "© %s Sanoma Digital The Netherlands B.V. NU - onderdeel van Sanoma Media Netherlands Group" % date.today().year).decode(
            "utf-8").encode("utf-16be"),
        "Reuters_Japanese": (
                "© Copyright Reuters %s. All rights reserved.　ユーザーは、自己の個人的使用及び非商用目的に限り、このサイトにおけるコンテンツの抜粋をダウンロードまたは印刷することができます。ロイターが事前に書面により承認した場合を除き、ロイター・コンテンツを再発行や再配布すること（フレーミングまたは類似の方法による場合を含む）は、明示的に禁止されています。Reutersおよび地球をデザインしたマークは、登録商標であり、全世界のロイター・グループの商標となっています。 " % date.today().year).decode(
            "utf-8").encode("utf-16be"),
    }

    for article in data.values():
        if article[8] not in sources:
            if article[8] in source_names:
                source_name = source_names[article[8]]

                source_table["name_size_%s" % article[8]] = u32(len(source_name))  # Size of the source name.

                source_table["name_offset_%s" % article[8]] = offset_count()  # Offset for the source name.

                source_name_copyright["source_name_read_%s" % article[8]] = source_name  # Read the source name.
                source_name_copyright["padding_source_name_%s" % article[8]] = u16(0)  # Padding for the source name.

            copyright = copyrights[article[8]]

            source_table["copyright_size_%s" % article[8]] = u32(len(copyright))  # Size of the copyright.

            source_table["copyright_offset_%s" % article[8]] = offset_count()  # Offset for the copyright.

            source_name_copyright["copyright_read_%s" % article[8]] = copyright  # Read the copyright.
            source_name_copyright["padding_copyright_%s" % article[8]] = u16(0)  # Padding for the copyright.

            sources.append(article[8])


"""Add the locations."""


def make_locations():
    locations = collections.OrderedDict()
    dictionaries.append(locations)

    for locations_strings in locations_data.keys():
        numbers = locations_data.keys().index(locations_strings)
        locations_table["location_%s_offset" % numbers] = offset_count()  # Offset for the locations.

        locations["location_%s_read" % numbers] = locations_strings  # Read the locations.
        locations["nullbyte_%s_locations" % numbers] = u16(0)  # Null byte for the locations.

    return locations


"""Add the source pictures."""


def make_source_pictures():
    source_pictures = collections.OrderedDict()
    dictionaries.append(source_pictures)

    source_articles = []

    """These are the news sources which will use a custom JPG for the logo."""

    sources = ["ANP", "AP", "dpa", "Reuters", "SID", "NU.nl", "Reuters_Japanese"]

    for article in data.values():
        if article[8] not in source_articles:
            if article[8] in sources:
                source_articles.append(article[8])

                source_table["pictures_size_%s" % article[8]] = u32(os.path.getsize("./logos/%s.jpg" % article[8]))
                source_table["pictures_offset_%s" % article[8]] = offset_count()

                with open("./logos/%s.jpg" % article[8], "rb") as source_file:
                    source_pictures[
                        "logo_%s" % article[8]] = source_file.read()

    return source_pictures


"""Add the pictures."""


def make_pictures():
    pictures = collections.OrderedDict()
    dictionaries.append(pictures)

    numbers = 0

    for article in data.values():
        numbers += 1
        if article[4] is not None:
            pictures_table["pictures_%s_offset" % numbers] = offset_count()  # Offset for the pictures.
            pictures["pictures_%s_read" % numbers] = article[4]  # Read the pictures.
            pictures["nullbyte_%s_pictures" % numbers] = u8(0)  # Null byte for the pictures.

            for types in ["captions", "credits"]:
                if pictures_table["%s_%s_offset" % (types, numbers)] != u32(0) and pictures_table[
                    "%s_%s_size" % (types, numbers)] == u32(0):
                    pictures_table["%s_%s_offset" % (types, numbers)] = u32(0)

    return pictures


"""Add RiiConnect24 text."""


def make_riiconnect24_text():
    riiconnect24_text = collections.OrderedDict()
    dictionaries.append(riiconnect24_text)

    """This can be used to identify that we made this file."""

    riiconnect24_text["padding"] = u32(0) * 4  # Padding.
    riiconnect24_text["text"] = "RIICONNECT24"  # Text.


"""Write everything to the file."""


def write_dictionary(mode):
    newsfilename = "news.bin.%s.%s.%s" % (str(datetime.utcnow().hour).zfill(2), mode, system)

    for dictionary in dictionaries:
        for values in dictionary.values():
            with open(newsfilename + "-1", "a+") as dest_file:
                dest_file.write(values)

    with open(newsfilename + "-1", "rb") as source_file:
        read = source_file.read()

    with open(newsfilename, "w+") as dest_file:
        dest_file.write(u32(512))
        dest_file.write(u32(len(read) + 12))
        dest_file.write(binascii.unhexlify(format(binascii.crc32(read) & 0xFFFFFFFF, '08x')))
        dest_file.write(read)

    subprocess.call(["%s/lzss" % lzss_path, "-evf", newsfilename], stdout=subprocess.PIPE)

    with open(newsfilename, "rb") as source_file:
        read = source_file.read()

    with open(key_path, "rb") as source_file:
        private_key_data = source_file.read()

    private_key = rsa.PrivateKey.load_pkcs1(private_key_data, "PEM")

    signature = rsa.sign(read, private_key, "SHA-1")

    with open(newsfilename, "wb") as dest_file:
        dest_file.write(binascii.unhexlify("0".zfill(128)))
        dest_file.write(signature)
        dest_file.write(read)

    """Remove the rest of the other files."""

    os.remove(newsfilename + "-1")
