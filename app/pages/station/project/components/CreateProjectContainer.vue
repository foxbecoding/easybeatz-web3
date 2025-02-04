<script setup lang="ts">
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";
import AlbumForm from "./AlbumForm.vue";
import TrackForm from "./TrackForm.vue";

const props = defineProps<{
  genres: Genre[] | null;
  moods: Mood[] | null;
}>();

const { albumForm, activeStep } = useCreateProject();

const test = computed(() => activeStep.value);
</script>

<template>
  <div class="card bg-neutral max-w-[1200px] w-full shadow-md block mx-auto">
    <div class="card-body">
      {{ albumForm }}
      <ul class="steps w-full">
        <li class="step" :class="activeStep === 'step1' || activeStep === 'step2' ? 'step-primary' : ''">Project details
        </li>
        <li class="step" :class="activeStep === 'step2' ? 'step-primary' : ''">Tracks</li>
        <li class="step" :class="activeStep === 'step3' ? 'step-primary' : ''">Review</li>
      </ul>
      <div class="pt-4">
        <AlbumForm v-if="activeStep === 'step1'" />
        <TrackForm v-if="activeStep === 'step2'" />
      </div>
    </div>
  </div>

</template>
