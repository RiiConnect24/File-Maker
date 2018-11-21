#!/usr/bin/python
# -*- coding: utf-8 -*-

from Channels.News_Channel import newsdownload, newsmake
from newsdownload import News
from newsmake import process_news
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
    international = ["008", "009", "010", "011", "012", "013", "014", "015", "016", "017", "018", "019", "020",
                       "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032", "033",
                       "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046",
                       "047", "048", "049", "050", "051", "052", "065", "066", "067", "074", "076", "077", "078",
                       "079", "082", "083", "088", "094", "095", "096", "098", "105", "107", "108", "110"]
    america = ["008", "009", "010", "011", "012", "013", "014", "015", "016", "017", "018", "019", "020",
                 "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032", "033",
                 "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046",
                 "047", "048", "049", "050", "051", "052"]
    europe = ["065", "066", "067", "074", "076", "077", "078", "079", "082", "083", "088", "094", "095",
               "096", "098", "105", "107", "108", "110"]
    japan = ["001"]

    if source == "ap_english":
        process_news("AP English", "ap_english", 1, america, News("ap_english"))
    elif source == "ap_spanish":
        process_news("AP Spanish", "ap_spanish", 4, america, News("ap_spanish"))
    elif source == "reuters_europe_english":
        process_news("Reuters Europe English", "reuters_europe_english", 1, europe, News("reuters_europe_english"))
    elif source == "afp_spanish":
        process_news("AFP Spanish", "afp_spanish", 4, europe, News("afp_spanish"))
    elif source == "afp_french":
        process_news("AFP French", "afp_french", 3, international, News("afp_french"))
    elif source == "dtoday_german":
        process_news("AFP German", "dtoday_german", 2, europe, News("dtoday_german"))
    elif source == "ansa_italian":
        process_news("ANSA Italian", "ansa_italian", 5, europe, News("ansa_italian"))
    elif source == "nu_dutch":
        process_news("NU.nl Dutch", "nu_dutch", 6, europe, News("nu_dutch"))
    elif source == "reuters_japanese":
        process_news("Reuters Japanese", "reuters_japanese", 0, japan, News("reuters_japanese"))
    else:
        print "Invalid source specified."
        exit()


if __name__ == "__main__":
    main()
