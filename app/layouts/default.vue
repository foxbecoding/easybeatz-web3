<template>
  <div class="drawer lg:drawer-open">
    <input id="app-drawer" type="checkbox" class="drawer-toggle" />
    <div class="drawer-content flex flex-col ">

      <AppNavBar />
      <div class="divider my-0" style="height: 0rem"></div>
      <main>
        <slot />
      </main>

    </div>
    <div class="drawer-side min-h-full bg-base-200">
      <label for="app-drawer" aria-label="close sidebar" class="drawer-overlay"></label>
      <img src="/logo.png" width="200px" class="px-4 py-4" />
      <ul class="menu bg-base-200 text-base-content w-80 px-4 py-2">
        <li v-for="(item, i) in menuList" :key="i">
          <a class="text-lg">
            <Icon :icon="item.icon" class="text-2xl" />
            {{ item.label }}
          </a>
        </li>
        <div class="divider"></div>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
interface MenuListItem {
  label: string
  icon: string
}

const menuList: MenuListItem[] = [
  { label: "Home", icon: "solar:home-2-bold" },
  { label: "Explore", icon: "solar:turntable-music-note-bold" },
  { label: "Library", icon: "solar:music-library-2-bold" },
  { label: "Upload", icon: "solar:upload-track-2-bold" },
  { label: "Playlist", icon: "solar:playlist-2-bold" },
]

</script>
