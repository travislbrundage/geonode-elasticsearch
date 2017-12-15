from django.db.models.signals import post_save
from django.dispatch import receiver
from elasticsearch_app.utils import index_object

geonode_imported = True
try:
    from geonode.layers.models import Layer
    from geonode.maps.models import Map
    from geonode.documents.models import Document
    from geonode.people.models import Profile
    from geonode.groups.models import GroupProfile
    from elasticsearch_app.search import LayerIndex, \
        MapIndex, DocumentIndex, ProfileIndex, GroupIndex
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

# To extend this app in your project, add
# import statements for the models you need from your
# project here



if geonode_imported:
    @receiver(post_save, sender=Layer)
    def layer_index_post(sender, instance, **kwargs):
        index_object(instance, LayerIndex)


    @receiver(post_save, sender=Map)
    def map_index_post(sender, instance, **kwargs):
        index_object(instance, MapIndex)


    @receiver(post_save, sender=Document)
    def document_index_post(sender, instance, **kwargs):
        index_object(instance, DocumentIndex)


    @receiver(post_save, sender=Profile)
    def profile_index_post(sender, instance, **kwargs):
        index_object(instance, ProfileIndex)


    @receiver(post_save, sender=GroupProfile)
    def group_index_post(sender, instance, **kwargs):
        index_object(instance, GroupIndex)

if exchange_imported:
    @receiver(post_save, sender=Story)
    def story_index_post(sender, instance, **kwargs):
        index_object(instance, StoryIndex)


# To extend this app in your project, add a post_save
# signal for every model you wish to index.
# Be sure to update your model with any custom
# indexing for this model in the indexing() function.
# Otherwise, only the id will be indexed.
# <Model> = your model you wish to index
#
# @receiver(post_save, sender=<Model>)
# def <Model>_index_post(sender, instance, **kwargs):
#     index_object(instance)
