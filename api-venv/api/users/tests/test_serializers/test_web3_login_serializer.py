import pytest
from users.serializers import Web3LoginSerializer

@pytest.fixture
def valid_data():
    return {
        "pubkey": "D3c6JWSDHXsUCHf8uuQ9raYmDnbnCHTvb5FHHvNrdjPF",  # 44-char Solana pubkey
        "signedMessage": {"type": "Buffer", "data": [100, 200, 150, 50, 255, 30]},  # Mock binary data
        "originalMessage": "Mocked Original Message"
    }

def test_web3_login_serializer_valid_data(valid_data):
    """Test that the serializer correctly validates and processes valid data."""
    serializer = Web3LoginSerializer(data=valid_data)
    assert serializer.is_valid(), serializer.errors  # Ensure data is valid
    assert serializer.validated_data["pubkey"] == valid_data["pubkey"]
    assert serializer.validated_data["signedMessage"] == [100, 200, 150, 50, 255, 30]  # Processed binary data
    assert serializer.validated_data["originalMessage"] == valid_data["originalMessage"]

def test_web3_login_serializer_invalid_pubkey():
    """Test that an invalid public key length fails validation."""
    invalid_data = {
        "pubkey": "short_key",
        "signedMessage": {"type": "Buffer", "data": [100, 200]},
        "originalMessage": "Mocked Original Message"
    }
    serializer = Web3LoginSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert "pubkey" in serializer.errors
    assert serializer.errors["pubkey"][0] == "Invalid public key length."

def test_web3_login_serializer_missing_fields():
    """Test that missing required fields fail validation."""
    invalid_data = {}
    serializer = Web3LoginSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert "signedMessage" in serializer.errors
    assert "pubkey" in serializer.errors
    assert "originalMessage" in serializer.errors

