import binascii
import enum
import json
import nlzss
import os
import sqlite3
import struct
import sys
import textwrap
from ninfile import NinchDllist
from ninfile2 import GameTDB
from ninfile3 import *

with open("./config.json", "rb") as f:
    config = json.load(f)


def u8(data):
    if not 0 <= data <= 255:
        print("u8 out of range: %s" % data, "INFO")
        data = 0
    return struct.pack(">B", data)


def u16(data):
    if not 0 <= data <= 65535:
        print("u16 out of range: %s" % data, "INFO")
        data = 0
    return struct.pack(">H", data)


def u32(data):
    if not 0 <= data <= 4294967295:
        print("u32 out of range: %s" % data, "INFO")
        data = 0
    return struct.pack(">I", data)


def enc(text, length):
    name_fixes = {
        "Take-Two Interactive / GameTek / Rockstar Games / Global Star Software": "Take-Two Interactive",
        "Sierra Entertainment / Vivendi Games / Universal Interactive Studios": "Sierra Entertainment",
        "Marvelous Entertainment / Victor Entertainment / Pack-In-Video / Rising Star Games": "Marvelous Entertainment",
        "Take-Two Interactive / Global Star Software / Gotham Games / Gathering of Developers": "Take-Two Interactive",
    }

    if text in name_fixes:
        text = name_fixes[text]

    if len(text) > length:
        print("Error: Text too long.")
        print(text)
        # sys.exit(1)
    return text.encode("utf-16be").ljust(length, b"\0")[:length]


def enc_utf_8(text, length):
    if len(text) > length:
        print("Error: Text too long.")
        sys.exit(1)
    return text.encode("utf-8").ljust(length, b"\0")[:length]


class MakeDList:
    def __init__(self, databases):
        self.header = {}
        self.databases = databases
        self.make_header()
        self.write_ratings_table()
        self.write_title_types()
        self.write_company_table()
        self.write_title_table()
        self.write_new_title_table()
        self.write_videos()
        self.write_new_video_table()
        self.write_demos()
        self.write_recommendations()
        self.write_recent_recommendation_table()
        self.write_pop_videos()
        self.write_rating_images()
        self.write_detailed_ratings_table()
        self.write_file()

    def offset_count(self):
        """
        This function returns the offset of where the selected table is
        """
        return sum(len(values) for values in list(self.header.values()) if values)

    def make_header(self):
        """Creates the header for the DlList"""
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
        for i in range(4):
            self.header["unknown7_%s" % i] = u32(0)
        self.header["recentRecommendationsEntryNumber"] = u32(0)
        self.header["recentRecommendationsTableOffset"] = u32(0)
        for i in range(2):
            self.header["unknown8_%s" % i] = u32(0)
        self.header["popularVideosEntryNumber"] = u32(0)
        self.header["popularVideosTableOffset"] = u32(0)
        self.header["detailedRatingsEntryNumber"] = u32(0)
        self.header["detailedRatingsTableOffset"] = u32(0)
        self.header["lastUpdate"] = enc("RiiConnect24 Edition 2.0", 62)
        self.header["unknown9_0"] = u8(0)
        self.header["unknown9_1"] = u8(0x2E)
        self.header["unknown9_2"] = u8(1)
        for i in range(5):
            self.header["dlUrlIds_%s" % i] = enc_utf_8(
                "THqOxqSaiDd5bjhSQS6hk6nkYJVdioanD5Lc8mOHkobUkblWf8KxczDUZwY84FIV", 256
            )
        self.header["unknown10"] = u32(285278430)

    def write_ratings_table(self):
        """Writes the ESRB rating scales from EC (Early Childhood) to M (Mature)"""
        self.header["ratingsTableOffset"] = u32(self.offset_count())
        ratings_entry_number = 0
        for rating in nin_ratings_table:
            # This is the ESRB value.
            rating_group = 2

            self.header[f"rating_ratingID{ratings_entry_number}"] = u8(
                nin_ratings_table[rating]["rating_id"]
            )
            self.header[f"rating_ratingGroup{ratings_entry_number}"] = u8(rating_group)
            self.header[f"rating_age{ratings_entry_number}"] = u8(
                nin_ratings_table[rating]["age"]
            )
            self.header[f"rating_unknown{ratings_entry_number}"] = u8(222)
            self.header[f"rating_jpegOffset{ratings_entry_number}"] = u32(
                nin_ratings_table[rating]["jpeg_offset"]
            )
            self.header[f"rating_jpegSize{ratings_entry_number}"] = u32(
                nin_ratings_table[rating]["jpeg_size"]
            )
            self.header[f"rating_title{ratings_entry_number}"] = enc(
                nin_ratings_table[rating]["title"], 22
            )

            ratings_entry_number += 1

        self.header["ratingsEntryNumber"] = u32(ratings_entry_number)

    def write_detailed_ratings_table(self):
        """Writes the detailed ratings for titles.
        Examples are "Alcohol Reference" and "Blood and Gore"
        """
        self.header["detailedRatingsTableOffset"] = u32(self.offset_count())
        detail_entry_number = 0
        for detail in nin_detailed_ratings_table:
            self.header["detailedRatingGroup_%s" % detail_entry_number] = u8(
                nin_detailed_ratings_table[detail]["rating_group"]
            )
            self.header["detailedRatingID_%s" % detail_entry_number] = u8(
                nin_detailed_ratings_table[detail]["rating_id"]
            )
            self.header["detailedTitle_%s" % detail_entry_number] = enc(
                nin_detailed_ratings_table[detail]["title"], 204
            )
            detail_entry_number += 1

        self.header["detailedRatingsEntryNumber"] = u32(detail_entry_number)

    def write_title_types(self):
        """Writes the types of titles that the Nintendo Channel supports
        They are Wii Channels, Virtual Console, Disc Games, WiiWare, 3DS and DS/DSi games.
        """
        self.header["titleTypesTableOffset"] = u32(self.offset_count())
        title_types_entry_number = 0
        for title_type in nin_title_types_table:
            self.header["typeID_%s" % title_types_entry_number] = u8(
                nin_title_types_table[title_type]["type_id"]
            )
            self.header["consoleModel_%s" % title_types_entry_number] = enc_utf_8(
                nin_title_types_table[title_type]["console_model"], 3
            )
            self.header["title_%s" % title_types_entry_number] = enc(
                nin_title_types_table[title_type]["title"], 102
            )
            self.header["groupID_%s" % title_types_entry_number] = u8(
                nin_title_types_table[title_type]["group_id"]
            )
            self.header["unknown_title_type_%s" % title_types_entry_number] = u8(
                nin_title_types_table[title_type]["unknown"]
            )
            title_types_entry_number += 1

        self.header["titleTypesEntryNumber"] = u32(title_types_entry_number)

    def write_rating_images(self):
        """Writes the ESRB rating images to the file. It also updates the JPEG Offset and Size which is handy"""
        rating_names = [
            "EC.jpg",
            "E.jpg",
            "E10.jpg",
            "T.jpg",
            "M.jpg",
            "visitesrb.jpg",
            "visitesrb.jpg",
            "maycontain.jpg",
        ]
        for i, rating in enumerate(nin_ratings_table):
            deadbeef = {0: 0xDE, 1: 0xAD, 2: 0xBE, 3: 0xEF}
            # Write the image to our file then update the rating table's offset to the image
            if i == 8:
                return
            with open(f"./ratings/ESRB/{rating_names[i]}", "rb") as image:
                self.header[f"jpegOffset{i}"] = u32(self.offset_count())
                self.header[f"ratingJPEGData{i}"] = image.read()
                counter = 0
                while self.offset_count() % 32 != 0:
                    self.header[f"deadbeef_{i}_{counter}"] = u8(deadbeef[counter % 4])
                    counter += 1
                # Seek to end of file to set filesize
                image.seek(0, os.SEEK_END)
                self.header[f"jpegSize{i}"] = u32(image.tell())
                image.close()

    def write_company_table(self):
        """Writes the companies that made games on the Wii."""
        self.header["companyTableOffset"] = u32(self.offset_count())
        entry_number = 0
        for s in self.databases["Wii"][1].findall("companies"):
            for w in s.findall("company"):
                id = w.get("code").encode()
                id = int(id.hex(), base=16)
                self.header["company_id_%s" % w] = u32(id)
                self.header["devTitle_%s" % w] = enc(w.get("name"), 62)
                self.header["pubTitle_%s" % w] = enc(w.get("name"), 62)
                entry_number += 1
        self.header["companyEntryNumber"] = u32(entry_number)

    def write_title_table(self):
        self.header["titleTableOffset"] = u32(self.offset_count())
        entry_number = 0
        game_type = {
            None: 0x01,
            "Channel": 0x02,
            "VC-NES": 0x03,
            "VC-SNES": 0x04,
            "VC-N64": 0x05,
            "VC-SMS": 0x0C,
            "VC-MD": 0x07,
            "VC-PCE": 0x06,
            "VC-C64": 0x0D,
            "VC-NEOGEO": 0x08,
            "VC-Arcade": 0x0E,
            "WiiWare": 0x0B,
            "DS": 0x0A,
            "DSi": 0x10,
            "DSiWare": 0x11,
            "3DS": 0x12,
            "3DSWare": 0x13,
            "New3DS": 0x12,
            "New3DSWare": 0x13,
            "WiiU": 0x15,
            "Switch": 0x17,
        }

        platforms = ["Wii", "NDS", "3DS", "WiiU", "Switch"]

        titles = {}

        # import leaderboards from RiiTag
        if config["production"]:
            con = sqlite3.connect("/var/www/rc24/tag.rc24.xyz/public_html/games.db")

            cur = con.cursor()

            titles_ranking = []

            for row in cur.execute("SELECT * FROM games ORDER BY count DESC"):
                titles_ranking.append(row[2])

        titles_keys = {}

        for platform in platforms:
            for title in self.databases[platform][1].findall("game"):
                if title.find("locale", {"lang": "EN"}) is not None:
                    titles[
                        title.find("locale", {"lang": "EN"}).find("title").text
                        + " - "
                        + title.find("id").text
                        + " - "
                        + platform
                    ] = title

        j = 0
        conflict_number = 0
        for key, s in sorted(titles.items()):
            if (
                s.find("region").text == "NTSC-U"
                or s.find("region").text == "USA"
                or s.find("region").text == "ALL"
            ):
                if (
                    s.find("type").text != "CUSTOM"
                    and s.find("type").text != "GameCube"
                ):
                    title = "lmfao null"
                    if s.find("locale", {"lang": "EN"}) is not None:
                        title = (
                            s.find("locale", {"lang": "EN"})
                            .find("title")
                            .text.replace(" - ", ": ")
                            .replace("Ō", "O")
                            .replace("&amp;", "&")
                        )

                    title_platform = key.split(" - ")[-1]

                    titles_key = (
                        " - ".join(key.split(" - ")[:-2]) + " - " + title_platform
                    )

                    if titles_key in titles_keys.keys():
                        """if titles_keys[titles_key][0] == "ALL" and s.find("region").text == "USA" or len(titles_keys[titles_key][2]) == 4 and len(key.split(" - ")[-2]) == 6:
                            for header_key in self.header.keys():
                                if "title_" in header_key and str(titles_keys[titles_key][1]) in header_key:
                                    conflict_number += 1
                                    del header_key
                        else:
                             continue"""

                        continue

                    titles_keys[titles_key] = [
                        s.find("region").text,
                        entry_number,
                        key.split(" - ")[-2],
                    ]

                    if title_platform == "Switch" and s.find("type").text == "eShop":
                        continue

                    # Create custom ID
                    text_id = s.find("id").text[:4]
                    id = int(text_id.encode().hex(), base=16)

                    # for NDS, 3DS, WiiU, and Switch, we xor the id to avoid conflicts. (for example, Mario Kart 7 for 3DS and Mario Kart 8 for Wii U both have the ID "AMKE")
                    if title_platform == "NDS":
                        id ^= 0x22222222

                    elif title_platform == "3DS":
                        id ^= 0x33333333

                    elif title_platform == "WiiU":
                        id ^= 0x44444444

                    elif title_platform == "Switch":
                        id ^= 0x55555555

                    self.header[f"title_id_{entry_number}"] = u32(id)
                    self.header[f"title_titleId_{entry_number}"] = enc_utf_8(
                        s.find("id").text[:4], 4
                    )

                    if title_platform == "WiiU" and "VC-" in s.find("type").text:
                        self.header[f"title_titleType_{entry_number}"] = u8(0x16)
                    elif title_platform == "3DS" and "VC-" in s.find("type").text:
                        self.header[f"title_titleType_{entry_number}"] = u8(0x14)
                    elif s.find("type").text in game_type:
                        self.header[f"title_titleType_{entry_number}"] = u8(
                            game_type[s.find("type").text]
                        )
                    else:
                        self.header[f"title_titleType_{entry_number}"] = u8(0)

                    # Parse the genre's. The XML is a giant mess for this, this will be a giant dictionary.
                    genre_dict = {
                        "arcade": 15,
                        "party": 13,
                        "puzzle": 5,
                        "action": 1,
                        "2D platformer": 1,
                        "3D platformer": 1,
                        "shooter": 12,
                        "first-person shooter": 12,
                        "third-person shooter": 12,
                        "rail shooter": 12,
                        "run and gun": 12,
                        "shoot 'em up": 12,
                        "stealth action": 1,
                        "survival horror": 1,
                        "sports": 4,
                        "adventure": 2,
                        "hidden object": 13,
                        "interactive fiction": 2,
                        "interactive movie": 2,
                        "point-and-click": 13,
                        "music": 10,
                        "rhythm": 10,
                        "dance": 10,
                        "karaoke": 10,
                        "racing": 7,
                        "fighting": 14,
                        "simulation": 9,
                        "role-playing": 6,
                        "strategy": 8,
                        "traditional": 11,
                        "health": 3,
                        "others": 13,
                    }

                    # We will have a static variable to store our genre. This is because I didn't include
                    # many subgenres in the dict since they share the same ID as their parent genre.
                    _genre = 13
                    genre_text = s.find("genre")

                    # Check for None
                    if genre_text is None:
                        self.header[f"title_genre_{entry_number}_0"] = u8(13)
                        self.header[f"title_genre_{entry_number}_1"] = u8(13)
                        self.header[f"title_genre_{entry_number}_2"] = u8(13)
                    else:
                        # This is a mess. Some titles don't have genres, some have only 1 or 2 genres, so
                        # workarounds were made
                        genre_list = genre_text.text.split(",")

                        for i in range(3):
                            try:
                                if genre_list[i] in genre_dict:
                                    _genre = genre_dict[genre_list[i]]
                                    self.header[f"title_genre_{entry_number}_{i}"] = u8(
                                        _genre
                                    )
                                else:
                                    self.header[f"title_genre_{entry_number}_{i}"] = u8(
                                        _genre
                                    )
                            except IndexError:
                                self.header[f"title_genre_{entry_number}_{i}"] = u8(
                                    _genre
                                )

                    # We will default to Nintendo because why not
                    self.header[f"title_companyOffset_{entry_number}"] = self.header[
                        "companyTableOffset"
                    ]
                    company_start = struct.unpack(
                        ">I", self.header["companyTableOffset"]
                    )[0]

                    for c in self.databases["Wii"][1].findall("companies"):
                        for i, company in enumerate(c.findall("company")):
                            # Firstly, we will try to find the company by the company code.
                            # This method will only work for disc games. As such, methods below exist
                            if s.find("id").text[4:] != "":
                                if s.find("id").text[4:] == company.get("code"):
                                    self.header[
                                        f"title_companyOffset_{entry_number}"
                                    ] = u32(company_start + (128 * i))
                                    break

                            # If None we will default to Nintendo as well
                            if s.find("publisher").text is None:
                                self.header[
                                    f"title_companyOffset_{entry_number}"
                                ] = self.header["companyTableOffset"]
                                break
                            if company.get("name") in s.find("publisher").text:
                                self.header[
                                    f"title_companyOffset_{entry_number}"
                                ] = u32(company_start + (128 * i))
                                break

                    if s.find("date").get("year") == "":
                        release_year = 0xFFFF
                    else:
                        release_year = s.find("date").get("year")

                    if s.find("date").get("month") == "":
                        release_month = 0xFF
                    else:
                        release_month = s.find("date").get("month")

                    if s.find("date").get("day") == "":
                        release_day = 0xFF
                    else:
                        release_day = s.find("date").get("day")

                    self.header[f"title_releaseYear_{entry_number}"] = u16(
                        int(release_year)
                    )
                    self.header[f"title_releaseMonth_{entry_number}"] = u8(
                        int(release_month) - 1
                    )  # the month starts at 0, not 1
                    self.header[f"title_releaseDay_{entry_number}"] = u8(
                        int(release_day)
                    )

                    if title_platform == "Switch":
                        try:
                            rating = s.find("rating_ESRB").get("value")
                        except AttributeError:
                            rating = ""

                        rating_group = "ESRB"

                    else:
                        try:
                            rating = s.find("rating").get("value")
                            rating_group = s.find("rating").get("type")
                        except AttributeError:
                            rating = ""
                            rating_group = "ESRB"

                    if rating == "E10+" or rating == "E10 ":
                        # GameTDB has E10 as E10+. As I cannot use that as an enum key, here we are
                        rating = "E10"
                    elif rating == "AO":
                        # The Wii has Adults Only?????
                        rating = "M"
                    elif rating == "3":
                        # I don't know why PEGI ratings are getting mixed in
                        rating = "E"
                    elif rating == "" or rating == "Ratin":
                        # Default to E
                        rating = "E"

                    self.header[f"title_ratingId_{entry_number}"] = u8(
                        self.RatingSystem[rating].value
                    )

                    # Unknown Value
                    self.header[f"title_unknown1_{entry_number}"] = u16(2080)

                    # Up ahead is some extremely lazy code. This should work, but some flags will be incorrect such as
                    # Hardcore and casual
                    self.header[f"title_hardcore_{entry_number}"] = u32(536872960)
                    self.header[f"title_friends_{entry_number}"] = u32(2863311530)
                    self.header[f"title_unknown2_{entry_number}"] = u32(2863311530)
                    self.header[f"title_unknown3_{entry_number}"] = u16(43690)
                    # Unknown4 will be a combo of what in the kaitai is unknown16 and unknown17 and other flags
                    self.header[f"title_unknown4_{entry_number}"] = u16(170)
                    self.header[
                        f"title_unknown5_{entry_number}"
                    ] = 168  # contains unknown17 through multiplayer
                    self.header[f"title_unknown6_{entry_number}"] = u32(50331648)
                    self.header[f"title_unknown7_{entry_number}"] = u32(0)
                    self.header[f"title_medal_{entry_number}"] = u8(0)
                    self.header[f"title_unknown9_{entry_number}"] = u8(222)

                    for feature in s.find("wi-fi").findall("feature"):
                        if "online" not in feature.text:
                            self.header[
                                f"title_unknown5_{entry_number}"
                            ] |= 4  # online flag set to no

                    try:
                        if int(s.find("input").get("players")) < 2:
                            self.header[
                                f"title_unknown5_{entry_number}"
                            ] |= 1  # multiplayer flag set to no
                    except TypeError:
                        pass

                    self.header[f"title_unknown5_{entry_number}"] = u8(
                        self.header[f"title_unknown5_{entry_number}"]
                    )

                    if len(title) > 30:
                        fixed_title = textwrap.wrap(title, width=30)[0]
                        fixed_subtitle = textwrap.wrap(title, width=30)[1]

                    elif ": " in title:
                        fixed_title = title.split(": ")[0] + ": "
                        fixed_subtitle = title.split(": ")[1]

                    elif " - " in title:
                        fixed_title = title.split(" - ")[0] + ": "
                        fixed_subtitle = title.split(" - ")[1]

                    else:
                        fixed_title = title
                        fixed_subtitle = ""

                    if config["production"]:
                        if s.find("id").text in titles_ranking:
                            if titles_ranking.index(s.find("id").text) <= 15:
                                self.header[f"title_medal_{entry_number}"] = u8(
                                    4
                                )  # platinum
                            elif titles_ranking.index(s.find("id").text) <= 30:
                                self.header[f"title_medal_{entry_number}"] = u8(
                                    3
                                )  # gold
                            elif titles_ranking.index(s.find("id").text) <= 50:
                                self.header[f"title_medal_{entry_number}"] = u8(
                                    2
                                )  # silver
                            elif titles_ranking.index(s.find("id").text) <= 100:
                                self.header[f"title_medal_{entry_number}"] = u8(
                                    1
                                )  # bronze

                    self.header[f"title_title_{entry_number}"] = enc(fixed_title, 62)
                    self.header[f"title_subtitle_{entry_number}"] = enc(
                        fixed_subtitle, 62
                    )

                    # print(title)

                    self.header[f"title_shortTitle_{entry_number}"] = enc("", 62)
                    entry_number += 1

                    if config["make_info"]:
                        if not os.path.exists(
                            config["file_path"] + "/soft/US/en/" + str(id) + ".info"
                        ):
                            print(
                                "Making info file for {} {}...".format(
                                    title_platform, text_id
                                )
                            )

                            os.system(
                                "python3.8 info.py {} {}".format(
                                    title_platform, text_id
                                )
                            )

            j += 1

        entry_number -= conflict_number

        self.header["titleEntryNumber"] = u32(entry_number)

    def write_new_title_table(self):
        """Writes the offset where the title is in the title table."""
        self.header["newTitleTableOffset"] = u32(self.offset_count())
        entry_number = 0
        for new_title in nin_new_title_table:
            self.header[f"newTitle_offset_{entry_number}"] = self.header[
                "titleTableOffset"
            ]
            entry_number += 1
        self.header["newTitleEntryNumber"] = u32(entry_number)

    def write_videos(self):
        """Writes the videos"""
        self.header["videos1TableOffset"] = u32(self.offset_count())
        entry_number = 0
        for video in nin_videos_1_table:
            self.header["video_id_%s" % entry_number] = u32(
                nin_videos_1_table[video]["id"]
            )
            self.header["video_timeLength_%s" % entry_number] = u16(
                nin_videos_1_table[video]["time_length"]
            )
            self.header["video_titleID_%s" % entry_number] = u32(
                nin_videos_1_table[video]["title_id"]
            )
            for i in range(15):
                self.header["bruh_unknown_%s_%s" % (i, entry_number)] = u8(0)
            self.header["video_unknown2_%s" % entry_number] = u8(
                nin_videos_1_table[video]["unknown_2"]
            )
            self.header["video_ratingID_%s" % entry_number] = u8(
                nin_videos_1_table[video]["rating_id"]
            )
            self.header["video_unknown3_%s" % entry_number] = u8(
                nin_videos_1_table[video]["unknown_3"]
            )
            self.header["video_newTag_%s" % entry_number] = u8(
                nin_videos_1_table[video]["new_tag"]
            )
            self.header["videoIndex_%s" % entry_number] = u8(
                nin_videos_1_table[video]["video_index"]
            )
            self.header["unknown4_1_%s" % entry_number] = u8(61 + entry_number)
            self.header["unknown4_2_%s" % entry_number] = u8(222)
            self.header["video_title_%s" % entry_number] = enc(
                nin_videos_1_table[video]["title"], 246
            )
            entry_number += 1

        self.header["videos1EntryNumber"] = u32(entry_number)

    def write_new_video_table(self):
        """Writes the new videos"""
        self.header["newVideoTableOffset"] = u32(self.offset_count())
        entry_number = 0
        for new_video in nin_new_video_table:
            entry_number += 1
            self.header["new_videoID_%s" % entry_number] = u32(
                nin_new_video_table[new_video]["id"]
            )
            self.header["new_video_unknown_%s" % entry_number] = u16(
                nin_new_video_table[new_video]["unknown"]
            )
            self.header["new_video_titleID_%s" % entry_number] = u32(
                nin_new_video_table[new_video]["title_id"]
            )
            for i, data in enumerate(nin_new_video_table[new_video]["unknown_2"]):
                if i == 0:
                    self.header["new_video_unknown2_%s_%s" % (i, entry_number)] = u8(8)
                elif i == 1:
                    self.header["new_video_unknown2_%s_%s" % (i, entry_number)] = u8(1)
                else:
                    self.header["new_video_unknown2_%s_%s" % (i, entry_number)] = u8(
                        data
                    )
            self.header["new_video_title_%s" % entry_number] = enc(
                nin_new_video_table[new_video]["title"], 204
            )

        self.header["newVideoEntryNumber"] = u32(entry_number)

    def write_demos(self):
        """Writes the demos"""
        self.header["demosTableOffset"] = u32(self.offset_count())
        entry_number = 0
        for demo in nin_demos_table:
            self.header["demo_id_%s" % entry_number] = u32(nin_demos_table[demo]["id"])
            self.header["demo_title_%s" % entry_number] = enc(
                nin_demos_table[demo]["title"], 62
            )
            self.header["demo_subtitle_%s" % entry_number] = enc(
                nin_demos_table[demo]["subtitle"], 62
            )
            self.header["demo_titleID_%s" % entry_number] = u32(
                nin_demos_table[demo]["titleid"]
            )
            self.header["demo_company_offset_%s" % entry_number] = u32(
                nin_demos_table[demo]["company_offset"]
            )
            self.header["demo_removal_year_%s" % entry_number] = u16(65535)
            self.header["demo_removal_month_%s" % entry_number] = u8(255)
            self.header["demo_removal_day_%s" % entry_number] = u8(255)
            self.header["demo_unknown_%s" % entry_number] = u32(0)
            self.header["demo_rating_id_%s" % entry_number] = u8(
                nin_demos_table[demo]["rating_id"]
            )
            self.header["demo_new_tag_%s" % entry_number] = u8(
                nin_demos_table[demo]["new_tag"]
            )
            self.header["demo_new_tag_index_%s" % entry_number] = u8(
                nin_demos_table[demo]["new_tag_index"]
            )
            for i in range(205):
                self.header["demo_unknown2_%s_%s" % (entry_number, i)] = u8(0)
            entry_number += 1

        self.header["demosEntryNumber"] = u32(entry_number)

    def write_recommendations(self):
        """Writes the recommended games"""
        self.header["recommendationsTableOffset"] = u32(self.offset_count())
        entry_number = 0
        for recommend in nin_recommendations_table:
            self.header[
                "recommend_recommendation_title_offset_%s" % entry_number
            ] = self.header["titleTableOffset"]
            entry_number += 1
        self.header["recommendationsEntryNumber"] = u32(entry_number)

    def write_recent_recommendation_table(self):
        self.header["recentRecommendationsTableOffset"] = u32(self.offset_count())
        entry_number = 0
        for idk in nin_recent_recommendations_table:
            self.header[
                "recent_recommendation_title_offset_%s" % entry_number
            ] = self.header["titleTableOffset"]
            self.header["recent_recommendation_unknown_%s" % entry_number] = u16(
                nin_recent_recommendations_table[idk]["unknown"]
            )
            entry_number += 1

        self.header["recentRecommendationsEntryNumber"] = u32(entry_number)

    def write_pop_videos(self):
        self.header["popularVideosTableOffset"] = u32(self.offset_count())
        entry_number = 0
        for pop in nin_popular_videos_table:
            self.header["pop_video_id_%s" % entry_number] = u32(
                nin_popular_videos_table[pop]["id"]
            )
            self.header["pop_video_time_%s" % entry_number] = u16(
                nin_popular_videos_table[pop]["time_length"]
            )
            self.header["pop_video_title_id_%s" % entry_number] = u32(0)
            self.header["pop_video_bar_color_%s" % entry_number] = u8(0)
            for i in range(15):
                self.header["pop_video_unknown_%s_%s" % (i, entry_number)] = u8(0)
            self.header["pop_video_ratingID_%s" % entry_number] = u8(
                nin_popular_videos_table[pop]["rating_id"]
            )
            self.header["pop_video_unknown3_%s" % entry_number] = u8(1)
            self.header["pop_video_videoRank_%s" % entry_number] = u8(1)
            self.header["pop_video_unknown4_%s" % entry_number] = u8(222)
            self.header["pop_video_title_%s" % entry_number] = enc(
                nin_popular_videos_table[pop]["title"], 204
            )
            entry_number += 1
        self.header["popularVideosEntryNumber"] = u32(entry_number)

    class RatingSystem(enum.Enum):
        EC = 8
        E = 9
        E10 = 10
        T = 11
        M = 12

    def write_file(self):
        # Now that all the file contents are written, calculate filesize
        self.header["filesize"] = u32(self.offset_count())

        filename = "testing.bin"

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
        self.writef2.write(
            binascii.unhexlify(format(binascii.crc32(read) & 0xFFFFFFFF, "08x"))
        )

        os.remove(filename + "-1")

        self.writef2.close()

        nlzss.encode_file(filename, filename.replace(".bin", ".LZ"))


MakeDList(GameTDB(True).parse())

# Get genres
# genre_type = {"action": 1, "adventure": 2, "sports": 4, "puzzle": 5,
# "strategy RPG": 6, "tactical RPG": 6, "action RPG": 6, "MMORPG": 6, "roguelike": 6}
# for s in self.databases["Wii"][1].findall("genres"):
# for k in s.findall("maingenre"):
# print(k.get("name"))
