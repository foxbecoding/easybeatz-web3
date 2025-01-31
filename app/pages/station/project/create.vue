<template>
  <AppPageContainer>
  </AppPageContainer>
</template>

<script setup lang="ts">
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";
import { useUserStore } from "@/store/user";
import { useAuthStore } from "@/store/auth";

definePageMeta({
  middleware: ["auth", "station"]
});

const userStore = useUserStore();
const authStore = useAuthStore();
const config = useRuntimeConfig();
const pubkey = userStore.pubkey as string;
const fetchGenrePath = `${config.public.API_GENRE}/${pubkey}/`;
const fetchMoodPath = `${config.public.API_MOOD}/${pubkey}/`;

const { data: genre, error: genre_error, status: genre_status, } = await useLazyFetch<Genre>(fetchGenrePath, {
  server: false,
  key: `station-genres-for-project-create`,
});

const toast = useToast();

const submitHandler = async () => {
  toast.setToast('Station upated', 'SUCCESS')
}

</script>
