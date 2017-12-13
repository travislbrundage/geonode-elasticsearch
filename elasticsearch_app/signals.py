from geonode.layers.models import Layer
from geonode.maps.models import Map
from geonode.documents.models import Document
from geonode.people.models import Profile
from geonode.groups.models import GroupProfile
from exchange.storyscapes.models.base import Story
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Layer)
def layer_index_post(sender, instance, **kwargs):
    instance.indexing()


@receiver(post_save, sender=Map)
def map_index_post(sender, instance, **kwargs):
    instance.indexing()


@receiver(post_save, sender=Document)
def document_index_post(sender, instance, **kwargs):
    instance.indexing()


@receiver(post_save, sender=Profile)
def profile_index_post(sender, instance, **kwargs):
    instance.indexing()


@receiver(post_save, sender=GroupProfile)
def group_index_post(sender, instance, **kwargs):
    instance.indexing()


@receiver(post_save, sender=Story)
def story_index_post(sender, instance, **kwargs):
    instance.indexing()



# To extend this app in your project, add a post_save
# signal for every model you wish to index.
# Be sure to update utils.py with any custom
# indexing for this model in the indexing() function.
# Otherwise, only the id will be indexed.
# <Model> = your model you wish to index
#
# @receiver(post_save, sender=<Model>)
# def <Model>_index_post(sender, instance, **kwargs):
#     instance.indexing()
