<script setup lang="ts">
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";

const props = defineProps<{
  genres: Genre[] | null;
  moods: Mood[] | null;
}>();
</script>

<template>
  <ul class="steps w-full">
    <li class="step step-primary">Project details</li>
    <li class="step step-primary">Tracks</li>
    <li class="step">Review</li>
  </ul>
</template>
