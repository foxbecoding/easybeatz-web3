<template>
  <button @click="connectWallet()" class="btn btn-neutral text-xl">
    <Icon class="text-2xl" icon="solar:wallet-2-bold" />
    Login
    <Icon icon="token-branded:phantom" class="text-2xl" />
  </button>
</template>

<script setup lang="ts">
import { useAuthStore } from "@/store/auth";
import { useUserStore } from "@/store/user";
import type { ApiData } from "@/composables/useApi";

const walletAddress = ref("");

const connectWallet = async () => {

  if (window.phantom?.solana) {
    try {
      // Request wallet connection
      const response = await window.phantom.solana.connect();
      walletAddress.value = response.publicKey.toString();

      //Request login nonce
      const nonce = await requestLoginNonce();

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

const requestLoginNonce = async () => {
  const apiData: ApiData = {
    method: 'POST',
    path: '/api/web3-login-nonce/',
    data: {
      pubkey: walletAddress.value
    }
  }

  const res = await useApi(apiData)

  if (res.error) {
    throw new Error(`requestLoginNonce() - Response status: ${res.error}`);
  }

  return res.nonce;
}

const authenticateUser = async (signature: any, message: string) => {
  const apiData: ApiData = {
    method: 'POST',
    path: '/api/web3-login/',
    data: {
      signedMessage: signature,
      originalMessage: message,
      pubkey: walletAddress.value
    }
  }

  const res = await useApi(apiData);

  if (res.error) {
    throw new Error(`authenticateNonce() - Response status: ${res.error}`);
  }

  const userStore = useUserStore();
  userStore.pubkey = res.pubkey

  const authStore = useAuthStore();
  authStore.setAuthData(res.access_token, true);
}

</script>
