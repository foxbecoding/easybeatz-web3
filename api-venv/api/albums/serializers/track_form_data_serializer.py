from rest_framework import serializers

class TrackFormSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    genres = serializers.ListField()
    mood = serializers.CharField()
    mp3 = serializers.FileField()
    wav = serializers.FileField(allow_empty_file=True, allow_null=True)
    bpm = serializers.CharField()
    has_exclusive = serializers.BooleanField()
    price = serializers.CharField()
    exclusive_price = serializers.CharField(allow_blank=True)
    collaborators = serializers.ListField(allow_empty=True)
    stems = serializers.ListField(allow_empty=True)

