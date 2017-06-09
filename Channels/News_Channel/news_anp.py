#!/usr/bin/python
# -*- coding: utf-8 -*-

from newsdownload import download_anp_dutch
from newsmake import download_source

download_source("ANP Dutch", "anp_dutch", "https://rc24.xyz/images/webhooks/news/anp_dutch.png", 6, ["065", "066", "067", "074", "076", "077", "078", "079", "082", "083", "088", "094", "095", "096", "098", "105", "107", "108", "110"], download_anp_dutch())
