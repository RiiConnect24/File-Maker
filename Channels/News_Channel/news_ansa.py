#!/usr/bin/python
# -*- coding: utf-8 -*-

from newsdownload import download_ansa_italian
from newsmake import download_source

download_source("ANSA Italian", "ansa_italian", "https://rc24.xyz/images/profile_news_ansa.png", 5, ["065", "066", "067", "074", "076", "077", "078", "079", "082", "083", "088", "094", "095", "096", "098", "105", "107", "108", "110"], download_ansa_italian())