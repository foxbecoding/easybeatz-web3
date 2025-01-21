<template>
  <AppPageContainer>
    <div v-if="status == 'success' && station" class="flex">
      <div class="mr-4 min-w-[200px] h-[200px] group relative">
        <NuxtImg class="mask mask-squircle" :src="imagePreview ? imagePreview : '/easy-glow.png'" width="200"
          height="200" />
        <button v-show="station.is_owner" @click="triggerFileInput"
          class="btn btn-neutral mask mask-squircle upload-button opacity-0 group-hover:opacity-75">
          <Icon icon="solar:camera-add-bold" class="text-xl" />
        </button>
        <input v-if="station.is_owner" ref="fileInput" type="file" id="fileInput" accept=".png,.jpg,.jpeg,.avif"
          @change="onFileChange" class="hidden" />
      </div>
      <div>
        <p class="text-2xl font-semibold">{{ station.name ? station.name : 'Unnamed Station' }}</p>
        <p class="text-lg font-semibold">@{{ station.handle }}</p>
        <p class="mb-2 opacity-70">Joined {{ station.created }}</p>
        <NuxtLink v-if="station.is_owner" :to="{ name: 'station-edit' }" class="text-lg btn btn-neutral">
          Customize station</NuxtLink>
        <button v-else class="btn btn-primary text-lg">Subscribe</button>
      </div>
    </div>

    <div v-if="status == 'idle' || status == 'pending'">
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

      <div v-if="false" class="divider mt-8"></div>

      <div v-if="false" class="grid grid-cols-6 md:grid-cols-6 sm:grid-cols-2 gap-8">
        <div v-for="i in demoAlbums" class="flex flex-col w-full gap-4">
          <div class="skeleton aspect-square w-full"></div>
          <div class="skeleton h-4 w-full"></div>
          <div class="skeleton h-4 w-48"></div>
        </div>
      </div>
    </div>

    <div v-if="status == 'idle' || status == 'pending' || status == 'success'">
      <div class="divider mt-8"></div>

      <div class="grid grid-cols-6 md:grid-cols-6 sm:grid-cols-2 gap-8">
        <div v-for="i in demoAlbums" class="flex flex-col w-full gap-4">
          <div class="skeleton aspect-square w-full"></div>
          <div class="skeleton h-4 w-full"></div>
          <div class="skeleton h-4 w-48"></div>
        </div>
      </div>

    </div>

    <div v-if="status == 'error'" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <Icon icon="solar:station-outline" class="text-9xl mx-auto" />
      <div class="flex flex-col gap-2">
        <span class="text-xl">{{ isOwner ? 'Create your station' : 'Station does not exists' }}</span>
        <NuxtLink v-if="isOwner" :to="{ name: 'station-create' }" class="btn btn-primary text-lg"> Create</NuxtLink>
      </div>
    </div>
  </AppPageContainer>
</template>

<script setup lang="ts">
import { useAuthStore } from "@/store/auth";
import { type Station, uploadStationPicture } from "@/services/models/station";

const route = useRoute();
const config = useRuntimeConfig();
const authStore = useAuthStore();
const pubkey = ref(route.params.pubkey)
const fetchPath = `${config.public.API_STATION}/${pubkey.value}/public_station/`;
const isAuthenticated = computed(() => authStore.isAuthenticated)
const isOwner = ref<boolean>(false);
const demoAlbums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
const fileInput = ref();
const imagePreview = ref();

//const { data: cachedStation } = useNuxtData<Station>(`station-${pubkey.value}`);

const { data: station, error, status, } = await useLazyFetch<Station>(fetchPath, {
  server: false,
  key: `station-${pubkey.value}`,
  watch: [isAuthenticated],
  onRequest({ request, options }) {
    if (authStore.accessToken) {
      options.headers.set('Authorization', `Bearer ${authStore.accessToken}`)
    }
  },
  onResponseError({ request, response, options }) {
    isOwner.value = response._data.is_owner;
  }
});

const onFileChange = (event: any) => {
  const file: File = event.target.files[0];
  if (!file) return;

  // Generate preview
  imagePreview.value = URL.createObjectURL(file)

  //upload picture
  uploadPicture(file)
}

const uploadPicture = async (file: File) => {
  const formData = new FormData;
  formData.append('picture', file);
  const res = await uploadStationPicture(formData);
  const toast = useToast();
  if (!res.error) {
    toast.setToast("Picture uploaded successfully", "SUCCESS");
    return;
  }
  toast.setToast(res.error, "ERROR")
}

const triggerFileInput = () => {
  fileInput.value.click();
}

</script>

<style scoped>
.upload-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) !important;
}
</style>
