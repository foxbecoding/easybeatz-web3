<template>
  <AppPageContainer>
    <ProjectBuilder v-if="genre_status === 'success' && mood_status === 'success'" :genres="genres" :moods="moods" />
  </AppPageContainer>
</template>

<script setup lang="ts">
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";
import ProjectBuilder from "./components/ProjectBuilder.vue"

definePageMeta({
  middleware: ["auth", "station"]
});

const config = useRuntimeConfig();
const fetchGenrePath = `${config.public.API_GENRE}/`;
const fetchMoodPath = `${config.public.API_MOOD}/`;

const { data: genres, error: genre_error, status: genre_status } = await useLazyFetch<Genre[]>(fetchGenrePath, {
  server: false,
  key: `station-genres-for-project-create`,
});

const { data: moods, error: mood_error, status: mood_status } = await useLazyFetch<Mood[]>(fetchMoodPath, {
  server: false,
  key: `station-moods-for-project-create`,
});
</script>
