from django.apps import AppConfig


class ElasticsearchAppConfig(AppConfig):
    name = 'elasticsearch_app'

    def ready(self):
        import elasticsearch_app.signals
