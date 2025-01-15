<template>
  <div class="dropdown dropdown-bottom dropdown-end dropdown-hover">
    <button tabindex="0" role="button" class="btn btn-neutral btn-square">
      <Icon icon="solar:user-bold" class="text-2xl" />
    </button>

    <ul tabindex="0" class="dropdown-content menu bg-neutral rounded-box z-[1] w-[300px] p-2 shadow">
      <li v-for=" (item, i) in menuItems" :key="i">
        <NuxtLink :to="item.to" class="text-lg font-semibold">
          <Icon :icon="item.icon" class="text-2xl mr-2" />
          {{ item.label }}
        </NuxtLink>
      </li>
      <li>
        <button @click="logout()" class="text-lg font-semibold">
          <Icon icon="solar:logout-2-bold" class="text-2xl mr-2" />
          Logout
        </button>

      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { useStationStore } from "@/store/station"

const { logout } = useAuth();
const stationStore = useStationStore();
const router = useRouter();

interface MenuItem {
  to: string;
  icon: string;
  label: string;
}

const menuItems = computed<MenuItem[]>(() => [
  { to: "/", icon: "solar:station-bold", label: "Your Station" },
  { to: "/", icon: "solar:heart-angle-bold", label: "Favorites" },
  { to: "/", icon: "solar:chat-round-money-bold", label: "Purchases" },
  { to: "/", icon: "solar:headphones-round-sound-bold", label: "Studio" },
]);
</script>
