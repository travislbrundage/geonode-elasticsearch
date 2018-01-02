from elasticsearch_dsl import (
    DocType,
    Integer,
    Keyword,
    Boolean,
    Date,
    Float,
    Text,
    connections
)
from django.conf import settings

connections.create_connection(hosts=[settings.ES_URL])


class LayerIndex(DocType):
    id = Integer()
    abstract = Text()
    category__gn_description = Text()
    csw_type = Keyword()
    csw_wkt_geometry = Keyword()
    detail_url = Keyword()
    owner__username = Keyword()
    owner__first_name = Text()
    owner__last_name = Text()
    is_published = Boolean()
    featured = Boolean()
    popular_count = Integer()
    share_count = Integer()
    rating = Integer()
    srid = Keyword()
    supplemental_information = Text()
    thumbnail_url = Keyword()
    uuid = Keyword()
    title = Text()
    date = Date()
    type = Keyword()
    subtype = Keyword()
    typename = Keyword()
    title_sortable = Text()
    category = Keyword()
    bbox_left = Float()
    bbox_right = Float()
    bbox_bottom = Float()
    bbox_top = Float()
    temporal_extent_start = Date()
    temporal_extent_end = Date()
    keywords = Keyword(multi=True)
    regions = Text(multi=True)
    num_ratings = Integer()
    num_comments = Integer()
    geogig_link = Keyword()
    has_time = Boolean()

    class Meta:
        index = 'layer-index'


class MapIndex(DocType):
    id = Integer()
    abstract = Text()
    category__gn_description = Keyword()
    csw_type = Keyword()
    csw_wkt_geometry = Keyword()
    detail_url = Keyword()
    owner__username = Keyword()
    popular_count = Integer()
    share_count = Integer()
    rating = Integer()
    srid = Keyword()
    supplemental_information = Text()
    thumbnail_url = Keyword()
    uuid = Keyword()
    title = Text()
    date = Date()
    type = Keyword()
    title_sortable = Text()
    category = Keyword()
    bbox_left = Float()
    bbox_right = Float()
    bbox_bottom = Float()
    bbox_top = Float()
    temporal_extent_start = Date()
    temporal_extent_end = Date()
    keywords = Keyword(multi=True)
    regions = Text(multi=True)
    num_ratings = Integer()
    num_comments = Integer()

    class Meta:
        index = 'map-index'


class DocumentIndex(DocType):
    id = Integer()
    abstract = Text()
    category__gn_description = Keyword()
    csw_type = Keyword()
    csw_wkt_geometry = Keyword()
    detail_url = Keyword()
    owner__username = Keyword()
    popular_count = Integer()
    share_count = Integer()
    rating = Integer()
    srid = Keyword()
    supplemental_information = Text()
    thumbnail_url = Keyword()
    uuid = Keyword()
    title = Text()
    date = Date()
    type = Keyword()
    title_sortable = Text()
    category = Keyword()
    bbox_left = Float()
    bbox_right = Float()
    bbox_bottom = Float()
    bbox_top = Float()
    temporal_extent_start = Date()
    temporal_extent_end = Date()
    keywords = Keyword(multi=True)
    regions = Text(multi=True)
    num_ratings = Integer()
    num_comments = Integer()

    class Meta:
        index = 'document-index'


class ProfileIndex(DocType):
    id = Integer()
    username = Keyword()
    first_name = Keyword()
    last_name = Keyword()
    profile = Keyword()
    organization = Text()
    position = Keyword()
    type = Keyword()

    class Meta:
        index = 'profile-index'


class GroupIndex(DocType):
    id = Integer()
    title = Text()
    title_sortable = Text()
    description = Text()
    json = Text()
    type = Keyword()

    class Meta:
        index = 'group-index'


class StoryIndex(DocType):
    id = Integer()
    abstract = Text()
    category__gn_description = Keyword()
    distribution_description = Keyword()
    distribution_url = Keyword()
    owner__username = Keyword()
    popular_count = Integer()
    share_count = Integer()
    rating = Integer()
    thumbnail_url = Keyword()
    detail_url = Keyword()
    uuid = Keyword()
    title = Text()
    date = Date()
    type = Keyword()
    title_sortable = Text()
    category = Keyword()
    bbox_left = Float()
    bbox_right = Float()
    bbox_bottom = Float()
    bbox_top = Float()
    temporal_extent_start = Date()
    temporal_extent_end = Date()
    keywords = Keyword(multi=True)
    regions = Text(multi=True)
    num_ratings = Integer()
    num_comments = Integer()
    num_chapters = Integer()
    owner__first_name = Keyword()
    owner__last_name = Keyword()
    is_published = Boolean()
    featured = Boolean()

    class Meta:
        index = 'story-index'
