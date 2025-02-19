<script setup lang="ts">
import { type Track } from "@/services/models/album";
import { type Station } from "@/services/models/station";

const props = defineProps<{
  tracks: Track[];
  station: Station;
  albumCover: string;
}>();

const config = useRuntimeConfig();
const img = useImage();
const albumCover = computed(() => props.albumCover);

const albumCoverStyles = computed(() => {
  const imgUrl = img(albumCover.value, { width: 108 })
  return { backgroundImage: `url('${imgUrl}')`, backgroundSize: 'cover', backgroundPosition: 'center' }
})

</script>

<template>
</template>
