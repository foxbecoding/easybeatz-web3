<script setup lang="ts">
import { type Track } from "@/services/models/album";
import { type Station } from "@/services/models/station";

const props = defineProps<{
  tracks: Track[];
  station: Station;
  albumCover: string;
}>();

const route = useRoute();
const img = useImage();
const albumCover = computed(() => props.albumCover);

const albumCoverStyles = computed(() => {
  const imgUrl = img(albumCover.value, { width: 108 })
  return { backgroundImage: `url('${imgUrl}')`, backgroundSize: 'cover', backgroundPosition: 'center' }
})

const showProjectCover = computed(() => {
  const hideOnRoutes = ['project-aid']
  if (hideOnRoutes.includes(String(route.name))) {
    return false;
  }
  return true;
});

</script>

<template>
  <div class="flex flex-col gap-4">
    <div v-for="(track, t) in tracks" :key="t" class="md:h-[128px] bg-base-200 rounded-[1rem]">
      <div class="flex flex-col gap-4 md:flex-row justify-between h-full p-4">
        <div class="flex items-center gap-2">
          <span class="font-semibold">{{ t + 1 }}</span>
          <div class="flex gap-4">
            <div v-if="showProjectCover" :style="albumCoverStyles"
              class="min-w-[108px] h-[108px] group relative bg-neutral rounded-[0.5rem]">
            </div>
            <div class="flex flex-col gap-1 items-start">
              <p class="text-lg font-bold line-clamp-2 overflow-hidden text-ellipsis">
                {{ track.title }}
              </p>
              <AppStationBlock :station="station" />
              <div class="flex gap-4">
                <span>duration: {{ track.formatted_duration }}</span>
                <span>BPM: {{ track.bpm }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="flex flex-col md:flex-row gap-2  items-start md:items-center">
          <NuxtLink class="btn btn-primary w-full md:w-[116px] rounded-[1rem] order-last md:order-first">
            Buy ${{ track.price }}
          </NuxtLink>
          <div class="flex gap-2 order-first md:order-last">
            <button class="btn btn-square btn-ghost mask mask-squircle">
              <Icon icon="solar:heart-linear" width="24" height="24" />
            </button>
            <button class="btn btn-square btn-ghost mask mask-squircle">
              <Icon icon="solar:menu-dots-bold" width="24" height="24" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
