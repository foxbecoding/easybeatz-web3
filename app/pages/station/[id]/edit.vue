<template>
  <AppPageContainer>
    EDIT STATION {{ pubkey }}
  </AppPageContainer>
</template>

<script setup lang="ts">

const route = useRoute();
const pubkey = route.params.pubkey

</script>
