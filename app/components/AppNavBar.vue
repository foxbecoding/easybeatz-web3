<template>
  <div class="navbar bg-base-100 relative">
    <div class="mx-auto w-full max-w-[2560px] px-4 sm:px-8 2xl:px-16 flex items-center justify-between">

      <div class="flex">
        <a class="btn btn-neutral text-xl">Button</a>
      </div>

      <label class="input bg-neutral input-ghost flex items-center gap-2 max-w-[480px] w-full">
        <input type="text" class="grow" placeholder="Search" />
        <Icon icon="solar:magnifer-linear" width="24" height="24" />
      </label>

      <div class="flex-none">
        <AppWalletConnect v-if="!userStore.isAuthenticated" class="mr-4" />
        <button v-else class="btn btn-neutral btn-square mr-4">
          <Icon icon="solar:user-bold" class="text-2xl" />
        </button>
        <button class="btn btn-neutral btn-square">
          <Icon v-if="false" icon="solar:cart-large-bold" class="text-2xl" />
          <Icon icon="solar:bag-music-2-bold" class="text-2xl" />
        </button>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from "@/store/user"

const userStore = useUserStore();

</script>
