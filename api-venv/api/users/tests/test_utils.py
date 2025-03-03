from users.utils import web3_login_message_generator

def test_web3_login_message_generator():
    """Test the web3 login message generator function."""

    nonce = "123456"
    wallet_address = "SOLANA_WALLET_ADDRESS"

    expected_message = f"""Welcome to EasyBeatz!

Click to sign in and accept the EasyBeatz Terms of Service (https://easybeatz.com/tos) and Privacy Policy (https://easybeatz.com/privacy).

This request will not trigger a blockchain transaction or cost any gas fees.

Wallet address: {wallet_address}

Nonce: {nonce}"""

    # Call function
    result = web3_login_message_generator(nonce, wallet_address)

    # Assert the generated message matches the expected message
    assert result == expected_message
