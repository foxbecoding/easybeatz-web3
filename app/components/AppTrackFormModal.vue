<script setup lang="ts">
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";

//component types and interfaces
interface TrackStemForm {
  name: string;
  file: File | null;
}

interface CollaboratorForm {
  pubkey: string;
}

interface TrackForm {
  bpm: string;
  collaborators: CollaboratorForm[];
  exclusive_price: string;
  genres: string[];
  mood: string;
  mp3: File | null;
  price: string;
  stems: TrackStemForm[];
  title: string;
  wav?: File | null;
}

// Component props
const props = defineProps<{
  genres: Genre[];
  moods: Mood[];
  formTitle: string;
}>();

// Emiiters
const emit = defineEmits(['submit'])

// Modal control logic
const model = defineModel({ default: false, required: true });
const closeModal = () => model.value = false;
watch(model, (newVal) => {
  if (newVal) {
    document.getElementById('app_track_form_modal')?.showModal();
  } else {
    document.getElementById('app_track_form_modal')?.close();
  }
});

</script>

<template>
</template>
