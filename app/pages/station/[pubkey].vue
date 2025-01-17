<template>
  <AppPageContainer>
    <div v-if="status == 'success' && station" class="flex">
      <div class="mr-4 min-w-[200px]">
        <NuxtImg class="mask mask-squircle" src='/easy-glow.png' width="200" height="200" />
      </div>
      <div>
        <p class="text-2xl font-semibold">{{ station.name ? station.name : 'Unnamed Station' }}</p>
        <p class="text-lg font-semibold">@{{ route.params.pubkey }}</p>
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

      <div class="divider mt-8"></div>

      <div class="grid grid-cols-6 md:grid-cols-6 sm:grid-cols-2 gap-8">
        <div v-for="i in demoAlbums" class="flex flex-col w-full gap-4">
          <div class="skeleton aspect-square w-full"></div>
          <div class="skeleton h-4 w-full"></div>
          <div class="skeleton h-4 w-48"></div>
        </div>
      </div>
    </div>

    <div v-if="status == 'error'">
      BITCH {{ isOwner }}
    </div>

  </AppPageContainer>
</template>

<script setup lang="ts">
import { useAuthStore } from "@/store/auth";
import { type Station } from "@/services/models/station";

const route = useRoute();
const config = useRuntimeConfig();
const authStore = useAuthStore();
const pubkey = ref(route.params.pubkey)
const fetchPath = `${config.public.API_STATION}/${pubkey.value}/public_station/`;
const isAuthenticated = computed(() => authStore.isAuthenticated)
const isOwner = ref<boolean>(false)
const demoAlbums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

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
})
</script>
