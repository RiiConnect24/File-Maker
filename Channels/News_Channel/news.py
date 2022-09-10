#!/usr/bin/python
# -*- coding: utf-8 -*-

from Channels.News_Channel import newsdownload, newsmake
from .newsdownload import News
from .newsmake import process_news
import sys
import threading
from utils import *


def main():
    print("News Channel File Generator \nBy Larsen Vallecillo / www.rc24.xyz\n")
    if len(sys.argv) > 1:
        download(sys.argv[1])
    else:
        threads = []

        sources = [
            "ap_english",
            "ap_spanish",
            "reuters_europe_english",
            "afp_french",
            "afp_german",
            "afp_spanish",
            "ansa_italian",
            "anp_dutch",
            "reuters_japanese",
        ]

        for source in sources:
            t = threading.Thread(target=download, args=(source,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()


def download(source):
    try:
        if source == "ap_english":
            process_news("AP English", "ap_english", 1, "America", News("ap_english"))
        elif source == "ap_spanish":
            process_news("AP Spanish", "ap_spanish", 4, "America", News("ap_spanish"))
        elif source == "reuters_europe_english":
            process_news(
                "Reuters Europe English",
                "reuters_europe_english",
                1,
                "Europe",
                News("reuters_europe_english"),
            )
        elif source == "afp_french":
            process_news(
                "AFP French", "afp_french", 3, "International", News("afp_french")
            )
        elif source == "afp_german":
            process_news("AFP German", "afp_german", 2, "Europe", News("afp_german"))
        elif source == "afp_spanish":
            process_news("AFP Spanish", "afp_spanish", 4, "Europe", News("afp_spanish"))
        elif source == "ansa_italian":
            process_news(
                "ANSA Italian", "ansa_italian", 5, "Europe", News("ansa_italian")
            )
        elif source == "anp_dutch":
            process_news("ANP Dutch", "anp_dutch", 6, "Europe", News("anp_dutch"))
        elif source == "reuters_japanese":
            process_news(
                "Reuters Japanese",
                "reuters_japanese",
                0,
                "Japan",
                News("reuters_japanese"),
            )
        elif source == "ap_canada":
            process_news("AP Canada", "ap_canada", 1, "Canada", News("ap_canada"))
        elif source == "ap_australia":
            process_news(
                "AP Australia", "ap_australia", 1, "Australia", News("ap_australia")
            )
        else:
            print("Invalid source specified.")
            exit()
    except Exception as e:
        print("Failed to make news for " + source + ".")
        raise e


if __name__ == "__main__":
    main()
