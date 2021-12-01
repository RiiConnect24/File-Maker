import binascii
import os
import struct
import sys
import textwrap
import requests
from PIL import Image
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
    sys.exit(1)
elif len(sys.argv[2]) != 4:
    print("Error: Title ID must be 4 characters.")
    sys.exit(1)


def enc(text, length):
    if len(text) > length:
        print("Error: Text too long.")
        sys.exit(1)
    return text.encode("utf-16be").ljust(length, b'\0')[:length]


class make_info():
    def __init__(self, databases):
        self.databases = databases

        self.make_header()
        self.write_gametdb_info()
        self.write_file()
        self.insert_image()

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
        self.header["picture_offset"] = u32(0x2351)
        # The channel only seems to care if this offset is lower than the last offset in the file.
        # If this offset is lower, then the image will not display. I am pretty sure no covers in GameTDB are larger than 36 KB.
        self.header["picture_size"] = u32(0x9999)
        self.header["unknown_3"] = u32(0)
        self.header["rating_picture_offset"] = u32(0)
        self.header["rating_picture_size"] = u32(0)
        for i in range(1, 8):
            self.header["rating_detail_picture_%s_offset" % i] = u32(0)
            self.header["rating_detail_picture_%s_size" % i] = u32(0)
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
        for s in self.databases[sys.argv[1]][1].findall("game"):
            if s.find("id").text[:4] == sys.argv[2] and s.find("type") != "CUSTOM":
                print("Found {}!".format(sys.argv[2]))

                self.header["game_id"] = sys.argv[2].encode("utf-8")

                # Get the game type
                game_type = {None: 0x01, "Channel": 0x02, "VC-NES": 0x03, "VC-SNES": 0x04, "VC-N64": 0x05, "VC-SMS": 0x0C, "VC-MD": 0x07,
                             "VC-PCE": 0x06, "VC-C64": 0x0D, "VC-NEOGEO": 0x08, "VC-Arcade": 0x0E,
                              "WiiWare": 0x0B, "DS": 0x0A, "DSi": 0x10, "DSiWare": 0x11, "3DS": 0x12}
                                                    # The XML returns None for disc games when we query the type.
                if s.find("type").text in game_type:
                    self.header["platform_flag"] = u8(game_type[s.find("type").text])
                else:
                    print("Could not find game type")
                    sys.exit(1)

                self.header["purchase_button_flag"] = u8(1)  # we'll make it go to gametdb
                # Some games, more notably DSiWare and some 3DS games do not have a release date in the xml.
                # Due to this, we must set defaults in the case of no date.
                if s.find("date").get("year") == "":
                    release_year = 2011 # Chose this year because of the release year of the 3DS
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

                self.header["release_year"] = u16(int(release_year))
                self.header["release_month"] = u8(int(release_month) - 1)
                self.header["release_day"] = u8(int(release_day))

                controllers = {"wiimote": "wii_remote", "nunchuk": "nunchuk", "classiccontroller": "classic_controller",
                               "gamecube": "gamecube_controller", "mii": "mii"}
                controllers2 = {"wheel": "Wii Wheel", "balanceboard": "Wii Balance Board", "wiispeak": "Wii Speak",
                                "microphone": "Microphone", "guitar": "Guitar", "drums": "Drums",
                                "dancepad": "Dance Pad", "keyboard": "Keyboard", "udraw": "uDraw"}

                other_peripherals = False

                for controller in s.find("input").findall("control"):
                    if controller.get("type") in controllers:
                        self.header["{}_flag".format(controllers[controller.get("type")])] = u8(1)
                    elif controller.get("type") in controllers2:
                        if not other_peripherals:
                            self.header["peripherals_text"] = ""

                        self.header["peripherals_text"] += controllers2[controller.get("type")] + ", "

                        other_peripherals = True

                if other_peripherals:
                    self.header["peripherals_text"] = enc(self.header["peripherals_text"][:-2], 88)

                for feature in s.find("wi-fi").findall("feature"):
                    if "online" in feature.text:
                        self.header["online_flag"] = u8(1)
                        self.header["nintendo_wifi_connection_flag"] = u8(1)

                # what languages does this game apparently support? (not sure how accurate the db is)

                languages = {"ZHCN": "chinese", "KO": "korean", "JA": "japanese", "EN": "english", "FR": "french",
                             "ES": "spanish", "DE": "german", "IT": "italian", "NL": "dutch"}
                languages_list = s.find("languages").text.split(",")

                for l in languages.keys():
                    if l in languages_list:
                        self.header["language_{}_flag".format(languages[l])] = u8(1)

                # The 3DS games don't have a synopsis for some reason
                if sys.argv[1] != "3DS" and s.find("locale", {"lang": "EN"}).find("synopsis").text:
                    synopsis = s.find("locale", {"lang": "EN"}).find("synopsis").text

                    wrap = textwrap.wrap(synopsis, 41)

                    if len(wrap) <= 4:
                        text_type = "description"  # put the synopsis at the top of the page
                    elif len(wrap) <= 11:
                        text_type = "custom_field"  # put the synopsis in the middle of the page
                    else:
                        text_type = "custom_field"  # put the synopsis in the middle of the page

                        # let's shorten the synopsis until it fits

                        synopsis_text = s.find("locale", {"lang": "EN"}).find("synopsis").text.split(". ")

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

                    for w in wrap:
                        self.header["{}_text_{}".format(text_type, i)] = enc(w, 82)
                        i += 1

                self.header["title"] = title = s.find("locale", {"lang": "EN"}).find("title").text

                # make separator in game name have a subtitle too

                if ": " in self.header["title"]:
                    self.header["title"] = title.split(": ")[0]
                    self.header["subtitle"] = enc(title.split(": ")[1], 62)

                elif " - " in self.header["title"]:
                    self.header["title"] = title.split(" - ")[0]
                    self.header["subtitle"] = enc(title.split(" - ")[1], 62)

                self.header["title"] = enc(self.header["title"], 62)

                self.header["genre_text"] = enc(s.find("genre").text.title().replace(",", ", "), 58)

                players_local = s.find("input").get("players")
                players_online = s.find("wi-fi").get("players")

                if sys.argv[1] == "Wii":
                    self.header["players_text"] = players_local + " Player"

                    if players_local != "1":
                        self.header["players_text"] += "s"

                    if players_online != "0":
                        self.header["players_text"] += " (Local), " + players_online + " Player"

                        if players_online != "1":
                            self.header["players_text"] += "s"

                        self.header["players_text"] += " (Online)"

                    self.header["players_text"] = enc(self.header["players_text"], 82)

                self.header["disclaimer_text"] = enc(
                    'Game information is provided by GameTDB. Press the "Purchase this Game" button to get redirected '
                    'to the GameTDB page.',
                    4800)

                # Download cover and convert to JPEG
                print("Downloading cover art...")
                title_id = s.find("id").text
                url = f"https://art.gametdb.com/ds/box/US/{title_id}.png"
                if sys.argv[1] == "Wii":
                    url = f"https://art.gametdb.com/wii/cover/US/{title_id}.png"
                if sys.argv[1] == "3DS":
                    url = f"https://art.gametdb.com/3ds/box/US/{title_id}.png"

                r = requests.get(
                    url, headers={"User-Agent": "Nintendo Channel Info Downloader"})
                open(f"{title_id}.png", "wb").write(r.content)
                im = Image.open(f"{title_id}.png")
                rgb_im = im.convert("RGB")
                rgb_im.save(f"{title_id[:4]}.jpg")
                os.remove(f"{title_id}.png")

                self.header["filesize"] = u32(sum(len(values) for values in list(self.header.values()) if values))

                print(self.header)

                return

        print("Error: Could not find {}.".format(sys.argv[2]))
        sys.exit(1)

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
        self.writef2.seek(8)
        self.writef2.write(binascii.unhexlify(format(binascii.crc32(read) & 0xFFFFFFFF, '08x')))

        os.remove(filename + "-1")

        self.writef2.close()

    def insert_image(self):
        game_id = sys.argv[2]
        cover_offset = 0x2351

        with open(f"{game_id}.jpg", "rb") as f:
            cover = f.read()


        with open(f"{game_id}-output.info", 'r+b') as f:
            f.seek(cover_offset)
            f.write(cover)

        os.remove(f"{game_id}.jpg")


make_info(GameTDB(True).parse())
