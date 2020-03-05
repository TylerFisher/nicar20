from django.apps import AppConfig


class TweetsConfig(AppConfig):
    name = 'tweets'

    def ready(self):
        from tweets import signals
