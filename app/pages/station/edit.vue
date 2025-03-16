<template>
  <AppPageContainer>
    <StationForm v-if="status == 'success'" title="Customize Station" type="EDIT" :pubkey="pubkey" :station="station"
      @submit="submitHandler" />
  </AppPageContainer>
</template>

<script setup lang="ts">
import { type Station } from "@/services/models/station";
import { useUserStore } from "@/store/user";
import { useAuthStore } from "@/store/auth";
import StationForm from "./components/StationForm.vue";

definePageMeta({
  middleware: ["auth", "station"]
});

const userStore = useUserStore();
const authStore = useAuthStore();
const config = useRuntimeConfig();
const pubkey = userStore.pubkey as string;
const fetchPath = `${config.public.API_STATION}/${pubkey}/`;

const { data, error, status, } = await useLazyFetch(fetchPath, {
  server: false,
  key: `station-edit-${pubkey}`,
  onRequest({ request, options }) {
    if (authStore.accessToken) {
      options.headers.set('Authorization', `Bearer ${authStore.accessToken}`)
    }
  },
  onResponseError({ request, response, options }) {
  }
});

const station = computed(() => data.value.data as Station)

const submitHandler = async () => {
  useToast().setToast('Station upated', 'SUCCESS')
}

</script>
