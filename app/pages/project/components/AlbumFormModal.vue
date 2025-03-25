<script setup lang="ts">
import { updateAlbum } from "@/services/models/album";

const props = defineProps<{
  title: String;
  bio: String;
}>();

const aid = useRoute().params.aid

</script>

<template>
</template>
