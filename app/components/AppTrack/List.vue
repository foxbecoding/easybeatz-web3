<script setup lang="ts">
import { type Album, type Track } from "@/services/models/album";
import { type Station } from "@/services/models/station";
import { type TrackList, useMusicPlayerStore } from "@/store/musicPlayer";

const props = defineProps<{
  tracks: Track[];
  station: Station;
  album: Album;
}>();

const isEditMode = defineModel("edit", { default: false, required: false });
const config = useRuntimeConfig();
const route = useRoute();
const img = useImage();
const albumCover = computed(() => `${config.public.MEDIA_URL}${props.album.cover}`);
const musicPlayerStore = useMusicPlayerStore();

const albumCoverStyles = computed(() => {
  const imgUrl = img(albumCover.value, { width: 108 })
  return { backgroundImage: `url('${imgUrl}')`, backgroundSize: 'cover', backgroundPosition: 'center' }
})

const showProjectCover = computed(() => {
  const hideOnRoutes = ['project-aid']
  return hideOnRoutes.includes(String(route.name)) ? false : true;
});

const setMusicPlayerDetails = (trackIndex: number) => {
  let trackList: TrackList[] = [];

  props.tracks.forEach(track => {
    trackList.push({ album: props.album, station: props.station, track })
  });
  const selectedTrackListItem: TrackList = trackList[trackIndex];
  musicPlayerStore.isShuffled = false;
  musicPlayerStore.setMusicPlayerDetails(selectedTrackListItem, trackList, String(route.path));
}

// Edit track control logic
const emit = defineEmits(["editDetails", "editPrice", "editExclusivePrice"]);
</script>

<template>
  <div class="flex flex-col gap-4">
    <div v-for="(track, t) in tracks" :key="t" @click="setMusicPlayerDetails(t)"
      class="md:h-[128px] bg-base-200 rounded-[1rem] cursor-pointer">
      <div v-if="showProjectCover" :style="albumCoverStyles"
        class="w-full h-full max-w-[640px] max-h-[640px] aspect-square group relative bg-neutral rounded-t-[0.5rem] flex sm:hidden items-center">
      </div>
      <div class="flex flex-col gap-4 md:flex-row justify-between h-full p-4">
        <div class="flex flex-1 items-center gap-2">
          <span class="font-semibold">{{ t + 1 }}</span>
          <div class="flex gap-2 md:gap-4">
            <div v-if="showProjectCover" :style="albumCoverStyles"
              class="min-w-[72px] h-[72px] sm:min-w-[108px] sm:h-[108px] group relative bg-neutral rounded-[0.5rem] hidden sm:flex">
            </div>
            <div class="flex flex-col gap-1 items-start">
              <p class="text-lg font-bold line-clamp-1 overflow-hidden text-ellipsis">
                {{ track.title }}
              </p>
              <AppStationBlock :station="station" @click.stop />
              <div class="flex gap-4">
                <span>duration: {{ track.formatted_duration }}</span>
                <span>BPM: {{ track.bpm }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="flex flex-col md:flex-row gap-2 items-start md:items-center">
          <NuxtLink class="btn btn-primary w-full md:w-[116px] rounded-[1rem] order-last md:order-first">
            Buy ${{ track.price }}
          </NuxtLink>
          <div class="flex order-first md:order-last">
            <AppTrackControls :album="album" :station="station" :track="track" />
            <div v-if="isEditMode" class="tooltip" data-tip="edit">
              <button class="btn btn-square btn-ghost mask mask-squircle">
                <Icon icon="solar:pen-bold" class="text-warning" width="24" height="24" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
