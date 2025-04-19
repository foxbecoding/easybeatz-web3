<script setup lang="ts">
import { useCartStore } from "@/store/cart";

const cartStore = useCartStore();
</script>

<template>
  <AppPageContainer>
    <h1 class="text-3xl font-bold">Cart</h1>
  </AppPageContainer>
</template>
