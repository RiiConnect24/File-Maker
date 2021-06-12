import binascii
import os
import struct
import sys
from ninfile2 import GameTDB


def u8(data):
    if not 0 <= data <= 255:
        log("u8 out of range: %s" % data, "INFO")
        data = 0
    return struct.pack(">B", data)


def u16(data):
    if not 0 <= data <= 65535:
        log("u16 out of range: %s" % data, "INFO")
        data = 0
    return struct.pack(">H", data)


def u32(data):
    if not 0 <= data <= 4294967295:
        log("u32 out of range: %s" % data, "INFO")
        data = 0
    return struct.pack(">I", data)


def enc(text, length):
    return text.encode("utf-16be").ljust(length, b'\0')[:length]


def enc_utf_8(text, length):
    if len(text) > length:
        print("Error: Text too long.")
        sys.exit(1)
    return text.encode("utf-8").ljust(length, b'\0')[:length]


class MakeDList:
    def __init__(self, databases):
        self.header = {}
        self.databases = databases
        self.make_header()
        self.parse_gametdb_data()
        self.write_file()

    def make_header(self):
        # A lot of these values are from the dllist I am basing this off of, they will be changed when it can fully
        # generate it's own file.
        self.header["unknown"] = u16(0)
        self.header["version"] = u8(6)
        self.header["unknownRegion"] = u8(2)
        self.header["filesize"] = u32(0)
        self.header["crc32"] = u32(0)
        self.header["dllistid"] = u32(0x14454D5B)
        self.header["thumbnailId"] = u32(1)
        self.header["countryCode"] = u32(49)
        self.header["languageCode"] = u32(1)
        self.header["unknown2_0"] = u8(1)
        self.header["unknown2_1"] = u8(0x50)
        self.header["unknown2_2"] = u8(0x3C)
        self.header["unknown2_3"] = u8(0xEF)
        self.header["unknown2_4"] = u8(0)
        self.header["unknown2_5"] = u8(0)
        self.header["unknown2_6"] = u8(0)
        self.header["unknown2_7"] = u8(0)
        self.header["unknown2_8"] = u8(0)
        self.header["ratingsEntryNumber"] = u32(9)
        self.header["ratingsTableOffset"] = u32(0x5EA)
        self.header["titleTypesEntryNumber"] = u32(0x13)
        self.header["titleTypesTableOffset"] = u32(0x71C)
        # As per the amount of companies in GameTDB Wii database
        self.header["companyEntryNumber"] = u32(0x2A7)
        self.header["companyTableOffset"] = u32(0xF20)
        self.header["titleEntryNumber"] = u32(0xC08)
        self.header["titleTableOffset"] = u32(0x1629F)
        self.header["newTitleEntryNumber"] = u32(0xE)
        self.header["newTitleTableOffset"] = u32(0xBB780)
        self.header["videos1EntryNumber"] = u32(0x3C)
        self.header["videos1TableOffset"] = u32(0xBB7B8)
        self.header["newVideoEntryNumber"] = u32(0x32)
        self.header["newVideoTableOffset"] = u32(0xBF8E0)
        self.header["demosEntryNumber"] = u32(0x17)
        self.header["demosTableOffset"] = u32(0xC2630)
        self.header["unknown5"] = u32(0)
        self.header["unknown6"] = u32(0)
        self.header["recommendationsEntryNumber"] = u32(0x64)
        self.header["recommendationsTableOffset"] = u32(0xC45D0)
        for i in range(0, 4):
            self.header["unknown7_%s" % i] = u32(0)
        self.header["recentRecommendationsEntryNumber"] = u32(2)
        self.header["recentRecommendationsTableOffset"] = u32(0xC4760)
        for i in range(0, 2):
            self.header["unknown8_%s" % i] = u32(0)
        self.header["popularVideosEntryNumber"] = u32(0x1E)
        self.header["popularVideosTableOffset"] = u32(0xC476C)
        self.header["detailedRatingsEntryNumber"] = u32(0x5C)
        self.header["detailedRatingsTableOffset"] = u32(0xDCBA0)
        self.header["lastUpdate"] = enc("RiiConnect24 Edition", 62)
        self.header["unknown9_0"] = u8(0)
        self.header["unknown9_1"] = u8(0x2E)
        self.header["unknown9_2"] = u8(1)
        for i in range(0, 5):
            self.header["dlUrlIds_%s" % i] = enc_utf_8(
                "THqOxqSaiDd5bjhSQS6hk6nkYJVdioanD5Lc8mOHkobUkblWf8KxczDUZwY84FIV\0", 256)
        # TODO: Build ratings and titleTypes using dictionaries
        with open("ratings", "rb") as f:
            data = f.read()
        self.header["ratingsTable"] = data
        self.header["demosTable"] = u32(0)
        
        with open("title_types", "rb") as f:
            data = f.read()
        self.header["titleTypesTable"] = data

    def parse_gametdb_data(self):
        # Get all the companies
        for s in self.databases["Wii"][1].findall("companies"):
            for w in s.findall("company"):
                # TODO: Use int_to_strID or strID_to_int
                id = w.get("code").encode()
                id = int(id.hex(), base=16)
                self.header["id_%s" % w] = u32(id)
                self.header["devTitle_%s" % w] = enc(w.get("name"), 62)
                self.header["pubTitle_%s" % w] = enc(w.get("name"), 62)

    def write_file(self):
        print(self.header)
        filename = "dllist.info"

        if os.path.exists(filename + "-1"):
            os.remove(filename + "-1")

        if os.path.exists(filename):
            os.remove(filename)

        self.writef = open(filename + "-1", "ab")

        for values in self.header.values():
            self.writef.write(values)

        self.writef.close()

        self.readf = open(filename + "-1", "rb")

        read = self.readf.read()

        self.writef2 = open(filename, "wb")

        self.writef2.write(read)
        self.writef2.seek(8)
        self.writef2.write(binascii.unhexlify(format(binascii.crc32(read) & 0xFFFFFFFF, '08x')))

        os.remove(filename + "-1")

        self.writef2.close()


MakeDList(GameTDB(True).parse())
