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

const { data: cachedProject } = useNuxtData<Album>(`project-${aid.value}`);

const { data: fetchedProject, error, status, refresh } = await useLazyFetch<Album>(fetchPath, {
  server: false,
  key: `project-${aid.value}`,
  watch: [isAuthenticated],
  onRequest({ request, options }) {
    if (authStore.accessToken) {
      options.headers.set('Authorization', `Bearer ${authStore.accessToken}`)
    }
  },
  onResponseError({ request, response, options }) {
    //isOwner.value = response._data.is_owner;
  }
});

const project = computed(() => fetchedProject.value || cachedProject.value)
const projectCover = computed(() => `${config.public.MEDIA_URL}` + project.value?.cover);
const projectStationPicture = computed(() => `${config.public.MEDIA_URL}` + project.value?.station.picture);

const img = useImage()
const projectImgStyles = computed(() => {
  const imgUrl = img(projectCover.value, { width: 100 })
  return { backgroundImage: `url('${imgUrl}')`, backgroundSize: 'cover', backgroundPosition: 'center' }
})

const projectStationImgStyles = computed(() => {
  const imgUrl = img(projectStationPicture.value, { width: 36, height: 36 })
  return { backgroundImage: `url('${imgUrl}')`, backgroundSize: 'cover', backgroundPosition: 'center' }
})
</script>
<template>
</template>
