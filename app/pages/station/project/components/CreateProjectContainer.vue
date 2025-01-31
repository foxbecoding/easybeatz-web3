<script setup lang="ts">
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";

const props = defineProps<{
  genres: Genre[] | null;
  moods: Mood[] | null;
}>();
</script>

<template></template>
