<template>
  <div v-show="toastStore.show" class="toast toast-center">
    <div v-if="false" class="alert" :class="toastStore.alertClass">
      <span>{{ toastStore.text }}</span>
    </div>
    <div class="alert alert-info">
      <span>{{ toastStore.text }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useToastStore } from "@/store/toast";

const toastStore = useToastStore();

</script>
