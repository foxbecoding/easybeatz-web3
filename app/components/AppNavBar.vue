<template>
  <div class="navbar bg-base-100 lg:bg-base-200 fixed left-0 z-50 mx-auto w-full max-w-[2560px] px-4 sm:px-8">
    <div class="navbar-start gap-4">
      <button tabindex="0" role="button" class="btn btn-neutral btn-square mask mask-squircle hidden lg:flex">
        <Icon icon="solar:hamburger-menu-linear" class="text-2xl" />
      </button>
      <NuxtLink :to="{ name: 'index' }">
        <NuxtImg src="/logo.png" width="120px" />
      </NuxtLink>
    </div>

    <div class="navbar-center max-w-[600px] w-full hidden lg:block">
      <label class="hidden input bg-neutral input-ghost rounded-[1rem] md:flex items-center gap-2 w-full">
        <input type="text" class="grow" placeholder="Search" />
        <Icon icon="solar:magnifer-linear" width="24" height="24" />
      </label>
    </div>

    <div class="navbar-end">
      <AppWalletConnect v-if="!authStore.isAuthenticated" class="mr-4" />
      <AppAccountMenu v-else class="mr-4" />
      <div class="flex relative">
        <NuxtLink :to="{ name: 'cart' }" class="btn btn-neutral mask mask-squircle btn-square btn-sm lg:btn-md">
          <Icon icon="solar:bag-music-2-bold" class="text-lg lg:text-2xl" />
        </NuxtLink>
        <div v-if="isCartEmpty" class="badge badge-primary mask mask-circle absolute -right-[9px]">{{
          cartStore.cart_count }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "@/store/auth"
import { useCartStore } from "@/store/cart"

const authStore = useAuthStore();
const cartStore = useCartStore();
const isCartEmpty = computed(() => cartStore.cart_count)

</script>
