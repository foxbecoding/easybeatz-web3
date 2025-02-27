<script setup lang="ts">
import { type TrackList, useMusicPlayerStore } from "@/store/musicPlayer";
import { type Album, type Track } from "@/services/models/album";
import { type Station } from "@/services/models/station";

const config = useRuntimeConfig();
const img = useImage();
const musicPlayerStore = useMusicPlayerStore();
const show = computed(() => musicPlayerStore.show);
const trackList = computed<TrackList>(() => musicPlayerStore.selectedTrackListItem as TrackList);
const album = computed<Album>(() => trackList.value.album as Album);
const albumCover = computed(() => `${config.public.MEDIA_URL}${album.value.cover}`);
const track = computed<Track>(() => trackList.value.track);
const station = computed<Station>(() => trackList.value.station);

const albumCoverStyles = computed(() => {
  const imgUrl = img(albumCover.value, { width: 108 })
  return { backgroundImage: `url('${imgUrl}')`, backgroundSize: 'cover', backgroundPosition: 'center' }
})

</script>

<template>
  <div v-if="show"
    class="absolute bottom-[24px] lg:bottom-[88px] left-1/2 transform -translate-x-1/2 w-full max-w-[90%] h-[72px] sm:h-[84px] md:h-[96px] rounded-[1rem]"
    :style="albumCoverStyles">
    <!-- Dark Overlay -->
    <div class="absolute inset-0 bg-black bg-opacity-70 rounded-[1rem]"></div>
    <!-- Frosted Glass Overlay -->
    <div class="absolute inset-0 bg-white bg-opacity-15 backdrop-blur-md rounded-[1rem] items-center justify-center">
      <div class="flex justify-between items-center h-full p-4 navbar">
        <!-- Start -->
        <div class="navbar-start">
          <AppMusicPlayerDetailsBlock />
        </div>

        <!-- Center -->
        <div class="navbar-center hidden md:flex w-full md:max-w-[300px] lg:max-w-[400px]">
          <AppMusicPlayerMusicControlBlock />
        </div>

        <!-- End -->
        <div class="navbar-end">
          <AppMusicPlayerTrackControlBlock />
        </div>
      </div>
    </div>
  </div>
</template>
