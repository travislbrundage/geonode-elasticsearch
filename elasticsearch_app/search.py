from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Integer, String, Boolean, Date, Float
from django.conf import settings

connections.create_connection(hosts=[settings.ES_URL])


class LayerIndex(DocType):
    id = Integer()
    abstract = String(analyzer='snowball')
    category__gn_description = String(analyzer='snowball')
    csw_type = String(analyzer='snowball')
    csw_wkt_geometry = String(analyzer='snowball')
    detail_url = String(analyzer='snowball')
    owner__username = String(analyzer='snowball')
    owner__first_name = String(analyzer='snowball')
    owner__last_name = String(analyzer='snowball')
    is_published = Boolean()
    featured = Boolean()
    popular_count = Integer()
    share_count = Integer()
    rating = Integer()
    srid = String(analyzer='snowball')
    supplemental_information = String(analyzer='snowball')
    thumbnail_url = String(analyzer='snowball')
    uuid = String(analyzer='snowball')
    title = String(analyzer='snowball')
    date = Date()
    type = String(analyzer='snowball')
    subtype = String(analyzer='snowball')
    typename = String(analyzer='snowball')
    title_sortable = String()
    category = String(analyzer='snowball')
    bbox_left = Float()
    bbox_right = Float()
    bbox_bottom = Float()
    bbox_top = Float()
    temporal_extent_start = Date()
    temporal_extent_end = Date()
    keywords = String(multi=True, analyzer='snowball')
    regions = String(multi=True, analyzer='snowball')
    num_ratings = Integer()
    num_comments = Integer()
    geogig_link = String(analyzer='snowball')
    has_time = Boolean()

    class Meta:
        index = 'layer-index'


class MapIndex(DocType):
    id = Integer()
    abstract = String(analyzer='snowball')
    category__gn_description = String(analyzer='snowball')
    csw_type = String(analyzer='snowball')
    csw_wkt_geometry = String(analyzer='snowball')
    detail_url = String(analyzer='snowball')
    owner__username = String(analyzer='snowball')
    popular_count = Integer()
    share_count = Integer()
    rating = Integer()
    srid = String(analyzer='snowball')
    supplemental_information = String(analyzer='snowball')
    thumbnail_url = String(analyzer='snowball')
    uuid = String(analyzer='snowball')
    title = String(analyzer='snowball')
    date = Date()
    type = String(analyzer='snowball')
    title_sortable = String()
    category = String(analyzer='snowball')
    bbox_left = Float()
    bbox_right = Float()
    bbox_bottom = Float()
    bbox_top = Float()
    temporal_extent_start = Date()
    temporal_extent_end = Date()
    keywords = String(multi=True, analyzer='snowball')
    regions = String(multi=True, analyzer='snowball')
    num_ratings = Integer()
    num_comments = Integer()

    class Meta:
        index = 'map-index'


class DocumentIndex(DocType):
    id = Integer()
    abstract = String(analyzer='snowball')
    category__gn_description = String(analyzer='snowball')
    csw_type = String(analyzer='snowball')
    csw_wkt_geometry = String(analyzer='snowball')
    detail_url = String(analyzer='snowball')
    owner__username = String(analyzer='snowball')
    popular_count = Integer()
    share_count = Integer()
    rating = Integer()
    srid = String(analyzer='snowball')
    supplemental_information = String(analyzer='snowball')
    thumbnail_url = String(analyzer='snowball')
    uuid = String(analyzer='snowball')
    title = String(analyzer='snowball')
    date = Date()
    type = String(analyzer='snowball')
    title_sortable = String()
    category = String(analyzer='snowball')
    bbox_left = Float()
    bbox_right = Float()
    bbox_bottom = Float()
    bbox_top = Float()
    temporal_extent_start = Date()
    temporal_extent_end = Date()
    keywords = String(multi=True, analyzer='snowball')
    regions = String(multi=True, analyzer='snowball')
    num_ratings = Integer()
    num_comments = Integer()

    class Meta:
        index = 'document-index'


class ProfileIndex(DocType):
    id = Integer()
    username = String(analyzer='snowball')
    first_name = String(analyzer='snowball')
    last_name = String(analyzer='snowball')
    profile = String(analyzer='snowball')
    organization = String(analyzer='snowball')
    position = String(analyzer='snowball')
    type = String(analyzer='snowball')

    class Meta:
        index = 'profile-index'


class GroupIndex(DocType):
    id = Integer()
    title = String(analyzer='snowball')
    title_sortable = String()
    description = String(analyzer='snowball')
    json = String()
    type = String(analyzer='snowball')

    class Meta:
        index = 'group-index'


class StoryIndex(DocType):
    id = Integer()
    abstract = String(analyzer='snowball')
    category__gn_description = String(analyzer='snowball')
    distribution_description = String(analyzer='snowball')
    distribution_url = String(analyzer='snowball')
    owner__username = String(analyzer='snowball')
    popular_count = Integer()
    share_count = Integer()
    rating = Integer()
    thumbnail_url = String(analyzer='snowball')
    detail_url = String(analyzer='snowball')
    uuid = String(analyzer='snowball')
    title = String(analyzer='snowball')
    date = Date()
    type = String(analyzer='snowball')
    title_sortable = String()
    category = String(analyzer='snowball')
    bbox_left = Float()
    bbox_right = Float()
    bbox_bottom = Float()
    bbox_top = Float()
    temporal_extent_start = Date()
    temporal_extent_end = Date()
    keywords = String(multi=True, analyzer='snowball')
    regions = String(multi=True, analyzer='snowball')
    num_ratings = Integer()
    num_comments = Integer()
    num_chapters = Integer()
    owner__first_name = String(analyzer='snowball')
    owner__last_name = String(analyzer='snowball')
    is_published = Boolean()
    featured = Boolean()

    class Meta:
        index = 'story-index'
