<template>
  <div class="dropdown dropdown-bottom dropdown-end dropdown-hover">
    <button tabindex="0" role="button" class="btn btn-neutral btn-square mask mask-squircle">
      <Icon icon="solar:user-bold" class="text-2xl" />
    </button>

    <ul tabindex="0" class="dropdown-content menu bg-neutral rounded-box rounded-[2rem] z-[1] w-[300px] p-2 shadow">
      <li v-for=" (item, i) in menuItems" :key="i">
        <NuxtLink :to="item.to" class="text-lg rounded-[1rem] font-semibold">
          <Icon :icon="item.icon" class="text-2xl mr-2" />
          {{ item.label }}
        </NuxtLink>
      </li>
      <li>
        <button @click="logout()" class="text-lg rounded-[1rem] font-semibold">
          <Icon icon="solar:logout-2-bold" class="text-2xl mr-2" />
          Logout
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from "@/store/user";

const { logout } = useAuth();
const userStore = useUserStore();

interface MenuItem {
  to: string | object;
  icon: string;
  label: string;
}

const menuItems = computed<MenuItem[]>(() => [
  { to: { name: 'station-pubkey', params: { pubkey: userStore.pubkey } }, icon: "solar:station-bold", label: "Your Station" },
  { to: "/", icon: "solar:heart-angle-bold", label: "Favorites" },
  { to: "/", icon: "solar:chat-round-money-bold", label: "Purchases" },
  { to: "/", icon: "solar:headphones-round-sound-bold", label: "Studio" },
]);
</script>
