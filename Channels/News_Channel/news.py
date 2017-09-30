#!/usr/bin/python
# -*- coding: utf-8 -*-

from newsdownload import *
from newsmake import download_source
import sys

if len(sys.argv) > 1:
    if sys.argv[1] == "reuters_america_english": download_source("Reuters America English", "reuters_america_english", 1, ["008", "009", "010", "011", "012", "013", "014", "015", "016", "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032", "033", "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046", "047", "048", "049", "050", "051", "052"], download_reuters_america_english())
    elif sys.argv[1] == "reuters_europe_english": download_source("Reuters Europe English", "reuters_europe_english", 1, ["065", "066", "067", "074", "076", "077", "078", "079", "082", "083", "088", "094", "095", "096", "098", "105", "107", "108", "110"], download_reuters_europe_english())
    elif sys.argv[1] == "expansion_spanish": download_source("Expansión Spanish", "expansion_spanish", 4, ["008", "009", "010", "011", "012", "013", "014", "015", "016", "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032", "033", "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046", "047", "048", "049", "050", "051", "052"], download_expansion_spanish())
    elif sys.argv[1] == "efe_europe_spanish": download_source("EFE Europe Spanish", "efe_europe_spanish", 4, ["065", "066", "067", "074", "076", "077", "078", "079", "082", "083", "088", "094", "095", "096", "098", "105", "107", "108", "110"], download_efe_europe_spanish())
    elif sys.argv[1] == "afp_french": download_source("AFP French", "afp_french", 3, ["008", "009", "010", "011", "012", "013", "014", "015", "016", "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032", "033", "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046", "047", "048", "049", "050", "051", "052", "065", "066", "067", "074", "076", "077", "078", "079", "082", "083", "088", "094", "095", "096", "098", "105", "107", "108", "110"], download_afp_french())
    elif sys.argv[1] == "zeit_german": download_source("ZEIT German", "zeit_german", 2, ["065", "066", "067", "074", "076", "077", "078", "079", "082", "083", "088", "094", "095", "096", "098", "105", "107", "108", "110"], download_zeit_german())
    elif sys.argv[1] == "ansa_italian": download_source("ANSA Italian", "ansa_italian", 5, ["065", "066", "067", "074", "076", "077", "078", "079", "082", "083", "088", "094", "095", "096", "098", "105", "107", "108", "110"], download_ansa_italian())
    elif sys.argv[1] == "nu_dutch": download_source("NU.nl Dutch", "nu_dutch", 6, ["065", "066", "067", "074", "076", "077", "078", "079", "082", "083", "088", "094", "095", "096", "098", "105", "107", "108", "110"], download_nu_dutch())
    elif sys.argv[1] == "reuters_japanese": download_source("Reuters Japanese", "reuters_japanese", 0, ["001"], download_reuters_japanese())
    else:
        print "Invalid argument. Valid arguments include the following:"
        print "reuters_america_english, reuters_europe_english, expansion_spanish, efe_europe_spanish, afp_french, zeit_german, ansa_italian, nu_dutch, reuters_japanese"
else:
    download_source("Reuters America English", "reuters_america_english", 1, ["008", "009", "010", "011", "012", "013", "014", "015", "016", "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032", "033", "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046", "047", "048", "049", "050", "051", "052"], download_reuters_america_english())
    download_source("Reuters Europe English", "reuters_europe_english", 1, ["065", "066", "067", "074", "076", "077", "078", "079", "082", "083", "088", "094", "095", "096", "098", "105", "107", "108", "110"], download_reuters_europe_english())
    download_source("Expansión Spanish", "expansion_spanish", 4, ["008", "009", "010", "011", "012", "013", "014", "015", "016", "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032", "033", "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046", "047", "048", "049", "050", "051", "052"], download_expansion_spanish())
    download_source("EFE Europe Spanish", "efe_europe_spanish", 4, ["065", "066", "067", "074", "076", "077", "078", "079", "082", "083", "088", "094", "095", "096", "098", "105", "107", "108", "110"], download_efe_europe_spanish())
    download_source("AFP French", "afp_french", 3, ["008", "009", "010", "011", "012", "013", "014", "015", "016", "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032", "033", "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046", "047", "048", "049", "050", "051", "052", "065", "066", "067", "074", "076", "077", "078", "079", "082", "083", "088", "094", "095", "096", "098", "105", "107", "108", "110"], download_afp_french())
    download_source("ZEIT German", "zeit_german", 2, ["065", "066", "067", "074", "076", "077", "078", "079", "082", "083", "088", "094", "095", "096", "098", "105", "107", "108", "110"], download_zeit_german())
    download_source("ANSA Italian", "ansa_italian", 5, ["065", "066", "067", "074", "076", "077", "078", "079", "082", "083", "088", "094", "095", "096", "098", "105", "107", "108", "110"], download_ansa_italian())
    download_source("NU.nl Dutch", "nu_dutch", 6, ["065", "066", "067", "074", "076", "077", "078", "079", "082", "083", "088", "094", "095", "096", "098", "105", "107", "108", "110"], download_nu_dutch())
    download_source("Reuters Japanese", "reuters_japanese", 0, ["001"], download_reuters_japanese())
