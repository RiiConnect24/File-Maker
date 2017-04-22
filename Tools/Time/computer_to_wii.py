#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import struct # Needed to pack u32s and other integers.
import binascii # Used to write to stuff in hex.
from datetime import datetime, date

def u8(data):
    return struct.pack(">B", data)


def u16(data):
    return struct.pack(">H", data)


def u32(data):
    return struct.pack(">I", data)

seconds_to_2000 = 946684800
ticks_per_second = 71582788

timecurrent = time.time()

wiitimestamp1 = binascii.hexlify(u32(int(hex(int(ticks_per_second * (float(timecurrent) - seconds_to_2000)))[2:8], 16)))
wiitimestamp2 = int(wiitimestamp1, 16)

print 'Timestamp in Hex Form:'
print wiitimestamp1
print 'Timestamp in Decimal Form:'
print wiitimestamp2