<script setup lang="ts">
import { type Track, updateTrack } from "@/services/models/album";
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";

const props = defineProps<{
  track: Track;
  genres: Genre[];
  moods: Mood[];
}>();

// Modal control logic
const model = defineModel({ default: false, required: true });
const closeModal = () => model.value = false;
watch(model, (newVal) => {
  if (newVal) {
    document.getElementById('track_form_modal')?.showModal();
  } else {
    document.getElementById('track_form_modal')?.close();
  }
});

// Form fields logic
const form = ref();
const formFields = reactive<any>({
  title: props.track.title,
  bpm: props.track.bpm,
  genres: props.track.genres.slug,
  mood: props.track.mood.slug,
});

const formErrors = reactive<any>({
  title: '',
  bpm: '',
  genres: '',
  mood: '',
});

const setFormErrors = (res: any) => {
  const obj = res;
  Object.keys(formErrors).forEach(key => {
    if (key in obj) {
      formErrors[`${key}`] = obj[key].length === 1 ? obj[key][0] : obj[key];
    } else {
      formErrors[key] = '';
    }
  });
}

const clearFormErrors = () => {
  Object.keys(formErrors).forEach(key => {
    formErrors[key] = '';
  });
}

</script>

<template>
  <dialog id="track_form_modal" class="modal modal-bottom sm:modal-middle">
    <div class="modal-box">
      <h2 class="text-2xl font-bold">Edit track</h2>
      <form id="track-form" ref="trackForm">
      </form>
    </div>
    <div class="modal-action">
      <form id="dialog-form" method="dialog" class="flex justify-end gap-2">
        <button class="btn btn-neutral">Close</button>
        <button class="btn btn-primary">
          Submit
        </button>
      </form>
    </div>
  </dialog>
</template>
