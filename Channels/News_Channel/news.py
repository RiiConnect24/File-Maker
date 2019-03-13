#!/usr/bin/python
# -*- coding: utf-8 -*-

from Channels.News_Channel import newsdownload, newsmake
from .newsdownload import News
from .newsmake import process_news
import sys
from utils import *

def main():
    if len(sys.argv) > 1:
        download(sys.argv[1])
    else:
        download("ap_english")
        download("ap_spanish")
        download("reuters_europe_english")
        download("afp_spanish")
        download("afp_french")
        download("dtoday_german")
        download("ansa_italian")
        download("nu_dutch")
        download("reuters_japanese")

def download(source):
    news_list = {
        "ap_english": process_news("AP English", "ap_english", 1, "America", News("ap_english")),
        "ap_spanish": process_news("AP Spanish", "ap_spanish", 4, "America", News("ap_spanish")),
        "reuters_europe_english": process_news("Reuters Europe English", "reuters_europe_english", 1, "Europe", News("reuters_europe_english")),
        "afp_spanish": process_news("AFP Spanish", "afp_spanish", 4, "Europe", News("afp_spanish")),
        "afp_french": process_news("AFP French", "afp_french", 3, "International", News("afp_french")),
        "dtoday_german": process_news("AFP German", "dtoday_german", 2, "Europe", News("dtoday_german")),
        "ansa_italian": process_news("ANSA Italian", "ansa_italian", 5, "Europe", News("ansa_italian")),
        "nu_dutch": process_news("NU.nl Dutch", "nu_dutch", 6, "Europe", News("nu_dutch")),
        "reuters_japanese": process_news("Reuters Japanese", "reuters_japanese", 0, "Japan", News("reuters_japanese"))
    }[source]

if __name__ == "__main__":
    main()
