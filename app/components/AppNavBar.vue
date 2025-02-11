<template>

      <div class="flex">
        <a class="btn btn-neutral rounded-[1rem] text-xl">Create</a>
      </div>

      <label class="hidden input bg-neutral input-ghost rounded-[1rem] md:flex items-center gap-2 max-w-[480px] w-full">
        <input type="text" class="grow" placeholder="Search" />
        <Icon icon="solar:magnifer-linear" width="24" height="24" />
      </label>

      <div class="flex-none">
        <AppWalletConnect v-if="!authStore.isAuthenticated" class="mr-4" />
        <AppAccountMenu v-else class="mr-4" />
        <NuxtLink :to="{ name: 'cart' }" class="btn btn-neutral mask mask-squircle btn-square">
          <Icon icon="solar:bag-music-2-bold" class="text-2xl" />
        </NuxtLink>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "@/store/auth"

const authStore = useAuthStore();

</script>
