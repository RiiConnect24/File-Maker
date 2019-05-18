import binascii
import collections
import requests
import struct
import sys
import xml.etree.cElementTree as ElementTree
import zipfile

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


def u32_littleendian(data):
    if not 0 <= data <= 4294967295:
        log("u32 little endian out of range: %s" % data, "INFO")
        data = 0
    return struct.pack("<I", data)

if len(sys.argv) != 2:
    print("Usage: info.py <title id>")
    if len(sys.argv[1]) != 4:
        print("Error: Title ID must be 4 characters.")
    sys.exit(1)

class make_rom():
    def __init__(self):
        self.make_header()
        self.write_file()

        print "Completed Successfully"
        
    def make_header(self):
        self.header = collections.OrderedDict()

        self.header["unknown"] = u16(0)
        self.header["version"] = u8(6)
        self.header["unknown_region"] = u8(2)
        self.header["filesize"] = u32(0)
        self.header["crc32"] = u32(0)
        self.header["dllistid"] = u32(0)
        self.header["country_code"] = u32(49)
        self.header["language_code"] = u32(1)
        self.header["ratings_table_offset"] = u32(0)
        self.header["times_played_table_offset"] = u32(0)
        self.header["people_who_liked_this_also_liked_entry_number"] = u32(0)
        self.header["people_who_liked_this_also_liked_table_offset"] = u32(0)
        self.header["related_titles_entry_number"] = u32(0)
        self.header["related_titles_table_offset"] = u32(0)
        self.header["videos_entry_number"] = u32(0)
        self.header["videos_table_offset"] = u32(0)
        self.header["demos_entry_number"] = u32(0)
        self.header["demos_table_offset"] = u32(0)
        self.header["unknown_2"] = u32(0) * 2
        self.header["picture_offset"] = u32(0)
        self.header["picture_size"] = u32(0)
        self.header["unknown_3"] = u32(0)
        self.header["rating_picture_offset"] = u32(0)
        self.header["rating_picture_size"] = u32(0)
        for i in range(1, 8):
            self.header["rating_detail_picture_%s" % i] = u32(0)
        self.header["unknown_4"] = u32(0) * 2
        self.header["soft_id"] = u32(0)
        self.header["game_id"] = sys.argv[1].encode("utf-8")
        self.header["platform_flag"] = u8(0)
        self.header["company_id"] = u32(0)
        self.header["unknown_5"] = u16(0)
        self.header["unknown_6"] = u16(0)
        self.header["unknown_7"] = u8(0)
        self.header["wii_shop_channel_button_flag"] = u8(0)
        self.header["purchase_button_flag"] = u8(0)
        self.header["release_year"] = u16(0)
        self.header["release_month"] = u8(0)
        self.header["release_day"] = u8(0)
        self.header["shop_points"] = u32(0)
        for i in range(1, 5):
            self.header["unknown_8_%s" % i] = u8(0)
        self.header["wii_remote_flag"] = u8(0)
        self.header["nunchuk_flag"] = u8(0)
        self.header["classic_controller_flag"] = u8(0)
        self.header["gamecube_controller_flag"] = u8(0)
        self.header["mii_flag"] = u8(0)
        self.header["online_flag"] = u8(0)
        self.header["wiiconnect24_flag"] = u8(0)
        self.header["nintendo_wifi_connection_flag"] = u8(0)
        self.header["downloadable_content_flag"] = u8(0)
        self.header["wireless_play_flag"] = u8(0)
        self.header["download_play_flag"] = u8(0)
        self.header["touch_generations_flag"] = u8(0)
        self.header["language_chinese_flag"] = u8(0)
        self.header["language_korean_flag"] = u8(0)
        self.header["language_japanese_flag"] = u8(0)
        self.header["language_english_flag"] = u8(0)
        self.header["language_french_flag"] = u8(0)
        self.header["language_spanish_flag"] = u8(0)
        self.header["language_german_flag"] = u8(0)
        self.header["language_italian_flag"] = u8(0)
        self.header["language_dutch_flag"] = u8(0)
        for i in range(1, 11):
            self.header["unknown_9_%s" % i] = u8(0)
        self.header["title"] = "\0" * 31
        self.header["subtitle"] = "\0" * 31
        self.header["short_title"] = "\0" * 31
        for i in range(1, 4):
            self.header["description_text_%s" % i] = "\0" * 41
        self.header["genre_text"] = "\0" * 29
        self.header["players_text"] = "\0" * 41
        self.header["peripherals_text"] = "\0" * 44
        self.header["unknown_10"] = "\0" * 40
        self.header["disclaimer_text"] = "\0" * 2400
        self.header["unknown_11"] = u8(0)
        self.header["distribution_date_text"] = "\0" * 41
        self.header["wii_points_text"] = "\0" * 41
        for i in range(1, 11):
            self.header["custom_field_text_%s" % i] = "\0" * 41
    
    def write_file(self):
        self.writef = open(sys.argv[1] + "-output.info", "wb")

        for values in self.header.values():
            self.writef.write(values)
        
        self.readf = open(sys.argv[1] + "-output.info", "rb")

        self.writef.seek(8)
        self.writef.write(binascii.unhexlify(format(binascii.crc32(self.readf.read()) & 0xFFFFFFFF, '08x')))  

        self.writef.close()

class gametdb():
    def __init__():
        self.databases = {
            "Wii": ["wii", None],
            "3DS": ["3ds", None],
            "NDS": ["ds", None]
        }
    
    def download(self):
        for k,v in databases.items():
            print("Downloading {} Database from GameTDB...".format(k))
            requests.get("https://www.gametdb.com/{}tdb.zip".format(v[0]))
            self.zip = zipfile.ZipFile("{}tdb.zip".format(v[0]))
            self.zip.extractall(".")
            self.zip.close()

    def parse(self):
        for k,v in database.items():
            v[1] = ElementTree.parse("{}tdb.xml".format(v[0]))

gametdb()
make_rom()