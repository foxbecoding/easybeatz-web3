from django.contrib import admin
from .models import Album, AlbumCover, Track, TrackMp3, TrackWav, TrackStem, TrackPrice, TrackExclusivePrice

# Register your models here.
admin.site.register(Album)
admin.site.register(AlbumCover)
admin.site.register(Track)
admin.site.register(TrackMp3)
admin.site.register(TrackWav)
admin.site.register(TrackStem)
admin.site.register(TrackPrice)
admin.site.register(TrackExclusivePrice)

