<script setup lang="ts">
import { useAuthStore } from "@/store/auth";
import { type Station, uploadStationPicture } from "@/services/models/station";

const route = useRoute();
const config = useRuntimeConfig();
const authStore = useAuthStore();
const pubkey = ref(route.params.pubkey)
const fetchPath = `${config.public.API_STATION}/${pubkey.value}/retrieve_with_albums_and_relations/`;
const isAuthenticated = computed(() => authStore.isAuthenticated)
const isOwner = ref<boolean>(false);
const demoAlbums = Array.from({ length: 12 }, (_, i) => i);
const fileInput = ref();
const defaultStationImage = '/easy-glow.png'

const { data: cachedStation } = useNuxtData<Station>(`station-${pubkey.value}`);

const { data: fetchedStation, error, status, refresh } = await useLazyFetch(fetchPath, {
  server: false,
  key: `station-${pubkey.value}`,
  watch: [isAuthenticated],
  onRequest({ request, options }) {
    if (authStore.accessToken) {
      options.headers.set('Authorization', `Bearer ${authStore.accessToken}`)
    }
  },
  onResponseError({ request, response, options }) {
    isOwner.value = response._data.data.is_owner;
  }
});

const station = computed<Station>(() => fetchedStation.value.data as Station || cachedStation.value)

const isStationOwner = computed(() => station.value?.is_owner);

const stationPicture = computed(() => station.value?.picture ? `${config.public.MEDIA_URL}` + station.value?.picture : defaultStationImage);

const img = useImage()
const stationImgStyles = computed(() => {
  const imgUrl = img(stationPicture.value, { width: 100 })
  return { backgroundImage: `url('${imgUrl}')`, backgroundSize: 'cover', backgroundPosition: 'center' }
})

const onFileChange = (event: any) => {
  const file: File = event.target.files[0];
  if (!file) return;
  //upload picture
  uploadPicture(file)
}

const triggerFileInput = () => {
  fileInput.value.click();
}

const uploadPicture = async (file: File) => {
  const formData = new FormData;
  formData.append('picture', file);
  try {
    const { message, data } = await uploadStationPicture(formData);
    await refresh()
    useToast().setToast(message, "SUCCESS");
  } catch (error: any) {
    const { message, data } = error.data;
    await refresh()
    useToast().setToast(message, "ERROR");
  }
}

const albumCoverStyles = (cover_picture: string) => {
  const img = useImage();
  const imgUrl = img(`${config.public.MEDIA_URL}${cover_picture}`, { width: 100 });
  return { backgroundImage: `url('${imgUrl}')`, backgroundSize: 'cover', backgroundPosition: 'center' };
}
</script>

<template>
  <AppPageContainer>
    <div v-if="(status == 'success' && station) || cachedStation"
      class="flex flex-col md:flex-row gap-4 items-center md:items-start">
      <div
        class="min-w-[200px] h-[200px] mask mask-squircle bg-neutral p-1 box-content aspect-square flex items-center justify-center">
        <div :style="stationImgStyles" class="min-w-[200px] h-[200px] group relative mask mask-squircle bg-neutral">
          <button v-show="station.is_owner" @click="triggerFileInput"
            class="btn btn-neutral mask mask-squircle upload-button opacity-0 group-hover:opacity-95">
            <Icon icon="solar:camera-add-bold" class="text-xl" />
          </button>
          <input v-if="station.is_owner" ref="fileInput" type="file" id="fileInput"
            accept=".png,.jpg,.jpeg,.avif,.bmp,.webp" @change="onFileChange" class="hidden" />
        </div>
      </div>

      <div class="text-center md:text-left w-full">
        <p class="text-3xl font-bold">{{ station.name ? station.name : 'Unnamed Station' }}</p>
        <p class="text-xl font-semibold">@{{ station.handle }}</p>
        <p class="mb-2 opacity-70">{{ station.formatted_launched_date }}</p>
        <div v-if="station.is_owner" class="flex flex-col md:flex-row gap-4">
          <NuxtLink :to="{ name: 'station-edit' }" class="text-lg btn btn-neutral btn-block md:w-auto rounded-[1rem]">
            Customize station
          </NuxtLink>
          <NuxtLink :to="{ name: 'station-project-create' }"
            class="text-lg btn btn-secondary btn-block md:w-auto rounded-[1rem]">
            Create project
          </NuxtLink>
        </div>
        <button v-else class="btn btn-secondary btn-block md:w-auto rounded-[1rem] text-lg">Subscribe</button>
      </div>
    </div>

    <div v-if="(status == 'idle' || status == 'pending') && !cachedStation">
      <div class="flex">
        <div class="mr-4 min-w-[200px]">
          <div class="skeleton mask mask-squircle w-[200px] h-[200px]"></div>
        </div>
        <div class="flex flex-col w-[500px] gap-4">
          <div class="skeleton h-4 w-full"></div>
          <div class="skeleton h-4 w-full"></div>
          <div class="skeleton h-4 w-48"></div>
          <div class="skeleton h-[48px] w-[120px]"></div>
        </div>
      </div>

      <div class="divider mt-8"></div>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-8">
        <div v-for="i in demoAlbums" class="flex flex-col w-full gap-4">
          <div class="skeleton aspect-square rounded-[1rem] w-full"></div>
          <div class="skeleton h-4 w-full"></div>
          <div class="skeleton h-4 w-full"></div>
        </div>
      </div>
    </div>

    <div v-if="(status == 'success' && station) || cachedStation">
      <div class="divider mt-8"></div>
      <div v-if="station.albums.length > 0"
        class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-8">
        <NuxtLink v-for="(album, a) in station.albums" :key="a"
          :to="{ name: 'project-aid', params: { aid: album.aid } }" class="flex flex-col w-full h-full gap-2">
          <div class="aspect-square">
            <div :style="albumCoverStyles(album.cover)" class="w-full h-full rounded-[1rem]">
            </div>
          </div>
          <p class="line-clamp-2 overflow-hidden text-ellipsis font-bold">{{ album.title }}</p>
        </NuxtLink>
      </div>

      <div v-else class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
        <Icon icon="solar:station-outline" class="text-9xl mx-auto" />
        <div class="flex flex-col gap-2">
          <span class="text-xl">
            {{ isStationOwner ? 'Add projects to your station' : 'Nothing here yet' }}
          </span>
        </div>
      </div>
    </div>

    <div v-if="status == 'error'" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <Icon icon="solar:station-outline" class="text-9xl mx-auto" />
      <div class="flex flex-col gap-2">
        <span class="text-xl">{{ isOwner ? 'Create your station' : 'Station does not exists' }}</span>
        <NuxtLink v-if="isOwner" :to="{ name: 'station-create' }" class="btn btn-primary rounded-[1rem] text-lg">
          Create
        </NuxtLink>
      </div>
    </div>
  </AppPageContainer>
</template>

<style scoped>
.upload-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) !important;
}
</style>
