# encoding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from django.core.management.base import BaseCommand
from django.conf import settings
from elasticsearch import Elasticsearch


class Command(BaseCommand):
    help = "Clears out haystack's modelresult index from elasticsearch."

    def handle(self, **options):
        '''
        Clears out haystack's modelresult index from elasticsearch
        '''
        self.stdout.write("Removing modelresult index from elasticsearch")
        es = Elasticsearch(settings.ES_URL)

        try:
            es.indices.delete(index='modelresult')
        except TransportError:
            self.stdout.write("ERROR: Could not find index to delete: modelresult")
