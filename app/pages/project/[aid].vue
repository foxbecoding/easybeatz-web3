<script lang="ts" setup>
import { useAuthStore } from "@/store/auth";
import { type Album } from "@/services/models/album";

const route = useRoute();
const authStore = useAuthStore();
const config = useRuntimeConfig();
const aid = ref(route.params.aid)
const isAuthenticated = computed(() => authStore.isAuthenticated)
const fetchPath = `${config.public.API_ALBUM_PROJECT}/${aid.value}/`;
const demoTracks = Array.from({ length: 12 }, (_, i) => i);

</script>
<template>
</template>
