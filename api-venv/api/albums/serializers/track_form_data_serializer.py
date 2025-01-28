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

    def validate_mp3(self, value):
        if value is None:  # If the value is null, skip validation
            return value

        if not value.name.lower().endswith('.mp3'):
            raise serializers.ValidationError("The file must have a .mp3 extension.")

        # Check if the file is a valid MP3 file
        try:
            from mutagen.mp3 import MP3
            MP3(value)
        except Exception:
            raise serializers.ValidationError("The file is not a valid MP3 file.")

        return value

    def validate_wav(self, value):
       pass 

