#!/usr/bin/python
# -*- coding: utf-8 -*-

# ===========================================================================
# NEWS CHANNEL GENERATION SCRIPT
# AUTHORS: LARSEN VALLECILLO
# ****************************************************************************
# Copyright (c) 2015-2022 RiiConnect24, and its (Lead) Developers
# ===========================================================================

import binascii
import calendar
import CloudFlare
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
        "countries": [
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
        ],
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
        "countries": [
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
        ],
    },
    "ap_canada": {
        "topics_news": {
            "National News": "canada",
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
        "country_code": 18,  # Canada
        "picture": 0,
        "position": 1,
        "copyright": "Copyright {} The Associated Press. All rights reserved. This material may not be published, broadcast, rewritten or redistributed.",
        "countries": [
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
        ],
    },
    "ap_australia": {
        "topics_news": {
            "National News": "australia",
            "International News": "world",
            "Sports": "sports",
            "Arts/Entertainment": "entertainment",
            "Business": "business",
            "Science/Health": "science",
            "Technology": "technology",
            "Oddities": "oddities",
        },
        "languages": [1, 2, 3, 4, 5, 6],
        "language_code": 1,
        "country_code": 65,  # Australia
        "picture": 0,
        "position": 1,
        "copyright": "Copyright {} The Associated Press. All rights reserved. This material may not be published, broadcast, rewritten or redistributed.",
        "countries": [
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
        ],
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
        "countries": [
            65,
            66,
            67,
            74,
            76,
            77,
            78,
            79,
            82,
            83,
            88,
            94,
            95,
            96,
            97,
            98,
            105,
            107,
            108,
            110,
        ],
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
        "picture": 0,
        "position": 4,
        "copyright": "Tous droits de reproduction et de diffusion réservés. © {} Agence France-Presse",
        "countries": [
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
            65,
            66,
            67,
            74,
            76,
            77,
            78,
            79,
            82,
            83,
            88,
            94,
            95,
            96,
            97,
            98,
            105,
            107,
            108,
            110,
        ],
    },
    "afp_german": {
        "topics_news": {
            "Politik": "politics",
            "Wirtschaft": "economy",
            "Gesundheit": "health",
            "Panorama": "panorama",
            "Sport": "sports",
        },
        "languages": [1, 2, 3, 4, 5, 6],
        "language_code": 2,
        "country_code": 110,  # UK
        "picture": 0,
        "position": 4,
        "copyright": "© {} AFP",
        "countries": [
            65,
            66,
            67,
            74,
            76,
            77,
            78,
            79,
            82,
            83,
            88,
            94,
            95,
            96,
            97,
            98,
            105,
            107,
            108,
            110,
        ],
    },
    "afp_spanish": {
        "topics_news": {
            "Mundo": "world",
            "Cultura": "culture",
            "Sociedad": "society",
            "Economía": "economy",
            "Deportes": "sports",
            "Gente": "people",
        },
        "languages": [1, 2, 3, 4, 5, 6],
        "language_code": 4,
        "country_code": 110,  # UK
        "picture": 0,
        "position": 4,
        "copyright": "© {} AFP",
        "countries": [
            65,
            66,
            67,
            74,
            76,
            77,
            78,
            79,
            82,
            83,
            88,
            94,
            95,
            96,
            97,
            98,
            105,
            107,
            108,
            110,
        ],
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
        "countries": [
            65,
            66,
            67,
            74,
            76,
            77,
            78,
            79,
            82,
            83,
            88,
            94,
            95,
            96,
            97,
            98,
            105,
            107,
            108,
            110,
        ],
    },
    "anp_dutch": {
        "topics_news": {
            "Algemeen": "general",
            "Regionaal": "national",
            "Economie": "economy",
            "Sport": "sports",
            "Entertainment": "entertainment",
            "Lifestyle": "lifestyle",
        },
        "languages": [1, 2, 3, 4, 5, 6],
        "language_code": 6,
        "country_code": 110,  # UK
        "picture": 0,
        "position": 5,
        "copyright": "© {} B.V. Algemeen Nederlands Persbureau ANP",
        "countries": [
            65,
            66,
            67,
            74,
            76,
            77,
            78,
            79,
            82,
            83,
            88,
            94,
            95,
            96,
            97,
            98,
            105,
            107,
            108,
            110,
        ],
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
        "countries": [1],
    },
}


class NewsMake:
    def __init__(self, name, mode, language, region, d):
        self.name = name
        self.mode = mode
        self.language = language
        self.region = region
        self.d = d

        self.process_news()

    def process_news(self):
        print("Making news.bin for {}...\n".format(self.name))

        self.language_code = self.language
        self.data = self.d.newsdata
        self.newsfilename = "news.bin.{}.{}".format(
            str(datetime.utcnow().hour).zfill(2), self.mode
        )

        # This is where we do some checks so that the file doesn't get too large
        # There's a limit on how much news we can have in total
        # The maximum we can have is 25, but if the whole directory of news files is too large,
        # multiple news articles will be removed

        i = 0
        limit = 20

        if config[
            "production"
        ]:  # brilliant way to keep the news flowing when it's close to or over the file size limit, surprisingly seems to work?
            path = "{}/v2/{}_{}".format(
                config["file_path"], self.language_code, self.region
            )
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
                    os.path.getsize(f) - 320 for f in glob.glob(path + "/news.bin.*")
                )  # let's do one more check to see if the filesize is ok

                if filesize > 3712000:
                    log("News files exceed the maximum file size amount.", "error")
            except:
                pass

        for key in list(self.data.keys()):
            i += 1
            if i > limit:
                del self.data[key]

        self.data = self.remove_duplicates(self.data)

        self.locations_data = newsdownload.locations_download(
            self.language_code, self.data
        )

        make_news = self.make_news_bin()

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
                                "value": "News Channel (" + self.name + ")",
                                "short": "false",
                            }
                        ],
                        "thumb_url": "https://rc24.xyz/images/webhooks/news/%s.png"
                        % self.mode,
                        "footer": "RiiConnect24 Script",
                        "footer_icon": "https://rc24.xyz/images/logo-small.png",
                        "ts": int(calendar.timegm(datetime.utcnow().timetuple())),
                    }
                ],
            }

            for url in config["webhook_urls"]:
                requests.post(url, json=webhook, allow_redirects=True)

            self.copy_file()

            if config["packVFF"]:
                self.packVFF()

            os.remove(self.newsfilename)

    # Remove duplicate articles

    def remove_duplicates(self, data):
        headlines = []

        for k, v in list(data.items()):
            if v[3] not in headlines:
                headlines.append(v[3])
            elif v[3] in headlines:
                del data[k]

        return data

    # Run the functions to make the news

    def make_news_bin(self):
        self.source = sources[self.mode]

        if self.source is None:
            print("Could not find %s in sources.")

        self.topics_news = self.source["topics_news"]
        self.languages = self.source["languages"]
        self.country_code = self.source["country_code"]

        numbers = 0

        if not os.path.exists("newstime"):
            os.mkdir("newstime")

        for topics in list(self.topics_news.values()):
            newstime = {}

            for keys in list(self.data.keys()):
                if topics in keys:
                    numbers += 1

                    newstime[self.data[keys][3]] = self.get_timestamp(1) + u32(numbers)

            pickle.dump(
                newstime,
                open(
                    "newstime/newstime.%s-%s-%s-wii"
                    % (str(datetime.now().hour).zfill(2), self.mode, topics),
                    "wb",
                ),
            )

        self.dictionaries = []

        # ton of functions to make news

        self.make_header()
        self.make_wiimenu_articles()
        self.make_topics_table()
        self.make_timestamps_table()
        self.make_articles_table()
        self.make_source_table()
        self.make_locations_table()
        self.make_pictures_table()
        self.make_articles()
        self.make_topics()
        self.make_source_name_copyright()
        self.make_locations()
        self.make_source_pictures()
        self.make_pictures()
        self.make_riiconnect24_text()

        self.write_dictionary()

        headlines = []

        for article in list(self.data.values()):
            try:
                if article[3].replace(b"\n", b"").decode("utf-16be") not in headlines:
                    headlines.append(
                        article[3].replace(b"\n", b"").decode("utf-16be") + "\n"
                    )
            except UnicodeDecodeError:
                pass

        make_news = "".join(headlines)

        self.purge_cache()

        return make_news

    # First part of the header

    def make_header(self):
        self.header = {}
        self.dictionaries.append(self.header)

        self.header["updated_timestamp_1"] = self.get_timestamp(1)  # Updated time.
        self.header["term_timestamp"] = self.get_timestamp(2)  # Timestamp for the term.
        self.header["country_code"] = u32_littleendian(
            self.country_code
        )  # Wii Country Code.
        self.header["updated_timestamp_2"] = self.get_timestamp(1)  # 3rd timestamp.

        # List of languages that appear on the language select screen

        numbers = 0

        for language in self.languages:
            numbers += 1

            self.header["language_select_%s" % numbers] = u8(language)

        # Fills the rest of the languages as null

        while numbers < 16:
            numbers += 1

            self.header["language_select_%s" % numbers] = u8(255)

        self.header["language_code"] = u8(self.language_code)  # Wii language code.
        self.header["goo_flag"] = u8(
            0
        )  # Flag to make the Globe display "Powered by Goo".
        self.header["language_select_screen_flag"] = u8(
            0
        )  # Flag to bring up the language select screen.
        self.header["download_interval"] = u8(
            30
        )  # Interval in minutes to check for new articles to display on the Wii Menu.
        self.header["message_offset"] = u32(0)  # Offset for a message.
        self.header["topics_number"] = u32(0)  # Number of entries for the topics table.
        self.header["topics_offset"] = u32(0)  # Offset for the topics table.
        self.header["articles_number"] = u32(
            0
        )  # Number of entries for the articles table.
        self.header["articles_offset"] = u32(0)  # Offset for the articles table.
        self.header["source_number"] = u32(0)  # Number of entries for the source table.
        self.header["source_offset"] = u32(0)  # Offset for the source table.
        self.header["locations_number"] = u32(0)  # Number of entries for the locations.
        self.header["locations_offset"] = u32(0)  # Offset for the locations table.
        self.header["pictures_number"] = u32(
            0
        )  # Number of entries for the pictures table.
        self.header["pictures_offset"] = u32(0)  # Offset for the pictures table.
        self.header["count"] = u16(480)  # Count value.
        self.header["unknown"] = u16(0)  # Unknown.
        self.header["wiimenu_articles_number"] = u32(
            0
        )  # Number of Wii Menu article entries.
        self.header["wiimenu_articles_offset"] = u32(
            0
        )  # Offset for the Wii Menu article table.
        self.header[
            "wiimenu_articles_offset"
        ] = self.offset_count()  # Offset for the Wii Menu article table.

        numbers = 0

        headlines = []

        for article in list(self.data.values()):
            if numbers < 11:
                if article[3].replace(b"\n", b"") not in headlines:
                    numbers += 1
                    headlines.append(article[3])
                    self.header["headline_%s_size" % numbers] = u32(
                        0
                    )  # Size of the headline.
                    self.header["headline_%s_offset" % numbers] = u32(
                        0
                    )  # Offset for the headline.

    # Headlines to display on the Wii Menu

    def make_wiimenu_articles(self):
        self.wiimenu_articles = {}
        self.dictionaries.append(self.wiimenu_articles)

        numbers = 0

        headlines = []

        for article in list(self.data.values()):
            if numbers < 11:
                if article[3] not in headlines:
                    numbers += 1
                    headlines.append(article[3])
                    self.header["headline_%s_size" % numbers] = u32(
                        len(article[3].replace(b"\n", b""))
                    )  # Size of the headline.
                    self.header[
                        "headline_%s_offset" % numbers
                    ] = self.offset_count()  # Offset for the headline.
                    self.wiimenu_articles["headline_%s" % numbers] = article[3].replace(
                        b"\n", b""
                    )  # Headline.

                    # for some reason, the News Channel uses this padding to separate news articles

                    if (int(binascii.hexlify(self.offset_count()), 16) + 2) % 4 == 0:
                        self.wiimenu_articles["padding_%s" % numbers] = u16(
                            0
                        )  # Padding.
                    elif (int(binascii.hexlify(self.offset_count()), 16) + 4) % 4 == 0:
                        self.wiimenu_articles["padding_%s" % numbers] = u32(
                            0
                        )  # Padding.

        self.header["wiimenu_articles_number"] = u32(
            numbers
        )  # Number of Wii Menu article entries.

        return self.wiimenu_articles

    # Topics table

    def make_topics_table(self):
        self.topics_table = {}
        self.dictionaries.append(self.topics_table)

        self.header[
            "topics_offset"
        ] = self.offset_count()  # Offset for the topics table.
        self.topics_table["new_topics_offset"] = u32(0)  # Offset for the newest topic.
        self.topics_table["new_topics_article_size"] = u32(
            0
        )  # Size for the amount of articles to choose for the newest topic.
        self.topics_table["new_topics_article_offset"] = u32(
            0
        )  # Offset for the articles to choose for the newest topic.

        numbers = 0

        for _ in list(self.topics_news.values()):
            numbers += 1
            self.topics_table["topics_%s_offset" % str(numbers)] = u32(
                0
            )  # Offset for the topic.
            self.topics_table["topics_%s_article_number" % str(numbers)] = u32(
                0
            )  # Number of articles that will be in a certain topic.
            self.topics_table["topics_%s_article_offset" % str(numbers)] = u32(
                0
            )  # Offset for the articles to choose for the topic.

        self.header["topics_number"] = u32(
            numbers + 1
        )  # Number of entries for the topics table.

        return self.topics_table

    def timestamps_table_add(self, topics):
        times = {}
        times_files = []

        for numbers in range(0, 24):
            start_time = datetime.today() - timedelta(hours=numbers)
            times_files.append(
                "newstime/newstime.%s-%s-%s-wii"
                % (str(start_time)[11:-13], str(self.mode), topics)
            )

        try:
            for files in times_files:
                with open(files, "rb") as pickled:
                    newstime = pickle.load(
                        pickled, encoding="bytes"
                    )  # TODO: Change stored encoding later

                    for keys in list(newstime.keys()):
                        removed = False

                        # Check if any headlines are similar and exclude them.

                        if keys not in times:
                            for keys2 in times.keys():
                                if (
                                    difflib.SequenceMatcher(
                                        None,
                                        keys.decode("utf-16be"),
                                        keys2.decode("utf-16be"),
                                    ).ratio()
                                    > 0.85
                                ):
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

    # Timestamps table

    def make_timestamps_table(self):
        self.timestamps_table = {}
        self.dictionaries.append(self.timestamps_table)

        numbers = 0

        for topics in list(self.topics_news.values()):
            numbers += 1
            timestamps = self.timestamps_table_add(topics)
            if timestamps[1] != 0:
                self.topics_table["topics_%s_article_number" % numbers] = u32(
                    timestamps[1]
                )
                self.topics_table[
                    "topics_%s_article_offset" % numbers
                ] = (
                    self.offset_count()
                )  # Offset for the articles to choose for the topic.
                self.timestamps_table["timestamps_%s" % numbers] = timestamps[
                    0
                ]  # Timestamps.

    # Articles table

    def make_articles_table(self):
        self.articles_table = {}
        self.dictionaries.append(self.articles_table)

        p_number = 0
        numbers = 0

        self.header["articles_offset"] = self.offset_count()

        for keys, article in list(self.data.items()):
            numbers += 1
            self.articles_table["article_%s_number" % numbers] = u32(
                numbers
            )  # Number for the article.
            self.articles_table["source_%s_number" % numbers] = u32(
                0
            )  # Number for the source.
            self.articles_table["location_%s_number" % numbers] = u32(
                4294967295
            )  # Number for the location.

            for locations in list(self.locations_data.keys()):
                for article_name in self.locations_data[locations][2]:
                    if keys == article_name:
                        self.articles_table["location_%s_number" % numbers] = u32(
                            list(self.locations_data.keys()).index(locations)
                        )  # Number for the location.

            if article[4] is not None:
                self.articles_table["term_timestamp_%s" % numbers] = self.get_timestamp(
                    1
                )  # Timestamp for the term.
                self.articles_table["picture_%s_number" % numbers] = u32(
                    p_number
                )  # Number for the picture.
                p_number += 1
            else:
                self.articles_table["term_timestamp_%s" % numbers] = u32(
                    0
                )  # Timestamp for the term.
                self.articles_table["picture_%s_number" % numbers] = u32(
                    4294967295
                )  # Number for the picture.

            self.articles_table["published_time_%s" % numbers] = article[
                0
            ]  # Published time.
            self.articles_table["updated_time_%s" % numbers] = self.get_timestamp(
                1
            )  # Updated time.
            self.articles_table["headline_%s_size" % numbers] = u32(
                len(article[3].replace(b"\n", b""))
            )  # Size of the headline.
            self.articles_table["headline_%s_offset" % numbers] = u32(
                0
            )  # Offset for the headline.
            self.articles_table["article_%s_size" % numbers] = u32(
                len(article[2])
            )  # Size of the article.
            self.articles_table["article_%s_offset" % numbers] = u32(
                0
            )  # Offset for the article.

        self.header["articles_number"] = u32(
            numbers
        )  # Number of entries for the articles table.

        if config["production"]:
            statsd.increment("news.total_articles", numbers)

    # Source table

    def make_source_table(self):
        self.source_table = {}
        self.dictionaries.append(self.source_table)

        self.header[
            "source_offset"
        ] = self.offset_count()  # Offset for the source table.

        source_articles = []

        numbers = 0

        numbers_article = 0

        for article in list(self.data.values()):
            if article[8] not in source_articles:
                source_articles.append(article[8])

                self.source_table["source_picture_%s" % article[8]] = u8(
                    self.source["picture"]
                )  # Picture for the source.
                self.source_table["source_position_%s" % article[8]] = u8(
                    self.source["position"]
                )  # Position for the source.
                self.source_table["padding_%s" % article[8]] = u16(0)  # Padding.

                self.source_table["pictures_size_%s" % article[8]] = u32(
                    0
                )  # Size of the source picture.
                self.source_table["pictures_offset_%s" % article[8]] = u32(
                    0
                )  # Offset for the source picture.

                self.source_table["name_size_%s" % article[8]] = u32(
                    0
                )  # Size of the source name.
                self.source_table["name_offset_%s" % article[8]] = u32(
                    0
                )  # Offset for the source name.

                self.source_table["copyright_size_%s" % article[8]] = u32(
                    0
                )  # Size of the copyright.
                self.source_table["copyright_offset_%s" % article[8]] = u32(
                    0
                )  # Offset for the copyright.

                numbers += 1

        for article in list(self.data.values()):
            numbers_article += 1

            self.articles_table["source_%s_number" % numbers_article] = u32(
                source_articles.index(article[8])
            )  # Number for the source.

        self.header["source_number"] = u32(
            numbers
        )  # Number of entries for the source table.

    # Locations data table

    def make_locations_table(self):
        self.locations_table = {}
        self.dictionaries.append(self.locations_table)

        self.header[
            "locations_offset"
        ] = self.offset_count()  # Offset for the locations table.

        locations_number = 0

        for loc_coord in list(self.locations_data.values()):
            self.locations_table["location_%s_offset" % locations_number] = u32(
                0
            )  # Offset for the locations.
            self.locations_table[
                "location_%s_coordinates" % locations_number
            ] = loc_coord[
                0
            ]  # Coordinates of the locations.
            locations_number += 1

        self.header["locations_number"] = u32(
            locations_number
        )  # Number of entries for the locations.

        if config["production"]:
            statsd.increment("news.total_locations", locations_number)

    # Pictures table

    def make_pictures_table(self):
        self.pictures_table = {}
        self.dictionaries.append(self.pictures_table)

        self.header[
            "pictures_offset"
        ] = self.offset_count()  # Offset for the pictures table.

        pictures_number = 0

        numbers = 0

        for article in list(self.data.values()):
            numbers += 1
            if article[4] is not None:
                if article[5] is not None:
                    self.pictures_table["credits_%s_size" % numbers] = u32(
                        len(article[5])
                    )  # Size of the credits.
                    self.pictures_table["credits_%s_offset" % numbers] = u32(
                        0
                    )  # Offset for the credits.
                else:
                    self.pictures_table["credits_%s_size" % numbers] = u32(
                        0
                    )  # Size of the credits.
                    self.pictures_table["credits_%s_offset" % numbers] = u32(
                        0
                    )  # Offset for the credits.

                if article[6] is not None:
                    self.pictures_table["captions_%s_size" % numbers] = u32(
                        len(article[6])
                    )  # Size of the captions.
                    self.pictures_table["captions_%s_offset" % numbers] = u32(
                        0
                    )  # Offset for the captions.
                else:
                    self.pictures_table["captions_%s_size" % numbers] = u32(
                        0
                    )  # Size of the credits.
                    self.pictures_table["captions_%s_offset" % numbers] = u32(
                        0
                    )  # Offset for the captions.

                pictures_number += 1
                self.pictures_table["pictures_%s_size" % numbers] = u32(
                    len(article[4])
                )  # Size of the pictures.
                self.pictures_table["pictures_%s_offset" % numbers] = u32(
                    0
                )  # Offset for the pictures.

        self.header["pictures_number"] = u32(
            pictures_number
        )  # Number of entries for the pictures table.

        if config["production"]:
            statsd.increment("news.total_pictures", pictures_number)

    # Add the articles

    def make_articles(self):
        self.articles = {}
        self.dictionaries.append(self.articles)

        numbers = 0

        for article in list(self.data.values()):
            numbers += 1
            self.articles_table[
                "headline_%s_offset" % numbers
            ] = self.offset_count()  # Offset for the headline.
            self.articles["headline_%s_read" % numbers] = article[3].replace(
                b"\n", b""
            )  # Read the headline.
            self.articles["padding_%s_headline" % numbers] = u16(
                0
            )  # Padding for the headline.
            self.articles_table[
                "article_%s_offset" % numbers
            ] = self.offset_count()  # Offset for the article.
            self.articles["article_%s_read" % numbers] = article[2]  # Read the article.
            self.articles["padding_%s_article" % numbers] = u16(
                0
            )  # Padding for the article.

            if article[4] is not None:
                if article[6] is not None:
                    self.pictures_table[
                        "captions_%s_offset" % numbers
                    ] = self.offset_count()  # Offset for the caption.
                    self.articles["captions_%s_read" % numbers] = article[
                        6
                    ]  # Read the caption.
                    self.articles["padding_%s_captions" % numbers] = u16(
                        0
                    )  # Padding for the caption.
                if article[5] is not None:
                    self.pictures_table[
                        "credits_%s_offset" % numbers
                    ] = self.offset_count()  # Offset for the credits.
                    self.articles["credits_%s_read" % numbers] = article[
                        5
                    ]  # Read the credits.
                    self.articles["padding_%s_credits" % numbers] = u16(
                        0
                    )  # Padding for the credits.

    # Add the topics

    def make_topics(self):
        self.topics = {}
        self.dictionaries.append(self.topics)

        numbers = 0

        for keys in list(self.topics_news.keys()):
            numbers += 1
            self.topics_table[
                "topics_%s_offset" % str(numbers)
            ] = self.offset_count()  # Offset for the topics.
            self.topics["topics_%s_read" % numbers] = newsdownload.enc(
                keys
            )  # Read the topics.
            self.topics["padding_%s_topics" % numbers] = u16(
                0
            )  # Padding for the topics.

    def make_source_name_copyright(self):
        self.source_name_copyright = {}
        self.dictionaries.append(self.source_name_copyright)

        sources = []

        source_names = {}

        for article in list(self.data.values()):
            if article[8] not in sources:
                if article[8] in source_names:
                    source_name = source_names[article[8]]

                    self.source_table["name_size_%s" % article[8]] = u32(
                        len(source_name)
                    )  # Size of the source name.

                    self.source_table[
                        "name_offset_%s" % article[8]
                    ] = self.offset_count()  # Offset for the source name.

                    self.source_name_copyright[
                        "source_name_read_%s" % article[8]
                    ] = source_name  # Read the source name.
                    self.source_name_copyright[
                        "padding_source_name_%s" % article[8]
                    ] = u16(
                        0
                    )  # Padding for the source name.

                copyright = newsdownload.enc(
                    self.source["copyright"].format(date.today().year)
                )

                self.source_table["copyright_size_%s" % article[8]] = u32(
                    len(copyright)
                )  # Size of the copyright.

                self.source_table[
                    "copyright_offset_%s" % article[8]
                ] = self.offset_count()  # Offset for the copyright.

                self.source_name_copyright[
                    "copyright_read_%s" % article[8]
                ] = copyright  # Read the copyright.
                self.source_name_copyright["padding_copyright_%s" % article[8]] = u16(
                    0
                )  # Padding for the copyright.

                sources.append(article[8])

    # Add the locations

    def make_locations(self):
        self.locations = {}
        self.dictionaries.append(self.locations)

        numbers = 0

        for loc_text in list(self.locations_data.values()):
            self.locations_table[
                "location_%s_offset" % numbers
            ] = self.offset_count()  # Offset for the locations.

            self.locations["location_%s_read" % numbers] = loc_text[
                1
            ]  # Read the locations.
            self.locations["nullbyte_%s_locations" % numbers] = u16(
                0
            )  # Null byte for the locations.

            numbers += 1

    # Add the source pictures

    def make_source_pictures(self):
        self.source_pictures = {}
        self.dictionaries.append(self.source_pictures)

        source_articles = []

        sources = [
            "AFP_French",
            "AFP_German",
            "AFP_Spanish",
            "ANP",
            "AP",
            "CanadianPress",
            "Reuters",
            "SID",
        ]  # these are the news sources which will use a custom JPG for the logo

        for article in list(self.data.values()):
            if article[8] not in source_articles:
                if article[8] in sources:
                    source_articles.append(article[8])

                    self.source_table[
                        "pictures_offset_%s" % article[8]
                    ] = self.offset_count()

                    with open(
                        "./Channels/News_Channel/logos/%s.jpg" % article[8], "rb"
                    ) as source_file:
                        image = self.source_pictures[
                            "logo_%s" % article[8]
                        ] = source_file.read()
                        self.source_table["pictures_size_%s" % article[8]] = u32(
                            len(image)
                        )

                    if self.source_table["source_picture_%s" % article[8]] != u8(0):
                        self.source_table["source_picture_%s" % article[8]] = u8(0)

    # Add the pictures

    def make_pictures(self):
        self.pictures = {}
        self.dictionaries.append(self.pictures)

        numbers = 0

        for article in list(self.data.values()):
            numbers += 1
            if article[4] is not None:
                if "pictures_%s_offset" % numbers in self.pictures_table:
                    self.pictures_table[
                        "pictures_%s_offset" % numbers
                    ] = self.offset_count()  # Offset for the pictures.
                self.pictures["pictures_%s_read" % numbers] = article[
                    4
                ]  # Read the pictures.
                self.pictures["nullbyte_%s_pictures" % numbers] = u8(
                    0
                )  # Null byte for the pictures.

                for types in ["captions", "credits"]:
                    if self.pictures_table["%s_%s_offset" % (types, numbers)] != u32(
                        0
                    ) and self.pictures_table["%s_%s_size" % (types, numbers)] == u32(
                        0
                    ):
                        self.pictures_table["%s_%s_offset" % (types, numbers)] = u32(0)

    # Add RiiConnect24 text

    def make_riiconnect24_text(self):
        self.riiconnect24_text = {}
        self.dictionaries.append(self.riiconnect24_text)

        # This can be used to identify that we made this file

        self.riiconnect24_text["padding"] = u32(0) * 4  # Padding.
        self.riiconnect24_text["text"] = "RIICONNECT24".encode("ascii")  # Text.

    # Write everything to the file

    def write_dictionary(self):
        for dictionary in self.dictionaries:
            for name, value in dictionary.items():
                with open(self.newsfilename + "-1", "ba+") as dest_file:
                    dest_file.write(value)

        with open(self.newsfilename + "-1", "rb") as source_file:
            read = source_file.read()

        with open(self.newsfilename, "bw+") as dest_file:
            dest_file.write(u32(512))
            dest_file.write(u32(len(read) + 12))
            dest_file.write(
                binascii.unhexlify(format(binascii.crc32(read) & 0xFFFFFFFF, "08x"))
            )
            dest_file.write(read)

        if config["production"]:
            nlzss.encode_file(self.newsfilename, self.newsfilename)

            with open(self.newsfilename, "rb") as source_file:
                read = source_file.read()

            with open(config["key_path"], "rb") as source_file:
                private_key_data = source_file.read()

            private_key = rsa.PrivateKey.load_pkcs1(private_key_data, "PEM")

            signature = rsa.sign(read, private_key, "SHA-1")

            with open(self.newsfilename, "wb") as dest_file:
                dest_file.write(binascii.unhexlify("0".zfill(128)))
                dest_file.write(signature)
                dest_file.write(read)

        # Remove the rest of the other files

        os.remove(self.newsfilename + "-1")

        print("\n")
        print("Wrote " + self.newsfilename)

    def purge_cache(self):
        if config["production"]:
            if config["cloudflare_cache_purge"]:
                print("\nPurging cache...")

                cf = CloudFlare.CloudFlare(token=config["cloudflare_token"])
                for country in self.source["countries"]:
                    self.url = "http://{}/v2/{}/{}/news.bin.{}".format(
                        config["cloudflare_hostname"],
                        str(self.source["language_code"]),
                        str(country).zfill(3),
                        str(datetime.utcnow().hour).zfill(2),
                    )

                    self.purge_cache2()

                self.url = "http://{}/v2/{}_{}/wc24dl.vff".format(
                    config["cloudflare_hostname"],
                    str(self.source["language_code"]),
                    self.region,
                )

                self.purge_cache2()

    def purge_cache2(self):
        cf = CloudFlare.CloudFlare(token=config["cloudflare_token"])

        try:
            cf.zones.purge_cache.post(
                config["cloudflare_zone_name"],
                data={
                    "files": [
                        self.url,
                    ]
                },
            )
        except:
            pass

    # copy the temp files to the correct path that the Wii will request from the server

    def copy_file(self):
        if config["force_all"]:
            for hour in range(0, 24):
                self.copy(hour)  # copy to all 24 files
        else:
            self.copy(datetime.utcnow().hour)

    def copy(self, hour):
        newsfilename2 = "news.bin.{}".format(str(hour).zfill(2))
        path = "{}/v2/{}_{}".format(
            config["file_path"], self.language_code, self.region
        )
        mkdir_p(path)
        path = "{}/{}".format(path, newsfilename2)
        subprocess.call(["cp", self.newsfilename, path])

    # This is a function used to count offsets

    def offset_count(self):
        return u32(
            12
            + sum(
                len(values)
                for dictionary in self.dictionaries
                for values in list(dictionary.values())
                if values
            )
        )

    # Return a timestamp

    def get_timestamp(self, mode):
        if mode == 1:
            return u32(
                int((calendar.timegm(datetime.utcnow().timetuple()) - 946684800) / 60)
            )
        elif mode == 2:
            return u32(
                int((calendar.timegm(datetime.utcnow().timetuple()) - 946684800) / 60)
                + 1500
            )

    # Make the news.bin

    def packVFF(self):
        path = "{}/v2/{}_{}/".format(
            config["file_path"], self.language_code, self.region
        )
        os.makedirs(path + "wc24dl", exist_ok=True)
        for i in range(0, 24):
            with open(path + "news.bin.%s" % str(i).zfill(2), "rb") as source:
                with open(path + "wc24dl/2.BIN.%s" % str(i).zfill(2), "wb") as dest:
                    dest.write(source.read()[320:])
        os.remove(path + "wc24dl.vff")
        subprocess.call(
            ["vfftool", "create", path + "wc24dl.vff", path + "wc24dl", "3801088"],
            stdout=subprocess.DEVNULL,
        )  # Pack VFF

        for i in range(0, 24):
            os.remove(path + "wc24dl/2.BIN.%s" % str(i).zfill(2))
        os.rmdir(path + "wc24dl")
