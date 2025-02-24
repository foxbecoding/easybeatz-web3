<script setup lang="ts">
import { type Station } from "@/services/models/station";

const props = defineProps<{
  station: Station;
}>();

const config = useRuntimeConfig();
const stationPicture = computed(() => `${config.public.MEDIA_URL}` + props.station.picture);
const img = useImage();

const imgStyles = computed(() => {
  const imgUrl = img(stationPicture.value, { width: 36, height: 36 })
  return { backgroundImage: `url('${imgUrl}')`, backgroundSize: 'cover', backgroundPosition: 'center' }
})
</script>

<template>
  <NuxtLink class="flex flex-1 gap-2 items-center md:justify-start"
    :to="{ name: 'station-pubkey', params: { pubkey: station.pubkey } }">
    <div
      class="min-w-[36px] h-[36px] mask mask-squircle bg-neutral p-[20px] aspect-square flex items-center justify-center">
      <div :style="imgStyles" class="min-w-[36px] h-[36px] group relative mask mask-squircle bg-neutral">
      </div>
    </div>
    <div class="flex flex-col items-start">
      <span class="text-sm font-semibold line-clamp-1 overflow-hidden text-ellipsis">{{ station.name }}</span>
      <span class="text-sm opacity-80 line-clamp-1 overflow-hidden text-ellipsis">@{{ station.handle }}</span>
    </div>
  </NuxtLink>
</template>
