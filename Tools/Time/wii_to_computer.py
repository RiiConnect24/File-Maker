#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import sys
import struct # Needed to pack u32s and other integers.
import binascii # Used to write to stuff in hex.
import argparse
from datetime import datetime, date

def u8(data):
    return struct.pack(">B", data)


def u16(data):
    return struct.pack(">H", data)


def u32(data):
    return struct.unpack(">I", data)

seconds_to_2000 = 946684800

wiitimestamp = int(sys.argv[1], 16)

wiitimestamp1 = seconds_to_2000 + (wiitimestamp * 60)
wiitimestamp2 = datetime.utcfromtimestamp(wiitimestamp1)
					
print "Converted Timestamp in Decimal Form:"
print wiitimestamp1
print "Converted Timestamp in Date Form:"
print wiitimestamp2