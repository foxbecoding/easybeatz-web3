<template>
  <div class="navbar bg-base-100 lg:bg-base-200 fixed left-0 z-50 mx-auto w-full max-w-[2560px] px-4 sm:px-8">
    <div class="navbar-start gap-4">
      <NuxtLink :to="{ name: 'index' }">
        <NuxtImg src="/logo.png" width="200px" />
      </NuxtLink>
    </div>

    <div class="navbar-center max-w-[600px] w-full hidden md:block">
      <label class="hidden input bg-neutral input-ghost rounded-[1rem] md:flex items-center gap-2 w-full">
        <input type="text" class="grow" placeholder="Search" />
        <Icon icon="solar:magnifer-linear" width="24" height="24" />
      </label>
    </div>

    <div class="navbar-end">
      <AppWalletConnect v-if="!authStore.isAuthenticated" class="mr-4" />
      <AppAccountMenu v-else class="mr-4" />
      <NuxtLink :to="{ name: 'cart' }" class="btn btn-neutral mask mask-squircle btn-square">
        <Icon icon="solar:bag-music-2-bold" class="text-2xl" />
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "@/store/auth"

const authStore = useAuthStore();

</script>
