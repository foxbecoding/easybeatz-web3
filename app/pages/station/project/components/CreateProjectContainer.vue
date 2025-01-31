<script setup lang="ts">
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";

const props = defineProps<{
  genres: Genre[];
  moods: Mood[];
}>();
</script>

<template></template>
