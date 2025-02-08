<script setup lang="ts">
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";
import { useCreateProjectStore } from "@/store/createProject";
import AlbumForm from "./AlbumForm.vue";
import TrackForm from "./TrackForm.vue";

const props = defineProps<{
  genres: Genre[] | null;
  moods: Mood[] | null;
}>();

const createProjectStore = useCreateProjectStore();
const isProjectValid = computed(() => createProjectStore.isProjectValid);

</script>

<template>
  <div class="card bg-base-100 max-w-[600px] w-full block mx-auto">
    <div class="card-body px-0 pt-0 pb-4">
      <AlbumForm />
      <div class="divider" />
      <TrackForm :genres="genres" :moods="moods" />
    </div>
    <div class="card-actions">
      <button class="btn btn-primary w-full rounded-[1rem] text-lg" :disabled="!isProjectValid">Submit</button>
    </div>
  </div>

</template>
