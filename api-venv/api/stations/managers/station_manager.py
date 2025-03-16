from django.db import models
from django.db.models import Prefetch, Q
from django.apps import apps

class StationManager(models.Manager):
    def with_albums_and_relations(self, user_pubkey):
        Album = apps.get_model("albums", "Album")

        # Ensure `user_pubkey` is iterable
        query_filter = Q(user__pubkey=user_pubkey) if isinstance(user_pubkey, str) else Q(user__pubkey__in=user_pubkey)

        queryset = self.select_related("user")

        # Check if any station has a related picture
        if self.filter(query_filter, picture__isnull=False).exists():
            queryset = queryset.select_related("picture").only(
                "description", "email", "handle", "name", "picture__picture"
            )
        else:
            queryset = queryset.only(
                "description", "email", "handle", "name"
            )

        queryset = queryset.prefetch_related(
            Prefetch(
                'albums',
                queryset=Album.objects
                .select_related("cover")
                .prefetch_related('tracks')
                .only('aid', 'bio', 'title', 'cover__picture')
            )
        ).filter(query_filter)

        # Return a single object if user_pubkey was a string, otherwise return the queryset
        return queryset.first() if isinstance(user_pubkey, str) else queryset
