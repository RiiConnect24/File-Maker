#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import subprocess
import shutil
import urllib2
import time
import re
import platform
import os
import hashlib
import glob
import codecs
import binascii
from datetime import datetime, date
from newspaper import *
from itertools import ifilter
from HTMLParser import HTMLParser
reload(sys)
sys.setdefaultencoding('ISO-8859-1')

wiitimestamp1 = sys.argv[1]
wiitimestamp1 = int(wiitimestamp1, 16)
wiitimestamp2 = sys.argv[2]
wiitimestamp2 = int(wiitimestamp2, 16)
wiitimestamps = [wiitimestamp2, wiitimestamp1]

seconds_to_2000 = 946684800
ticks_per_second = 71582750

timecurrent = time.time()

wiitimestampconversion1 = max(wiitimestamps) - min(wiitimestamps)
wiitimestampconversion2 = hex(int(wiitimestampconversion1))[2:]

print 'Difference in Hex:'
print wiitimestampconversion2
print 'Difference in Decimal:'
print wiitimestampconversion1