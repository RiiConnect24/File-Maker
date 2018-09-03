#!/usr/bin/python
# -*- coding: utf-8 -*-

import binascii
import collections
import subprocess

from utils import setup_log, log, mkdir_p, u8, u16, u32, u32_littleendian

dictionaries = []

def offset_count(): return u32(sum(len(values) for dictionary in dictionaries for values in dictionary.values() if values))

def main():
    header = make_header()

    write_dictionary()

def make_header():
    header = collections.OrderedDict()
    dictionaries.append(header)

    header["unknown_0"] = u16(0)
    header["version"] = u8(6)
    header["unknown_region"] = u8(2)
    header["filesize"] = u32(0)
    header["crc32"] = u32(0)
    header["dllistid"] = u32(434968891)
    header["thumbnail_id"] = u32(1)
    header["country_code"] = u32(49)
    header["language_code"] = u32(1)
    header["unknown_6"] = u8(255) * 9
    header["ratings_total"] = u32(0)
    header["ratings_offset"] = u32(0)
    header["title_types_total"] = u32(0)
    header["title_types_offset"] = u32(0)
    header["companies_total"] = u32(0)
    header["companies_offset"] = u32(0)
    header["titles_total"] = u32(0)
    header["titles_offset"] = u32(0)
    header["unknown"] = u32(4294967295) * 2
    header["videos_0_total"] = u32(0)
    header["videos_0_offset"] = u32(0)
    header["unknown_1"] = u32(4294967295) * 2
    header["demos_total"] = u32(0)
    header["demos_offset"] = u32(0)
    header["unknown_20"] = u8(255) * 32
    header["videos_1_total"] = u32(0)
    header["videos_1_offset"] = u32(0)
    header["detailed_ratings_total"] = u32(0)
    header["detailed_ratings_offset"] = u32(0)

    return header

def write_dictionary():
    for dictionary in dictionaries:
        for values in dictionary.values():
            with open("434968891.LZ-1", "a+") as dest_file:
                dest_file.write(values)

    with open("434968891.LZ-1", "rb") as source_file:
        read = source_file.read()
        read = read[0:4] + u32(len(read)) + read[8:]

        with open("434968891.LZ", "wb") as dest_file:
            dest_file.write(read)
            dest_file.seek(8)
            dest_file.write(binascii.unhexlify(format(binascii.crc32(read) & 0xFFFFFFFF, '08x')))

    subprocess.call(["lzss", "-evf", "434968891.LZ"])

main()