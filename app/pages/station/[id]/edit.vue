<template>
  <AppPageContainer>
    EDIT STATION {{ pubkey }}
  </AppPageContainer>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: ["auth"]
  // or middleware: 'auth'
})
const route = useRoute();
const pubkey = route.params.pubkey

</script>
