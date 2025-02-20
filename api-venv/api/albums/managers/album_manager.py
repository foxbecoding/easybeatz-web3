from django.db import models
from django.db.models import Prefetch, Sum, Q
from django.apps import apps
from genres.models import Genre

class AlbumManager(models.Manager):
    def with_tracks_and_relations(self, aid):
        Track = apps.get_model('albums', 'Track')

        # Ensure `aid` is iterable
        aid_filter = Q(aid=aid) if isinstance(aid, str) else Q(aid__in=aid)

        queryset = self.select_related(
            "cover",
            "station",
            "station__user"
        ).only(
            "aid", "bio", "title",
            "cover__picture",
            "station__handle", "station__name", "station__picture__picture", "station__user__pubkey"
        ).prefetch_related(
            Prefetch(
                "tracks",
                queryset=Track.objects
                .prefetch_related(
                    Prefetch(
                        "genres",  
                        queryset=Genre.objects.only("name", "slug")
                    )
                )
                .select_related("display", "exclusive_price", "mood", "price")
                .only(
                    "bpm", "duration", "order_no", "tid", "title",
                    "display__audio",
                    "exclusive_price__value",
                    "mood__name",
                    "mood__slug",
                    "price__value",
                )
                .order_by("order_no")
            )
        ).annotate(
            total_duration=Sum("tracks__duration")
        ).filter(aid_filter)

        # Return a single object if aid was a string, otherwise return the queryset
        return queryset.first() if isinstance(aid, str) else queryset
