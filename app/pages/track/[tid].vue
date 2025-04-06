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

// Album cover logic
const albumCover = computed(() => {
  const { album } = track.value;
  if (!album) return "";
  return `${config.public.MEDIA_URL}` + album.cover
});

const albumCoverStyles = computed(() => {
  const imgUrl = img(albumCover.value, { width: 100 })
  return { backgroundImage: `url('${imgUrl}')`, backgroundSize: 'cover', backgroundPosition: 'center' }
});

// Track play audio logic
const playHandler = () => { }

// Track details logic
interface TrackDetail {
  label: string;
  content: string;
  icon: string;
  to?: string;
}

const trackDetailItems = computed<TrackDetail[]>(() => [
  { label: "Duration", content: track.value.formatted_duration, icon: "solar:clock-circle-bold" },
  { label: "BPM", content: track.value.bpm, icon: "solar:playback-speed-bold" },
  { label: "Uploaded", content: "2025", icon: "solar:upload-track-2-bold" },
  { label: "Genre", content: track.value.genres.name, icon: "solar:music-notes-bold" },
  { label: "Mood", content: track.value.mood.name, icon: "solar:music-notes-bold" },
  {
    label: "Project",
    content: track.value.album?.title,
    icon: "solar:music-library-2-bold",
    to: {
      name: "project-aid", params: { aid: track.value.album?.aid }
    }
  },
] as TrackDetail[]);
</script>

<template>
  <AppPageContainer>
  </AppPageContainer>
</template>
