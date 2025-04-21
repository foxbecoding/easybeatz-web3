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
  <div class="flex gap-2">
    <NuxtLink :to="{ name: 'project-aid', params: { aid: album.aid } }" :style="albumCoverStyles"
      class="w-[44px] min-w-[44px] sm:w-[56px] sm:min-w-[56px] md:w-[68px] md:min-w-[68px] h-[44px] min-h-[44px] sm:h-[56px] sm:min-h-[56px] md:h-[68px] md:min-h-[68px] relative bg-neutral rounded-[0.5rem] flex">
    </NuxtLink>
    <div class="flex flex-col gap-0 items-start">
      <span
        class="text-sm md:text-md font-bold line-clamp-1 sm:line-clamp-2 overflow-hidden text-ellipsis [line-height:0.8rem] md:[line-height:1rem]">
        {{ track.title }}
      </span>
      <NuxtLink :to="{ name: 'station-pubkey', params: { pubkey: station.pubkey } }"
        class="text-xs md:text-sm font-semibold opacity-80 line-clamp-1 sm:line-clamp-2 overflow-hidden text-ellipsis [line-height:0.8rem] md:[line-height:1rem]">
        {{ station.name }}
      </NuxtLink>
    </div>
  </div>
</template>
