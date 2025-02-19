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
  <AppPageContainer>
    <div v-if="status == 'success' && project" class="flex flex-col md:flex-row gap-4 items-center md:items-start">
      <div :style="projectImgStyles" class="min-w-[300px] h-[300px] group relative bg-neutral rounded-[1rem]"></div>

      <div class="flex flex-col gap-4 items-center md:items-start md:justify-between h-[300px] w-full max-w-[600px]">
        <div class="text-center md:text-left w-full flex flex-col gap-2">
          <p class="text-3xl font-bold">{{ project.title }}</p>
          <NuxtLink class="flex gap-2 items-center justify-center md:justify-start"
            :to="{ name: 'station-pubkey', params: { pubkey: project.station.pubkey } }">
            <div
              class="min-w-[36px] h-[36px] mask mask-squircle bg-neutral p-[20px] aspect-square flex items-center justify-center">
              <div :style="projectStationImgStyles"
                class="min-w-[36px] h-[36px] group relative mask mask-squircle bg-neutral">
              </div>
            </div>
            <span class="text-xl font-semibold">{{ project.station.name }}</span>
          </NuxtLink>
        </div>
        <div class="flex gap-2 items-center w-full">
          <button class="btn btn-primary flex-1 rounded-[1rem] text-lg">
            <Icon class="text-lg lg:text-xl" icon="solar:play-line-duotone" />
            Play
          </button>
          <button class="btn btn-primary flex-1 rounded-[1rem] text-lg">
            <Icon class="text-lg lg:text-xl" icon="solar:shuffle-outline" />
            Shuffle
          </button>
        </div>
      </div>
    </div>
  </AppPageContainer>
</template>
