<script setup lang="ts">
import { type Track } from "@/services/models/album";
import { useAuthStore } from "@/store/auth";
import type { NuxtLink } from "~/components";

const route = useRoute();
const config = useRuntimeConfig();
const authStore = useAuthStore();
const isAuthenticated = computed(() => authStore.isAuthenticated)
const img = useImage();

// Track request logic
const tid = ref(route.params.tid)
const fetchPath = `${config.public.API_TRACK}/${route.params.tid}/track_page/`;

const { data: cachedTrack } = useNuxtData<{ message: string; data: any }>(`track-${tid.value}`);
const { data: fetchedTrack, error, status, refresh } = await useLazyFetch<{ message: string; data: any }>(fetchPath, {
  server: false,
  key: `track-${tid.value}`,
  watch: [isAuthenticated],
  onRequest({ request, options }) {
    if (authStore.accessToken) {
      options.headers.set('Authorization', `Bearer ${authStore.accessToken}`)
    }
  },
  onResponseError({ request, response, options }) {
    console.log(response);
  }
});

const track = computed<Track>(() => fetchedTrack.value?.data as Track || cachedTrack.value?.data as Track);

<template>
  <AppPageContainer>
  </AppPageContainer>
</template>
