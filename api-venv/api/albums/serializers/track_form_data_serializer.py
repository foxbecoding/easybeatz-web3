from rest_framework import serializers
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from genres.models import Genre
from moods.models import Mood

class TrackFormSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    genres = serializers.ListField()
    mood = serializers.CharField()
    mp3 = serializers.FileField()
    wav = serializers.FileField(allow_empty_file=True, allow_null=True)
    bpm = serializers.CharField()
    price = serializers.CharField()
    exclusive_price = serializers.CharField(allow_blank=True, allow_null=True)
    collaborators = serializers.ListField(allow_empty=True)
    stems = serializers.ListField(allow_empty=True)

    def validate_price(self, value):
        index = self.context['index']
        if not value.isdigit():
            raise serializers.ValidationError({ f"track_{index}": "Price can only contain numbers. eg: 5, 50, 500" })

        if value.startswith("0") and len(value) > 1:
            raise serializers.ValidationError({ f"track_{index}": "Price cannot contain leading zeros. eg: 5, 50, 500" })

        if value == "0":
            raise serializers.ValidationError({ f"track_{index}": "Price cannot be 0." })

        return value

    def validate_exclusive_price(self, value):
        # index = self.context['index']
        track_data, index = [self.context['track_data'], self.context['index']]
        
        if value and not track_data['stems']:
            raise serializers.ValidationError({f"track_{index}": "Tracks with an exclusive price must have stems"})
        
        if not value:
            return value

        if not value.isdigit():
            raise serializers.ValidationError({ f"track_{index}": "Exclusive price can only contain numbers. eg: 5, 50, 500" })

        if value.startswith("0") and len(value) > 1:
            raise serializers.ValidationError({ f"track_{index}": "Exclusive price cannot contain leading zeros. eg: 5, 50, 500" })

        if value == "0":
            raise serializers.ValidationError({ f"track_{index}": "Exclusive price cannot be 0." })

        return value

    def validate_mp3(self, value):
        index = self.context['index']

        if not value.name.lower().endswith('.mp3'):
            raise serializers.ValidationError({ f"track_{index}": "The file must have a .mp3 extension." })

        # Check if the file is a valid MP3 file
        try:
            MP3(value)
        except Exception:
            raise serializers.ValidationError({ f"track_{index}": "The file is not a valid MP3 file." })

        return value

    def validate_wav(self, value):
        index = self.context['index']

        if value is None:  # If the value is null, skip validation
            return value

        if not value.name.lower().endswith('.wav'):
            raise serializers.ValidationError({ f"track_{index}": "The file must have a .wav extension." })

        # Check if the file is a valid WAV file
        try:
            WAVE(value)
        except Exception:
            raise serializers.ValidationError({ f"track_{index}": "The file is not a valid WAV file." })

        return value

    def validate_stems(self, value):
        index = self.context['index']
        if not value:  # Allow empty list
            return value

        # Ensure each item in the list is a dictionary with `name` and `file`
        for stem_index, item in enumerate(value):
            if not isinstance(item, dict):
                raise serializers.ValidationError({ f"track_{index}": { f"stem_{stem_index}": "Item in the stems list must be a dictionary." } })

            # Check that `name` is provided and is not empty
            name = item.get('name')
            if not name:
                raise serializers.ValidationError({ f"track_{index}": { f"stem_{stem_index}": "Item in the stems list must have a non-empty `name`." } })

            # Check that `file` is a WAV file
            file = item.get('file')
            if not file:
                raise serializers.ValidationError({ f"track_{index}": { f"stem_{stem_index}": "Item in the stems list must have a `file`." } })
            if not file.name.lower().endswith('.wav'):
                raise serializers.ValidationError({ f"track_{index}": { f"stem_{stem_index}": "File in item must have a .wav extension." } })

            # Validate that the file is a valid WAV file by checking its content
            try:
                WAVE(file)
            except Exception:
                raise serializers.ValidationError({ f"track_{index}": { f"stem_{stem_index}": "File in item is not a valid WAV file." } })

        return value

    def validate_genres(self, value):
        index = self.context['index']
        for genre_index, pk in enumerate(value):
            if not Genre.objects.filter(pk=str(pk)).exists():
                raise serializers.ValidationError({ f"track_{index}": { f"genre_{genre_index}": "Genre does not exists" } })
        return value

    def validate_mood(self, value):
        index = self.context['index']
        if not Mood.objects.filter(pk=str(value)).exists():
            raise serializers.ValidationError({ f"track_{index}": "Mood does not exists."})
        return value

class AddTrackFormSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    genres = serializers.ListField()
    mood = serializers.CharField()
    mp3 = serializers.FileField()
    wav = serializers.FileField(allow_empty_file=True, allow_null=True)
    bpm = serializers.CharField()
    price = serializers.CharField()
    exclusive_price = serializers.CharField(allow_blank=True, allow_null=True)
    collaborators = serializers.ListField(allow_empty=True)
    stems = serializers.ListField(allow_empty=True)

    def validate_price(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Price can only contain numbers. eg: 5, 50, 500" )

        if value.startswith("0") and len(value) > 1:
            raise serializers.ValidationError("Price cannot contain leading zeros. eg: 5, 50, 500")

        if value == "0":
            raise serializers.ValidationError("Price cannot be 0.")

        return value

    def validate_exclusive_price(self, value):
        track_data = self.context['track_data']
        
        if value and not track_data['stems']:
            raise serializers.ValidationError("Tracks with an exclusive price must have stems")
        
        if not value:
            return value

        if not value.isdigit():
            raise serializers.ValidationError("Exclusive price can only contain numbers. eg: 5, 50, 500")

        if value.startswith("0") and len(value) > 1:
            raise serializers.ValidationError("Exclusive price cannot contain leading zeros. eg: 5, 50, 500")

        if value == "0":
            raise serializers.ValidationError("Exclusive price cannot be 0.")

        return value

    def validate_mp3(self, value):
        if not value.name.lower().endswith('.mp3'):
            raise serializers.ValidationError("The file must have a .mp3 extension.")

        # Check if the file is a valid MP3 file
        try:
            MP3(value)
        except Exception:
            raise serializers.ValidationError("The file is not a valid MP3 file.")

        return value

    def validate_wav(self, value):
        if value is None:  # If the value is null, skip validation
            return value

        if not value.name.lower().endswith('.wav'):
            raise serializers.ValidationError("The file must have a .wav extension.")

        # Check if the file is a valid WAV file
        try:
            WAVE(value)
        except Exception:
            raise serializers.ValidationError("The file is not a valid WAV file.")

        return value

    def validate_stems(self, value):
        if not value:  # Allow empty list
            return value

        # Ensure each item in the list is a dictionary with `name` and `file`
        for stem_index, item in enumerate(value):
            if not isinstance(item, dict):
                raise serializers.ValidationError({ f"stem_{stem_index}": "Item in the stems list must be a dictionary." })

            # Check that `name` is provided and is not empty
            name = item.get('name')
            if not name:
                raise serializers.ValidationError({ f"stem_{stem_index}": "Item in the stems list must have a non-empty `name`." })

            # Check that `file` is a WAV file
            file = item.get('file')
            if not file:
                raise serializers.ValidationError({ f"stem_{stem_index}": "Item in the stems list must have a `file`." })
            if not file.name.lower().endswith('.wav'):
                raise serializers.ValidationError({ f"stem_{stem_index}": "File in item must have a .wav extension." })

            # Validate that the file is a valid WAV file by checking its content
            try:
                WAVE(file)
            except Exception:
                raise serializers.ValidationError({ f"stem_{stem_index}": "File in item is not a valid WAV file." })

        return value

    def validate_genres(self, value):
        for genre_index, pk in enumerate(value):
            if not Genre.objects.filter(pk=str(pk)).exists():
                raise serializers.ValidationError({ f"genre_{genre_index}": "Genre does not exists" })
        return value

    def validate_mood(self, value):
        if not Mood.objects.filter(pk=str(value)).exists():
            raise serializers.ValidationError("Mood does not exists.")
        return value
