#!/usr/bin/python
# -*- coding: utf-8 -*-

# ===========================================================================
# NEWS CHANNEL GENERATION SCRIPT
# AUTHORS: LARSEN VALLECILLO
# ****************************************************************************
# Copyright (c) 2015-2021 RiiConnect24, and its (Lead) Developers
# ===========================================================================

import binascii
import calendar
import difflib
import glob
import json
import nlzss
import os
import pickle
import requests
import subprocess
import sys
import time
import utils
from datetime import timedelta, datetime, date

import rsa

from . import newsdownload
from datadog import statsd
from utils import setup_log, log, mkdir_p, u8, u16, u32, u32_littleendian

with open("./Channels/News_Channel/config.json", "rb") as f:
    config = json.load(f)  # load config

if config["production"]:
    setup_log(config["sentry_url"], True)  # error logging

sources = {
    "ap_english": {
        "topics_news": {
            "National News": "national",
            "International News": "world",
            "Sports": "sports",
            "Arts/Entertainment": "entertainment",
            "Business": "business",
            "Science/Health": "science",
            "Technology": "technology",
            "Oddities": "oddities",
        },
        "languages": [1, 3, 4],
        "language_code": 1,
        "country_code": 49,  # USA
        "picture": 0,
        "position": 1,
        "copyright": "Copyright {} The Associated Press. All rights reserved. This material may not be published, broadcast, rewritten or redistributed.",
    },
    "ap_spanish": {
        "topics_news": {
            "Generales": "general",
            "Financieras": "finance",
            "Deportivas": "sports",
            "Espectáculos": "shows",
        },
        "languages": [1, 3, 4],
        "language_code": 4,
        "country_code": 49,  # USA
        "picture": 0,
        "position": 1,
        "copyright": "Copyright {} The Associated Press. All rights reserved. This material may not be published, broadcast, rewritten or redistributed.",
    },
    "reuters_europe_english": {
        "topics_news": {
            "World": "world",
            "UK": "uk",
            "Science": "science",
            "Technology": "technology",
            "Entertainment": "entertainment",
            "Sports": "sports",
            "Lifestyle": "lifestyle",
            "Business": "business",
        },
        "languages": [1, 2, 3, 4, 5, 6],
        "language_code": 1,
        "country_code": 110,  # UK
        "picture": 0,
        "position": 4,
        "copyright": "© {} Thomson Reuters. All rights reserved. Republication or redistribution of Thomson Reuters content, including by framing or similar means, is prohibited without the prior written consent of Thomson Reuters. Thomson Reuters and the Kinesis logo are trademarks of Thomson Reuters and its affiliated companies.",
    },
    "afp_french": {
        "topics_news": {
            "Monde": "world",
            "Sport": "sports",
            "Societe": "society",
            "Culture": "culture",
            "Economie": "economy",
            "Politique": "politics",
        },
        "languages": [1, 2, 3, 4, 5, 6],
        "language_code": 3,
        "country_code": 110,  # UK
        "picture": 4,
        "position": 4,
        "copyright": "Tous droits de reproduction et de diffusion réservés. © {} Agence France-Presse",
    },
    "dpa_german": {
        "topics_news": {
            "Deutschland": "germany",
            "Nachrichten": "world",
            "Politik": "politics",
            "Wirtschaft": "economy",
            "Gesundheit": "health",
            "Boulevard": "boulevard",
            "Unterhaltung": "entertainment",
            "Sport": "sports",
        },
        "languages": [1, 2, 3, 4, 5, 6],
        "language_code": 2,
        "country_code": 110,  # UK
        "picture": 4,
        "position": 4,
        "copyright": "Alle Rechte für die Wiedergabe, Verwertung und Darstellung reserviert. © {} dpa",
    },
    "ansa_italian": {
        "topics_news": {
            "Dal mondo": "world",
            "Dall'Italia": "italy",
            "Sport": "sports",
            "Economia": "economy",
            "Tecnologia": "technology",
            "Cultura": "culture",
        },
        "languages": [1, 2, 3, 4, 5, 6],
        "language_code": 5,
        "country_code": 110,  # UK
        "picture": 6,
        "position": 6,
        "copyright": "© {} ANSA, Tutti i diritti riservati. Testi, foto, grafica non potranno essere pubblicali, riscritti, commercializzati, distribuiti, videotrasmessi, da parte dagli tanti e del terzi in genere, in alcun modo e sotto qualsiasi forma.",
    },
    "anp_dutch": {
        "topics_news": {
            "Algemeen": "general",
            "Economie": "economy",
            "Sport": "sports",
            "Entertainment": "entertainment",
            "Lifestyle": "lifestyle",
        },
        "languages": [1, 2, 3, 4, 5, 6],
        "language_code": 6,
        "country_code": 110,  # Uk
        "picture": 0,
        "position": 5,
        "copyright": "© {} B.V. Algemeen Nederlands Persbureau ANP",
    },
    "reuters_japanese": {
        "topics_news": {
            "ワールド": "world",
            "ビジネス": "business",
            "スポーツ": "sports",
            "テクノロジー": "technology",
            "エンタテインメント": "entertainment",
        },
        "languages": [0],
        "language_code": 0,
        "country_code": 1,  # Japan
        "picture": 0,
        "position": 4,
        "copyright": "© Copyright Reuters {}. All rights reserved.　ユーザーは、自己の個人的使用及び非商用目的に限り、このサイトにおけるコンテンツの抜粋をダウンロードまたは印刷することができます。ロイターが事前に書面により承認した場合を除き、ロイター・コンテンツを再発行や再配布すること（フレーミングまたは類似の方法による場合を含む）は、明示的に禁止されています。Reutersおよび地球をデザインしたマークは、登録商標であり、全世界のロイター・グループの商標となっています。 ",
    },
}


def process_news(name, mode, language, region, d):
    print("Making news.bin for {}...\n".format(name))
    global language_code, newsfilename  # I don't like global variables but we're still using them for now

    language_code = language
    data = d.newsdata
    newsfilename = "news.bin.{}.{}".format(str(datetime.utcnow().hour).zfill(2), mode)

    # This is where we do some checks so that the file doesn't get too large
    # There's a limit on how much news we can have in total
    # The maximum we can have is 25, but if the whole directory of news files is too large,
    # multiple news articles will be removed

    i = 0
    limit = 22

    if config[
        "production"
    ]:  # brilliant way to keep the news flowing when it's close to or over the file size limit, surprisingly seems to work?
        path = "{}/v2/{}_{}".format(config["file_path"], language_code, region)
        try:
            size = round(
                float(
                    subprocess.check_output(["du", "-sh", path])
                    .split()[0]
                    .decode("utf-8")
                    .replace("M", "")
                )
                - 3.7,
                1,
            )
            if size >= 3.8:
                limit -= 20
            elif size == 3.7:
                limit -= 15
            elif size == 3.6:
                limit -= 4
            elif size == 3.5:
                limit -= 3

            filesize = sum(
                os.path.getsize(f) - 320
                for f in glob.glob(
                    path + "/news.bin.*"
                )
            )  # let's do one more check to see if the filesize is ok

            if filesize > 3712000:
                log("News files exceed the maximum file size amount.", "error")
        except:
            pass

    for key in list(data.keys()):
        i += 1
        if i > limit:
            del data[key]

    data = remove_duplicates(data)

    locations_data = newsdownload.locations_download(language_code, data)

    make_news = make_news_bin(mode, data, locations_data)

    if config["production"]:
        # Log stuff to Datadog

        statsd.increment("news.total_files_built")

        # This will use a webhook to log that the script has been ran

        webhook = {
            "username": "News Bot",
            "content": "News Data has been updated!",
            "avatar_url": "https://rc24.xyz/images/logo-small.png",
            "attachments": [
                {
                    "fallback": "News Data Update",
                    "color": "#1B691E",
                    "author_name": "RiiConnect24 News Script",
                    "author_icon": "https://rc24.xyz/images/webhooks/news/profile.png",
                    "text": make_news,
                    "title": "Update!",
                    "fields": [
                        {
                            "title": "Script",
                            "value": "News Channel (" + name + ")",
                            "short": "false",
                        }
                    ],
                    "thumb_url": "https://rc24.xyz/images/webhooks/news/%s.png" % mode,
                    "footer": "RiiConnect24 Script",
                    "footer_icon": "https://rc24.xyz/images/logo-small.png",
                    "ts": int(calendar.timegm(datetime.utcnow().timetuple())),
                }
            ],
        }

        for url in config["webhook_urls"]:
            requests.post(url, json=webhook, allow_redirects=True)

        copy_file(region)

        if config["packVFF"]:
            packVFF(region)

        os.remove(newsfilename)


# copy the temp files to the correct path that the Wii will request from the server


def copy(region, hour):
    newsfilename2 = "news.bin.{}".format(str(datetime.utcnow().hour).zfill(2))
    path = "{}/v2/{}_{}".format(config["file_path"], language_code, region)
    mkdir_p(path)
    path = "{}/{}".format(path, newsfilename2)
    subprocess.call(["cp", newsfilename, path])


def copy_file(region):
    if config["force_all"]:
        for hour in range(0, 24):
            copy(region, hour)  # copy to all 24 files
    else:
        copy(region, datetime.utcnow().hour)


# Run the functions to make the news


def make_news_bin(mode, data, locations_data):
    global dictionaries, languages, country_code, language_code

    source = sources[mode]

    if source is None:
        print("Could not find %s in sources.")

    topics_news = source["topics_news"]
    languages = source["languages"]
    language_code = source["language_code"]
    country_code = source["country_code"]

    numbers = 0

    if not os.path.exists("newstime"):
        os.mkdir("newstime")

    for topics in list(topics_news.values()):
        newstime = {}

        for keys in list(data.keys()):
            if topics in keys:
                numbers += 1

                newstime[data[keys][3]] = get_timestamp(1) + u32(numbers)

        pickle.dump(
            newstime,
            open(
                "newstime/newstime.%s-%s-%s-wii"
                % (str(datetime.now().hour).zfill(2), mode, topics),
                "wb",
            ),
        )

    dictionaries = []

    # ton of functions to make news

    header = make_header(data)
    make_wiimenu_articles(header, data)
    topics_table = make_topics_table(header, topics_news)
    make_timestamps_table(mode, topics_table, topics_news)
    articles_table = make_articles_table(mode, locations_data, header, data)
    source_table = make_source_table(header, articles_table, source, data)
    locations_table = make_locations_table(header, locations_data)
    pictures_table = make_pictures_table(header, data)
    make_articles(articles_table, pictures_table, data)
    make_topics(topics_table, topics_news)
    make_source_name_copyright(source_table, source, data)
    make_locations(locations_data, locations_table)
    make_source_pictures(source_table, data)
    make_pictures(pictures_table, data)
    make_riiconnect24_text()

    write_dictionary(mode)

    headlines = []

    for article in list(data.values()):
        try:
            if article[3].replace(b"\n", b"").decode("utf-16be") not in headlines:
                headlines.append(
                    article[3].replace(b"\n", b"").decode("utf-16be") + "\n"
                )
        except UnicodeDecodeError:
            pass

    make_news = "".join(headlines)

    return make_news


# This is a function used to count offsets


def offset_count():
    return u32(
        12
        + sum(
            len(values)
            for dictionary in dictionaries
            for values in list(dictionary.values())
            if values
        )
    )


# Return a timestamp


def get_timestamp(mode):
    if mode == 1:
        return u32(
            int((calendar.timegm(datetime.utcnow().timetuple()) - 946684800) / 60)
        )
    elif mode == 2:
        return u32(
            int((calendar.timegm(datetime.utcnow().timetuple()) - 946684800) / 60)
            + 1500
        )


# Remove duplicate articles


def remove_duplicates(data):
    headlines = []

    for k, v in list(data.items()):
        if v[3] not in headlines:
            headlines.append(v[3])
        elif v[3] in headlines:
            del data[k]

    return data


# Make the news.bin

# First part of the header


def make_header(data):
    header = {}
    dictionaries.append(header)

    header["updated_timestamp_1"] = get_timestamp(1)  # Updated time.
    header["term_timestamp"] = get_timestamp(2)  # Timestamp for the term.
    header["country_code"] = u32_littleendian(country_code)  # Wii Country Code.
    header["updated_timestamp_2"] = get_timestamp(1)  # 3rd timestamp.

    # List of languages that appear on the language select screen

    numbers = 0

    for language in languages:
        numbers += 1

        header["language_select_%s" % numbers] = u8(language)

    # Fills the rest of the languages as null

    while numbers < 16:
        numbers += 1

        header["language_select_%s" % numbers] = u8(255)

    header["language_code"] = u8(language_code)  # Wii language code.
    header["goo_flag"] = u8(0)  # Flag to make the Globe display "Powered by Goo".
    header["language_select_screen_flag"] = u8(
        0
    )  # Flag to bring up the language select screen.
    header["download_interval"] = u8(
        30
    )  # Interval in minutes to check for new articles to display on the Wii Menu.
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
    header[
        "wiimenu_articles_offset"
    ] = offset_count()  # Offset for the Wii Menu article table.

    numbers = 0

    headlines = []

    for article in list(data.values()):
        if numbers < 11:
            if article[3].replace(b"\n", b"") not in headlines:
                numbers += 1
                headlines.append(article[3])
                header["headline_%s_size" % numbers] = u32(0)  # Size of the headline.
                header["headline_%s_offset" % numbers] = u32(
                    0
                )  # Offset for the headline.

    return header


# Headlines to display on the Wii Menu


def make_wiimenu_articles(header, data):
    wiimenu_articles = {}
    dictionaries.append(wiimenu_articles)

    numbers = 0

    headlines = []

    for article in list(data.values()):
        if numbers < 11:
            if article[3] not in headlines:
                numbers += 1
                headlines.append(article[3])
                header["headline_%s_size" % numbers] = u32(
                    len(article[3].replace(b"\n", b""))
                )  # Size of the headline.
                header[
                    "headline_%s_offset" % numbers
                ] = offset_count()  # Offset for the headline.
                wiimenu_articles["headline_%s" % numbers] = article[3].replace(
                    b"\n", b""
                )  # Headline.

                # for some reason, the News Channel uses this padding to separate news articles

                if (int(binascii.hexlify(offset_count()), 16) + 2) % 4 == 0:
                    wiimenu_articles["padding_%s" % numbers] = u16(0)  # Padding.
                elif (int(binascii.hexlify(offset_count()), 16) + 4) % 4 == 0:
                    wiimenu_articles["padding_%s" % numbers] = u32(0)  # Padding.

    header["wiimenu_articles_number"] = u32(
        numbers
    )  # Number of Wii Menu article entries.

    return wiimenu_articles


# Topics table


def make_topics_table(header, topics_news):
    topics_table = {}
    dictionaries.append(topics_table)

    header["topics_offset"] = offset_count()  # Offset for the topics table.
    topics_table["new_topics_offset"] = u32(0)  # Offset for the newest topic.
    topics_table["new_topics_article_size"] = u32(
        0
    )  # Size for the amount of articles to choose for the newest topic.
    topics_table["new_topics_article_offset"] = u32(
        0
    )  # Offset for the articles to choose for the newest topic.

    numbers = 0

    for _ in list(topics_news.values()):
        numbers += 1
        topics_table["topics_%s_offset" % str(numbers)] = u32(
            0
        )  # Offset for the topic.
        topics_table["topics_%s_article_number" % str(numbers)] = u32(
            0
        )  # Number of articles that will be in a certain topic.
        topics_table["topics_%s_article_offset" % str(numbers)] = u32(
            0
        )  # Offset for the articles to choose for the topic.

    header["topics_number"] = u32(
        numbers + 1
    )  # Number of entries for the topics table.

    return topics_table


# Timestamps table


def make_timestamps_table(mode, topics_table, topics_news):
    timestamps_table = {}
    dictionaries.append(timestamps_table)

    def timestamps_table_add(topics):
        times = {}
        times_files = []

        for numbers in range(0, 24):
            start_time = datetime.today() - timedelta(hours=numbers)
            times_files.append(
                "newstime/newstime.%s-%s-%s-wii"
                % (str(start_time)[11:-13], str(mode), topics)
            )

        try:
            for files in times_files:
                with open(files, "rb") as pickled:
                    newstime = pickle.load(
                        pickled, encoding="bytes"
                    )  # TODO: Change stored encoding later

                    for keys in list(newstime.keys()):
                        removed = False

                        if keys not in times:
                            for keys2 in times.keys():
                                if difflib.SequenceMatcher(None, keys.decode("utf-16be"), keys2.decode("utf-16be")).ratio() > 0.85:
                                    removed = True
                                    break
                        else:
                            removed = True
                        
                        if not removed:
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
                "topics_%s_article_offset" % numbers
            ] = offset_count()  # Offset for the articles to choose for the topic.
            timestamps_table["timestamps_%s" % numbers] = timestamps[0]  # Timestamps.

    return timestamps_table


# Articles table


def make_articles_table(mode, locations_data, header, data):
    articles_table = {}
    dictionaries.append(articles_table)

    p_number = 0
    numbers = 0

    header["articles_offset"] = offset_count()

    for keys, article in list(data.items()):
        numbers += 1
        articles_table["article_%s_number" % numbers] = u32(
            numbers
        )  # Number for the article.
        articles_table["source_%s_number" % numbers] = u32(0)  # Number for the source.
        articles_table["location_%s_number" % numbers] = u32(
            4294967295
        )  # Number for the location.

        for locations in list(locations_data.keys()):
            for article_name in locations_data[locations][2]:
                if keys == article_name:
                    articles_table["location_%s_number" % numbers] = u32(
                        list(locations_data.keys()).index(locations)
                    )  # Number for the location.

        if article[4] is not None:
            articles_table["term_timestamp_%s" % numbers] = get_timestamp(
                1
            )  # Timestamp for the term.
            articles_table["picture_%s_number" % numbers] = u32(
                p_number
            )  # Number for the picture.
            p_number += 1
        else:
            articles_table["term_timestamp_%s" % numbers] = u32(
                0
            )  # Timestamp for the term.
            articles_table["picture_%s_number" % numbers] = u32(
                4294967295
            )  # Number for the picture.

        articles_table["published_time_%s" % numbers] = article[0]  # Published time.
        articles_table["updated_time_%s" % numbers] = get_timestamp(1)  # Updated time.
        articles_table["headline_%s_size" % numbers] = u32(
            len(article[3].replace(b"\n", b""))
        )  # Size of the headline.
        articles_table["headline_%s_offset" % numbers] = u32(
            0
        )  # Offset for the headline.
        articles_table["article_%s_size" % numbers] = u32(
            len(article[2])
        )  # Size of the article.
        articles_table["article_%s_offset" % numbers] = u32(
            0
        )  # Offset for the article.

    header["articles_number"] = u32(
        numbers
    )  # Number of entries for the articles table.

    if config["production"]:
        statsd.increment("news.total_articles", numbers)
        statsd.increment("news.articles." + mode, numbers)

    return articles_table


# Source table


def make_source_table(header, articles_table, source, data):
    source_table = {}
    dictionaries.append(source_table)

    header["source_offset"] = offset_count()  # Offset for the source table.

    source_articles = []

    numbers = 0

    numbers_article = 0

    for article in list(data.values()):
        if article[8] not in source_articles:
            source_articles.append(article[8])

            source_table["source_picture_%s" % article[8]] = u8(
                source["picture"]
            )  # Picture for the source.
            source_table["source_position_%s" % article[8]] = u8(
                source["position"]
            )  # Position for the source.
            source_table["padding_%s" % article[8]] = u16(0)  # Padding.

            source_table["pictures_size_%s" % article[8]] = u32(
                0
            )  # Size of the source picture.
            source_table["pictures_offset_%s" % article[8]] = u32(
                0
            )  # Offset for the source picture.

            source_table["name_size_%s" % article[8]] = u32(
                0
            )  # Size of the source name.
            source_table["name_offset_%s" % article[8]] = u32(
                0
            )  # Offset for the source name.

            source_table["copyright_size_%s" % article[8]] = u32(
                0
            )  # Size of the copyright.
            source_table["copyright_offset_%s" % article[8]] = u32(
                0
            )  # Offset for the copyright.

            numbers += 1

    for article in list(data.values()):
        numbers_article += 1

        articles_table["source_%s_number" % numbers_article] = u32(
            source_articles.index(article[8])
        )  # Number for the source.

    header["source_number"] = u32(numbers)  # Number of entries for the source table.

    return source_table


# Locations data table


def make_locations_table(header, locations_data):
    locations_table = {}
    dictionaries.append(locations_table)

    header["locations_offset"] = offset_count()  # Offset for the locations table.

    locations_number = 0

    for loc_coord in list(locations_data.values()):
        locations_table["location_%s_offset" % locations_number] = u32(
            0
        )  # Offset for the locations.
        locations_table["location_%s_coordinates" % locations_number] = loc_coord[
            0
        ]  # Coordinates of the locations.
        locations_number += 1

    header["locations_number"] = u32(
        locations_number
    )  # Number of entries for the locations.

    if config["production"]:
        statsd.increment("news.total_locations", locations_number)

    return locations_table


# Pictures table


def make_pictures_table(header, data):
    pictures_table = {}
    dictionaries.append(pictures_table)

    header["pictures_offset"] = offset_count()  # Offset for the pictures table.

    pictures_number = 0

    numbers = 0

    for article in list(data.values()):
        numbers += 1
        if article[4] is not None:
            if article[5] is not None:
                pictures_table["credits_%s_size" % numbers] = u32(
                    len(article[5])
                )  # Size of the credits.
                pictures_table["credits_%s_offset" % numbers] = u32(
                    0
                )  # Offset for the credits.
            else:
                pictures_table["credits_%s_size" % numbers] = u32(
                    0
                )  # Size of the credits.
                pictures_table["credits_%s_offset" % numbers] = u32(
                    0
                )  # Offset for the credits.

            if article[6] is not None:
                pictures_table["captions_%s_size" % numbers] = u32(
                    len(article[6])
                )  # Size of the captions.
                pictures_table["captions_%s_offset" % numbers] = u32(
                    0
                )  # Offset for the captions.
            else:
                pictures_table["captions_%s_size" % numbers] = u32(
                    0
                )  # Size of the credits.
                pictures_table["captions_%s_offset" % numbers] = u32(
                    0
                )  # Offset for the captions.

            pictures_number += 1
            pictures_table["pictures_%s_size" % numbers] = u32(
                len(article[4])
            )  # Size of the pictures.
            pictures_table["pictures_%s_offset" % numbers] = u32(
                0
            )  # Offset for the pictures.

    header["pictures_number"] = u32(
        pictures_number
    )  # Number of entries for the pictures table.

    if config["production"]:
        statsd.increment("news.total_pictures", pictures_number)

    return pictures_table


# Add the articles


def make_articles(articles_table, pictures_table, data):
    articles = {}
    dictionaries.append(articles)

    numbers = 0

    for article in list(data.values()):
        numbers += 1
        articles_table[
            "headline_%s_offset" % numbers
        ] = offset_count()  # Offset for the headline.
        articles["headline_%s_read" % numbers] = article[3].replace(
            b"\n", b""
        )  # Read the headline.
        articles["padding_%s_headline" % numbers] = u16(0)  # Padding for the headline.
        articles_table[
            "article_%s_offset" % numbers
        ] = offset_count()  # Offset for the article.
        articles["article_%s_read" % numbers] = article[2]  # Read the article.
        articles["padding_%s_article" % numbers] = u16(0)  # Padding for the article.

        if article[4] is not None:
            if article[6] is not None:
                pictures_table[
                    "captions_%s_offset" % numbers
                ] = offset_count()  # Offset for the caption.
                articles["captions_%s_read" % numbers] = article[6]  # Read the caption.
                articles["padding_%s_captions" % numbers] = u16(
                    0
                )  # Padding for the caption.
            if article[5] is not None:
                pictures_table[
                    "credits_%s_offset" % numbers
                ] = offset_count()  # Offset for the credits.
                articles["credits_%s_read" % numbers] = article[5]  # Read the credits.
                articles["padding_%s_credits" % numbers] = u16(
                    0
                )  # Padding for the credits.

    return articles


# Add the topics


def make_topics(topics_table, topics_news):
    topics = {}
    dictionaries.append(topics)

    numbers = 0

    for keys in list(topics_news.keys()):
        numbers += 1
        topics_table[
            "topics_%s_offset" % str(numbers)
        ] = offset_count()  # Offset for the topics.
        topics["topics_%s_read" % numbers] = newsdownload.enc(keys)  # Read the topics.
        topics["padding_%s_topics" % numbers] = u16(0)  # Padding for the topics.

    return topics


def make_source_name_copyright(source_table, source, data):
    source_name_copyright = {}
    dictionaries.append(source_name_copyright)

    sources = []

    source_names = {}

    for article in list(data.values()):
        if article[8] not in sources:
            if article[8] in source_names:
                source_name = source_names[article[8]]

                source_table["name_size_%s" % article[8]] = u32(
                    len(source_name)
                )  # Size of the source name.

                source_table[
                    "name_offset_%s" % article[8]
                ] = offset_count()  # Offset for the source name.

                source_name_copyright[
                    "source_name_read_%s" % article[8]
                ] = source_name  # Read the source name.
                source_name_copyright["padding_source_name_%s" % article[8]] = u16(
                    0
                )  # Padding for the source name.

            copyright = newsdownload.enc(source["copyright"].format(date.today().year))

            source_table["copyright_size_%s" % article[8]] = u32(
                len(copyright)
            )  # Size of the copyright.

            source_table[
                "copyright_offset_%s" % article[8]
            ] = offset_count()  # Offset for the copyright.

            source_name_copyright[
                "copyright_read_%s" % article[8]
            ] = copyright  # Read the copyright.
            source_name_copyright["padding_copyright_%s" % article[8]] = u16(
                0
            )  # Padding for the copyright.

            sources.append(article[8])


# Add the locations


def make_locations(locations_data, locations_table):
    locations = {}
    dictionaries.append(locations)

    numbers = 0

    for loc_text in list(locations_data.values()):
        locations_table[
            "location_%s_offset" % numbers
        ] = offset_count()  # Offset for the locations.

        locations["location_%s_read" % numbers] = loc_text[1]  # Read the locations.
        locations["nullbyte_%s_locations" % numbers] = u16(
            0
        )  # Null byte for the locations.

        numbers += 1

    return locations


# Add the source pictures


def make_source_pictures(source_table, data):
    source_pictures = {}
    dictionaries.append(source_pictures)

    source_articles = []

    sources = [
        "ANP",
        "AP",
        "dpa",
        "Reuters",
        "SID",
    ]  # these are the news sources which will use a custom JPG for the logo

    for article in list(data.values()):
        if article[8] not in source_articles:
            if article[8] in sources:
                source_articles.append(article[8])

                source_table["pictures_offset_%s" % article[8]] = offset_count()

                with open(
                    "./Channels/News_Channel/logos/%s.jpg" % article[8], "rb"
                ) as source_file:
                    image = source_pictures["logo_%s" % article[8]] = source_file.read()
                    source_table["pictures_size_%s" % article[8]] = u32(len(image))

                if source_table["source_picture_%s" % article[8]] != u8(0):
                    source_table["source_picture_%s" % article[8]] = u8(0)

    return source_pictures


# Add the pictures


def make_pictures(pictures_table, data):
    pictures = {}
    dictionaries.append(pictures)

    numbers = 0

    for article in list(data.values()):
        numbers += 1
        if article[4] is not None:
            if "pictures_%s_offset" % numbers in pictures_table:
                pictures_table[
                    "pictures_%s_offset" % numbers
                ] = offset_count()  # Offset for the pictures.
            pictures["pictures_%s_read" % numbers] = article[4]  # Read the pictures.
            pictures["nullbyte_%s_pictures" % numbers] = u8(
                0
            )  # Null byte for the pictures.

            for types in ["captions", "credits"]:
                if pictures_table["%s_%s_offset" % (types, numbers)] != u32(
                    0
                ) and pictures_table["%s_%s_size" % (types, numbers)] == u32(0):
                    pictures_table["%s_%s_offset" % (types, numbers)] = u32(0)

    return pictures


# Add RiiConnect24 text


def make_riiconnect24_text():
    riiconnect24_text = {}
    dictionaries.append(riiconnect24_text)

    # This can be used to identify that we made this file

    riiconnect24_text["padding"] = u32(0) * 4  # Padding.
    riiconnect24_text["text"] = "RIICONNECT24".encode("ascii")  # Text.

def packVFF(region):
    path = "{}/v2/{}_{}/".format(config["file_path"], language_code, region)
    os.makedirs(path + "wc24dl", exist_ok=True)
    for i in range(0, 24):
        with open(path + "news.bin.%s" % str(i).zfill(2), "rb") as source:
            with open(path + "wc24dl/2.BIN.%s" % str(i).zfill(2), "wb") as dest:
                dest.write(source.read()[320:])
    subprocess.call(
        [
            config["winePath"],
            config["prfArcPath"],
            "-v",
            "3712",
            path + "wc24dl",
            path + "wc24dl.vff",
        ],
        stdout=subprocess.DEVNULL,
    )  # Pack VFF
    
    for i in range(0, 24):
        os.remove(path + "wc24dl/2.BIN.%s" % str(i).zfill(2))
    os.rmdir(path + "wc24dl")


# Write everything to the file


def write_dictionary(mode):
    for dictionary in dictionaries:
        for name, value in dictionary.items():
            with open(newsfilename + "-1", "ba+") as dest_file:
                dest_file.write(value)

    with open(newsfilename + "-1", "rb") as source_file:
        read = source_file.read()

    with open(newsfilename, "bw+") as dest_file:
        dest_file.write(u32(512))
        dest_file.write(u32(len(read) + 12))
        dest_file.write(
            binascii.unhexlify(format(binascii.crc32(read) & 0xFFFFFFFF, "08x"))
        )
        dest_file.write(read)

    if config["production"]:
        nlzss.encode_file(newsfilename, newsfilename)

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


    # Remove the rest of the other files

    os.remove(newsfilename + "-1")

    print("\n")
    print("Wrote " + newsfilename)
