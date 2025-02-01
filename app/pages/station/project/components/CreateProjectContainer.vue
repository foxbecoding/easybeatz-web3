<script setup lang="ts">
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";
import AlbumForm from "./AlbumForm.vue"

const props = defineProps<{
  genres: Genre[] | null;
  moods: Mood[] | null;
}>();

const { albumForm, isStep1, isStep2, isStep3, isStep2Active } = useCreateProject();
</script>

<template>
  <div class="card bg-neutral max-w-[1200px] w-full shadow-md block mx-auto">
    <div class="card-body">
      <ul class="steps w-full">
        <li class="step" :class="isStep1 ? 'step-primary' : ''">Project details</li>
        <li class="step" :class="isStep2Active ? 'step-primary' : ''">Tracks</li>
        <li class="step" :class="isStep3 ? 'step-primary' : ''">Review</li>
      </ul>
      <div class="py-4">
        <AlbumForm v-if="!isStep2 || !isStep3" />
      </div>
    </div>
  </div>

</template>
