import binascii
import os
import struct
import sys
from ninfile import NinchDllist
from ninfile2 import GameTDB


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
        self.header["lastUpdate"] = enc("Sketch Edition", 62)
        self.header["unknown9_0"] = u8(0)
        self.header["unknown9_1"] = u8(0x2E)
        self.header["unknown9_2"] = u8(1)
        for i in range(5):
            self.header["dlUrlIds_%s" % i] = enc_utf_8(
                "THqOxqSaiDd5bjhSQS6hk6nkYJVdioanD5Lc8mOHkobUkblWf8KxczDUZwY84FIV", 256)
        self.header["unknown10"] = u32(285278430)

    def write_ratings_table(self):
        """Writes the ESRB rating scales from EC (Early Childhood) to M (Mature)"""
        self.header["ratingsTableOffset"] = u32(self.offset_count())
        ratings_entry_number = 0
        for rating in self.list.ratings_table:
            # This is the ESRB value.
            rating_group = 2

            self.header[f"rating_ratingID{ratings_entry_number}"] = u8(rating.rating_id)
            self.header[f"rating_ratingGroup{ratings_entry_number}"] = u8(rating_group)
            self.header[f"rating_age{ratings_entry_number}"] = u8(rating.age)
            self.header[f"rating_unknown{ratings_entry_number}"] = u8(222)
            self.header[f"rating_jpegOffset{ratings_entry_number}"] = u32(rating.jpeg_offset)
            self.header[f"rating_jpegSize{ratings_entry_number}"] = u32(rating.jpeg_size)
            self.header[f"rating_title{ratings_entry_number}"] = enc(rating.title, 22)

            ratings_entry_number += 1

        self.header["ratingsEntryNumber"] = u32(ratings_entry_number)

    def write_detailed_ratings_table(self):
        """Writes the detailed ratings for titles.
        Examples are "Alcohol Reference" and "Blood and Gore"
        """
        self.header["detailedRatingsTableOffset"] = u32(self.offset_count())
        detail_entry_number = 0
        for detail in self.list.detailed_ratings_table:
            self.header["detailedRatingGroup_%s" % detail_entry_number] = u8(detail.rating_group)
            self.header["detailedRatingID_%s" % detail_entry_number] = u8(detail.rating_id)
            self.header["detailedTitle_%s" % detail_entry_number] = enc(detail.title, 204)
            detail_entry_number += 1

        self.header["detailedRatingsEntryNumber"] = u32(detail_entry_number)

    def write_title_types(self):
        """Writes the types of titles that the Nintendo Channel supports
        They are Wii Channels, Virtual Console, Disc Games, WiiWare, 3DS and DS/DSi games.
        """
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

    def write_rating_images(self):
        """Writes the ESRB rating images to the file. It also updates the JPEG Offset and Size which is handy"""
        rating_names = ["EC.jpg", "E.jpg", "E10.jpg", "T.jpg", "M.jpg", "visitesrb.jpg", "visitesrb.jpg", "maycontain.jpg"]
        for i, rating in enumerate(self.list.ratings_table):
            # Write the image to our file then update the rating table's offset to the image
            if i == 8:
                return
            with open(f"./ratings/ESRB/{rating_names[i]}", "rb") as image:
                self.header[f"jpegOffset{i}"] = u32(self.offset_count())
                self.header[f"ratingJPEGData{i}"] = image.read()
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
        game_type = {"VC-NES": 0x03, "VC-SNES": 0x04, "VC-N64": 0x05, "VC-SMS": 0x0C, "VC-MD": 0x07,
                     "VC-PCE": 0x06, "VC-C64": 0x0D, "VC-NEOGEO": 0x08, "VC-Arcade": 0x0E, "Channel": 0x02,
                     None: 0x01, "WiiWare": 0x0B, "DS": 0x0A, "DSi": 0x10, "DSiWare": 0x11, "3DS": 0x12}
        database = self.databases["Wii"][1].findall("game") + self.databases["NDS"][1].findall("game") + self.databases["3DS"][1].findall("game")
        for s in database:
            if s.find("region").text == "NTSC-U":
                if s.find("type").text != "CUSTOM" and s.find("type").text != "GameCube":
                    title = "lmfao null"
                    if s.find("locale", {"lang": "EN"}):
                        title = s.find("locale", {"lang": "EN"}).find("title").text

                    # Create custom ID
                    id = s.find("id").text[:4].encode()
                    id = int(id.hex(), base=16)

                    self.header[f"title_id_{entry_number}"] = u32(id)
                    self.header[f"title_titleId_{entry_number}"] = enc_utf_8(s.find("id").text[:4], 4)
                    if s.find("type").text in game_type:
                        self.header[f"title_titleType_{entry_number}"] = u8(game_type[s.find("type").text])
                    else:
                        self.header[f"title_titleType_{entry_number}"] = u8(0)
                    for w in range(3):
                        self.header[f"title_genre_{entry_number}_{w}"] = u8(3)

                    self.header[f"title_companyOffset_{entry_number}"] = self.header["companyTableOffset"]

                    if s.find("date").get("year") == "":
                        release_year = 2011
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

                    self.header[f"title_releaseYear_{entry_number}"] = u16(int(release_year))
                    self.header[f"title_releaseMonth_{entry_number}"] = u8(int(release_month) - 1)
                    self.header[f"title_releaseDay_{entry_number}"] = u8(int(release_day))
                    self.header[f"title_ratingId_{entry_number}"] = u8(9)

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
                    self.header[f"title_unknown5_{entry_number}"] = u8(170)
                    self.header[f"title_unknown6_{entry_number}"] = u32(50331648)
                    self.header[f"title_unknown7_{entry_number}"] = u32(0)
                    self.header[f"title_unknown9_{entry_number}"] = u16(222)

                    if ": " in title:
                        self.header[f"title_title_{entry_number}"] = enc(title.split(": ")[0], 62)
                        self.header[f"title_subtitle_{entry_number}"] = enc(title.split(": ")[1], 62)

                    elif " - " in title:
                        self.header[f"title_title_{entry_number}"] = enc(title.split(" - ")[0], 62)
                        self.header[f"title_subtitle_{entry_number}"] = enc(title.split(" - ")[1], 62)
                    
                    else:
                        self.header[f"title_title_{entry_number}"] = enc(title, 62)
                        self.header[f"title_subtitle_{entry_number}"] = enc("", 62)
                        
                    self.header[f"title_shortTitle_{entry_number}"] = enc("", 62)
                    entry_number += 1

        self.header["titleEntryNumber"] = u32(entry_number)

    def write_new_title_table(self):
        """Writes the offset where the title is in the title table."""
        self.header["newTitleTableOffset"] = u32(self.offset_count())
        entry_number = 0
        for new_title in self.list.new_title_table:
            self.header[f"newTitle_offset_{entry_number}"] = self.header["titleTableOffset"]
            entry_number += 1
        self.header["newTitleEntryNumber"] = u32(entry_number)

    def write_videos(self):
        """Writes the videos"""
        self.header["videos1TableOffset"] = u32(self.offset_count())
        entry_number = 0
        for video in self.list.videos_1_table:
            self.header["video_id_%s" % entry_number] = u32(video.id)
            self.header["video_timeLength_%s" % entry_number] = u16(video.time_length)
            self.header["video_titleID_%s" % entry_number] = u32(video.title_id)
            for i in range(15):
                self.header["bruh_unknown_%s_%s" % (i, entry_number)] = u8(0)
            self.header["video_unknown2_%s" % entry_number] = u8(video.unknown_2)
            self.header["video_ratingID_%s" % entry_number] = u8(video.rating_id)
            self.header["video_unknown3_%s" % entry_number] = u8(video.unknown_3)
            self.header["video_newTag_%s" % entry_number] = u8(video.new_tag)
            self.header["videoIndex_%s" % entry_number] = u8(video.video_index)
            self.header["unknown4_1_%s" % entry_number] = u8(61 + entry_number)
            self.header["unknown4_2_%s" % entry_number] = u8(222)
            self.header["video_title_%s" % entry_number] = enc("Larsen gets grounded", 246)
            entry_number += 1

        self.header["videos1EntryNumber"] = u32(entry_number)

    def write_new_video_table(self):
        """Writes the new videos"""
        self.header["newVideoTableOffset"] = u32(self.offset_count())
        entry_number = 0
        for new_video in self.list.new_video_table:
            entry_number += 1
            self.header["new_videoID_%s" % entry_number] = u32(new_video.id)
            self.header["new_video_unknown_%s" % entry_number] = u16(new_video.unknown)
            self.header["new_video_titleID_%s" % entry_number] = u32(new_video.title_id)
            for i, data in enumerate(new_video.unknown_2):
                if i == 0:
                    self.header["new_video_unknown2_%s_%s" % (i, entry_number)] = u8(8)
                elif i == 1:
                    self.header["new_video_unknown2_%s_%s" % (i, entry_number)] = u8(1)
                else:
                    self.header["new_video_unknown2_%s_%s" % (i, entry_number)] = u8(data)
            self.header["new_video_title_%s" % entry_number] = enc("Larsen is grounded", 204)

        self.header["newVideoEntryNumber"] = u32(entry_number)

    def write_demos(self):
        """Writes the demos"""
        self.header["demosTableOffset"] = u32(self.offset_count())
        entry_number = 0
        for demo in self.list.demos_table:
            self.header["demo_id_%s" % entry_number] = u32(demo.id)
            self.header["demo_title_%s" % entry_number] = enc("Sketch's Demo", 62)
            self.header["demo_subtitle_%s" % entry_number] = enc(demo.subtitle, 62)
            self.header["demo_titleID_%s" % entry_number] = u32(demo.titleid)
            self.header["demo_company_offset_%s" % entry_number] = u32(demo.company_offset)
            self.header["demo_removal_year_%s" % entry_number] = u16(65535)
            self.header["demo_removal_month_%s" % entry_number] = u8(255)
            self.header["demo_removal_day_%s" % entry_number] = u8(255)
            self.header["demo_unknown_%s" % entry_number] = u32(0)
            self.header["demo_rating_id_%s" % entry_number] = u8(demo.rating_id)
            self.header["demo_new_tag_%s" % entry_number] = u8(demo.new_tag)
            self.header["demo_new_tag_index_%s" % entry_number] = u8(demo.new_tag_index)
            for i in range(205):
                self.header["demo_unknown2_%s_%s" % (entry_number, i)] = u8(0)
            entry_number += 1

        self.header["demosEntryNumber"] = u32(entry_number)

    def write_recommendations(self):
        """Writes the recommended games"""
        self.header["recommendationsTableOffset"] = u32(self.offset_count())
        entry_number = 0
        for recommend in self.list.recommendations_table:
            self.header["recommend_recommendation_title_offset_%s" % entry_number] = self.header["titleTableOffset"]
            entry_number += 1
        self.header["recommendationsEntryNumber"] = u32(entry_number)

    def write_recent_recommendation_table(self):
        self.header["recentRecommendationsTableOffset"] = u32(self.offset_count())
        entry_number = 0
        for idk in self.list.recent_recommendations_table:
            self.header["recent_recommendation_title_offset_%s" % entry_number] = self.header["titleTableOffset"]
            self.header["recent_recommendation_unknown_%s" % entry_number] = u16(idk.unknown)
            entry_number += 1

        self.header["recentRecommendationsEntryNumber"] = u32(entry_number)

    def write_pop_videos(self):
        self.header["popularVideosTableOffset"] = u32(self.offset_count())
        entry_number = 0
        for pop in self.list.popular_videos_table:
            self.header["pop_video_id_%s" % entry_number] = u32(pop.id)
            self.header["pop_video_time_%s" % entry_number] = u16(pop.time_length)
            self.header["pop_video_title_id_%s" % entry_number] = u32(0)
            self.header["pop_video_bar_color_%s" % entry_number] = u8(0)
            for i in range(15):
                self.header["pop_video_unknown_%s_%s" % (i, entry_number)] = u8(0)
            self.header["pop_video_ratingID_%s" % entry_number] = u8(pop.rating_id)
            self.header["pop_video_unknown3_%s" % entry_number] = u8(1)
            self.header["pop_video_videoRank_%s" % entry_number] = u8(1)
            self.header["pop_video_unknown4_%s" % entry_number] = u8(222)
            self.header["pop_video_title_%s" % entry_number] = enc("Larsen gets grounded", 204)
            entry_number += 1
        self.header["popularVideosEntryNumber"] = u32(entry_number)

    def write_file(self):
        # Now that all the file contents are written, calculate filesize
        self.header["filesize"] = u32(self.offset_count())

        filename = "testing.LZ"

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

# Get genres
# genre_type = {"action": 1, "adventure": 2, "sports": 4, "puzzle": 5,
# "strategy RPG": 6, "tactical RPG": 6, "action RPG": 6, "MMORPG": 6, "roguelike": 6}
# for s in self.databases["Wii"][1].findall("genres"):
# for k in s.findall("maingenre"):
# print(k.get("name"))
