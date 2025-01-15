<template>
  <AppPageContainer>
    <div class="flex">
      <div class="mr-4 min-w-[200px]">
        <NuxtImg class="mask mask-squircle" src='/easy-glow.png' width="200" height="200" />
      </div>
      <div v-if="station">
        <p class="text-2xl font-semibold">{{ station.name ? station.name : 'Unnamed Station' }}</p>
        <p class="text-lg font-semibold">@{{ route.params.pubkey }}</p>
        <p class="mb-2 opacity-70">Joined {{ station.created }}</p>
        <NuxtLink v-if="station.is_owner" class="text-lg btn btn-neutral">Customize station</NuxtLink>
        <button v-else class="btn bg-neutral-content text-base-200 text-lg">Subscribe</button>
      </div>
    </div>
    <div class="divider mt-8"></div>
  </AppPageContainer>
</template>

<script setup lang="ts">
import AppPageContainer from "@/components/AppPageContainer.vue";
import { useAuthStore } from "@/store/auth";

const route = useRoute();
const config = useRuntimeConfig();
const authStore = useAuthStore();
const { status, data: station } = await useLazyFetch(`${config.public.API_STATION}/${route.params.pubkey}/public_station`, {
  server: false,
  onRequest({ request, options }) {
    if (authStore.accessToken) {
      options.headers.set(' Authorization', `Bearer ${authStore.accessToken}`)
    }
  },
  onResponseError({ request, response, options }) {
    // TODO switch to middleware
    if (response.status === 404) {
      navigateTo({ name: "station" })
    }
  }
});

watch(station, (newStation) => {
  station.value = newStation
})
</script>
