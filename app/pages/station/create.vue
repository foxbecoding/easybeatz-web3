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

const submitHandler = async () => {
  return navigateTo({ name: "station-pubkey", params: { pubkey: pubkey }, replace: true })
}
</script>
