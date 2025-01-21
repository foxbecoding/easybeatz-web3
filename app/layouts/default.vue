<template>
  <div class="drawer lg:drawer-open">
    <input id="app-drawer" type="checkbox" class="drawer-toggle" />
    <div class="drawer-content flex flex-col ">

      <AppNavBar />
      <div class="divider my-0" style="height: 0rem"></div>
      <main class="relative" style="height: 100%">
        <slot />
        <AppToast />
      </main>

    </div>
    <div class="drawer-side min-h-full bg-base-200">
      <label for="app-drawer" aria-label="close sidebar" class="drawer-overlay"></label>
      <NuxtLink :to="{ name: 'index' }"><img src="/logo.png" width="200px" class="px-4 py-4" /></NuxtLink>
      <ul class="menu bg-base-200 text-base-content w-80 px-4 py-2">
        <li v-for="(item, i) in menuList" :key="i">
          <NuxtLink class="text-lg rounded-[1rem] font-semibold" :to="{ name: item.name }" active-class="bg-neutral">
            <Icon :icon="item.icon" class="text-2xl mr-2" :class="activeLinkIcon(item.name)" />
            {{ item.label }}
          </NuxtLink>
        </li>
        <div class="divider"></div>
      </ul>
      <AppCompanyBlock />
    </div>
  </div>
</template>

<script setup lang="ts">
interface MenuListItem {
  label: string;
  icon: string;
  name: string;
}

const menuList: MenuListItem[] = [
  { label: "Home", icon: "solar:home-2-bold", name: "index" },
  { label: "Explore", icon: "solar:turntable-music-note-bold", name: "explore" },
  { label: "Library", icon: "solar:music-library-2-bold", name: "library" },
  { label: "Upload", icon: "solar:upload-track-2-bold", name: "upload" },
  { label: "Playlist", icon: "solar:playlist-2-bold", name: "playlist" },
];

const route = useRoute();

const activeLinkIcon = (route_name: string) => route.name == route_name ? 'text-primary' : '';

</script>
