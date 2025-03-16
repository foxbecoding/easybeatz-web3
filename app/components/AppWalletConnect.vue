<script setup lang="ts">

const walletAddress = ref("");
const { login, requestLoginNonce } = useAuth();
const isConnecting = ref(false)

const connectWallet = async () => {
  if (isConnecting.value) return;
  if (window.phantom?.solana) {
    try {
      isConnecting.value = true;
      // Request wallet connection
      const response = await window.phantom.solana.connect();
      walletAddress.value = response.publicKey.toString();

      try {
        //Request login nonce
        const { message, data } = await requestLoginNonce(walletAddress.value) as any;

        // Request the user to sign the message
        const signedMessage = await window.phantom.solana.signMessage(new TextEncoder().encode(data.message));

        // Now that the wallet is connected, authenticate user
        await authenticateUser(signedMessage.signature, data.message);
      } catch (error: any) {
        const { message, data } = error.data
        if (message) {
          useToast().setToast(message, "ERROR");
        }
      }

      isConnecting.value = false;
    } catch (error) {
      //console.error("Failed to connect wallet", error);
      isConnecting.value = false;
    }
  } else {
    alert("Phantom Wallet not found. Please install phantom wallet in your browser.");
    isConnecting.value = false;
  }
}

const authenticateUser = async (signature: any, message: string) => {
  login(signature, message, walletAddress.value);
}

</script>


<template>
  <button @click="connectWallet()"
    class="btn btn-sm lg:btn-md btn-neutral rounded-[0.6rem] lg:rounded-[1rem] lg:text-lg" :disabled="isConnecting">
    <Icon class="text-lg lg:text-xl" icon="solar:wallet-2-bold" />
    Login
    <Icon icon="token-branded:phantom" class="text-lg lg:text-xl" />
  </button>
</template>
