<script setup lang="ts">
import { type Track } from "@/services/models/album";
import { type Station } from "@/services/models/station";

const props = defineProps<{
  tracks: Track[];
  station: Station;
  albumCover: string;
}>();



</script>

<template>
</template>
