import pytest
from users.serializers import Web3LoginSerializer

@pytest.fixture
def valid_data():
    return {
        "pubkey": "D3c6JWSDHXsUCHf8uuQ9raYmDnbnCHTvb5FHHvNrdjPF",  # 44-char Solana pubkey
        "signedMessage": {"type": "Buffer", "data": [100, 200, 150, 50, 255, 30]},  # Mock binary data
        "originalMessage": "Mocked Original Message"
    }

