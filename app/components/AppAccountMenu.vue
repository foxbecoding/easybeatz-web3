<template>
  <div class="dropdown dropdown-bottom dropdown-end dropdown-hover">
    <button tabindex="0" role="button" class="btn btn-neutral btn-square">
      <Icon icon="solar:user-bold" class="text-2xl" />
    </button>

    <ul tabindex="0" class="dropdown-content menu bg-neutral rounded-box z-[1] w-[300px] p-2 shadow">
      <li v-for=" (link, i) in menuLinks" :key="i">
        <button class="text-lg font-semibold">
          <Icon :icon="link.icon" class="text-2xl mr-2" />
          {{ link.label }}
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { useStationStore } from "@/store/station"

const stationStore = useStationStore();
const router = useRouter();

interface MenuLink {
  icon: string;
  label: string;
  clickHandler?: Function;
}


const stationClickHandler = () => {
  if (!stationStore.hasStation) {
    console.log("FOX");
  }
}

const menuLinks = computed<MenuLink[]>(() => [
  { icon: "solar:station-bold", label: "Your Station", clickHandler: stationClickHandler },
  { icon: "solar:heart-angle-bold", label: "Favorites" },
  { icon: "solar:chat-round-money-bold", label: "Purchases" },
  { icon: "solar:headphones-round-sound-bold", label: "Studio" },
  { icon: "solar:logout-2-bold", label: "Logout" },
]);
</script>
