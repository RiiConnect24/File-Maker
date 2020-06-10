import ninfile1
import os
import struct

"""Pack integers to specific type."""

# Unsigned integers


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

# Signed integer


def s8(data):
    if not -128 <= data <= 127:
        log("s8 out of range: %s" % data, "INFO")
        data = 0
    return struct.pack(">b", data)


def s16(data):
    if not -32768 <= data <= 32767:
        log("s16 out of range: %s" % data, "INFO")
        data = 0
    return struct.pack(">h", data)


def s32(data):
    if not -2147483648 <= data <= 2147483647:
        log("s32 out of range: %s" % data, "INFO")
        data = 0
    return struct.pack(">i", data)

class NintendoChannel:
    def __init__(self, ninfile):
        self.ninfile = ninfile
        self.build()
        self.write()
        
    def build(self):
        self.dictionaries = []

        self.dictionaries.append(self.make_header())
        self.dictionaries.append(self.make_ratings_table())
        self.dictionaries.append(self.make_title_types_table())
        self.dictionaries.append(self.make_company_table())
        self.dictionaries.append(self.make_title_table())
        self.dictionaries.append(self.make_new_title_table())
        self.dictionaries.append(self.make_videos_1_table())
        self.dictionaries.append(self.make_new_video_table())
        self.dictionaries.append(self.make_demos_table())
        self.dictionaries.append(self.make_recommendations_table())
        self.dictionaries.append(self.make_recent_recommendations_table())

    def write(self):
        filename = "434968893.LZ"

        if os.path.exists(filename):
            os.remove(filename)
            
        with open(filename, "ab+") as f:
            for dictionary in self.dictionaries:
                for v in dictionary.values():
                    f.write(v)

    def make_header(self):
        header = {}

        header["unknown"] = u16(self.ninfile["unknown"])
        header["version"] = u8(self.ninfile["version"])
        header["unknown_region"] = u8(self.ninfile["unknown_region"])
        header["filesize"] = u32(self.ninfile["filesize"])
        header["crc32"] = u32(self.ninfile["crc32"])
        header["dllistid"] = u32(self.ninfile["dllistid"])
        header["thumbnail_id"] = u32(self.ninfile["thumbnail_id"])
        header["country_code"] = u32(self.ninfile["country_code"])
        header["language_code"] = u32(self.ninfile["language_code"])
        
        for i in range(0, 9):
            header["unknown_2_" + str(i)] = u8(self.ninfile["unknown_2"][i])

        header["ratings_entry_number"] = u32(self.ninfile["ratings_entry_number"])
        header["ratings_table_offset"] = u32(self.ninfile["ratings_table_offset"])
        header["title_types_entry_number"] = u32(self.ninfile["title_types_entry_number"])
        header["title_types_table_offset"] = u32(self.ninfile["title_types_table_offset"])
        header["company_entry_number"] = u32(self.ninfile["company_entry_number"])
        header["company_table_offset"] = u32(self.ninfile["company_table_offset"])
        header["title_entry_number"] = u32(self.ninfile["title_entry_number"])
        header["title_table_offset"] = u32(self.ninfile["title_table_offset"])
        header["new_title_entry_number"] = u32(self.ninfile["new_title_entry_number"])
        header["new_title_table_offset"] = u32(self.ninfile["new_title_table_offset"])
        header["videos_1_entry_number"] = u32(self.ninfile["videos_1_entry_number"])
        header["videos_1_table_offset"] = u32(self.ninfile["videos_1_table_offset"])
        header["new_video_entry_number"] = u32(self.ninfile["new_video_entry_number"])
        header["new_video_table_offset"] = u32(self.ninfile["new_video_table_offset"])
        header["demos_entry_number"] = u32(self.ninfile["demos_entry_number"])
        header["demos_table_offset"] = u32(self.ninfile["demos_table_offset"])
        header["unknown_5"] = u32(self.ninfile["unknown_5"])
        header["unknown_6"] = u32(self.ninfile["unknown_6"])
        header["recommendations_entry_number"] = u32(self.ninfile["recommendations_entry_number"])
        header["recommendations_table_offset"] = u32(self.ninfile["recommendations_table_offset"])

        for i in range(0, 4):
            header["unknown_7_" + str(i)] = u32(self.ninfile["unknown_7"][i])

        header["recent_recommendations_entry_number"] = u32(self.ninfile["recent_recommendations_entry_number"])
        header["recent_recommendations_table_offset"] = u32(self.ninfile["recent_recommendations_table_offset"])

        for i in range(0, 2):
            header["unknown_8_" + str(i)] = u32(self.ninfile["unknown_8"][i])

        header["popular_videos_entry_number"] = u32(self.ninfile["popular_videos_entry_number"])
        header["popular_videos_table_offset"] = u32(self.ninfile["popular_videos_table_offset"])
        header["detailed_ratings_entry_number"] = u32(self.ninfile["detailed_ratings_entry_number"])
        header["detailed_ratings_table_offset"] = u32(self.ninfile["detailed_ratings_table_offset"])
        header["last_update"] = self.ninfile["last_update"].encode("utf-16be").rjust(62, b"\x00")

        for i in range(0, 3):
            header["unknown_9_" + str(i)] = u8(self.ninfile["unknown_9"][i])

        for i in range(0, 5):
            header["dl_url_ids_" + str(i)] = self.ninfile["dl_url_ids"][i].encode("utf-8").rjust(256, b"\x00")
        
        for i in range(0, 4):
            header["unknown_10_" + str(i)] = u8(self.ninfile["unknown_10"][i])

        return header

    def make_ratings_table(self):
        ratings_table = {}

        i = 0

        for r in self.ninfile["ratings_table"]:
            r = self.ninfile["ratings_table"][r]
            
            i += 1

            ratings_table["rating_id_" + str(i)] = u8(r["rating_id"])
            ratings_table["unknown_" + str(i)] = u8(r["unknown"])
            ratings_table["age_" + str(i)] = u8(r["age"])
            ratings_table["unknown2_" + str(i)] = u8(r["unknown2"])
            ratings_table["jpeg_offset_" + str(i)] = u32(r["jpeg_offset"])
            ratings_table["jpeg_size_" + str(i)] = u32(r["jpeg_size"])
            ratings_table["title_" + str(i)] = r["title"].encode("utf-16be").rjust(22, b"\x00")

        return ratings_table

    def make_title_types_table(self):
        title_types_table = {}

        i = 0

        for t in self.ninfile["title_types_table"]:
            t = self.ninfile["title_types_table"][t]

            i += 1

            title_types_table["type_id_" + str(i)] = u8(t["type_id"])
            title_types_table["console_model_" + str(i)] = t["console_model"].encode("utf-8").rjust(3, b"\x00")
            title_types_table["title_" + str(i)] = t["title"].encode("utf-16be").rjust(102, b"\x00")
            title_types_table["group_id_" + str(i)] = u8(t["group_id"])
            title_types_table["unknown_" + str(i)] = u8(t["unknown"])

        return title_types_table

    def make_company_table(self):
        company_table = {}

        i = 0

        for c in self.ninfile["company_table"]:
            c = self.ninfile["company_table"][c]

            i += 1

            company_table["id_" + str(i)] = u32(c["id"])
            company_table["dev_title_" + str(i)] = c["dev_title"].encode("utf-16be").rjust(62, b"\x00")
            company_table["pub_title_" + str(i)] = c["pub_title"].encode("utf-16be").rjust(62, b"\x00")

        return company_table

    def make_title_table(self):
        title_table = {}

        i = 0

        for t in self.ninfile["title_table"]:
            t = self.ninfile["title_table"][t]

            i += 1

            title_table["id_" + str(i)] = u32(t["id"])
            title_table["title_id_" + str(i)] = t["title_id"].encode("utf-8").rjust(4, b"\x00")
            title_table["title_type_" + str(i)] = u8(t["title_type"])
            
            for j in range(0, 3):
                title_table["genre_" + str(i) + "_" + str(j)] = u8(t["genre"][j])
                
            title_table["company_offset_" + str(i)] = u32(t["company_offset"])
            title_table["release_date_year_" + str(i)] = u16(t["release_date_year"])
            title_table["release_date_month_" + str(i)] = u8(t["release_date_month"])
            title_table["release_date_day_" + str(i)] = u8(t["release_date_day"])
            title_table["rating_id_" + str(i)] = u8(t["rating_id"])
            
            for j in range(0, 29):
                title_table["unknown_4_" + str(i) + "_" + str(j)] = u8(t["unknown_4"][j])
                
            title_table["title_" + str(i)] = t["title"].encode("utf-16be").rjust(62, b"\x00")
            title_table["subtitle_" + str(i)] = t["subtitle"].encode("utf-16be").rjust(62, b"\x00")
            title_table["short_title_" + str(i)] = t["short_title"].encode("utf-16be").rjust(62, b"\x00")

        return title_table

    def make_new_title_table(self):
        new_title_table = {}

        i = 0

        for n in self.ninfile["new_title_table"]:
            n = self.ninfile["new_title_table"][n]

            i += 1

            new_title_table["new_title_offset_" + str(i)] = u32(n["new_title_offset"])

        return new_title_table

    def make_videos_1_table(self):
        videos_1_table = {}

        i = 0

        for v in self.ninfile["videos_1_table"]:
            v = self.ninfile["videos_1_table"][v]

            i += 1

            videos_1_table["id_" + str(i)] = u32(v["id"])
            videos_1_table["time_length_" + str(i)] = u16(v["time_length"])
            videos_1_table["title_id_" + str(i)] = u32(v["title_id"])

            for j in range(0, 15):
                videos_1_table["unknown_" + str(i) + "_" + str(j)] = u8(v["unknown"][j])

            videos_1_table["unknown2_" + str(i)] = u8(v["unknown_2"])
            videos_1_table["rating_id_" + str(i)] = u8(v["rating_id"])
            videos_1_table["unknown3_" + str(i)] = u8(v["unknown_3"])
            videos_1_table["new_tag_" + str(i)] = u8(v["new_tag"])
            videos_1_table["video_index_" + str(i)] = u8(v["video_index"])

            for j in range(0, 2):
                videos_1_table["unknown4_" + str(i) + "_" + str(j)] = u8(v["unknown_4"][j])

            videos_1_table["title_" + str(i)] = v["title"].encode("utf-16be").rjust(246, b"\x00")

        return videos_1_table

    def make_new_video_table(self):
        new_video_table = {}

        i = 0

        for n in self.ninfile["new_video_table"]:
            n = self.ninfile["new_video_table"][n]

            i += 1

            new_video_table["id_" + str(i)] = u32(n["id"])
            new_video_table["unknown_" + str(i)] = u16(n["unknown"])
            new_video_table["title_id_" + str(i)] = u32(n["title_id"])

            for j in range(0, 18):
                new_video_table["unknown2_" + str(i) + "_" + str(j)] = u8(n["unknown_2"][j])
                
            new_video_table["title_" + str(i)] = n["title"].encode("utf-16be").rjust(204, b"\x00")

        return new_video_table

    def make_demos_table(self):
        demos_table = {}

        i = 0

        for d in self.ninfile["demos_table"]:
            d = self.ninfile["demos_table"][d]

            i += 1

            demos_table["id_" + str(i)] = u32(d["id"])
            demos_table["title_" + str(i)] = d["title"].encode("utf-16be").rjust(62, b"\x00")
            demos_table["subtitle_" + str(i)] = d["subtitle"].encode("utf-16be").rjust(62, b"\x00")
            demos_table["titleid_" + str(i)] = u32(d["titleid"])
            demos_table["company_offset_" + str(i)] = u32(d["company_offset"])
            demos_table["removal_year_" + str(i)] = u16(d["removal_year"])
            demos_table["removal_month_" + str(i)] = u8(d["removal_month"])
            demos_table["removal_day_" + str(i)] = u8(d["removal_day"])
            demos_table["unknown_" + str(i)] = u32(d["unknown"])
            demos_table["rating_id_" + str(i)] = u8(d["rating_id"])
            demos_table["new_tag_" + str(i)] = u8(d["new_tag"])
            demos_table["new_tag_index_" + str(i)] = u8(d["new_tag_index"])
            
            for j in range(0, 205):
                demos_table["unknown2_" + str(i) + "_" + str(j)] = u8(d["unknown_2"][j])

        return demos_table

    def make_recommendations_table(self):
        recommendations_table = {}

        i = 0

        for r in self.ninfile["recommendations_table"]:
            r = self.ninfile["recommendations_table"][r]

            i += 1

            recommendations_table["recommendation_table_offset_" + str(i)] = u32(r["recommendation_title_offset"])
            
        return recommendations_table

    def make_recent_recommendations_table(self):
        recent_recommendations_table = {}

        i = 0

        for r in self.ninfile["recent_recommendations_table"]:
            r = self.ninfile["recent_recommendations_table"][r]

            i += 1

            recent_recommendations_table["recent_recommendation_title_offset_" + str(i)] = u32(r["recent_recommendation_title_offset"])
            recent_recommendations_table["unknown_" + str(i)] = u16(r["unknown"])
            
        return recent_recommendations_table

NintendoChannel(ninfile1.nintendo_channel_file)
