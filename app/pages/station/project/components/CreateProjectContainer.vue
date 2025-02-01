<script setup lang="ts">
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";

const { isStep1, isStep2, isStep3 } = useCreateProject();

const props = defineProps<{
  genres: Genre[] | null;
  moods: Mood[] | null;
}>();
</script>

<template>
  <ul class="steps w-full">
    <li class="step" :class="isStep1 ? 'step-primary' : ''">Project details</li>
    <li class="step" :class="isStep2 ? 'step-primary' : ''">Tracks</li>
    <li class=" step" :class="isStep3 ? 'step-primary' : ''">Review</li>
  </ul>
</template>
