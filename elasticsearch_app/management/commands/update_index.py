# encoding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from django.core.management.base import BaseCommand
from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_app.search import LayerIndex, \
    MapIndex, DocumentIndex, ProfileIndex, GroupIndex, StoryIndex
from geonode.layers.models import Layer
from geonode.maps.models import Map
from geonode.documents.models import Document
from geonode.people.models import Profile
from geonode.groups.models import GroupProfile
from exchange.storyscapes.models.base import Story


class Command(BaseCommand):
    help = "Freshens the index for the given app(s)."

    def handle(self, **options):
        '''
        Repopulates the indices in elastic.
        '''
        es = Elasticsearch(settings.ES_URL)
        LayerIndex.init()
        MapIndex.init()
        DocumentIndex.init()
        ProfileIndex.init()
        GroupIndex.init()
        StoryIndex.init()

        body = {
            'analysis': {
                'analyzer': 'snowball'
            }
        }
        es.indices.put_settings(body, index='', ignore=400)

        bulk(client=es, actions=(index.indexing() for index in Layer.objects.all().iterator()))
        bulk(client=es, actions=(index.indexing() for index in Map.objects.all().iterator()))
        bulk(client=es, actions=(index.indexing() for index in Document.objects.all().iterator()))
        bulk(client=es, actions=(index.indexing() for index in Profile.objects.all().iterator()))
        bulk(client=es, actions=(index.indexing() for index in GroupProfile.objects.all().iterator()))
        bulk(client=es, actions=(index.indexing() for index in Story.objects.all().iterator()))
