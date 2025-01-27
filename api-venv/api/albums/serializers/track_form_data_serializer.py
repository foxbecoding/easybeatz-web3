from rest_framework import serializers

class TrackFormSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    # bio = serializers.CharField(allow_null=True)
    # cover = serializers.ImageField()

    # def validate_cover(self, value):
        # return value

