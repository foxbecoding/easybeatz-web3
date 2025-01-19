<template>
  <AppPageContainer>
    <StationForm title="Create station" type="CREATE" @submit="submitHandler" />
  </AppPageContainer>
</template>

<script setup lang="ts">
import { useUserStore } from "@/store/user";
import StationForm from "./components/StationForm.vue";


definePageMeta({
  middleware: ["auth", "station"]
})

const userStore = useUserStore();
const pubkey = userStore.pubkey as string;
const toast = useToast();

const submitHandler = async () => {
  toast.setToast('Station created', 'SUCCESS')
  return navigateTo({ name: "station-pubkey", params: { pubkey: pubkey }, replace: true })
}
</script>
