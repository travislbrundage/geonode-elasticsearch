from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Integer, Text, Boolean, Date, Float
from django.conf import settings

connections.create_connection(hosts=[settings.ES_URL])


class LayerIndex(DocType):
    id = Integer()
    abstract = Text()
    category__gn_description = Text(analyzer='snowball')
    csw_type = Text(analyzer='snowball')
    csw_wkt_geometry = Text(analyzer='snowball')
    detail_url = Text(analyzer='snowball')
    owner__username = Text()
    owner__first_name = Text(analyzer='snowball')
    owner__last_name = Text(analyzer='snowball')
    is_published = Boolean()
    featured = Boolean()
    popular_count = Integer()
    share_count = Integer()
    rating = Integer()
    srid = Text(analyzer='snowball')
    supplemental_information = Text(analyzer='snowball')
    thumbnail_url = Text(analyzer='snowball')
    uuid = Text(analyzer='snowball')
    title = Text()
    date = Date()
    type = Text()
    subtype = Text()
    typename = Text(analyzer='snowball')
    title_sortable = Text()
    category = Text()
    bbox_left = Float()
    bbox_right = Float()
    bbox_bottom = Float()
    bbox_top = Float()
    temporal_extent_start = Date()
    temporal_extent_end = Date()
    keywords = Text(multi=True)
    regions = Text(multi=True)
    num_ratings = Integer()
    num_comments = Integer()
    geogig_link = Text(analyzer='snowball')
    has_time = Boolean()

    class Meta:
        index = 'layer-index'


class MapIndex(DocType):
    id = Integer()
    abstract = Text()
    category__gn_description = Text(analyzer='snowball')
    csw_type = Text(analyzer='snowball')
    csw_wkt_geometry = Text(analyzer='snowball')
    detail_url = Text(analyzer='snowball')
    owner__username = Text()
    popular_count = Integer()
    share_count = Integer()
    rating = Integer()
    srid = Text(analyzer='snowball')
    supplemental_information = Text(analyzer='snowball')
    thumbnail_url = Text(analyzer='snowball')
    uuid = Text(analyzer='snowball')
    title = Text()
    date = Date()
    type = Text()
    title_sortable = Text()
    category = Text()
    bbox_left = Float()
    bbox_right = Float()
    bbox_bottom = Float()
    bbox_top = Float()
    temporal_extent_start = Date()
    temporal_extent_end = Date()
    keywords = Text(multi=True)
    regions = Text(multi=True)
    num_ratings = Integer()
    num_comments = Integer()

    class Meta:
        index = 'map-index'


class DocumentIndex(DocType):
    id = Integer()
    abstract = Text()
    category__gn_description = Text(analyzer='snowball')
    csw_type = Text(analyzer='snowball')
    csw_wkt_geometry = Text(analyzer='snowball')
    detail_url = Text(analyzer='snowball')
    owner__username = Text()
    popular_count = Integer()
    share_count = Integer()
    rating = Integer()
    srid = Text(analyzer='snowball')
    supplemental_information = Text(analyzer='snowball')
    thumbnail_url = Text(analyzer='snowball')
    uuid = Text(analyzer='snowball')
    title = Text()
    date = Date()
    type = Text()
    title_sortable = Text()
    category = Text()
    bbox_left = Float()
    bbox_right = Float()
    bbox_bottom = Float()
    bbox_top = Float()
    temporal_extent_start = Date()
    temporal_extent_end = Date()
    keywords = Text(multi=True)
    regions = Text(multi=True)
    num_ratings = Integer()
    num_comments = Integer()

    class Meta:
        index = 'document-index'


class ProfileIndex(DocType):
    id = Integer()
    username = Text(analyzer='snowball')
    first_name = Text(analyzer='snowball')
    last_name = Text(analyzer='snowball')
    profile = Text(analyzer='snowball')
    organization = Text(analyzer='snowball')
    position = Text(analyzer='snowball')
    type = Text()

    class Meta:
        index = 'profile-index'


class GroupIndex(DocType):
    id = Integer()
    title = Text()
    title_sortable = Text()
    description = Text(analyzer='snowball')
    json = Text()
    type = Text()

    class Meta:
        index = 'group-index'


class StoryIndex(DocType):
    id = Integer()
    abstract = Text()
    category__gn_description = Text(analyzer='snowball')
    distribution_description = Text(analyzer='snowball')
    distribution_url = Text(analyzer='snowball')
    owner__username = Text()
    popular_count = Integer()
    share_count = Integer()
    rating = Integer()
    thumbnail_url = Text(analyzer='snowball')
    detail_url = Text(analyzer='snowball')
    uuid = Text(analyzer='snowball')
    title = Text(analyzer='snowball')
    date = Date()
    type = Text()
    title_sortable = Text()
    category = Text()
    bbox_left = Float()
    bbox_right = Float()
    bbox_bottom = Float()
    bbox_top = Float()
    temporal_extent_start = Date()
    temporal_extent_end = Date()
    keywords = Text(multi=True)
    regions = Text(multi=True)
    num_ratings = Integer()
    num_comments = Integer()
    num_chapters = Integer()
    owner__first_name = Text(analyzer='snowball')
    owner__last_name = Text(analyzer='snowball')
    is_published = Boolean()
    featured = Boolean()

    class Meta:
        index = 'story-index'
