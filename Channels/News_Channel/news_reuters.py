#!/usr/bin/python
# -*- coding: utf-8 -*-

from newsdownload import download_reuters_english
from newsmake import download_source

download_source("Reuters English", "reuters_english", 1, ["065", "066", "067", "074", "076", "077", "078", "079", "082", "083", "088", "094", "095", "096", "098", "105", "107", "108", "110"], download_reuters_english())
