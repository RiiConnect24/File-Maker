#!/usr/bin/python3
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
import json
import pickle
import subprocess
import time
import feedparser
from utils import *
from datetime import timedelta, datetime, date  # Used to get time stuff.

import rsa

from . import newsdownload
from datadog import statsd
from utils import setup_log, log, mkdir_p, u8, u16, u32, u32_littleendian

try:
    with open("./Channels/News_Channel/config.json", "rb") as f:
        config = json.load(f)
except IOError:
    print("Could not load configuration. See config.json.example.")
    exit()

if config["production"]:
    setup_log(config["sentry_url"], True)

sources = {
    # name: What's referred to internally
    # type: Very messy hotfix for Parse, hope to remove after refactor
    # feed: lambda for getting feed
    # entries: fix for ap, making this a lambda is probably overkill but could come in handy later
    # lang: lang the feed is parsed in
    # topic_news: categories
    # cat: category keys used in feed url
    # languages: wii language codes
    # language_code: google maps language code
    # countries: country directories news will be generated for in production
    # country_code: wii country code
    # picture: picture for the source (see make_source_table in newsmake)
    # position: position for the source (see make_source_table in newsmake)

    "ap_english": {
        "name": "AP English",
        "type": "AP",
        "feed": lambda key: requests.get("https://afs-prod.appspot.com/api/v2/feed/tag?tags=%s" % key).json(),
        "entries": lambda feed: feed["cards"],
        "lang": "en",
        "topics_news": collections.OrderedDict([
            ("National News", "national"),
            ("International News", "world"),
            ("Sports", "sports"),
            ("Arts/Entertainment", "entertainment"),
            ("Business", "business"),
            ("Science/Health", "science"),
            ("Technology", "technology"),
            ("Oddities", "oddities")
        ]),
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
        ]),
        "languages": [1, 3, 4],
        "language_code": 1,
        "countries": ["008", "009", "010", "011", "012", "013", "014", "015", "016", "017", "018", "019", "020",
                      "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032", "033",
                      "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046",
                      "047", "048", "049", "050", "051", "052"],
        "country_code": 49,
        "picture": 0,
        "position": 1,
        "copyright": "Copyright %d The Associated Press. All rights reserved. This material may not be published, broadcast, rewritten or redistributed."
    },
    "ap_spanish": {
        "name": "AP Spanish",
        "type": "AP",
        "feed": lambda key: requests.get("https://afs-prod.appspot.com/api/v2/feed/tag?tags=%s" % key).json(),
        "entries": lambda feed: feed["cards"],
        "lang": "es",
        "topics_news": collections.OrderedDict([
            ("Generales", "general"),
            ("Financieras", "finance"),
            ("Deportivas", "sports"),
            ("Espectáculos", "shows")
        ]),
        "cat": collections.OrderedDict([
            ("apf-Noticias", "general"),
            ("apf-Finanzas", "finance"),
            ("apf-Deportes", "sports"),
            ("apf-Entretenimiento", "shows")
        ]),
        "languages": [1, 3, 4],
        "language_code": 4,
        "countries": ["008", "009", "010", "011", "012", "013", "014", "015", "016", "017", "018", "019", "020",
                      "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032", "033",
                      "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046",
                      "047", "048", "049", "050", "051", "052", "065", "066", "067", "074", "076", "077", "078",
                      "079", "082", "083", "088", "094", "095", "096", "098", "105", "107", "108", "110"],
        "country_code": 49,
        "picture": 0,
        "position": 1,
        "copyright": "Copyright %d The Associated Press. All rights reserved. This material may not be published, broadcast, rewritten or redistributed."
    },
    "reuters_europe_english": {
        "name": "Reuters Europe English",
        "type": "Reuters",
        "feed": lambda key: feedparser.parse("http://feeds.reuters.com/reuters/%s.rss" % key),
        "entries": lambda feed: feed.entries,
        "lang": "en",
        "topics_news": collections.OrderedDict([
            ("World", "world"),
            ("UK", "uk"),
            ("Health", "health"),
            ("Science", "science"),
            ("Technology", "technology"),
            ("Entertainment", "entertainment"),
            ("Sports", "sports"),
            ("Lifestyle", "lifestyle")
        ]),
        "cat": collections.OrderedDict([
            ("UKWorldNews", "world"),
            ("UKdomesticNews", "uk"),
            ("UKHealthNews", "health"),
            ("UKScienceNews", "science"),
            ("technology", "technology"),
            ("UKEntertainment", "entertainment"),
            ("UKSportsNews", "sports"),
            ("lifestyle", "lifestyle")
        ]),
        "languages": [1, 2, 3, 4, 5, 6],
        "language_code": 1,
        "countries": ["065", "066", "067", "074", "076", "077", "078", "079", "082", "083", "088", "094", "095",
                      "096", "098", "105", "107", "108", "110"],
        "country_code": 110,
        "picture": 0,
        "position": 4,
        "copyright": "© %d Thomson Reuters. All rights reserved. Republication or redistribution of Thomson Reuters content, including by framing or similar means, is prohibited without the prior written consent of Thomson Reuters. Thomson Reuters and the Kinesis logo are trademarks of Thomson Reuters and its affiliated companies."
    },
    "afp_french": {
        "name": "AFP French",
        "type": "AFP_French",
        "feed": lambda key: feedparser.parse("http://www.lepoint.fr/24h-infos/rss.xml"),
        "entries": lambda feed: feed.entries,
        "lang": "fr",
        "topics_news": collections.OrderedDict([
            ("Monde", "world"),
            ("Sport", "sports"),
            ("Societe", "society"),
            ("Culture", "culture"),
            ("Economie", "economy"),
            ("Politique", "politics")
        ]),
        "cat": collections.OrderedDict([
            ("monde", "world"),
            ("sport", "sports"),
            ("societe", "society"),
            ("culture", "culture"),
            ("economie", "economy"),
            ("politique", "politics")
        ]),
        "languages": [1, 2, 3, 4, 5, 6],
        "language_code": 3,
        "countries": ["008", "009", "010", "011", "012", "013", "014", "015", "016", "017", "018", "019", "020",
                      "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032", "033",
                      "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046",
                      "047", "048", "049", "050", "051", "052", "065", "066", "067", "074", "076", "077", "078",
                      "079", "082", "083", "088", "094", "095", "096", "098", "105", "107", "108", "110"],
        "country_code": 110,
        "picture": 4,
        "position": 4,
        "copyright": "Tous droits de reproduction et de diffusion réservés. © %d Agence France-Presse"
    },
    "donaukurier_german": {
        "name": "AFP German",
        "type": "AFP",
        "feed": lambda key: feedparser.parse("http://www.donaukurier.de/storage/rss/rss/%s.xml" % key),
        "entries": lambda feed: feed.entries,
        "lang": "de",
        "topics_news": collections.OrderedDict([
            ("Nachrichten", "world"),
            ("Wirtschaft", "economy"),
            ("Kultur", "culture")
        ]),
        "cat": collections.OrderedDict([
            ("nachrichten", "world"),
            ("wirtschaft", "economy"),
            ("kultur", "culture")
        ]),
        "languages": [1, 2, 3, 4, 5, 6],
        "language_code": 2,
        "countries": ["065", "066", "067", "074", "076", "077", "078", "079", "082", "083", "088", "094", "095",
                      "096", "098", "105", "107", "108", "110"],
        "country_code": 110,
        "picture": 0,
        "position": 4,
        "copyright": "All reproduction and representation rights reserved. © %d Agence France-Presse"
    },
    "ansa_italian": {
        "name": "ANSA Italian",
        "type": "ANSA",
        "feed": lambda key: feedparser.parse("http://ansa.it/sito/notizie/%s/%s_rss.xml" % (key, key)),
        "entries": lambda feed: feed.entries,
        "lang": "it",
        "topics_news": collections.OrderedDict([
            ("Dal mondo", "world"),
            ("Sport", "sports"),
            ("Economia", "economy"),
            ("Tecnologia", "technology"),
            ("Cultura", "culture")
        ]),
        "cat": collections.OrderedDict([
            ("mondo", "world"),
            ("sport", "sports"),
            ("economia", "economy"),
            ("tecnologia", "technology"),
            ("cultura", "culture")
        ]),
        "languages": [1, 2, 3, 4, 5, 6],
        "language_code": 5,
        "countries": ["065", "066", "067", "074", "076", "077", "078", "079", "082", "083", "088", "094", "095",
                      "096", "098", "105", "107", "108", "110"],
        "country_code": 110,
        "picture": 6,
        "position": 6,
        "copyright": "© %d ANSA, Tutti i diritti riservati. Testi, foto, grafica non potranno essere pubblicali, riscritti, commercializzati, distribuiti, videotrasmessi, da parte dagli tanti e del terzi in genere, in alcun modo e sotto qualsiasi forma."
    },
    "nu_dutch": {
        "name": "NU.nl Dutch",
        "type": "NU.nl",
        "feed": lambda key: feedparser.parse("https://www.nu.nl/rss/%s" % key),
        "entries": lambda feed: feed.entries,
        "lang": "nl",
        "topics_news": collections.OrderedDict([
            ("Algemeen", "general"),
            ("Economie", "economy"),
            ("Sport", "sports"),
            ("Tech", "technology"),
            ("Entertainment", "entertainment"),
            ("Lifestyle", "lifestyle"),
            ("Opmerkelijk", "noteworthy")
        ]),
        "cat": collections.OrderedDict([
            ("Algemeen", "algemeen"),
            ("Economie", "economy"),
            ("Sport", "sports"),
            ("Tech", "technology"),
            ("Entertainment", "entertainment"),
            ("Lifestyle", "lifestyle"),
            ("Opmerkelijk", "noteworthy")
        ]),
        "languages": [1, 2, 3, 4, 5, 6],
        "language_code": 6,
        "countries": ["065", "066", "067", "074", "076", "077", "078", "079", "082", "083", "088", "094", "095",
                      "096", "098", "105", "107", "108", "110"],
        "country_code": 110,
        "picture": 0,
        "position": 5,
        "copyright": "© %d Sanoma Digital The Netherlands B.V. NU - onderdeel van Sanoma Media Netherlands Group"
    },
    "reuters_japanese": {
        "name": "Reuters Japanese",
        "type": "Reuters_Japanese",
        "feed": lambda key: feedparser.parse("https://twitrss.me/twitter_user_to_rss/?user=%s" % key),
        "entries": lambda feed: feed.entries,
        "lang": "en",  # newspaper does not support japanese
        "topics_news": collections.OrderedDict([
            ("ワールド", "world"),
            ("ビジネス", "business"),
            ("スポーツ", "sports"),
            ("テクノロジー", "technology"),
            ("エンタテインメント", "entertainment")
        ]),
        "cat": collections.OrderedDict([
            ("ReutersJpWorld", "world"),
            ("ReutersJpBiz", "business"),
            ("ReutersJpSports", "sports"),
            ("ReutersJpTech", "technology"),
            ("ReutersJpEnt", "entertainment")
        ]),
        "languages": [0],
        "language_code": 0,
        "countries": ["001"],
        "country_code": 1,
        "picture": 0,
        "position": 4,
        "copyright": "© Copyright Reuters %d. All rights reserved.　ユーザーは、自己の個人的使用及び非商用目的に限り、このサイトにおけるコンテンツの抜粋をダウンロードまたは印刷することができます。ロイターが事前に書面により承認した場合を除き、ロイター・コンテンツを再発行や再配布すること（フレーミングまたは類似の方法による場合を含む）は、明示的に禁止されています。Reutersおよび地球をデザインしたマークは、登録商標であり、全世界のロイター・グループの商標となっています。 "

    }
}

"""
Not fully implemented?

"sid_german": {
    "name": "SID",
    "feed": lambda key: feedparser.parse("http://feed43.com/sid.xml"),
    "lang": "de",
    "cat": collections.OrderedDict([
        ("sport", "sport")
    ]),
    "picture": 0,
    "copyright": "Alle Rechte für die Wiedergabe, Verwertung und Darstellung reserviert. © %d SID"
},
"dpa": {
    "picture": 0
    "copyright": "Alle Rechte für die Wiedergabe, Verwertung und Darstellung reserviert. © %d dpa"   
},
"anp": {
    "picture": 0
}
"""

def process_news(mode, source):
    # TODO: Stop getting the current hour multiple times, could cause trouble if script is started right before the next hour

    name = source["name"]

    print("Generating news.bin for %s..." % name)

    global language_code, system

    countries = source["countries"]
    language_code = source["language_code"]
    data = newsdownload.News(source).newsdata

    """If there are more than 22 news articles, delete the rest. This is so the file doesn't get too large."""

    # TODO: Check size of article instead of having a set limit

    i = 0

    for key in list(data.keys()):
        i += 1
        if i > 22:
            del data[key]

    # data = remove_duplicates(data)
    data = remove_duplicates2(data)

    locations_data = newsdownload.locations_download(language_code, data)

    system = "wii"
    make_news = make_news_bin(source, mode, system, data, locations_data)
    system = "wii_u"
    make_news_bin(source, mode, "wii_u", data, locations_data)

    if config["production"]:
        """Log stuff to Datadog."""

        statsd.increment("news.total_files_built")

        """filesize = sum(os.path.getsize(f) - 320 for f in
                       glob.glob("/var/www/wapp.wii.com/news/v2/%s/%s/news.bin.*" % (language_code, countries[0])))

        if filesize > 3712000:
            log("News files exceed the maximum file size amount.", "error")"""

        newsfilename = "news.bin." + str(datetime.utcnow().hour).zfill(2) + "." + mode + "."

        for country in countries:
            copy_file(mode, "wii", country)
            copy_file(mode, "wii_u", country)

        os.remove(newsfilename + "wii")
        os.remove(newsfilename + "wii_u")

    return make_news


"""Copy the temp files to the correct path that the Wii will request from the server."""


def copy_file(mode, console, country):
    if config["force_all"]:
        for hours in range(0, 24):
            newsfilename = "news.bin.%s.%s.%s" % (str(datetime.utcnow().hour).zfill(2), mode, console)
            newsfilename2 = "news.bin.%s" % (str(hours).zfill(2))
            path = "%s/%s/%s/%s" % (config["file_path"], "v3" if console == "wii_u" else "v2", language_code, country)
            mkdir_p(path)
            path = "%s/%s" % (path, newsfilename2)
            subprocess.call(["cp", newsfilename, path])
    else:
        newsfilename = "news.bin.%s.%s.%s" % (str(datetime.utcnow().hour).zfill(2), mode, console)
        newsfilename2 = "news.bin.%s" % (str(datetime.utcnow().hour).zfill(2))
        path = "%s/%s/%s/%s" % (config["file_path"], "v3" if console == "wii_u" else "v2", language_code, country)
        mkdir_p(path)
        path = "%s/%s" % (path, newsfilename2)
        subprocess.call(["cp", newsfilename, path])


"""Run the functions to make the news."""


def make_news_bin(source, mode, console, data, locations_data):
    global system, dictionaries, languages, country_code, language_code

    if source is None:
        print("Could not find %s in sources!")

    topics_news = source["topics_news"]
    languages = source["languages"]
    language_code = source["language_code"]
    country_code = source["country_code"]

    numbers = 0

    if not os.path.exists("newstime"):
        os.mkdir("newstime")

    for topics in list(topics_news.values()):
        newstime = collections.OrderedDict()

        for keys in list(data.keys()):
            if topics in keys:
                numbers += 1

                newstime[data[keys][3]] = get_timestamp(1) + u32(numbers)

        pickle.dump(newstime,
                    open("newstime/newstime.%s-%s-%s-%s" % (str(datetime.now().hour).zfill(2), mode, topics, console),
                         "wb"))

    dictionaries = []

    header = make_header(data)
    make_wiimenu_articles(header, data)
    topics_table = make_topics_table(header, topics_news)
    make_timestamps_table(mode, topics_table, topics_news)
    articles_table = make_articles_table(mode, locations_data, header, data)
    source_table = make_source_table(source, header, articles_table, data)
    locations_table = make_locations_table(header, locations_data)
    pictures_table = make_pictures_table(header, data)
    make_articles(articles_table, pictures_table, data)
    make_topics(topics_table, topics_news)
    make_source_name_copyright(source, source_table, data)
    make_locations(locations_data, locations_table)
    make_source_pictures(source_table, data)
    make_pictures(pictures_table, data)
    make_riiconnect24_text()

    write_dictionary(mode)

    return "\n".join([dnc(article[3]) for article in data.values()])


"""This is a function used to count offsets."""


def offset_count(): return u32(
    12 + sum(len(values) for dictionary in dictionaries for values in list(dictionary.values()) if values))


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

"""Remove duplicate entries from a file. This doesn't work correctly so it's currently not being used."""


def remove_duplicates(data):
    data_dupe = collections.OrderedDict()

    headlines = []

    for k, v in list(data.items()):
        if v[3] not in headlines:
            headlines.append(v[3])
            data_dupe[k] = v
        elif v[3] in headlines:
            for k2, v2 in list(data_dupe.items()):
                if v[3] == v2[3]:
                    del data_dupe[k2]
                    data_dupe[k + k2] = v2

    return data_dupe

"""Remove duplicates a different kind of way!"""

def remove_duplicates2(data):
    headlines = []

    for k,v in list(data.items()):
        if v[3] not in headlines:
            headlines.append(v[3])
        elif v[3] in headlines:
            del data[k]

    return data

"""First part of the header."""


def make_header(data):
    header = collections.OrderedDict()
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
    header["language_select_screen_flag"] = u8(0)  # Flag to bring up the language select screen.
    header["download_interval"] = u8(30)  # Interval in minutes to check for new articles to display on the Wii Menu.
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

    for article in list(data.values()):
        if numbers < 11:
            if article[3] not in headlines:
                numbers += 1
                headlines.append(article[3])
                header["headline_%s_size" % numbers] = u32(0)  # Size of the headline.
                header["headline_%s_offset" % numbers] = u32(0)  # Offset for the headline.

    return header


"""Headlines to display on the Wii Menu."""


def make_wiimenu_articles(header, data):
    wiimenu_articles = collections.OrderedDict()
    dictionaries.append(wiimenu_articles)

    numbers = 0

    headlines = []

    for article in list(data.values()):
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


def make_topics_table(header, topics_news):
    topics_table = collections.OrderedDict()
    dictionaries.append(topics_table)

    header["topics_offset"] = offset_count()  # Offset for the topics table.
    topics_table["new_topics_offset"] = u32(0)  # Offset for the newest topic.
    topics_table["new_topics_article_size"] = u32(0)  # Size for the amount of articles to choose for the newest topic.
    topics_table["new_topics_article_offset"] = u32(0)  # Offset for the articles to choose for the newest topic.

    numbers = 0

    for _ in list(topics_news.values()):
        numbers += 1
        topics_table["topics_%s_offset" % str(numbers)] = u32(0)  # Offset for the topic.
        topics_table["topics_%s_article_number" % str(numbers)] = u32(
            0)  # Number of articles that will be in a certain topic.
        topics_table["topics_%s_article_offset" % str(numbers)] = u32(
            0)  # Offset for the articles to choose for the topic.

    header["topics_number"] = u32(numbers + 1)  # Number of entries for the topics table.

    return topics_table


"""Timestamps table."""


def make_timestamps_table(mode, topics_table, topics_news):
    timestamps_table = collections.OrderedDict()
    dictionaries.append(timestamps_table)

    def timestamps_table_add(topics):
        times = collections.OrderedDict()
        times_files = []

        for numbers in range(0, 24):
            start_time = datetime.today() - timedelta(hours=numbers)
            times_files.append("newstime/newstime.%s-%s-%s-%s" % (str(start_time)[11:-13], str(mode), topics, system))

        try:
            for files in times_files:
                with open(files, "rb") as pickled:
                    newstime = pickle.load(pickled, encoding='bytes') # TODO: Change stored encoding later

                    for keys in list(newstime.keys()):
                        if keys not in times:
                            times[keys] = newstime[keys]
        except:
            pass

        timestamps = b""
        counter = 0

        for value in times.values():
            timestamps = timestamps + value
            counter += 1

        return timestamps, counter

    numbers = 0

    for topics in list(topics_news.values()):
        numbers += 1
        timestamps = timestamps_table_add(topics)
        if timestamps[1] != 0:
            topics_table["topics_%s_article_number" % numbers] = u32(timestamps[1])
            topics_table[
                "topics_%s_article_offset" % numbers] = offset_count()  # Offset for the articles to choose for the topic.
            timestamps_table["timestamps_%s" % numbers] = timestamps[0]  # Timestamps.

    return timestamps_table


"""Articles table."""


def make_articles_table(mode, locations_data, header, data):
    articles_table = collections.OrderedDict()
    dictionaries.append(articles_table)

    p_number = 0
    numbers = 0

    header["articles_offset"] = offset_count()

    for keys, article in list(data.items()):
        numbers += 1
        articles_table["article_%s_number" % numbers] = u32(numbers)  # Number for the article.
        articles_table["source_%s_number" % numbers] = u32(0)  # Number for the source.
        articles_table["location_%s_number" % numbers] = u32(4294967295)  # Number for the location.

        for locations in list(locations_data.keys()):
            for article_name in locations_data[locations][1]:
                if keys == article_name:
                    articles_table["location_%s_number" % numbers] = u32(
                        list(locations_data.keys()).index(locations))  # Number for the location.

        if article[4] is not None:
            articles_table["term_timestamp_%s" % numbers] = get_timestamp(1)  # Timestamp for the term.
            articles_table["picture_%s_number" % numbers] = u32(p_number)  # Number for the picture.
            p_number += 1
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

    if config["production"] and system == "wii":
        statsd.increment("news.total_articles", numbers)
        statsd.increment("news.articles." + mode, numbers)

    return articles_table


"""Source table."""


def make_source_table(source, header, articles_table, data):
    source_table = collections.OrderedDict()
    dictionaries.append(source_table)

    header["source_offset"] = offset_count()  # Offset for the source table.

    source_articles = []

    numbers = 0

    numbers_article = 0

    for a in data.values():
        if a[8] is not source["type"]:
            print(a[8] + " " + source["copyright"])

    for article in list(data.values()):
        if article[8] not in source_articles:
            source_articles.append(article[8])

            source_table["source_picture_%s" % article[8]] = u8(source["picture"])  # Picture for the source.
            source_table["source_position_%s" % article[8]] = u8(source["position"])  # Position for the source.
            source_table["padding_%s" % article[8]] = u16(0)  # Padding.

            source_table["pictures_size_%s" % article[8]] = u32(0)  # Size of the source picture.
            source_table["pictures_offset_%s" % article[8]] = u32(0)  # Offset for the source picture.

            source_table["name_size_%s" % article[8]] = u32(0)  # Size of the source name.
            source_table["name_offset_%s" % article[8]] = u32(0)  # Offset for the source name.

            source_table["copyright_size_%s" % article[8]] = u32(0)  # Size of the copyright.
            source_table["copyright_offset_%s" % article[8]] = u32(0)  # Offset for the copyright.

            numbers += 1

    for article in list(data.values()):
        numbers_article += 1

        articles_table["source_%s_number" % numbers_article] = u32(
            source_articles.index(article[8]))  # Number for the source.

    header["source_number"] = u32(numbers)  # Number of entries for the source table.

    return source_table


"""Locations data table."""


def make_locations_table(header, locations_data):
    locations_table = collections.OrderedDict()
    dictionaries.append(locations_table)

    header["locations_offset"] = offset_count()  # Offset for the locations table.

    locations_number = 0

    for locations_coordinates in list(locations_data.keys()):
        locations_number += 1
        numbers = list(locations_data.keys()).index(locations_coordinates)
        locations_table["location_%s_offset" % numbers] = u32(0)  # Offset for the locations.
        locations_table["location_%s_coordinates" % numbers] = locations_data[locations_coordinates][
            0]  # Coordinates of the locations.

    header["locations_number"] = u32(locations_number)  # Number of entries for the locations.

    if config["production"] and system == "wii":
        statsd.increment("news.total_locations", locations_number)

    return locations_table


"""Pictures table."""


def make_pictures_table(header, data):
    pictures_table = collections.OrderedDict()
    dictionaries.append(pictures_table)

    header["pictures_offset"] = offset_count()  # Offset for the pictures table.

    pictures_number = 0

    numbers = 0

    for article in list(data.values()):
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

            pictures_number += 1
            pictures_table["pictures_%s_size" % numbers] = u32(len(article[4]))  # Size of the pictures.
            pictures_table["pictures_%s_offset" % numbers] = u32(0)  # Offset for the pictures.

    header["pictures_number"] = u32(pictures_number)  # Number of entries for the pictures table.

    if config["production"] and system == "wii":
        statsd.increment("news.total_pictures", pictures_number)

    return pictures_table


"""Add the articles."""


def make_articles(articles_table, pictures_table, data):
    articles = collections.OrderedDict()
    dictionaries.append(articles)

    numbers = 0

    for article in list(data.values()):
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


def make_topics(topics_table, topics_news):
    topics = collections.OrderedDict()
    dictionaries.append(topics)

    numbers = 0

    for keys in list(topics_news.keys()):
        numbers += 1
        topics_table["topics_%s_offset" % str(numbers)] = offset_count()  # Offset for the topics.
        topics["topics_%s_read" % numbers] = enc(keys)  # Read the topics.
        topics["padding_%s_topics" % numbers] = u16(0)  # Padding for the topics.

    return topics


def make_source_name_copyright(source, source_table, data):
    source_name_copyright = collections.OrderedDict()
    dictionaries.append(source_name_copyright)

    source_articles = []

    source_names = {}

    for article in list(data.values()):
        if article[8] not in source_articles:
            if article[8] in source_names:
                source_name = source_names[article[8]]

                source_table["name_size_%s" % article[8]] = u32(len(source_name))  # Size of the source name.

                source_table["name_offset_%s" % article[8]] = offset_count()  # Offset for the source name.

                source_name_copyright["source_name_read_%s" % article[8]] = source_name  # Read the source name.
                source_name_copyright["padding_source_name_%s" % article[8]] = u16(0)  # Padding for the source name.

            copyright = enc(source["copyright"] % date.today().year)

            source_table["copyright_size_%s" % article[8]] = u32(len(copyright))  # Size of the copyright.

            source_table["copyright_offset_%s" % article[8]] = offset_count()  # Offset for the copyright.

            source_name_copyright["copyright_read_%s" % article[8]] = copyright  # Read the copyright.
            source_name_copyright["padding_copyright_%s" % article[8]] = u16(0)  # Padding for the copyright.

            source_articles.append(article[8])


"""Add the locations."""


def make_locations(locations_data, locations_table):
    locations = collections.OrderedDict()
    dictionaries.append(locations)

    for locations_strings in list(locations_data.keys()):
        numbers = list(locations_data.keys()).index(locations_strings)
        locations_table["location_%s_offset" % numbers] = offset_count()  # Offset for the locations.

        locations["location_%s_read" % numbers] = locations_strings  # Read the locations.
        locations["nullbyte_%s_locations" % numbers] = u16(0)  # Null byte for the locations.

    return locations


"""Add the source pictures."""


def make_source_pictures(source_table, data):
    source_pictures = collections.OrderedDict()
    dictionaries.append(source_pictures)

    source_articles = []

    """These are the news sources which will use a custom JPG for the logo."""

    sources = ["ANP", "AP", "dpa", "Reuters", "SID", "NU.nl", "Reuters_Japanese"]

    for article in list(data.values()):
        if article[8] not in source_articles:
            if article[8] in sources:
                source_articles.append(article[8])

                source_table["pictures_offset_%s" % article[8]] = offset_count()

                with open("./Channels/News_Channel/logos/%s.jpg" % article[8], "rb") as source_file:
                    image = source_pictures["logo_%s" % article[8]] = source_file.read()
                    source_table["pictures_size_%s" % article[8]] = u32(len(image))
                

    return source_pictures


"""Add the pictures."""


def make_pictures(pictures_table, data):
    pictures = collections.OrderedDict()
    dictionaries.append(pictures)

    numbers = 0

    for article in list(data.values()):
        numbers += 1
        if article[4] is not None:
            pictures_table["pictures_%s_offset" % numbers] = offset_count()  # Offset for the pictures.
            pictures["pictures_%s_read" % numbers] = article[4]  # Read the pictures.
            pictures["nullbyte_%s_pictures" % numbers] = u8(0)  # Null byte for the pictures.

            for types in ["captions", "credits"]:
                if pictures_table["%s_%s_offset" % (types, numbers)] != u32(0) and pictures_table["%s_%s_size" % (types, numbers)] == u32(0):
                    pictures_table["%s_%s_offset" % (types, numbers)] = u32(0)

    return pictures


"""Add RiiConnect24 text."""


def make_riiconnect24_text():
    riiconnect24_text = collections.OrderedDict()
    dictionaries.append(riiconnect24_text)

    """This can be used to identify that we made this file."""

    riiconnect24_text["padding"] = u32(0) * 4  # Padding.
    riiconnect24_text["text"] = "RIICONNECT24".encode('ascii')  # Text.


"""Write everything to the file."""


def write_dictionary(mode):
    newsfilename = "news.bin.%s.%s.%s" % (str(datetime.utcnow().hour).zfill(2), mode, system)

    for dictionary in dictionaries:
        for name, value in dictionary.items():
            with open(newsfilename + "-1", "ba+") as dest_file:
                dest_file.write(value)



    with open(newsfilename + "-1", "rb") as source_file:
        read = source_file.read()

    with open(newsfilename, "bw+") as dest_file:
        dest_file.write(u32(512))
        dest_file.write(u32(len(read) + 12))
        dest_file.write(binascii.unhexlify(format(binascii.crc32(read) & 0xFFFFFFFF, '08x')))
        dest_file.write(read)

    subprocess.call(["%s/lzss" % config["lzss_path"], "-evf", newsfilename], stdout=subprocess.PIPE)

    with open(newsfilename, "rb") as source_file:
        read = source_file.read()

    with open(config["key_path"], "rb") as source_file:
        private_key_data = source_file.read()

    private_key = rsa.PrivateKey.load_pkcs1(private_key_data, "PEM")

    signature = rsa.sign(read, private_key, "SHA-1")

    with open(newsfilename, "wb") as dest_file:
        dest_file.write(binascii.unhexlify("0".zfill(128)))
        dest_file.write(signature)
        dest_file.write(read)

    """Remove the rest of the other files."""

    os.remove(newsfilename + "-1")

    if not config["production"]:
        print("Wrote " + newsfilename)
