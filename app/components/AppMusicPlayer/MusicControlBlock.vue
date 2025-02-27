<script setup lang="ts">
import { type TrackList, useMusicPlayerStore } from "@/store/musicPlayer";
import { type Track } from "@/services/models/album";

const musicPlayerStore = useMusicPlayerStore();
const currentTimeStr = computed(() => musicPlayerStore.currentTimeStr);
const trackList = computed<TrackList>(() => musicPlayerStore.selectedTrackListItem as TrackList);
const track = computed<Track>(() => trackList.value.track);
const isShuffled = computed<boolean>(() => musicPlayerStore.isShuffled);
const isRepeat = computed<boolean>(() => musicPlayerStore.isRepeatOne || musicPlayerStore.isRepeatAll ? true : false);
const repeatIcon = computed(() => !musicPlayerStore.isRepeatOne ? 'repeat' : 'repeat-once')
const playOrPauseIcon = computed(() => musicPlayerStore.isPlaying ? 'pause' : 'play');
const playOrPause = computed(() => musicPlayerStore.isPlaying ? pauseHandler() : playHandler());

const playHandler = () => musicPlayerStore.playTrackHandler;
const pauseHandler = () => musicPlayerStore.pauseTrackHandler;
const nextHandler = () => musicPlayerStore.nextTrackHandler();
const prevHandler = () => musicPlayerStore.prevTrackHandler();
const repeatHandler = () => musicPlayerStore.repeatHandler();
const shuffleHandler = () => musicPlayerStore.shuffleHandler();

const onSliderChange = (e: any) => {
  if (musicPlayerStore.audio) {
    musicPlayerStore.audio.currentTime = Number(e.target.value)
  }
}

</script>

<template>
  <div class="w-full flex flex-col gap-1">
    <div class="flex items-center justify-center">
      <button @click="shuffleHandler()" class="btn btn-ghost btn-circle btn-sm">
        <Icon icon="mingcute:shuffle-fill" :class="isShuffled ? 'text-primary' : ''" width="20" height="20" />
      </button>
      <button @click="prevHandler()" class="btn btn-ghost btn-circle btn-sm">
        <Icon icon="solar:rewind-back-bold" width="20" height="20" />
      </button>
      <button @click="playOrPause" class="btn btn-ghost btn-circle btn-sm">
        <Icon :icon="`solar:${playOrPauseIcon}-bold`" width="20" height="20" />
      </button>
      <button @click="nextHandler()" class="btn btn-ghost btn-circle btn-sm">
        <Icon icon="solar:rewind-forward-bold" width="20" height="20" />
      </button>
      <button @click="repeatHandler()" class="btn btn-ghost btn-circle btn-sm">
        <Icon :icon="`tabler:${repeatIcon}`" :class="isRepeat ? 'text-primary' : ''" width="20" height="20" />
      </button>
    </div>
    <input type="range" min="0" :max="track.duration" v-model="musicPlayerStore.currentTime" @input="onSliderChange"
      class="range range-xs" />
    <div class="flex justify-between">
      <span class="text-xs font-semibold">{{ currentTimeStr }}</span>
      <span class="text-xs font-semibold">{{ track.formatted_duration }}</span>
    </div>
  </div>
</template>
