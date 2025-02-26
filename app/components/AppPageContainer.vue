<script setup lang="ts">
import { useMusicPlayerStore } from "@/store/musicPlayer";

const musicPlayer = useMusicPlayerStore();
const containerAdjust = computed(() => {
  if (musicPlayer.show) {
    return 'padding-bottom: 128px';
  }

  return '';
})
</script>

<template>
  <div class="w-100 p-[0.5rem] lg:overflow-y-auto h-[calc(100vh-64px)]" :class="musicPlayer.show ? 'pb-[128px]' : ''">
    <div class="mx-auto w-full max-w-[2560px] px-4 sm:px-8 2xl:px-16 py-8">
      <slot />
    </div>
  </div>
</template>
