def web3_login_message_generator(nonce: str, wallet_address: str) -> str:
    message = f"""Welcome to EasyBeatz!

Click to sign in and accept the EasyBeatz Terms of Service (https://easybeatz.com/tos) and Privacy Policy (https://easybeatz.com/privacy).

This request will not trigger a blockchain transaction or cost any gas fees.

Wallet address: {wallet_address}

Nonce: {nonce}"""
    return message
