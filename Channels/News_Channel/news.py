#!/usr/bin/python
# -*- coding: utf-8 -*-

from Channels.News_Channel import newsdownload, newsmake
from .newsdownload import News
from .newsmake import process_news
import sys
from utils import *


def main():
    print("News Channel File Generator \nBy Larsen Vallecillo / www.rc24.xyz\n")
    if len(sys.argv) > 1:
        download(sys.argv[1])
    else:
        download("ap_english")
        download("ap_spanish")
        download("reuters_europe_english")
        download("afp_french")
        download("dpa_german")
        download("ansa_italian")
        download("anp_dutch")
        download("reuters_japanese")


def download(source):
    try:
        if source == "ap_english":
            process_news("AP English", "ap_english", 1, "America", News("ap_english"))
        elif source == "ap_spanish":
            process_news(
                "AP Spanish", "ap_spanish", 4, "International", News("ap_spanish")
            )
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
        elif source == "dpa_german":
            process_news("dpa German", "dpa_german", 2, "Europe", News("dpa_german"))
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
        else:
            print("Invalid source specified.")
            exit()
    except Exception as e:
        print("Failed to make news for " + source + ".")
        print(e)


if __name__ == "__main__":
    main()
