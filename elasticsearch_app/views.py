import re
import logging
from django.http import JsonResponse
# Does this 'just work'? Feels like we need to do something else
from django.conf import settings
# How to handle this situation too?
try:
    from geonode.base.models import TopicCategory
except ImportError:
    pass


logger = logging.getLogger(__name__)


# Reformat objects for use in the results.
#
# The ES objects need some reformatting in order to be useful
# for output to the client.
#
def get_unified_search_result_objects(hits):
    objects = []
    for hit in hits:
        try:
            source = hit.get('_source')
        except:  # No source
            pass
        result = {}
        result['index'] = hit.get('_index', None)
        registry_url = settings.REGISTRYURL.rstrip('/')
        for key, value in source.iteritems():
            if key == 'bbox':
                result['bbox_left'] = value[0]
                result['bbox_bottom'] = value[1]
                result['bbox_right'] = value[2]
                result['bbox_top'] = value[3]
            elif key == 'links':
                # Get source link from Registry
                xml = value['xml']
                js = '%s/%s' % (registry_url,
                                re.sub(r"xml$", "js", xml))
                png = '%s/%s' % (registry_url,
                                 value['png'])
                result['registry_url'] = js
                result['thumbnail_url'] = png

            else:
                result[key] = source.get(key, None)
        objects.append(result)

    return objects


# Function returns a generator searching recursively for a key in a dict
def gen_dict_extract(key, var):
    if hasattr(var, 'iteritems'):
        for k, v in var.iteritems():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result


# Checks if key is present in dictionary
def key_exists(key, var):
    return any(True for _ in gen_dict_extract(key, var))


def elastic_search(request, resourcetype='base'):
    from elasticsearch import Elasticsearch
    from six import iteritems
    from guardian.shortcuts import get_objects_for_user

    # elasticsearch_dsl overwrites any double underscores with a .
    # this changes the default to not overwrite
    import elasticsearch_dsl as edsl

    def newDSLBaseInit(self, _expand__to_dot=False, **params):
        self._params = {}
        for pname, pvalue in iteritems(params):
            if '__' in pname and _expand__to_dot:
                pname = pname.replace('__', '.')
            self._setattr(pname, pvalue)
    edsl.utils.DslBase.__init__ = newDSLBaseInit
    Search = edsl.Search
    Q = edsl.query.Q

    parameters = request.GET
    es = Elasticsearch(settings.ES_URL)
    search = Search(using=es)

    # Set base fields to search
    fields = ['title', 'abstract', 'title_alternate']

    # This configuration controls what fields will be added to faceted search
    # there is some special exception code later that combines the subtype
    # search and facet with type
    additional_facets = getattr(settings, 'ADDITIONAL_FACETS', {})

    facet_fields = ['type', 'subtype',
                    'owner__username', 'keywords', 'category', 'source_host',
                    'regions']

    if additional_facets:
        facet_fields.extend(additional_facets.keys())

    categories = TopicCategory.objects.all()
    category_lookup = {}
    for c in categories:
        if c.is_choice:
            category_lookup[c.identifier] = {
                'display': c.description,
                'icon': c.fa_class
            }

    facet_lookups = {
        'category': category_lookup,
        'type': {
            'OGC:WMS': {'display': 'ESRI MapServer'},
            'OGC:WFS': {'display': 'ESRI MapServer'},
            'OGC:WCS': {'display': 'ESRI MapServer'},
            'ESRI:ArcGIS:MapServer': {'display': 'ArcGIS MapServer'},
            'ESRI:ArcGIS:ImageServer': {'display': 'ArcGIS ImageServer'}
        }
    }

    # Allows settings that can be used by a client for display of the facets
    # 'open' is used by exchange client side to determine if a facet menu shows
    # up open or closed by default
    default_facet_settings = {'open': False, 'show': True}
    facet_settings = {
        'category': default_facet_settings,
        'source_host': {'open': False, 'display': 'Host'},
        'owner__username': {'open': True, 'display': 'Owner'},
        'type': {'open': True, 'display': 'Type'},
        'keywords': {'show': True},
        'regions': {'show': True}
    }

    if additional_facets:
        facet_settings.update(additional_facets)

    # Get paging parameters
    offset = int(parameters.get('offset', '0'))
    limit = int(parameters.get('limit', settings.API_LIMIT_PER_PAGE))

    # Text search
    query = parameters.get('q', None)

    # Sort order
    sort = parameters.get("order_by", "relevance")

    # Geospatial Elements
    bbox = parameters.get("extent", None)

    # get has_time element not used with facets
    has_time = parameters.get("has_time", None)

    # get max number of facets to return
    nfacets = parameters.get("nfacets", 15)

    # Build base query
    # The base query only includes filters relevant to what the user
    # is allowed to see and the overall types of documents to search.
    # This provides the overall counts and all fields for faceting

    # only show registry, documents, layers, stories, and maps
    q = Q({"match": {"_type": "layer"}}) | Q(
        {"match": {"type": "layer"}}) | Q(
        {"match": {"type": "story"}}) | Q(
        {"match": {"type": "document"}}) | Q(
        {"match": {"type": "map"}})
    search = search.query(q)

    # Filter geonode layers by permissions
    if not settings.SKIP_PERMS_FILTER:
        # Get the list of objects the user has access to
        filter_set = get_objects_for_user(
            request.user, 'base.view_resourcebase')
        if settings.RESOURCE_PUBLISHING:
            filter_set = filter_set.filter(is_published=True)

        filter_set_ids = map(str, filter_set.values_list('id', flat=True))
        # Do the query using the filterset and the query term. Facet the
        # results
        # Always show registry layers since they lack permissions
        q = Q({"match": {"_type": "layer"}})
        if len(filter_set_ids) > 0:
            q = Q({"terms": {"id": filter_set_ids}}) | q

        search = search.query(q)

    # Add facets to search
    # add filters to facet_filters to be used *after* initial overall search
    valid_facet_fields = []
    facet_filters = []
    for fn in facet_fields:
        if fn:
            valid_facet_fields.append(fn)
            search.aggs.bucket(
                fn, 'terms', field=fn, order={"_count": "desc"}, size=nfacets)
            # if there is a filter set in the parameters for this facet
            # add to the filters
            fp = parameters.getlist(fn)
            if not fp:
                fp = parameters.getlist("%s__in" % (fn))
            if fp:
                fq = Q({'terms': {fn: fp}})
                if fn == 'type':  # search across both type_exact and subtype
                    fq = fq | Q({'terms': {'subtype': fp}})
                facet_filters.append(fq)

    # run search only filtered by what a particular user is able to see
    # this makes sure to get every item that is possible in the facets
    # in order for a UI to build the choices
    overall_results = search[0:0].execute()

    # build up facets dict which contains all the options for a facet along
    # with overall count and any display name or icon that should be used in UI
    aggregations = overall_results.aggregations
    facet_results = {}
    for k in aggregations.to_dict():
        buckets = aggregations[k]['buckets']
        if len(buckets) > 0:
            lookup = None
            if k in facet_lookups:
                lookup = facet_lookups[k]
            fsettings = default_facet_settings.copy()
            fsettings['display'] = k
            # Default display to the id of the facet in case none is set
            if k in facet_settings:
                fsettings.update(facet_settings[k])
            if parameters.getlist(k):
                # Make sure list starts open when a filter is set
                fsettings['open'] = True
            facet_results[k] = {'settings': fsettings, 'facets': {}}

            for bucket in buckets:
                bucket_key = bucket.key
                bucket_count = bucket.doc_count
                bucket_dict = {'global_count': bucket_count,
                               'count': 0, 'display': bucket.key}
                if lookup:
                    if bucket_key in lookup:
                        bucket_dict.update(lookup[bucket_key])
                facet_results[k]['facets'][bucket_key] = bucket_dict

    # filter by resourcetype
    if resourcetype == 'documents':
        search = search.query("match", type="document")
    elif resourcetype == 'layers':
        search = search.query("match", type="layer")
    elif resourcetype == 'maps':
        search = search.query("match", type="map")

    # Build main query to search in fields[]
    # Filter by Query Params
    if query:
        if query.startswith('"') or query.startswith('\''):
            # Match exact phrase
            phrase = query.replace('"', '')
            search = search.query(
                "multi_match", type='phrase_prefix',
                query=phrase, fields=fields)
        else:
            words = [
                w for w in re.split(
                    '\W',
                    query,
                    flags=re.UNICODE) if w]
            for i, search_word in enumerate(words):
                if i == 0:
                    word_query = Q(
                        "multi_match", type='phrase_prefix',
                        query=search_word, fields=fields)
                elif search_word.upper() in ["AND", "OR"]:
                    pass
                elif words[i - 1].upper() == "OR":
                    word_query = word_query | Q(
                        "multi_match", type='phrase_prefix',
                        query=search_word, fields=fields)
                else:  # previous word AND this word
                    word_query = word_query & Q(
                        "multi_match", type='phrase_prefix',
                        query=search_word, fields=fields)
            # logger.debug('******* WORD_QUERY %s', word_query.to_dict())
            search = search.query(word_query)

    # Add the facet queries to the main search
    for fq in facet_filters:
        search = search.query(fq)

    # Add in has_time filter if set
    if has_time and has_time == 'true':
        search = search.query(Q({'match': {'has_time': True}}))

    # Add in Bounding Box filter
    if bbox:
        left, bottom, right, top = bbox.split(',')
        leftq = Q({'range': {'bbox_left': {'gte': float(left)}}})
        bottomq = Q({'range': {'bbox_bottom': {'gte': float(bottom)}}})
        rightq = Q({'range': {'bbox_right': {'lte': float(right)}}})
        topq = Q({'range': {'bbox_top': {'lte': float(top)}}})
        q = leftq & bottomq & rightq & topq
        search = search.query(q)

    # Add in Range Queries
    # Publication date range (start,end)
    date_range = parameters.get("date__range", None)
    date_end = parameters.get("date__lte", None)
    date_start = parameters.get("date__gte", None)
    if date_range is not None:
        dr = date_range.split(',')
        date_start = dr[0]
        date_end = dr[1]

    # Time Extent range (start, end)
    extent_range = parameters.get("extent__range", None)
    extent_end = parameters.get("extent__lte", None)
    extent_start = parameters.get("extent__gte", None)
    if extent_range is not None:
        er = extent_range.split(',')
        extent_start = er[0]
        extent_end = er[1]

    # Add range filters to the search
    if date_start:
        q = Q({'range': {'date': {'gte': date_start}}})
        search = search.query(q)

    if date_end:
        q = Q({'range': {'date': {'lte': date_end}}})
        search = search.query(q)

    if extent_start:
        q = Q(
            {'range': {'temporal_extent_end': {'gte': extent_start}}})
        search = search.query(q)

    if extent_end:
        q = Q(
            {'range': {'temporal_extent_start': {'lte': extent_end}}})
        search = search.query(q)

    # Apply sort
    if sort.lower() == "-date":
        search = search.sort({"date":
                              {"order": "desc",
                               "missing": "_last",
                               "unmapped_type": "date"
                               }})
    elif sort.lower() == "date":
        search = search.sort({"date":
                              {"order": "asc",
                               "missing": "_last",
                               "unmapped_type": "date"
                               }})
    elif sort.lower() == "title":
        search = search.sort('title')
    elif sort.lower() == "-title":
        search = search.sort('-title')
    elif sort.lower() == "-popular_count":
        search = search.sort('-popular_count')
    else:
        search = search.sort({"date":
                              {"order": "desc",
                               "missing": "_last",
                               "unmapped_type": "date"
                               }})

    # Run the search using the offset and limit
    search = search[offset:offset + limit]
    results = search.execute()

    logger.debug('search: %s, results: %s', search, results)

    # get facets based on search criteria, add to overall facets
    aggregations = results.aggregations
    for k in aggregations.to_dict():
        buckets = aggregations[k]['buckets']
        if len(buckets) > 0:
            for bucket in buckets:
                bucket_key = bucket.key
                bucket_count = bucket.doc_count
                try:
                    if bucket_count > 0:
                        (facet_results[k]['facets'][bucket_key]
                         ['count']) = bucket_count
                except Exception as e:
                    facet_results['errors'] = "%s %s %s" % (k, bucket_key, e)

    # combine buckets for type and subtype and get rid of subtype bucket
    if 'subtype' in facet_results:
        facet_results['type']['facets'].update(
            facet_results['subtype']['facets'])
        del facet_results['subtype']

    # Remove Empty Facets
    for item in facet_results.keys():
        try:
            facets = facet_results[item]['facets']
            if sum(facets[prop]['count'] for prop in facets) == 0:
                del facet_results[item]
        except Exception as e:
            logger.warn(e)

    # Get results
    objects = get_unified_search_result_objects(results.hits.hits)

    object_list = {
        "meta": {
            "limit": limit,
            "next": None,
            "offset": offset,
            "previous": None,
            "total_count": results.hits.total,
            "facets": facet_results,
        },
        "objects": objects,
    }

    return JsonResponse(object_list)