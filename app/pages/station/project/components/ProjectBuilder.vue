<script setup lang="ts">
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";
import { useCreateProjectStore } from "@/store/createProject";
import AlbumForm from "./AlbumForm.vue";
import TrackForm from "./TrackForm.vue";
import Review from "./Review.vue";

const props = defineProps<{
  genres: Genre[] | null;
  moods: Mood[] | null;
}>();

const createProjectStore = useCreateProjectStore();
const activeSteps = computed<string[]>(() => createProjectStore.activeSteps);
const activeStep = computed(() => createProjectStore.step);

</script>

<template>
  <div class="card bg-neutral max-w-[1200px] w-full shadow-md block mx-auto">
    <div class="card-body">
      <ul class="steps w-full">
        <li class="step" :class="activeSteps.includes('step1') ? 'step-primary' : ''">Project details
        </li>
        <li class="step" :class="activeSteps.includes('step2') ? 'step-primary' : ''">Tracks</li>
        <li class="step" :class="activeSteps.includes('step3') ? 'step-primary' : ''">Review</li>
      </ul>
      <div class="pt-4">
        <AlbumForm v-if="activeStep === 'step1'" />
        <TrackForm v-if="activeStep === 'step2'" />
        <Review v-if="activeStep === 'step3'" />
      </div>
    </div>
  </div>

</template>
