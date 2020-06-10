# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class NinchDllist(KaitaiStruct):
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

        self.unknown_10 = [None] * (4)
        for i in range(4):
            self.unknown_10[i] = self._io.read_u1()


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
            self._m_recommendation_title_entry = self._root.TitleTable(self._io, self, self._root)
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
            self._m_new_title_entry = self._root.TitleTable(self._io, self, self._root)
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
            self._m_recent_recommendation_title_entry = self._root.TitleTable(self._io, self, self._root)
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
            self.unknown = self._io.read_u1()
            self.age = self._io.read_u1()
            self.unknown2 = self._io.read_u1()
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
                self.genre[i] = self._io.read_u1()

            self.company_offset = self._io.read_u4be()
            self.release_date_year = self._io.read_u2be()
            self.release_date_month = self._io.read_u1()
            self.release_date_day = self._io.read_u1()
            self.rating_id = self._io.read_u1()
            self.unknown_4 = [None] * (29)
            for i in range(29):
                self.unknown_4[i] = self._io.read_u1()

            self.title = (self._io.read_bytes(62)).decode(u"utf-16be")
            self.subtitle = (self._io.read_bytes(62)).decode(u"utf-16be")
            self.short_title = (self._io.read_bytes(62)).decode(u"utf-16be")

        @property
        def company_entry(self):
            if hasattr(self, '_m_company_entry'):
                return self._m_company_entry if hasattr(self, '_m_company_entry') else None

            _pos = self._io.pos()
            self._io.seek(self.company_offset)
            self._m_company_entry = self._root.CompanyTable(self._io, self, self._root)
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
            self._m_company_entry = self._root.CompanyTable(self._io, self, self._root)
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
            self._m_demos_table[i] = self._root.DemosTable(self._io, self, self._root)

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
            self._m_ratings_table[i] = self._root.RatingsTable(self._io, self, self._root)

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
            self._m_videos_1_table[i] = self._root.Videos1Table(self._io, self, self._root)

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
            self._m_recent_recommendations_table[i] = self._root.RecentRecommendationsTable(self._io, self, self._root)

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
            self._m_title_table[i] = self._root.TitleTable(self._io, self, self._root)

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
            self._m_detailed_ratings_table[i] = self._root.DetailedRatingsTable(self._io, self, self._root)

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
            self._m_popular_videos_table[i] = self._root.PopularVideosTable(self._io, self, self._root)

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
            self._m_title_types_table[i] = self._root.TitleTypesTable(self._io, self, self._root)

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
            self._m_recommendations_table[i] = self._root.RecommendationsTable(self._io, self, self._root)

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
            self._m_new_video_table[i] = self._root.NewVideoTable(self._io, self, self._root)

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
            self._m_new_title_table[i] = self._root.NewTitleTable(self._io, self, self._root)

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
            self._m_company_table[i] = self._root.CompanyTable(self._io, self, self._root)

        self._io.seek(_pos)
        return self._m_company_table if hasattr(self, '_m_company_table') else None


