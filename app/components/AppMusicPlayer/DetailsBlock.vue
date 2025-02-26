<script setup lang="ts">
import { type TrackList, useMusicPlayerStore } from "@/store/musicPlayer";
import { type Album, type Track } from "@/services/models/album";
import { type Station } from "@/services/models/station";

const config = useRuntimeConfig();
const img = useImage();
const musicPlayerStore = useMusicPlayerStore();
const trackList = computed<TrackList>(() => musicPlayerStore.selectedTrackListItem as TrackList);
const album = computed<Album>(() => trackList.value.album);
const albumCover = computed(() => `${config.public.MEDIA_URL}${album.value.cover}`);
const track = computed<Track>(() => trackList.value.track);
const station = computed<Station>(() => trackList.value.station);

const albumCoverStyles = computed(() => {
  const imgUrl = img(albumCover.value, { width: 108 })
  return { backgroundImage: `url('${imgUrl}')`, backgroundSize: 'cover', backgroundPosition: 'center' }
})

</script>

<template>
  <div class="flex gap-2 md:gap-4">
    <div :style="albumCoverStyles"
      class="min-w-[68px] h-[68px] group relative bg-neutral rounded-[0.5rem] hidden sm:flex">
    </div>
    <div class="flex flex-col gap-0 items-start">
      <span class="text-md font-bold line-clamp-2 overflow-hidden text-ellipsis [line-height:0.8rem]">
        {{ track.title }}
      </span>
      <span class="font-semibold opacity-80">{{ station.name }}</span>
    </div>
  </div>
</template>
