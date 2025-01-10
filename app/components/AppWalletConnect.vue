<template>
  <button @click="connectWallet()" class="btn btn-neutral text-xl">
    <Icon class="text-2xl" icon="solar:wallet-2-bold" />
    Login
    <Icon icon="token-branded:phantom" class="text-2xl" />
  </button>
</template>

<script setup lang="ts">

const walletAddress = ref("");
const { login, requestLoginNonce } = useAuth();

const connectWallet = async () => {

  if (window.phantom?.solana) {
    try {
      // Request wallet connection
      const response = await window.phantom.solana.connect();
      walletAddress.value = response.publicKey.toString();

      //Request login nonce
      const nonce = await requestLoginNonce(walletAddress.value);

      // generate message to sign
      const message = generateMessage(nonce);

      // Request the user to sign the message
      const signedMessage = await window.phantom.solana.signMessage(new TextEncoder().encode(message));

      // Now that the wallet is connected, authenticate user
      await authenticateUser(signedMessage.signature, message);

    } catch (error) {
      console.error("Failed to connect wallet", error);
    }
  } else {
    alert("Phantom Wallet not found. Please install phantom wallet in your browser.");
  }
}

const generateMessage = (nonce: string): string => {
  const message = `Welcome to EasyBeatz! 

Click to sign in and accept the EasyBeatz Terms of Service (https://easybeatz.com/tos) and Privacy Policy (https://easybeatz.com/privacy). 

This request will not trigger a blockchain transaction or cost any gas fees. 

Wallet address: ${walletAddress.value}

Nonce: ${nonce}`;
  return message;
}

const authenticateUser = async (signature: any, message: string) => {
  login(signature, message, walletAddress.value);
}

</script>
