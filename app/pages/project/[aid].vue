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

const { data: cachedAlbum } = useNuxtData<Album>(`project-${aid.value}`);

const { data: fetchedAlbum, error, status, refresh } = await useLazyFetch<Album>(fetchPath, {
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

const album = computed(() => fetchedAlbum.value || cachedAlbum.value)
const albumTracks = computed(() => album.value?.tracks || [])
const albumCover = computed(() => `${config.public.MEDIA_URL}` + album.value?.cover);

const img = useImage()
const albumCoverStyles = computed(() => {
  const imgUrl = img(albumCover.value, { width: 100 })
  return { backgroundImage: `url('${imgUrl}')`, backgroundSize: 'cover', backgroundPosition: 'center' }
})

</script>

<template>
  <AppPageContainer>
    <div v-if="status == 'success' && album" class="flex flex-col gap-16">
      <div class="flex flex-col md:flex-row gap-4 items-center md:items-start">
        <div :style="albumCoverStyles" class="min-w-[300px] h-[300px] group relative bg-neutral rounded-[1rem]"></div>
        <div
          class="flex flex-col gap-4 items-center md:items-start md:justify-between md:h-[300px] w-full max-w-[600px]">
          <div class="text-center md:text-left w-full flex flex-col gap-2">
            <p class="text-3xl font-bold">{{ album.title }}</p>
            <AppStationBlock class="md:w-fit flex gap-2 items-center justify-center md:justify-start"
              :station="album.station" />
            <p class="opacity-70">{{ album.uploaded_at }}</p>
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

      <AppTrackList :tracks="albumTracks" :station="album.station" :album-cover="albumCover" />

    </div>

  </AppPageContainer>
</template>
