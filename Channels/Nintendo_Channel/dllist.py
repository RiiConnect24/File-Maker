import binascii
import os
import struct
import sys
from ninfile import NinchDllist
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
        self.list = NinchDllist.from_file("4349688911.LZ")
        self.make_header()
        self.parse_company_table()
        self.parse_titles()
        self.write_file()

    def offset_count(self):
        """
        This function returns the offset of where the selected table is
        """
        return sum(len(values) for values in list(self.header.values()) if values)

    def make_header(self):
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
        self.header["ratingsEntryNumber"] = u32(0)
        self.header["ratingsTableOffset"] = u32(0)
        self.header["titleTypesEntryNumber"] = u32(0)
        self.header["titleTypesTableOffset"] = u32(0)
        self.header["companyEntryNumber"] = u32(0)
        self.header["companyTableOffset"] = u32(0)
        self.header["titleEntryNumber"] = u32(0)
        self.header["titleTableOffset"] = u32(0)
        self.header["newTitleEntryNumber"] = u32(0)
        self.header["newTitleTableOffset"] = u32(0)
        self.header["videos1EntryNumber"] = u32(0)
        self.header["videos1TableOffset"] = u32(0)
        self.header["newVideoEntryNumber"] = u32(0)
        self.header["newVideoTableOffset"] = u32(0)
        self.header["demosEntryNumber"] = u32(0)
        self.header["demosTableOffset"] = u32(0)
        self.header["unknown5"] = u32(0)
        self.header["unknown6"] = u32(0)
        self.header["recommendationsEntryNumber"] = u32(0)
        self.header["recommendationsTableOffset"] = u32(0)
        for i in range(0, 4):
            self.header["unknown7_%s" % i] = u32(0)
        self.header["recentRecommendationsEntryNumber"] = u32(0)
        self.header["recentRecommendationsTableOffset"] = u32(0)
        for i in range(0, 2):
            self.header["unknown8_%s" % i] = u32(0)
        self.header["popularVideosEntryNumber"] = u32(0)
        self.header["popularVideosTableOffset"] = u32(0)
        self.header["detailedRatingsEntryNumber"] = u32(0)
        self.header["detailedRatingsTableOffset"] = u32(0)
        self.header["lastUpdate"] = enc("Sketch Edition", 62)
        self.header["unknown9_0"] = u8(0)
        self.header["unknown9_1"] = u8(0x2E)
        self.header["unknown9_2"] = u8(1)
        for i in range(0, 5):
            self.header["dlUrlIds_%s" % i] = enc_utf_8(
                "THqOxqSaiDd5bjhSQS6hk6nkYJVdioanD5Lc8mOHkobUkblWf8KxczDUZwY84FIV\0", 256)

        # Ratings table
        self.header["ratingsTableOffset"] = u32(self.offset_count())
        ratings_entry_number = 0
        for rating in self.list.ratings_table:
            self.header[f"ratingID{ratings_entry_number}"] = u8(rating.rating_id)
            self.header[f"ratingGroup{ratings_entry_number}"] = u8(rating.unknown)
            self.header[f"age{ratings_entry_number}"] = u8(rating.age)
            self.header[f"rating_unknown{ratings_entry_number}"] = u8(rating.unknown2)
            self.header[f"jpegOffset{ratings_entry_number}"] = u32(rating.jpeg_offset)
            self.header[f"jpegSize{ratings_entry_number}"] = u32(rating.jpeg_size)
            self.header[f"title{ratings_entry_number}"] = enc(rating.title, 22)
            ratings_entry_number += 1

        self.header["ratingsEntryNumber"] = u32(ratings_entry_number)

        # Title Types Table
        self.header["titleTypesTableOffset"] = u32(self.offset_count())
        title_types_entry_number = 0
        for title_type in self.list.title_types_table:
            self.header["typeID_%s" % title_types_entry_number] = u8(title_type.type_id)
            self.header["consoleModel_%s" % title_types_entry_number] = enc_utf_8(title_type.console_model, 3)
            self.header["title_%s" % title_types_entry_number] = enc(title_type.title, 102)
            self.header["groupID_%s" % title_types_entry_number] = u8(title_type.group_id)
            self.header["unknown_title_type_%s" % title_types_entry_number] = u8(title_type.unknown)
            title_types_entry_number += 1

        self.header["titleTypesEntryNumber"] = u32(title_types_entry_number)

        # Detailed Ratings Table
        self.header["detailedRatingsTableOffset"] = u32(self.offset_count())
        detail_entry_number = 0
        for detail in self.list.detailed_ratings_table:
            self.header["detailedRatingGroup_%s" % detail_entry_number] = u8(detail.rating_group)
            self.header["detailedRatingID_%s" % detail_entry_number] = u8(detail.rating_id)
            self.header["detailedTitle_%s" % detail_entry_number] = enc(detail.title, 204)
            detail_entry_number += 1

        self.header["detailedRatingsEntryNumber"] = u32(title_types_entry_number)

    def parse_company_table(self):
        # Get all the companies
        self.header["companyTableOffset"] = u32(self.offset_count())
        entry_number = 0
        for s in self.databases["Wii"][1].findall("companies"):
            for w in s.findall("company"):
                id = w.get("code").encode()
                id = int(id.hex(), base=16)
                self.header["id_%s" % w] = u32(id)
                self.header["devTitle_%s" % w] = enc(w.get("name"), 62)
                self.header["pubTitle_%s" % w] = enc(w.get("name"), 62)
                entry_number += 1
        self.header["companyEntryNumber"] = u32(entry_number)

    def parse_titles(self):
        self.header["titleTableOffset"] = u32(self.offset_count())
        entry_number = 0
        for s in self.databases["Wii"][1].findall("game"):
            if s.find("region").text == "NTSC-U":
                if s.find("type").text != "CUSTOM":
                    entry_number += 1
                    title = "lmfao null"
                    if s.find("locale", {"lang": "EN"}):
                        title = s.find("locale", {"lang": "EN"}).find("title").text

                    self.header["titletable_id_%s" % s] = u32(1)
                    self.header["titleID_%s" % s] = enc_utf_8(s.find("id").text[:4], 4)
                    self.header["titleType_%s" % s] = u8(0xB)
                    for w in range(3):
                        self.header[f"titlegenre{s}_{w}"] = u8(0)

                    self.header["companyOffset_%s" % s] = u32(0xF20)

                    if s.find("date").get("year") == "":
                        release_year = 2011  # Chose this year because of the release year of the 3DS
                    else:
                        release_year = s.find("date").get("year")

                    if s.find("date").get("month") == "":
                        release_month = 11
                    else:
                        release_month = s.find("date").get("month")
                    if s.find("date").get("day") == "":
                        release_day = 11
                    else:
                        release_day = s.find("date").get("day")

                    self.header["release_year_%s" % s] = u16(int(release_year))
                    self.header["release_month_%s" % s] = u8(int(release_month) - 1)
                    self.header["release_day_%s" % s] = u8(int(release_day))
                    self.header["ratingID_%s" % s] = u8(9)

                    for f in range(29):
                        self.header[f"unknownidk{s}_{f}"] = u8(0)
                    self.header["epictitle_%s" % s] = enc(title, 62)
                    self.header["subtitle_%s" % s] = enc("\0", 62)
                    self.header["shortTitle_%s" % s] = enc("\0", 62)

        self.header["titleEntryNumber"] = u32(entry_number)

    def write_file(self):
        # Now that all the file contents are written, calculate filesize
        self.header["filesize"] = u32(self.offset_count())

        filename = "dllist.LZ"

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
