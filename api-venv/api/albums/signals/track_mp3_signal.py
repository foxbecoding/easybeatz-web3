from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import TrackMp3

@receiver(post_save, sender=TrackMp3)
def after_save(sender, instance, created, **kwargs):
    if created:
        print(f"New instance created: {instance}")
