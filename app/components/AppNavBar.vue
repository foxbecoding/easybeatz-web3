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
        <AppWalletConnect v-if="!authStore.isAuthenticated" class="mr-4" />
        <AppAccountMenu v-else class="mr-4" />
        <NuxtLink :to="{ name: 'cart' }" class="btn btn-neutral btn-square">
          <Icon icon="solar:bag-music-2-bold" class="text-2xl" />
        </NuxtLink>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "@/store/auth"

const authStore = useAuthStore();

interface MenuLink {
  to: string;
  icon: string;
  label: string;
  show: boolean;
}

const menuLinks = computed<MenuLink[]>(() => [
  { to: "", icon: "solar:station-bold", label: "Your Station", show: true },
  { to: "", icon: "solar:heart-angle-bold", label: "Favorites", show: true },
  { to: "", icon: "solar:chat-round-money-bold", label: "Purchases", show: true },
  { to: "", icon: "solar:headphones-round-sound-bold", label: "Studio", show: true },
  { to: "", icon: "solar:logout-2-bold", label: "Logout", show: authStore.isAuthenticated },
]);

</script>
