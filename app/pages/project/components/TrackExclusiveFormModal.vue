<script setup lang="ts">
import { type Track, updateTrackExclusivePrice } from "@/services/models/album";

const props = defineProps<{
  track: Track;
}>();

// Modal control logic
const model = defineModel({ default: false, required: true });
const closeModal = () => model.value = false;
watch(model, (newVal) => {
  if (newVal) {
    document.getElementById('track_exclusive_modal')?.showModal();
  } else {
    document.getElementById('track_exclusive_modal')?.close();
  }
});

// Form fields logic
const form = ref();
const formFields = reactive<any>({
  exclusive_price: props.track.exclusive_price,
});

const formErrors = reactive<any>({
  exclusive_price: '',
});

</script>

<template>
</template>
