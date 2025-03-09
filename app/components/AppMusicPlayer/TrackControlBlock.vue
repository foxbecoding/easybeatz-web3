<script setup lang="ts">
import { useMusicPlayerStore } from "@/store/musicPlayer";
import { type Album, type Track } from "@/services/models/album";
import { type Station } from "@/services/models/station";

const props = defineProps<{
  track: Track;
  station: Station;
  album: Album;
}>();

const musicPlayerStore = useMusicPlayerStore();
const playOrPauseIcon = computed(() => musicPlayerStore.isPlaying ? 'pause' : 'play');
const playOrPause = computed(() => musicPlayerStore.isPlaying ? pauseHandler() : playHandler());

const playHandler = () => musicPlayerStore.playTrackHandler;
const pauseHandler = () => musicPlayerStore.pauseTrackHandler;
const nextHandler = () => musicPlayerStore.nextTrackHandler();

</script>

<template>
  <AppTrackControls class="hidden md:flex" />
  <div class="flex md:hidden items-center justify-center">
    <button @click="playOrPause" class="btn btn-ghost btn-circle btn-sm">
      <Icon :icon="`solar:${playOrPauseIcon}-bold`" width="20" height="20" />
    </button>
    <button @click="nextHandler()" class="btn btn-ghost btn-circle btn-sm">
      <Icon icon="solar:rewind-forward-bold" width="20" height="20" />
    </button>
  </div>

</template>
