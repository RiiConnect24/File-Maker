import binascii
import codecs
import feedparser

feed = feedparser.parse("http://hosted.ap.org/lineups/NOTICIAS_GENERALES-rss_2.0.xml?SITE=AP&SECTION=HOME&TEMPLATE=DEFAULT")

a = "&amp"

print a.encode("utf-16be") if a else None