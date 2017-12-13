# encoding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from django.core.management.base import BaseCommand
from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch import TransportError


class Command(BaseCommand):
    help = "Clears the search index of all elasticsearchapp indices."

    def handle(self, **options):
        '''
        Clears the search index of all elasticsearchapp indices
        '''
        self.stdout.write("Removing all documents indexed by elasticsearchapp")
        es = Elasticsearch(settings.ES_URL)

        # Delete all the indices this application creates
        elasticsearchapp_indicies = [
            'layer-index',
            'map-index',
            'document-index',
            'group-index',
            'profile-index',
            'story-index'
        ]
        for index in elasticsearchapp_indicies:
            try:
                es.indices.delete(index=index)
            except TransportError:
                self.stdout.write("ERROR: Could not find index to delete: %s" % index)
