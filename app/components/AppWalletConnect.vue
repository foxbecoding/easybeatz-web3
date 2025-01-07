<template>
  <button @click="connectWallet()" class="btn btn-neutral text-xl mr-4">
    <Icon class="text-2xl" icon="solar:wallet-2-bold" :ssr="true" />
    Login
  </button>
</template>

<script setup lang="ts">
import { Connection, clusterApiUrl, Keypair } from '@solana/web3.js';

const walletAddress = ref("")

const connectWallet = async () => {

  if (window.phantom?.solana) {
    try {
      // Request wallet connection
      const response = await window.phantom.solana.connect();

      walletAddress.value = response.publicKey.toString();

      // Define the message to be signed (could be anything, e.g., a random nonce)
      const message = ` Welcome to EasyBeatz!

Click to sign in and accept the EasyBeatz Terms of Service (https://easybeatz.com/tos)  and Privacy Policy (https://easybeatz.com/privacy)

This request will not trigger a blockchain transaction or cost any gas fees.

Wallet address: ${walletAddress.value}`

      // Request the user to sign the message
      const signedMessage = await window.phantom.solana.signMessage(new TextEncoder().encode(message));

      // The signed message contains the original message and the signature
      console.log("Message:", message);
      console.log("Signed Message:", signedMessage);

      console.log(walletAddress.value)

      // Now that the wallet is connected, send the address to the backend
      //await this.authenticateBackend();
    } catch (error) {
      console.error("Failed to connect wallet", error);
    }
  } else {
    alert("Phantom Wallet not found");
  }
}

</script>

<style scoped></style>
