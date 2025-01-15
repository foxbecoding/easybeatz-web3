<template>
  <div class="w-100 p-[0.5rem]">
    <div class="mx-auto w-full max-w-[2560px] px-4 sm:px-8 2xl:px-16">
      <img class="mask mask-squircle" src="/easy-glow.png" width="200" height="200" />
      <p>@{{ route.params.pubkey }}</p>
    </div>
  </div>

</template>

<script setup lang="ts">
import { useAuthStore } from "@/store/auth";

const route = useRoute();
const config = useRuntimeConfig();
const authStore = useAuthStore();
const { status, data: station } = await useLazyFetch(`${config.public.API_STATION}/${route.params.pubkey}/public_station`, {
  onRequest({ request, options }) {
    if (authStore.accessToken) {
      options.headers.set('Authorization', `Bearer ${authStore.accessToken}`)
    }
  },
});
watch(station, (newStation) => {
  console.log("station: ", newStation)
})
</script>
