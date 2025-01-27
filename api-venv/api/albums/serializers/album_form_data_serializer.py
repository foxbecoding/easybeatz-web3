from rest_framework import serializers

class AlbumFormSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    bio = serializers.CharField(required=False)
    cover = serializers.ImageField()
