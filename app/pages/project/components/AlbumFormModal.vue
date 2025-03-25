<script setup lang="ts">
import { updateAlbum } from "@/services/models/album";

const props = defineProps<{
  title: String;
  bio: String;
}>();

const aid = useRoute().params.aid

const model = defineModel({ default: false, required: true });
const closeModal = () => model.value = false;
const isLoading = ref(false);

</script>

<template>
</template>
