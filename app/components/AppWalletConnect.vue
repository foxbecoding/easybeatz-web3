<template>
  <button @click="!isConnecting ? connectWallet() : false" class="btn btn-neutral rounded-[1rem] text-xl"
    :disabled="isConnecting">
    <Icon class="text-2xl" icon="solar:wallet-2-bold" />
    Login
    <Icon icon="token-branded:phantom" class="text-2xl" />
  </button>
</template>
