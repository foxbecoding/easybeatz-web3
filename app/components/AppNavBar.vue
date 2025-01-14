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

        <div class="dropdown dropdown-bottom dropdown-end dropdown-hover">
          <button tabindex="0" role="button" class="btn btn-neutral btn-square mr-4">
            <Icon icon="solar:user-bold" class="text-2xl" />
          </button>

          <ul tabindex="0" class="dropdown-content menu bg-neutral rounded-box z-[1] w-[300px] p-2 shadow">
            <li v-show="link.show" v-for="(link, i) in menuLinks" :key="i">
              <NuxtLink class="text-lg font-semibold">
                <Icon :icon="link.icon" class="text-2xl mr-2" />
                {{ link.label }}
              </NuxtLink>
            </li>
          </ul>
        </div>
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
