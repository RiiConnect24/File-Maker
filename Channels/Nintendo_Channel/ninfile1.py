import ninfile
from kaitaistruct import KaitaiStream, BytesIO

file = ninfile.NinchDllist.from_file("434968891.LZ")

nintendo_channel_file = {}

# header

nintendo_channel_file["unknown"] = file.unknown
nintendo_channel_file["version"] = file.version
nintendo_channel_file["unknown_region"] = file.unknown_region
nintendo_channel_file["filesize"] = file.filesize
nintendo_channel_file["crc32"] = file.crc32
nintendo_channel_file["dllistid"] = file.dllistid
nintendo_channel_file["thumbnail_id"] = file.thumbnail_id
nintendo_channel_file["country_code"] = file.country_code
nintendo_channel_file["language_code"] = file.language_code
nintendo_channel_file["unknown_2"] = file.unknown_2
nintendo_channel_file["ratings_entry_number"] = file.ratings_entry_number
nintendo_channel_file["ratings_table_offset"] = file.ratings_table_offset
nintendo_channel_file["title_types_entry_number"] = file.title_types_entry_number
nintendo_channel_file["title_types_table_offset"] = file.title_types_table_offset
nintendo_channel_file["company_entry_number"] = file.company_entry_number
nintendo_channel_file["company_table_offset"] = file.company_table_offset
nintendo_channel_file["title_entry_number"] = file.title_entry_number
nintendo_channel_file["title_table_offset"] = file.title_table_offset
nintendo_channel_file["new_title_entry_number"] = file.new_title_entry_number
nintendo_channel_file["new_title_table_offset"] = file.new_title_table_offset
nintendo_channel_file["videos_1_entry_number"] = file.videos_1_entry_number
nintendo_channel_file["videos_1_table_offset"] = file.videos_1_table_offset
nintendo_channel_file["new_video_entry_number"] = file.new_video_entry_number
nintendo_channel_file["new_video_table_offset"] = file.new_video_table_offset
nintendo_channel_file["demos_entry_number"] = file.demos_entry_number
nintendo_channel_file["demos_table_offset"] = file.demos_table_offset
nintendo_channel_file["unknown_5"] = file.unknown_5
nintendo_channel_file["unknown_6"] = file.unknown_6
nintendo_channel_file["recommendations_entry_number"] = file.recommendations_entry_number
nintendo_channel_file["recommendations_table_offset"] = file.recommendations_table_offset
nintendo_channel_file["unknown_7"] = file.unknown_7
nintendo_channel_file["recent_recommendations_entry_number"] = file.recent_recommendations_entry_number
nintendo_channel_file["recent_recommendations_table_offset"] = file.recent_recommendations_table_offset
nintendo_channel_file["unknown_8"] = file.unknown_8
nintendo_channel_file["popular_videos_entry_number"] = file.popular_videos_entry_number
nintendo_channel_file["popular_videos_table_offset"] = file.popular_videos_table_offset
nintendo_channel_file["detailed_ratings_entry_number"] = file.detailed_ratings_entry_number
nintendo_channel_file["detailed_ratings_table_offset"] = file.detailed_ratings_table_offset
nintendo_channel_file["last_update"] = file.last_update
nintendo_channel_file["unknown_9"] = file.unknown_9
nintendo_channel_file["dl_url_ids"] = file.dl_url_ids
nintendo_channel_file["unknown_10"] = file.unknown_10

i = 0

nintendo_channel_file["ratings_table"] = {}

for f in file.ratings_table:
    nintendo_channel_file["ratings_table"][i] = {}
    nintendo_channel_file["ratings_table"][i]["rating_id"] = f.rating_id 
    nintendo_channel_file["ratings_table"][i]["unknown"] = f.unknown
    nintendo_channel_file["ratings_table"][i]["age"] = f.age
    nintendo_channel_file["ratings_table"][i]["unknown2"] = f.unknown2
    nintendo_channel_file["ratings_table"][i]["jpeg_offset"] = f.jpeg_offset
    nintendo_channel_file["ratings_table"][i]["jpeg_size"] = f.jpeg_size
    nintendo_channel_file["ratings_table"][i]["title"] = f.title

    i += 1

i = 0

nintendo_channel_file["title_types_table"] = {}

for f in file.title_types_table:
    nintendo_channel_file["title_types_table"][i] = {}
    nintendo_channel_file["title_types_table"][i]["type_id"] = f.type_id
    nintendo_channel_file["title_types_table"][i]["console_model"] = f.console_model
    nintendo_channel_file["title_types_table"][i]["title"] = f.title
    nintendo_channel_file["title_types_table"][i]["group_id"] = f.group_id
    nintendo_channel_file["title_types_table"][i]["unknown"] = f.unknown

    i += 1

i = 0

nintendo_channel_file["company_table"] = {}

for f in file.company_table:
    nintendo_channel_file["company_table"][i] = {}
    nintendo_channel_file["company_table"][i]["id"] = f.id
    nintendo_channel_file["company_table"][i]["dev_title"] = f.dev_title
    nintendo_channel_file["company_table"][i]["pub_title"] = f.pub_title

    i += 1

i = 0

nintendo_channel_file["title_table"] = {}

for f in file.title_table:
    nintendo_channel_file["title_table"][i] = {}
    nintendo_channel_file["title_table"][i]["id"] = f.id
    nintendo_channel_file["title_table"][i]["title_id"] = f.title_id
    nintendo_channel_file["title_table"][i]["title_type"] = f.title_type
    nintendo_channel_file["title_table"][i]["genre"] = f.genre
    nintendo_channel_file["title_table"][i]["company_offset"] = f.company_offset
    nintendo_channel_file["title_table"][i]["release_date_year"] = f.release_date_year
    nintendo_channel_file["title_table"][i]["release_date_month"] = f.release_date_month
    nintendo_channel_file["title_table"][i]["release_date_day"] = f.release_date_day
    nintendo_channel_file["title_table"][i]["rating_id"] = f.rating_id
    nintendo_channel_file["title_table"][i]["unknown_4"] = f.unknown_4
    nintendo_channel_file["title_table"][i]["title"] = f.title
    nintendo_channel_file["title_table"][i]["subtitle"] = f.subtitle
    nintendo_channel_file["title_table"][i]["short_title"] = f.short_title

    i += 1

i = 0

nintendo_channel_file["new_title_table"] = {}

for f in file.new_title_table:
    nintendo_channel_file["new_title_table"][i] = {}
    nintendo_channel_file["new_title_table"][i]["new_title_offset"] = f.new_title_offset

    i += 1

i = 0

nintendo_channel_file["videos_1_table"] = {}

for f in file.videos_1_table:
    nintendo_channel_file["videos_1_table"][i] = {}
    nintendo_channel_file["videos_1_table"][i]["id"] = f.id
    nintendo_channel_file["videos_1_table"][i]["time_length"] = f.time_length
    nintendo_channel_file["videos_1_table"][i]["title_id"] = f.title_id
    nintendo_channel_file["videos_1_table"][i]["unknown"] = f.unknown
    nintendo_channel_file["videos_1_table"][i]["unknown_2"] = f.unknown_2
    nintendo_channel_file["videos_1_table"][i]["rating_id"] = f.rating_id
    nintendo_channel_file["videos_1_table"][i]["unknown_3"] = f.unknown_3
    nintendo_channel_file["videos_1_table"][i]["new_tag"] = f.new_tag
    nintendo_channel_file["videos_1_table"][i]["video_index"] = f.video_index
    nintendo_channel_file["videos_1_table"][i]["unknown_4"] = f.unknown_4
    nintendo_channel_file["videos_1_table"][i]["title"] = f.title

    i += 1

i = 0

nintendo_channel_file["new_video_table"] = {}

for f in file.new_video_table:
    nintendo_channel_file["new_video_table"][i] = {}
    nintendo_channel_file["new_video_table"][i]["id"] = f.id
    nintendo_channel_file["new_video_table"][i]["unknown"] = f.unknown
    nintendo_channel_file["new_video_table"][i]["title_id"] = f.title_id
    nintendo_channel_file["new_video_table"][i]["unknown_2"] = f.unknown_2

    i += 1

i = 0

nintendo_channel_file["demos_table"] = {}

for f in file.demos_table:
    nintendo_channel_file["demos_table"][i] = {}
    nintendo_channel_file["demos_table"][i]["id"] = f.id
    nintendo_channel_file["demos_table"][i]["title"] = f.title
    nintendo_channel_file["demos_table"][i]["subtitle"] = f.subtitle
    nintendo_channel_file["demos_table"][i]["titleid"] = f.titleid
    nintendo_channel_file["demos_table"][i]["company_offset"] = f.company_offset
    nintendo_channel_file["demos_table"][i]["removal_year"] = f.removal_year
    nintendo_channel_file["demos_table"][i]["removal_month"] = f.removal_month
    nintendo_channel_file["demos_table"][i]["removal_day"] = f.removal_day
    nintendo_channel_file["demos_table"][i]["unknown"] = f.unknown
    nintendo_channel_file["demos_table"][i]["rating_id"] = f.rating_id
    nintendo_channel_file["demos_table"][i]["new_tag"] = f.new_tag
    nintendo_channel_file["demos_table"][i]["new_tag_index"] = f.new_tag_index
    nintendo_channel_file["demos_table"][i]["unknown_2"] = f.unknown_2

    i += 1

i = 0

nintendo_channel_file["recent_recommendations_table"] = {}

for f in file.recent_recommendations_table:
    nintendo_channel_file["recent_recommendations_table"][i] = {}
    nintendo_channel_file["recent_recommendations_table"][i]["recent_recommendation_title_offset"] = f.recent_recommendation_title_offset
    nintendo_channel_file["recent_recommendations_table"][i]["unknown"] = f.unknown

    i += 1

i = 0

nintendo_channel_file["popular_videos_table"] = {}

for f in file.popular_videos_table:
    nintendo_channel_file["popular_videos_table"][i] = {}
    nintendo_channel_file["popular_videos_table"][i]["id"] = f.id
    nintendo_channel_file["popular_videos_table"][i]["time_length"] = f.time_length
    nintendo_channel_file["popular_videos_table"][i]["title_id"] = f.title_id
    nintendo_channel_file["popular_videos_table"][i]["bar_color"] = f.bar_color
    nintendo_channel_file["popular_videos_table"][i]["unknown_2"] = f.unknown_2
    nintendo_channel_file["popular_videos_table"][i]["rating_id"] = f.rating_id
    nintendo_channel_file["popular_videos_table"][i]["unknown_3"] = f.unknown_3
    nintendo_channel_file["popular_videos_table"][i]["video_rank"] = f.video_rank
    nintendo_channel_file["popular_videos_table"][i]["unknown_4"] = f.unknown_4
    nintendo_channel_file["popular_videos_table"][i]["title"] = f.title

    i += 1

i = 0

nintendo_channel_file["detailed_ratings_table"] = {}

for f in file.detailed_ratings_table:
    nintendo_channel_file["detailed_ratings_table"][i] = {}
    nintendo_channel_file["detailed_ratings_table"][i]["rating_group"] = f.rating_group
    nintendo_channel_file["detailed_ratings_table"][i]["rating_id"] = f.rating_id
    nintendo_channel_file["detailed_ratings_table"][i]["title"] = f.title

    i += 1
