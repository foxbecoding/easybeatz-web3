<template>
  <AppPageContainer>
    <h1 class="text-3xl font-bold">Customize Station</h1>
    <form ref="form"></form>
  </AppPageContainer>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: ["auth"]
})

const route = useRoute();
const pubkey = route.params.pubkey
const form = ref()

</script>
