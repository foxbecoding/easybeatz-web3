<template>
  <button @click="connectWallet()" class="btn btn-neutral text-xl mr-4">
    <Icon class="text-2xl" icon="solar:wallet-2-bold" />
    Login
    <img src="/phantom-icon.svg" />
  </button>
</template>

<script setup lang="ts">
import type { ApiData } from "../composables/useApi"

const walletAddress = ref("")

const connectWallet = async () => {

  if (window.phantom?.solana) {
    try {
      // Request wallet connection
      const response = await window.phantom.solana.connect();
      walletAddress.value = response.publicKey.toString();

      //Request login nonce

      const message = generateMessage();
      // Request the user to sign the message
      const signedMessage = await window.phantom.solana.signMessage(new TextEncoder().encode(message));

      // Now that the wallet is connected, send the address to the backend
      const apiData: ApiData = {
        method: 'POST',
        path: '/api/web3-login/',
        data: {
          signedMessage: signedMessage.signature,
          originalMessage: message,
          pubkey: walletAddress.value
        }
      }

      const { data, error } = await useApi(apiData);
      console.log("error: ", error)
      console.log("data: ", data)
    } catch (error) {
      console.error("Failed to connect wallet", error);
    }
  } else {
    alert("Phantom Wallet not found. Please install phantom wallet in your browser.");
  }
}

const generateMessage = (): string => {
  const message = `Welcome to EasyBeatz! 

Click to sign in and accept the EasyBeatz Terms of Service (https://easybeatz.com/tos) and Privacy Policy (https://easybeatz.com/privacy). 

This request will not trigger a blockchain transaction or cost any gas fees. 

Wallet address: ${walletAddress.value}`;
  return message;
}

const requestLoginNonce = (): string => {

}

const authenticateUser = (signature, message) => {

}

</script>

<style scoped></style>
