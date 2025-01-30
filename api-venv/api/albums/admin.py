from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Album)
admin.site.register(AlbumCover)
admin.site.register(Track)
admin.site.register(TrackMp3)
admin.site.register(TrackWav)
admin.site.register(TrackStem)
admin.site.register(TrackPrice)
admin.site.register(TrackCollaborator)
admin.site.register(TrackExclusivePrice)

