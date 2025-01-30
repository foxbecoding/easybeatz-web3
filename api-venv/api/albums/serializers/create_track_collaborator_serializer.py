from rest_framework import serializers
from ..models import TrackCollaborator

class CreateTrackCollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackCollaborator
        fields = [
            'track',
            'station',
            'pubkey',
        ]
