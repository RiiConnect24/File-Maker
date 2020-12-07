import binascii
import collections
import os
import struct
import sys
import textwrap
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


def u32_littleendian(data):
    if not 0 <= data <= 4294967295:
        log("u32 little endian out of range: %s" % data, "INFO")
        data = 0
    return struct.pack("<I", data)

if len(sys.argv) != 3:
    print("Usage: info.py <platform> <title id>")
    if len(sys.argv[2]) != 4:
        print("Error: Title ID must be 4 characters.")
    sys.exit(1)

def enc(text, length):
    return text.encode("utf-16be").ljust(length, b'\0')[:length]

class make_info():
    def __init__(self, databases):
        self.databases = databases

        self.make_header()
        self.write_gametdb_info()
        self.write_file()

        print("Completed Successfully")
        
    def make_header(self):
        self.header = {}

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
            self.header["rating_detail_picture_%s_size" % i] = u32(0)
            self.header["rating_detail_picture_%s_offset" % i] = u32(0)
        self.header["unknown_4"] = u32(0) * 2
        self.header["soft_id"] = u32(0)
        self.header["game_id"] = u32(0)
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
        self.header["title"] = b'\0' * 62
        self.header["subtitle"] = b'\0' * 62
        self.header["short_title"] = b'\0' * 62
        for i in range(1, 4):
            self.header["description_text_%s" % i] = b'\0' * 82
        self.header["genre_text"] = b'\0' * 58
        self.header["players_text"] = b'\0' * 82
        self.header["peripherals_text"] = b'\0' * 88
        self.header["unknown_10"] = b'\0' * 80
        self.header["disclaimer_text"] = b'\0' * 4800
        self.header["unknown_11"] = u8(0)
        self.header["distribution_date_text"] = b'\0' * 82
        self.header["wii_points_text"] = b'\0' * 82
        for i in range(1, 11):
            self.header["custom_field_text_%s" % i] = b'\0' * 82

    def write_gametdb_info(self):
        for s in self.databases[sys.argv[1]][1].datafile.find_all("game"):
            if s.find("id").text[:4] == sys.argv[2] and s.find("type") != "CUSTOM":
                print("Found {}!".format(sys.argv[2]))

                self.header["game_id"] = sys.argv[2].encode("utf-8")

                self.header["purchase_button_flag"] = u8(1) # we'll make it go to gametdb
                self.header["release_year"] = u16(int(s.date["year"]))
                self.header["release_month"] = u8(int(s.date["month"]) - 1)
                self.header["release_day"] = u8(int(s.date["day"]))

                controllers = {"wiimote": "wii_remote", "nunchuk": "nunchuk", "classiccontroller": "classic_controller", "gamecube": "gamecube_controller"}

                for controller in s.find_all("control"):
                    if controller["type"] in controllers:
                        self.header["{}_flag".format(controllers[controller["type"]])] = u8(1)
                
                for feature in s.find_all("feature"):
                    if "online" in feature.text:
                        self.header["online_flag"] = u8(1)
                        self.header["nintendo_wifi_connection_flag"] = u8(1)

                # what languages does this game apparently support? (not sure how accurate the db is)
                
                languages = {"ZHCN": "chinese", "KO": "korean", "JA": "japanese", "EN": "english", "FR": "french", "ES": "spanish", "DE": "german", "IT": "italian", "NL": "dutch"}
                languages_list = s.languages.text.split(",")

                for l in languages.keys():
                    if l in languages_list:
                        self.header["language_{}_flag".format(languages[l])] = u8(1)

                wrap = textwrap.wrap(s.find("locale", {"lang": "EN"}).synopsis.text, 41)

                text_type = None

                if len(wrap) <= 4:
                    text_type = "description" # put the synoppsis at the top of the page
                elif len(wrap) <= 11:
                    text_type = "custom_field" # put the synopsis in the middle of the page
                else:
                    text_type = "custom_field"  # put the synopsis in the middle of the page

                    # let's shorten the synopsis until it fits

                    synopsis_text = s.find("locale", {"lang": "EN"}).synopsis.text.split(". ")

                    i = len(textwrap.wrap(". ".join(synopsis_text), 41)) + 1
                    j = len(synopsis_text)

                    while i > 11:
                        j -= 1
                        sentences = ". ".join(synopsis_text[:j])
                        if len(sentences) != 0:
                            sentences += "."
                        wrap = textwrap.wrap(sentences, 41)
                        i = len(wrap)

                i = 1

                print(wrap)
                
                for w in wrap:
                    self.header["{}_text_{}".format(text_type, i)] = enc(w, 82)
                    i += 1

                self.header["title"] = s.find("locale", {"lang": "EN"}).title.text

                # make separator in game name have a subtitle too
                
                if ": " in self.header["title"] or " - " in self.header["title"]:
                    self.header["title"] = self.header["title"].split(": ")[0].split(" - ")[0]
                    self.header["subtitle"] = enc(self.header["title"].split(": ")[1].split(" - ")[1], 62)
                
                self.header["title"] = enc(self.header["title"], 62)
                
                self.header["genre_text"] = enc(s.genre.text.title().replace(",", ", "), 58)
                self.header["disclaimer_text"] = enc('Game information is provided by GameTDB. Press the "Purchase this Game" button to get redirected to the GameTDB page.', 4800)

                print(self.header)

                return

    
    def write_file(self):
        filename = sys.argv[2] + "-output.info"

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
        self.writef2.seek(4)
        self.writef2.write(u32(len(read)))
        self.writef2.write(binascii.unhexlify(format(binascii.crc32(read) & 0xFFFFFFFF, '08x')))  

        os.remove(filename + "-1")

        self.writef2.close()

make_info(GameTDB().parse())
