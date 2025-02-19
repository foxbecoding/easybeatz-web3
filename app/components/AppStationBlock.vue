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
</template>
