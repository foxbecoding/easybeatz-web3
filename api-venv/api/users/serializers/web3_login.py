from rest_framework import serializers

class BinaryField(serializers.Field):
    """Custom field to handle binary arrays (buffers)."""

    def to_representation(self, value):
        # Converts binary data to a base64 string for JSON-safe representation
        return value.hex()

    def to_internal_value(self, data):
        # Expects the structure {'type': 'Buffer', 'data': [array of byte values]}
        if isinstance(data, dict) and 'data' in data:
            byte_array = data.get('data')
            if isinstance(byte_array, list):
                return byte_array
                # return bytes(byte_array)
            raise serializers.ValidationError("Invalid data array format.")
        else:
            raise serializers.ValidationError("Invalid structure: Expected a dict with a 'data' key.")

class Web3LoginSerializer(serializers.Serializer):
    signedMessage = BinaryField()  # Binary data as a buffer
    pubkey = serializers.CharField(max_length=128)  # Public key as a string
    originalMessage = serializers.CharField(max_length=512)  # Original message as a string

    def validate_pubkey(self, value):
        # Add custom validation for the pubkey if needed
        if len(value) != 44:  # Example: Check for specific length (e.g., Solana pubkey length)
            raise serializers.ValidationError("Invalid public key length.")
        return value

    def validate(self, attrs):
        # Additional validation logic (optional)
        if not attrs.get("signedMessage"):
            raise serializers.ValidationError({"signedMessage": "This field is required."})
        if not attrs.get("pubkey"):
            raise serializers.ValidationError({"pubkey": "This field is required."})
        if not attrs.get("originalMessage"):
            raise serializers.ValidationError({"originalMessage": "This field is required."})
        return attrs
