#!/usr/bin/python
# -*- coding: utf-8 -*-

from newsdownload import download_news24_mainichi_japanese
from newsmake import download_source

download_source("News24/Mainichi Japanese", "news24_mainichi_japanese", 0, ["001"], download_news24_mainichi_japanese())
