from django.apps import AppConfig


class AlbumsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'albums'

    def ready(self):
        from .signals import track_mp3_signal
