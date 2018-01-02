# encoding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from django.core.management.base import BaseCommand
from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_app.utils import index_object

geonode_imported = True
try:
    from geonode.layers.models import Layer
    from geonode.maps.models import Map
    from geonode.documents.models import Document
    from geonode.people.models import Profile
    from geonode.groups.models import GroupProfile
    from elasticsearch_app.search import (
        LayerIndex,
        MapIndex,
        DocumentIndex,
        ProfileIndex,
        GroupIndex
    )
    geonode_imported = True
except ImportError:
    geonode_imported = False

exchange_imported = True
try:
    from exchange.storyscapes.models.base import Story
    from elasticsearch_app.search import StoryIndex
    exchange_imported = True
except ImportError:
    exchange_imported = False


class Command(BaseCommand):
    help = "Freshens the index for the given app(s)."

    def handle(self, **options):
        '''
        Repopulates the indices in elastic.
        '''
        es = Elasticsearch(settings.ES_URL)

        # Any indices added in search.py should be initialized here
        if geonode_imported:
            LayerIndex.init()
            MapIndex.init()
            DocumentIndex.init()
            ProfileIndex.init()
            GroupIndex.init()

        if exchange_imported:
            StoryIndex.init()

        body = {
            'analysis': {
                'analyzer': 'snowball'
            }
        }
        es.indices.put_settings(body, index='', ignore=400)

        # Any indices added in search.py should be indexed here
        if geonode_imported:
            bulk(client=es,
                 actions=(index_object(layer, LayerIndex)
                          for layer in Layer.objects.all().iterator()))
            bulk(client=es,
                 actions=(index_object(map_obj, MapIndex)
                          for map_obj in Map.objects.all().iterator()))
            bulk(client=es,
                 actions=(index_object(document, DocumentIndex)
                          for document in Document.objects.all().iterator()))
            bulk(client=es,
                 actions=(index_object(profile, ProfileIndex)
                          for profile in Profile.objects.all().iterator()))
            bulk(client=es,
                 actions=(index_object(group, GroupIndex)
                          for group in GroupProfile.objects.all().iterator()))

        if exchange_imported:
            bulk(client=es,
                 actions=(index_object(story, StoryIndex)
                          for story in Story.objects.all().iterator()))
