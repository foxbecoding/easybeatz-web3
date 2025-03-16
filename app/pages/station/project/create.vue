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

const { data: fetchedGenres, status: genre_status } = await useLazyFetch(fetchGenrePath, {
  server: false,
  key: `station-genres-for-project-create`,
});

const { data: fetchedMoods, status: mood_status } = await useLazyFetch(fetchMoodPath, {
  server: false,
  key: `station-moods-for-project-create`,
});

const genres = computed<Genre[]>(() => fetchedGenres.value.data as Genre[]);
const moods = computed<Mood[]>(() => fetchedMoods.value.data as Mood[]);

</script>
