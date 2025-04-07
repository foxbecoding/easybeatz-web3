from django.db import models
from django.db.models import Prefetch, Sum, Q
from django.apps import apps
from genres.models import Genre

class TrackManager(models.Manager):
    def track_page(self, tid):

        queryset = self.select_related(
            "display",
            "exclusive_price",
            "mood",
            "price",
            "album",
            "album__cover",
            "album__station",
            "album__station__user"
        ).only(
            "bpm", "created", "duration", "order_no", "tid", "title",
            "display__audio",
            "exclusive_price__value",
            "mood__name", "mood__slug",
            "price__value",
            "album__aid", "album__title", 
            "album__cover__picture",
            "album__station__handle", "album__station__name",
            "album__station__picture__picture", "album__station__user__pubkey"
        ).prefetch_related(
            Prefetch(
                "genres",  
                queryset=Genre.objects.only("name", "slug")
            )
        ).filter(tid=tid).first()

        return queryset
