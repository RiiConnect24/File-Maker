# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class NinchDllist(KaitaiStruct):

    class Genre(Enum):
        action = 1
        adventure = 2
        life_training = 3
        sports = 4
        puzzles = 5
        role_playing = 6
        racing = 7
        strategy = 8
        simulation = 9
        music_rhythm = 10
        board_game = 11
        shooter = 12
        other = 13
        fighting = 14
        arcade = 15
        imports = 16

    class YesNo(Enum):
        true = 0
        false = 1

    class EveryoneGamers(Enum):
        gamers = 0
        everyone = 1

    class Medal(Enum):
        none = 0
        bronze = 1
        silver = 2
        gold = 3
        platinum = 4

    class RatingGroup(Enum):
        cero = 1
        esrb = 2
        usk = 3
        pegi = 4
        pegi_fin = 5
        pegi_por = 6
        bbfc = 7
        oflc_agcb = 8
        oflc_nz = 9

    class AloneWithFriends(Enum):
        with_friends = 0
        alone = 1

    class CasualHardcore(Enum):
        hardcore = 0
        casual = 1
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.unknown = self._io.read_u2be()
        self.version = self._io.read_u1()
        self.unknown_region = self._io.read_u1()
        self.filesize = self._io.read_u4be()
        self.crc32 = self._io.read_u4be()
        self.dllistid = self._io.read_u4be()
        self.thumbnail_id = self._io.read_u4be()
        self.country_code = self._io.read_u4be()
        self.language_code = self._io.read_u4be()
        self.unknown_2 = [None] * (9)
        for i in range(9):
            self.unknown_2[i] = self._io.read_u1()

        self.ratings_entry_number = self._io.read_u4be()
        self.ratings_table_offset = self._io.read_u4be()
        self.title_types_entry_number = self._io.read_u4be()
        self.title_types_table_offset = self._io.read_u4be()
        self.company_entry_number = self._io.read_u4be()
        self.company_table_offset = self._io.read_u4be()
        self.title_entry_number = self._io.read_u4be()
        self.title_table_offset = self._io.read_u4be()
        self.new_title_entry_number = self._io.read_u4be()
        self.new_title_table_offset = self._io.read_u4be()
        self.videos_1_entry_number = self._io.read_u4be()
        self.videos_1_table_offset = self._io.read_u4be()
        self.new_video_entry_number = self._io.read_u4be()
        self.new_video_table_offset = self._io.read_u4be()
        self.demos_entry_number = self._io.read_u4be()
        self.demos_table_offset = self._io.read_u4be()
        self.unknown_5 = self._io.read_u4be()
        self.unknown_6 = self._io.read_u4be()
        self.recommendations_entry_number = self._io.read_u4be()
        self.recommendations_table_offset = self._io.read_u4be()
        self.unknown_7 = [None] * (4)
        for i in range(4):
            self.unknown_7[i] = self._io.read_u4be()

        self.recent_recommendations_entry_number = self._io.read_u4be()
        self.recent_recommendations_table_offset = self._io.read_u4be()
        self.unknown_8 = [None] * (2)
        for i in range(2):
            self.unknown_8[i] = self._io.read_u4be()

        self.popular_videos_entry_number = self._io.read_u4be()
        self.popular_videos_table_offset = self._io.read_u4be()
        self.detailed_ratings_entry_number = self._io.read_u4be()
        self.detailed_ratings_table_offset = self._io.read_u4be()
        self.last_update = (self._io.read_bytes(62)).decode(u"utf-16be")
        self.unknown_9 = [None] * (3)
        for i in range(3):
            self.unknown_9[i] = self._io.read_u1()

        self.dl_url_ids = [None] * (5)
        for i in range(5):
            self.dl_url_ids[i] = (self._io.read_bytes(256)).decode(u"utf-8")


    class NewVideoTable(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u4be()
            self.unknown = self._io.read_u2be()
            self.title_id = self._io.read_u4be()
            self.unknown_2 = [None] * (18)
            for i in range(18):
                self.unknown_2[i] = self._io.read_u1()

            self.title = (self._io.read_bytes(204)).decode(u"utf-16be")


    class RecommendationsTable(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.recommendation_title_offset = self._io.read_u4be()

        @property
        def recommendation_title_entry(self):
            if hasattr(self, '_m_recommendation_title_entry'):
                return self._m_recommendation_title_entry if hasattr(self, '_m_recommendation_title_entry') else None

            _pos = self._io.pos()
            self._io.seek(self.recommendation_title_offset)
            self._m_recommendation_title_entry = NinchDllist.TitleTable(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_recommendation_title_entry if hasattr(self, '_m_recommendation_title_entry') else None


    class NewTitleTable(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.new_title_offset = self._io.read_u4be()

        @property
        def new_title_entry(self):
            if hasattr(self, '_m_new_title_entry'):
                return self._m_new_title_entry if hasattr(self, '_m_new_title_entry') else None

            _pos = self._io.pos()
            self._io.seek(self.new_title_offset)
            self._m_new_title_entry = NinchDllist.TitleTable(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_new_title_entry if hasattr(self, '_m_new_title_entry') else None


    class DetailedRatingsTable(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rating_group = self._io.read_u1()
            self.rating_id = self._io.read_u1()
            self.title = (self._io.read_bytes(204)).decode(u"utf-16be")


    class CompanyTable(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u4be()
            self.dev_title = (self._io.read_bytes(62)).decode(u"utf-16be")
            self.pub_title = (self._io.read_bytes(62)).decode(u"utf-16be")


    class PopularVideosTable(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u4be()
            self.time_length = self._io.read_u2be()
            self.title_id = self._io.read_u4be()
            self.bar_color = self._io.read_u1()
            self.unknown_2 = [None] * (15)
            for i in range(15):
                self.unknown_2[i] = self._io.read_u1()

            self.rating_id = self._io.read_u1()
            self.unknown_3 = self._io.read_u1()
            self.video_rank = self._io.read_u1()
            self.unknown_4 = self._io.read_u1()
            self.title = (self._io.read_bytes(204)).decode(u"utf-16be")


    class RecentRecommendationsTable(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.recent_recommendation_title_offset = self._io.read_u4be()
            self.unknown = self._io.read_u2be()

        @property
        def recent_recommendation_title_entry(self):
            if hasattr(self, '_m_recent_recommendation_title_entry'):
                return self._m_recent_recommendation_title_entry if hasattr(self, '_m_recent_recommendation_title_entry') else None

            _pos = self._io.pos()
            self._io.seek(self.recent_recommendation_title_offset)
            self._m_recent_recommendation_title_entry = NinchDllist.TitleTable(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_recent_recommendation_title_entry if hasattr(self, '_m_recent_recommendation_title_entry') else None


    class TitleTypesTable(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type_id = self._io.read_u1()
            self.console_model = (self._io.read_bytes(3)).decode(u"utf-8")
            self.title = (self._io.read_bytes(102)).decode(u"utf-16be")
            self.group_id = self._io.read_u1()
            self.unknown = self._io.read_u1()


    class RatingsTable(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rating_id = self._io.read_u1()
            self.rating_group = KaitaiStream.resolve_enum(NinchDllist.RatingGroup, self._io.read_u1())
            self.age = self._io.read_u1()
            self.unknown = self._io.read_u1()
            self.jpeg_offset = self._io.read_u4be()
            self.jpeg_size = self._io.read_u4be()
            self.title = (self._io.read_bytes(22)).decode(u"utf-16be")


    class Videos1Table(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u4be()
            self.time_length = self._io.read_u2be()
            self.title_id = self._io.read_u4be()
            self.unknown = [None] * (15)
            for i in range(15):
                self.unknown[i] = self._io.read_u1()

            self.unknown_2 = self._io.read_u1()
            self.rating_id = self._io.read_u1()
            self.unknown_3 = self._io.read_u1()
            self.new_tag = self._io.read_u1()
            self.video_index = self._io.read_u1()
            self.unknown_4 = [None] * (2)
            for i in range(2):
                self.unknown_4[i] = self._io.read_u1()

            self.title = (self._io.read_bytes(246)).decode(u"utf-16be")


    class TitleTable(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u4be()
            self.title_id = (self._io.read_bytes(4)).decode(u"utf-8")
            self.title_type = self._io.read_u1()
            self.genre = [None] * (3)
            for i in range(3):
                self.genre[i] = KaitaiStream.resolve_enum(NinchDllist.Genre, self._io.read_u1())

            self.company_offset = self._io.read_u4be()
            self.release_date_year = self._io.read_u2be()
            self.release_date_month = self._io.read_u1()
            self.release_date_day = self._io.read_u1()
            self.rating_id = self._io.read_u1()
            self.unknown_1 = [None] * (2)
            for i in range(2):
                self.unknown_1[i] = self._io.read_u1()

            self.unknown_2 = self._io.read_bits_int_be(1) != 0
            self.casual_hardcore_1 = KaitaiStream.resolve_enum(NinchDllist.CasualHardcore, self._io.read_bits_int_be(1))
            self.unknown_3 = self._io.read_bits_int_be(1) != 0
            self.casual_hardcore_2 = KaitaiStream.resolve_enum(NinchDllist.CasualHardcore, self._io.read_bits_int_be(1))
            self.unknown_4 = self._io.read_bits_int_be(1) != 0
            self.casual_hardcore_3 = KaitaiStream.resolve_enum(NinchDllist.CasualHardcore, self._io.read_bits_int_be(1))
            self.unknown_5 = self._io.read_bits_int_be(1) != 0
            self.casual_hardcore_4 = KaitaiStream.resolve_enum(NinchDllist.CasualHardcore, self._io.read_bits_int_be(1))
            self.unknown_6 = self._io.read_bits_int_be(1) != 0
            self.casual_hardcore_5 = KaitaiStream.resolve_enum(NinchDllist.CasualHardcore, self._io.read_bits_int_be(1))
            self.unknown_7 = self._io.read_bits_int_be(1) != 0
            self.casual_hardcore_6 = KaitaiStream.resolve_enum(NinchDllist.CasualHardcore, self._io.read_bits_int_be(1))
            self.unknown_8 = self._io.read_bits_int_be(1) != 0
            self.casual_hardcore_7 = KaitaiStream.resolve_enum(NinchDllist.CasualHardcore, self._io.read_bits_int_be(1))
            self.unknown_9 = self._io.read_bits_int_be(1) != 0
            self.casual_hardcore_8 = KaitaiStream.resolve_enum(NinchDllist.CasualHardcore, self._io.read_bits_int_be(1))
            self.unknown_10 = self._io.read_bits_int_be(1) != 0
            self.casual_hardcore_9 = KaitaiStream.resolve_enum(NinchDllist.CasualHardcore, self._io.read_bits_int_be(1))
            self.unknown_11 = self._io.read_bits_int_be(1) != 0
            self.casual_hardcore_10 = KaitaiStream.resolve_enum(NinchDllist.CasualHardcore, self._io.read_bits_int_be(1))
            self.unknown_12 = self._io.read_bits_int_be(1) != 0
            self.casual_hardcore_11 = KaitaiStream.resolve_enum(NinchDllist.CasualHardcore, self._io.read_bits_int_be(1))
            self.unknown_13 = self._io.read_bits_int_be(1) != 0
            self.casual_hardcore_12 = KaitaiStream.resolve_enum(NinchDllist.CasualHardcore, self._io.read_bits_int_be(1))
            self.unknown_14 = self._io.read_bits_int_be(7)
            self.casual_hardcore_all_ages_and_genders = KaitaiStream.resolve_enum(NinchDllist.CasualHardcore, self._io.read_bits_int_be(1))
            self.everyone_gamers_1 = KaitaiStream.resolve_enum(NinchDllist.EveryoneGamers, self._io.read_bits_int_be(1))
            self.alone_with_friends_1 = KaitaiStream.resolve_enum(NinchDllist.AloneWithFriends, self._io.read_bits_int_be(1))
            self.everyone_gamers_2 = KaitaiStream.resolve_enum(NinchDllist.EveryoneGamers, self._io.read_bits_int_be(1))
            self.alone_with_friends_2 = KaitaiStream.resolve_enum(NinchDllist.AloneWithFriends, self._io.read_bits_int_be(1))
            self.everyone_gamers_3 = KaitaiStream.resolve_enum(NinchDllist.EveryoneGamers, self._io.read_bits_int_be(1))
            self.alone_with_friends_3 = KaitaiStream.resolve_enum(NinchDllist.AloneWithFriends, self._io.read_bits_int_be(1))
            self.everyone_gamers_4 = KaitaiStream.resolve_enum(NinchDllist.EveryoneGamers, self._io.read_bits_int_be(1))
            self.alone_with_friends_4 = KaitaiStream.resolve_enum(NinchDllist.AloneWithFriends, self._io.read_bits_int_be(1))
            self.everyone_gamers_5 = KaitaiStream.resolve_enum(NinchDllist.EveryoneGamers, self._io.read_bits_int_be(1))
            self.alone_with_friends_5 = KaitaiStream.resolve_enum(NinchDllist.AloneWithFriends, self._io.read_bits_int_be(1))
            self.everyone_gamers_6 = KaitaiStream.resolve_enum(NinchDllist.EveryoneGamers, self._io.read_bits_int_be(1))
            self.alone_with_friends_6 = KaitaiStream.resolve_enum(NinchDllist.AloneWithFriends, self._io.read_bits_int_be(1))
            self.everyone_gamers_7 = KaitaiStream.resolve_enum(NinchDllist.EveryoneGamers, self._io.read_bits_int_be(1))
            self.alone_with_friends_7 = KaitaiStream.resolve_enum(NinchDllist.AloneWithFriends, self._io.read_bits_int_be(1))
            self.everyone_gamers_8 = KaitaiStream.resolve_enum(NinchDllist.EveryoneGamers, self._io.read_bits_int_be(1))
            self.alone_with_friends_8 = KaitaiStream.resolve_enum(NinchDllist.AloneWithFriends, self._io.read_bits_int_be(1))
            self.everyone_gamers_9 = KaitaiStream.resolve_enum(NinchDllist.EveryoneGamers, self._io.read_bits_int_be(1))
            self.alone_with_friends_9 = KaitaiStream.resolve_enum(NinchDllist.AloneWithFriends, self._io.read_bits_int_be(1))
            self.everyone_gamers_10 = KaitaiStream.resolve_enum(NinchDllist.EveryoneGamers, self._io.read_bits_int_be(1))
            self.alone_with_friends_10 = KaitaiStream.resolve_enum(NinchDllist.AloneWithFriends, self._io.read_bits_int_be(1))
            self.everyone_gamers_11 = KaitaiStream.resolve_enum(NinchDllist.EveryoneGamers, self._io.read_bits_int_be(1))
            self.alone_with_friends_11 = KaitaiStream.resolve_enum(NinchDllist.AloneWithFriends, self._io.read_bits_int_be(1))
            self.everyone_gamers_12 = KaitaiStream.resolve_enum(NinchDllist.EveryoneGamers, self._io.read_bits_int_be(1))
            self.alone_with_friends_12 = KaitaiStream.resolve_enum(NinchDllist.AloneWithFriends, self._io.read_bits_int_be(1))
            self.unknown_15 = self._io.read_bits_int_be(6)
            self.everyone_gamers_all_ages_and_genders = KaitaiStream.resolve_enum(NinchDllist.EveryoneGamers, self._io.read_bits_int_be(1))
            self.alone_with_friends_all_ages_and_genders = KaitaiStream.resolve_enum(NinchDllist.AloneWithFriends, self._io.read_bits_int_be(1))
            self._io.align_to_byte()
            self.unknown_16 = [None] * (7)
            for i in range(7):
                self.unknown_16[i] = self._io.read_u1()

            self.unknown_17 = self._io.read_bits_int_be(5)
            self.online = KaitaiStream.resolve_enum(NinchDllist.YesNo, self._io.read_bits_int_be(1))
            self.video_flag = KaitaiStream.resolve_enum(NinchDllist.YesNo, self._io.read_bits_int_be(1))
            self.multiplayer = KaitaiStream.resolve_enum(NinchDllist.YesNo, self._io.read_bits_int_be(1))
            self._io.align_to_byte()
            self.unknown_18 = [None] * (8)
            for i in range(8):
                self.unknown_18[i] = self._io.read_u1()

            self.unknown_19 = self._io.read_bits_int_be(5)
            self.medal = KaitaiStream.resolve_enum(NinchDllist.Medal, self._io.read_bits_int_be(3))
            self._io.align_to_byte()
            self.unknown_20 = [None] * (2)
            for i in range(2):
                self.unknown_20[i] = self._io.read_u1()

            self.title = (self._io.read_bytes(62)).decode(u"utf-16be")
            self.subtitle = (self._io.read_bytes(62)).decode(u"utf-16be")
            self.short_title = (self._io.read_bytes(62)).decode(u"utf-16be")

        @property
        def company_entry(self):
            if hasattr(self, '_m_company_entry'):
                return self._m_company_entry if hasattr(self, '_m_company_entry') else None

            _pos = self._io.pos()
            self._io.seek(self.company_offset)
            self._m_company_entry = NinchDllist.CompanyTable(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_company_entry if hasattr(self, '_m_company_entry') else None


    class DemosTable(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u4be()
            self.title = (self._io.read_bytes(62)).decode(u"utf-16be")
            self.subtitle = (self._io.read_bytes(62)).decode(u"utf-16be")
            self.titleid = self._io.read_u4be()
            self.company_offset = self._io.read_u4be()
            self.removal_year = self._io.read_u2be()
            self.removal_month = self._io.read_u1()
            self.removal_day = self._io.read_u1()
            self.unknown = self._io.read_u4be()
            self.rating_id = self._io.read_u1()
            self.new_tag = self._io.read_u1()
            self.new_tag_index = self._io.read_u1()
            self.unknown_2 = [None] * (205)
            for i in range(205):
                self.unknown_2[i] = self._io.read_u1()


        @property
        def company_entry(self):
            if hasattr(self, '_m_company_entry'):
                return self._m_company_entry if hasattr(self, '_m_company_entry') else None

            _pos = self._io.pos()
            self._io.seek(self.company_offset)
            self._m_company_entry = NinchDllist.CompanyTable(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_company_entry if hasattr(self, '_m_company_entry') else None


    @property
    def demos_table(self):
        if hasattr(self, '_m_demos_table'):
            return self._m_demos_table if hasattr(self, '_m_demos_table') else None

        _pos = self._io.pos()
        self._io.seek(self.demos_table_offset)
        self._m_demos_table = [None] * (self.demos_entry_number)
        for i in range(self.demos_entry_number):
            self._m_demos_table[i] = NinchDllist.DemosTable(self._io, self, self._root)

        self._io.seek(_pos)
        return self._m_demos_table if hasattr(self, '_m_demos_table') else None

    @property
    def ratings_table(self):
        if hasattr(self, '_m_ratings_table'):
            return self._m_ratings_table if hasattr(self, '_m_ratings_table') else None

        _pos = self._io.pos()
        self._io.seek(self.ratings_table_offset)
        self._m_ratings_table = [None] * (self.ratings_entry_number)
        for i in range(self.ratings_entry_number):
            self._m_ratings_table[i] = NinchDllist.RatingsTable(self._io, self, self._root)

        self._io.seek(_pos)
        return self._m_ratings_table if hasattr(self, '_m_ratings_table') else None

    @property
    def videos_1_table(self):
        if hasattr(self, '_m_videos_1_table'):
            return self._m_videos_1_table if hasattr(self, '_m_videos_1_table') else None

        _pos = self._io.pos()
        self._io.seek(self.videos_1_table_offset)
        self._m_videos_1_table = [None] * (self.videos_1_entry_number)
        for i in range(self.videos_1_entry_number):
            self._m_videos_1_table[i] = NinchDllist.Videos1Table(self._io, self, self._root)

        self._io.seek(_pos)
        return self._m_videos_1_table if hasattr(self, '_m_videos_1_table') else None

    @property
    def recent_recommendations_table(self):
        if hasattr(self, '_m_recent_recommendations_table'):
            return self._m_recent_recommendations_table if hasattr(self, '_m_recent_recommendations_table') else None

        _pos = self._io.pos()
        self._io.seek(self.recent_recommendations_table_offset)
        self._m_recent_recommendations_table = [None] * (self.recent_recommendations_entry_number)
        for i in range(self.recent_recommendations_entry_number):
            self._m_recent_recommendations_table[i] = NinchDllist.RecentRecommendationsTable(self._io, self, self._root)

        self._io.seek(_pos)
        return self._m_recent_recommendations_table if hasattr(self, '_m_recent_recommendations_table') else None

    @property
    def title_table(self):
        if hasattr(self, '_m_title_table'):
            return self._m_title_table if hasattr(self, '_m_title_table') else None

        _pos = self._io.pos()
        self._io.seek(self.title_table_offset)
        self._m_title_table = [None] * (self.title_entry_number)
        for i in range(self.title_entry_number):
            self._m_title_table[i] = NinchDllist.TitleTable(self._io, self, self._root)

        self._io.seek(_pos)
        return self._m_title_table if hasattr(self, '_m_title_table') else None

    @property
    def detailed_ratings_table(self):
        if hasattr(self, '_m_detailed_ratings_table'):
            return self._m_detailed_ratings_table if hasattr(self, '_m_detailed_ratings_table') else None

        _pos = self._io.pos()
        self._io.seek(self.detailed_ratings_table_offset)
        self._m_detailed_ratings_table = [None] * (self.detailed_ratings_entry_number)
        for i in range(self.detailed_ratings_entry_number):
            self._m_detailed_ratings_table[i] = NinchDllist.DetailedRatingsTable(self._io, self, self._root)

        self._io.seek(_pos)
        return self._m_detailed_ratings_table if hasattr(self, '_m_detailed_ratings_table') else None

    @property
    def popular_videos_table(self):
        if hasattr(self, '_m_popular_videos_table'):
            return self._m_popular_videos_table if hasattr(self, '_m_popular_videos_table') else None

        _pos = self._io.pos()
        self._io.seek(self.popular_videos_table_offset)
        self._m_popular_videos_table = [None] * (self.popular_videos_entry_number)
        for i in range(self.popular_videos_entry_number):
            self._m_popular_videos_table[i] = NinchDllist.PopularVideosTable(self._io, self, self._root)

        self._io.seek(_pos)
        return self._m_popular_videos_table if hasattr(self, '_m_popular_videos_table') else None

    @property
    def title_types_table(self):
        if hasattr(self, '_m_title_types_table'):
            return self._m_title_types_table if hasattr(self, '_m_title_types_table') else None

        _pos = self._io.pos()
        self._io.seek(self.title_types_table_offset)
        self._m_title_types_table = [None] * (self.title_types_entry_number)
        for i in range(self.title_types_entry_number):
            self._m_title_types_table[i] = NinchDllist.TitleTypesTable(self._io, self, self._root)

        self._io.seek(_pos)
        return self._m_title_types_table if hasattr(self, '_m_title_types_table') else None

    @property
    def recommendations_table(self):
        if hasattr(self, '_m_recommendations_table'):
            return self._m_recommendations_table if hasattr(self, '_m_recommendations_table') else None

        _pos = self._io.pos()
        self._io.seek(self.recommendations_table_offset)
        self._m_recommendations_table = [None] * (self.recommendations_entry_number)
        for i in range(self.recommendations_entry_number):
            self._m_recommendations_table[i] = NinchDllist.RecommendationsTable(self._io, self, self._root)

        self._io.seek(_pos)
        return self._m_recommendations_table if hasattr(self, '_m_recommendations_table') else None

    @property
    def new_video_table(self):
        if hasattr(self, '_m_new_video_table'):
            return self._m_new_video_table if hasattr(self, '_m_new_video_table') else None

        _pos = self._io.pos()
        self._io.seek(self.new_video_table_offset)
        self._m_new_video_table = [None] * (self.new_video_entry_number)
        for i in range(self.new_video_entry_number):
            self._m_new_video_table[i] = NinchDllist.NewVideoTable(self._io, self, self._root)

        self._io.seek(_pos)
        return self._m_new_video_table if hasattr(self, '_m_new_video_table') else None

    @property
    def new_title_table(self):
        if hasattr(self, '_m_new_title_table'):
            return self._m_new_title_table if hasattr(self, '_m_new_title_table') else None

        _pos = self._io.pos()
        self._io.seek(self.new_title_table_offset)
        self._m_new_title_table = [None] * (self.new_title_entry_number)
        for i in range(self.new_title_entry_number):
            self._m_new_title_table[i] = NinchDllist.NewTitleTable(self._io, self, self._root)

        self._io.seek(_pos)
        return self._m_new_title_table if hasattr(self, '_m_new_title_table') else None

    @property
    def company_table(self):
        if hasattr(self, '_m_company_table'):
            return self._m_company_table if hasattr(self, '_m_company_table') else None

        _pos = self._io.pos()
        self._io.seek(self.company_table_offset)
        self._m_company_table = [None] * (self.company_entry_number)
        for i in range(self.company_entry_number):
            self._m_company_table[i] = NinchDllist.CompanyTable(self._io, self, self._root)

        self._io.seek(_pos)
        return self._m_company_table if hasattr(self, '_m_company_table') else None


