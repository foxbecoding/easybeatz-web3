from django.db import models
from albums.models.track import Track
from users.models import User

class TrackFavorite(models.Model):
    track = models.ForeignKey(
        Track,
        on_delete=models.CASCADE,
        related_name='track_favorite_set'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_track_favorites'
    )
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)

    objects = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'track'],
                name='unique_user_track_favorite'
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.track}"
